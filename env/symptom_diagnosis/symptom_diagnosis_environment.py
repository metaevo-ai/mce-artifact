import json
import logging
import re
from typing import Any, Dict, List

from env import EnvironmentResult, Sample, TaskEnvironment

logger = logging.getLogger(__name__)


class SymptomDiagnosisResponse:
    """Simple wrapper for symptom diagnosis response."""
    def __init__(self, reasoning: str, final_answer: str):
        self.reasoning = reasoning
        self.final_answer = final_answer
    
    def model_dump(self):
        """For compatibility with eval code."""
        return {"reasoning": self.reasoning, "final_answer": self.final_answer}


class SymptomDiagnosisEnvironment(TaskEnvironment):
    """Environment for medical symptom-based diagnosis prediction task."""
    
    def __init__(self):
        pass

    def get_primary_metric_name(self) -> str:
        """Return the primary metric name for symptom diagnosis environment."""
        return "accuracy"
    
    def parse_structured_output(self, response_text: str):
        """
        Parse symptom diagnosis response to extract diagnosis.
        
        Args:
            response_text: Raw text response from LLM
        
        Returns:
            SymptomDiagnosisResponse with extracted diagnosis
        """
        # Try to extract diagnosis from [DIAGNOSIS]...[/DIAGNOSIS] format
        pattern = r'\[DIAGNOSIS\](.*?)\[/DIAGNOSIS\]'
        match = re.search(pattern, response_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            diagnosis = match.group(1).strip()
        else:
            # Fallback: try to find diagnosis after "Diagnosis:" or similar patterns
            logger.warning(f"No [DIAGNOSIS]...[/DIAGNOSIS] format found, attempting fallback extraction")
            pattern = r'(?:diagnosis|final diagnosis|conclusion)[:：]\s*([^\n]+)'
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                diagnosis = match.group(1).strip()
            else:
                # Last resort: look for common disease names in the last few lines
                logger.error(f"Could not extract diagnosis from response: {response_text[:200]}")
                lines = response_text.strip().split('\n')
                diagnosis = lines[-1].strip() if lines else "unknown"
        
        # Clean up the diagnosis (remove trailing punctuation, extra spaces)
        diagnosis = re.sub(r'[.!?]+$', '', diagnosis).strip()
        
        return SymptomDiagnosisResponse(reasoning=response_text, final_answer=diagnosis)

    async def get_generator_prompt(self, sample: Sample, playbook_context: str) -> str:
        """
        Build a specialized prompt for symptom diagnosis task.
        
        Args:
            sample: The symptom diagnosis sample with patient symptoms
            playbook_context: Retrieved context/instructions for this sample
        
        Returns:
            Formatted prompt string optimized for medical diagnosis
        """
        # Build prompt with instructional context if provided
        context_section = ""
        if playbook_context and playbook_context.strip():
            context_section = f"\n\n## Instructional Context\n{playbook_context}\n"
        
        prompt = f"""You are an expert medical diagnostician. Based on the patient's symptoms, provide a diagnosis. 

Possible diagnoses include: drug reaction, allergy, chicken pox, diabetes, psoriasis, hypertension, cervical spondylosis, bronchial asthma, varicose veins, malaria, dengue, arthritis, impetigo, fungal infection, common cold, gastroesophageal reflux disease, urinary tract infection, typhoid, pneumonia, peptic ulcer disease, jaundice, migraine.

Please analyze the symptoms step by step, then provide your final diagnosis in the format:
[DIAGNOSIS]diagnosis_name[/DIAGNOSIS]

For example:
[DIAGNOSIS]diabetes[/DIAGNOSIS]
{context_section}

## Patient Symptoms
{sample.question}

Please provide your reasoning and final diagnosis."""
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
                    context="",  # Symptom diagnosis dataset has no additional context
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

    def _normalize_diagnosis(self, diagnosis: str) -> str:
        """
        Normalize diagnosis string for comparison.
        
        - Convert to lowercase
        - Remove extra whitespace
        - Remove trailing punctuation
        """
        diagnosis = diagnosis.lower().strip()
        diagnosis = re.sub(r'\s+', ' ', diagnosis)  # Normalize whitespace
        diagnosis = re.sub(r'[.!?]+$', '', diagnosis)  # Remove trailing punctuation
        return diagnosis

    def _diagnosis_is_correct(self, predicted: str, ground_truth: str) -> bool:
        """
        Check if predicted diagnosis matches ground truth.
        
        Uses normalized string comparison (case-insensitive, whitespace-normalized).
        """
        pred_normalized = self._normalize_diagnosis(predicted)
        gt_normalized = self._normalize_diagnosis(ground_truth)
        
        return pred_normalized == gt_normalized

    async def aevaluate(self, sample: Sample, generator_output: str) -> EnvironmentResult:
        """Evaluate the generator output against the ground truth."""
        ground_truth_str = sample.ground_truth

        is_correct = self._diagnosis_is_correct(generator_output, ground_truth_str)

        accuracy = 1.0 if is_correct else 0.0

        if accuracy == 1.0:
            feedback = "Correct! Your diagnosis matches the ground truth."
        else:
            feedback = f"Incorrect. The correct diagnosis is: {ground_truth_str}"

        return EnvironmentResult(
            feedback=feedback,
            ground_truth=sample.ground_truth,
            metrics={"accuracy": accuracy},
        )

    def format_result_for_training(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a single evaluation result for training data.
        
        For symptom diagnosis, we include:
        - The patient symptoms (question)
        - The model's complete response (with reasoning)
        - The model's predicted diagnosis (extracted from [DIAGNOSIS]...[/DIAGNOSIS])
        - The ground truth diagnosis
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
            "patient_symptoms": sample.get("question"),
            "llm_response": llm_output.get("reasoning", ""),
            "llm_diagnosis": llm_output.get("final_answer"),
            "ground_truth_diagnosis": sample.get("ground_truth"),
            "is_correct": is_correct,
        }

        return result
