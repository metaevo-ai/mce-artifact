import json
import logging
import re
from typing import Any, Dict, List

from env import EnvironmentResult, Sample, TaskEnvironment

logger = logging.getLogger(__name__)


class CrimePredictionResponse:
    """Simple wrapper for crime prediction response."""
    def __init__(self, reasoning: str, final_answer: str):
        self.reasoning = reasoning
        self.final_answer = final_answer
    
    def model_dump(self):
        """For compatibility with eval code."""
        return {"reasoning": self.reasoning, "final_answer": self.final_answer}


class CrimePredictionEnvironment(TaskEnvironment):
    """Environment for Chinese legal crime prediction task."""
    
    def __init__(self):
        pass

    def get_primary_metric_name(self) -> str:
        """Return the primary metric name for crime prediction environment."""
        return "accuracy"
    
    def parse_structured_output(self, response_text: str):
        """
        Parse crime prediction response to extract crimes from [罪名]...<eoa> format.
        
        Args:
            response_text: Raw text response from LLM
        
        Returns:
            CrimePredictionResponse with extracted crimes
        """
        # Extract crimes from [罪名]...<eoa> format
        pattern = r'\[罪名\](.*?)(?:<eoa>|$)'
        match = re.search(pattern, response_text)
        
        if match:
            crimes = match.group(1).strip()
        else:
            # Fallback: try to find crimes after 罪名: or similar patterns
            logger.warning(f"No [罪名]...<eoa> format found, attempting fallback extraction")
            pattern = r'罪名[:：](.*?)(?:\n|$)'
            match = re.search(pattern, response_text)
            if match:
                crimes = match.group(1).strip()
            else:
                # Last resort: try to find common crime names in the text
                logger.error(f"Could not extract crimes from response: {response_text[:200]}")
                crimes = "未知罪名"
        
        return CrimePredictionResponse(reasoning=response_text, final_answer=crimes)

    async def get_generator_prompt(self, sample: Sample, playbook_context: str) -> str:
        """
        Build a specialized prompt for crime prediction task.
        
        Args:
            sample: The crime prediction sample with case facts
            playbook_context: Retrieved context/instructions for this sample
        
        Returns:
            Formatted prompt string optimized for crime prediction
        """
        # Build prompt with instructional context if provided
        context_section = ""
        if playbook_context and playbook_context.strip():
            context_section = f"\n\n## 指导上下文\n{playbook_context}\n"
        
        prompt = f"""请你模拟法官依据下面事实给出罪名。请先进行推理分析，然后将最终答案写在[罪名]和<eoa>之间。

格式示例：
- 单个罪名: [罪名]盗窃<eoa>
- 多个罪名: [罪名]盗窃;诈骗<eoa>
{context_section}

## 案件事实
{sample.question}"""
        return prompt

    def load_samples(self, path: str, limit: int = 10, random_sample: bool = False, shuffle: bool = False) -> List[Sample]:
        """Load samples from the benchmark.

        Args:
            path: Path to the data file to load
            limit: Maximum number of samples to load
            random_sample: If True, randomly sample limit items; if False, take first limit items
            shuffle: If True, shuffle the order of loaded samples

        Returns:
            List of Sample objects
        """
        import random
        
        # First, load all samples (or up to limit if not random sampling)
        all_samples = []
        with open(path, encoding="utf-8") as f:
            for i, row in enumerate(f):
                if not random_sample and limit is not None and i >= limit:
                    break
                data = json.loads(row)
                
                sample = Sample(
                    id=i,
                    question=data["question"],
                    context="",  # Crime prediction dataset has no additional context
                    ground_truth=data["answer"],
                )
                all_samples.append(sample)
        
        # If random sampling and we have more samples than limit, randomly sample
        if random_sample and limit is not None and len(all_samples) > limit:
            samples = random.sample(all_samples, limit)
        else:
            samples = all_samples
        
        # Shuffle if requested (affects order for mini-batching)
        if shuffle:
            random.shuffle(samples)
        
        return samples

    def _extract_crimes(self, text: str) -> set:
        """
        Extract crime names from text.
        Handles formats like:
        - [罪名]盗窃<eoa>
        - [罪名]盗窃;诈骗<eoa>
        - 罪名:盗窃
        - 盗窃;诈骗
        """
        # Try to extract from [罪名]...<eoa> format
        pattern = r'\[罪名\](.*?)(?:<eoa>|$)'
        match = re.search(pattern, text)
        if match:
            crimes_str = match.group(1).strip()
        else:
            # Try to extract from 罪名: format
            pattern = r'罪名[:：](.*?)(?:\n|$)'
            match = re.search(pattern, text)
            if match:
                crimes_str = match.group(1).strip()
            else:
                # Fallback: use the entire text
                crimes_str = text.strip()
        
        # Remove common suffixes and clean up
        crimes_str = re.sub(r'<eoa>.*', '', crimes_str).strip()
        
        # Split by semicolon or other delimiters
        crimes = re.split(r'[;；,，、]', crimes_str)
        
        # Clean each crime name
        crimes = [c.strip() for c in crimes if c.strip()]
        
        return set(crimes)

    def _crime_answer_is_correct(self, predicted: str, ground_truth: str) -> bool:
        """
        Check if predicted crimes match ground truth.
        
        This is a set matching problem - both sets of crimes must match.
        """
        pred_crimes = self._extract_crimes(predicted)
        gt_crimes = self._extract_crimes(ground_truth)
        
        # Exact match required
        return pred_crimes == gt_crimes

    async def aevaluate(self, sample: Sample, generator_output: str) -> EnvironmentResult:
        """Evaluate the generator output against the ground truth."""
        ground_truth_str = sample.ground_truth

        is_correct = self._crime_answer_is_correct(generator_output, ground_truth_str)

        accuracy = 1.0 if is_correct else 0.0

        if accuracy == 1.0:
            feedback = "正确！你的罪名预测与标准答案完全一致。"
        else:
            feedback = f"不正确。正确答案是: {ground_truth_str}"

        return EnvironmentResult(
            feedback=feedback,
            ground_truth=sample.ground_truth,
            metrics={"accuracy": accuracy},
        )

    def format_result_for_training(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a single evaluation result for training data.
        
        For crime prediction, we include:
        - The case facts (question)
        - The model's complete response (with reasoning)
        - The model's predicted crimes (extracted from [罪名]...<eoa>)
        - The ground truth crimes
        - Whether the prediction was correct
        
        Args:
            item: Raw evaluation result with nested structure
        
        Returns:
            Formatted dict with fields to include in training data
        """
        sample = item.get("sample", {})
        llm_output = item.get("llm_output", {})
        evaluation = item.get("evaluation", {})
        metrics = evaluation.get("metrics", {})
        
        # Get primary metric value
        primary_metric = self.get_primary_metric_name()
        is_correct = metrics.get(primary_metric, 0.0) == 1.0
        
        # Build the result dict
        result = {
            "id": sample.get("id"),
            "case_facts": sample.get("question"),
            "llm_response": llm_output.get("reasoning", ""),
            "llm_predicted_crimes": llm_output.get("final_answer"),
            "ground_truth_crimes": sample.get("ground_truth"),
            "is_correct": is_correct,
        }

        return result
