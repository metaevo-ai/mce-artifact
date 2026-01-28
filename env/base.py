"""
Base classes and interfaces for benchmark integration.
"""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type

from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

load_dotenv(override=True)


class GeneratorSchema(BaseModel):
    """Generic schema for Generator output."""
    reasoning: str = Field(description="Your step-by-step analysis and calculations")
    final_answer: str = Field(description="Your concise final answer")


async def generic_generator_prompt(sample: Sample, playbook_context: str) -> str:
    """Generate a generic prompt for the task."""
    prompt = f"""You are an expert domain problem solver.

Task Context:
{sample.context}

Instructional Context:
{playbook_context}

Question: {sample.question}

You MUST respond with a valid JSON object containing exactly two fields:
1. "reasoning": Your step-by-step analysis
2. "final_answer": Your concise final answer
"""
    return prompt


@dataclass
class Sample:
    """
    Single task instance with dynamic fields.
    
    Core fields are defined, but additional fields can be stored in extras.
    This allows environments to include domain-specific data (e.g., solutions, hints).
    """

    id: int
    question: str
    context: str = ""  # context is shared across all instances for the same task
    ground_truth: Optional[str] = None
    extras: Dict[str, Any] = field(default_factory=dict)  # Environment-specific fields
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sample to dictionary with all fields flattened."""
        result = {
            "id": self.id,
            "question": self.question,
            "context": self.context,
            "ground_truth": self.ground_truth,
        }
        # Merge extras into the result
        result.update(self.extras)
        return result


@dataclass
class EnvironmentResult:
    """Feedback returned by the task environment after executing the generator output."""

    feedback: str
    ground_truth: Optional[str]
    metrics: Dict[str, float] = field(default_factory=dict)


class TaskEnvironment(ABC):
    """
    Abstract interface of task environment.
    """

    @abstractmethod
    async def aevaluate(
        self, sample: Sample, generator_output: Any
    ) -> EnvironmentResult:
        """
        Async version of evaluate() for batch processing.

        Default implementation runs the sync evaluate() in an executor.
        Override this method if your environment supports native async evaluation.

        Args:
            sample: The input sample with question and context
            generator_output: The Generator's produced answer

        Returns:
            EnvironmentResult with feedback and optional ground truth
        """

    @abstractmethod
    def load_samples(self, path: str, limit: int = 10, random_sample: bool = False, shuffle: bool = False) -> List[Sample]:
        """Load samples from the benchmark.
        
        Args:
            path: Path to the data file to load
            limit: Maximum number of samples to load
            random_sample: If True, randomly sample limit items; if False, take first limit items
            shuffle: If True, shuffle the order of loaded samples (useful for mini-batching)

        Returns:
            List of Sample objects
        """
    
    def get_generator_schema(self) -> Type[BaseModel]:
        """
        Get the Pydantic schema for structured LLM output.
        
        Returns:
            A Pydantic BaseModel class with at least a 'final_answer' field.
        
        Note:
            Default implementation returns GeneratorSchema with 'reasoning' and 'final_answer'.
            Override this method to customize the schema for your environment.
            The schema MUST include a 'final_answer' field.
        """
        return GeneratorSchema
    
    async def get_generator_prompt(self, sample: Sample, playbook_context: str) -> str:
        """
        Build the prompt for the generator LLM.
        
        Args:
            sample: The sample to generate a prompt for
            playbook_context: Retrieved context/instructions for this sample
        
        Returns:
            Formatted prompt string
        
        Note:
            Default implementation uses generic_generator_prompt().
            Override this method to customize the prompt for your environment.
        """
        return await generic_generator_prompt(sample, playbook_context)
    
    def get_primary_metric_name(self) -> str:
        """
        Get the name of the primary metric for this environment.
        
        The primary metric is used for:
        - Determining the "best" iteration
        - Logging a single performance number
        - Sorting/comparing results
        
        Returns:
            Name of the primary metric (e.g., "accuracy", "f1", "pass_at_1")
        
        Note:
            Default implementation returns "accuracy".
            If your environment returns multiple metrics, the FIRST metric
            in the metrics dict will be used as primary if this is not overridden.
        """
        return "accuracy"
    
    def format_result_for_training(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a single evaluation result for training data.
        
        Override this method to customize what fields are presented
        in the training data for the meta-agent to learn from.
        
        Args:
            item: Raw evaluation result with nested structure:
                {
                    "sample": {id, question, context, ground_truth, ...extras},
                    "llm_output": {reasoning, final_answer, ...},
                    "evaluation": {playbook_context, feedback, metrics}
                }
        
        Returns:
            Formatted dict with fields to include in training data
        
        Note:
            Default implementation returns minimal fields.
            Override to include reasoning, context, or domain-specific fields.
        """
        sample = item.get("sample", {})
        llm_output = item.get("llm_output", {})
        evaluation = item.get("evaluation", {})
        metrics = evaluation.get("metrics", {})
        
        # Get primary metric value
        primary_metric = self.get_primary_metric_name()
        is_correct = metrics.get(primary_metric, 0.0) == 1.0
        
        return {
            "id": sample.get("id"),
            "question": sample.get("question"),
            "llm_answer": llm_output.get("final_answer"),
            "target": sample.get("ground_truth"),
            "is_correct": is_correct,
        }
    
    def parse_structured_output(self, response_text: str) -> BaseModel:
        """
        Parse LLM response text into structured output.
        
        Args:
            response_text: Raw text response from LLM
        
        Returns:
            Parsed BaseModel instance matching get_generator_schema()
        
        Raises:
            ValueError: If parsing or validation fails
        
        Note:
            Default implementation extracts JSON from markdown code blocks.
            Override this method for custom parsing logic.
        """
        schema = self.get_generator_schema()
        
        # Extract JSON from markdown code blocks
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            json_lines = []
            in_json = False
            for line in lines:
                if line.strip().startswith("```json"):
                    in_json = True
                    continue
                elif line.strip().startswith("```") and in_json:
                    break
                elif in_json:
                    json_lines.append(line)
            if json_lines:
                text = "\n".join(json_lines)
            elif "```" in text:
                parts = text.split("```")
                if len(parts) >= 3:
                    text = parts[1]
        
        # Parse JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in text
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
            if json_match:
                data = json.loads(json_match.group())
            else:
                raise ValueError(f"Could not parse JSON from response: {text[:200]}")
        
        # Validate against schema
        try:
            return schema(**data)
        except ValidationError as e:
            raise ValueError(f"Validation failed: {e}")
