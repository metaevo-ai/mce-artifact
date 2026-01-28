import json
import os
from typing import Any, Dict

from env import EnvironmentResult, Sample, TaskEnvironment

from .finer_context import FINER_CONTEXT


class FinerEnvironment(TaskEnvironment):
    def __init__(self):
        """Initialize FinerEnvironment with ACE-compatible simple feedback mode."""
        pass
    
    def get_primary_metric_name(self) -> str:
        """Return the primary metric name for Finer environment."""
        return "accuracy"
    
    def format_result_for_training(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format evaluation result for training data.
        
        For Finer, we include:
        - Basic fields: id, question, llm_answer, target
        - Correctness based on token-level accuracy (primary metric)
        
        Args:
            item: Nested evaluation result with sample, llm_output, evaluation
        
        Returns:
            Formatted dict for training
        """
        sample = item.get("sample", {})
        llm_output = item.get("llm_output", {})
        evaluation = item.get("evaluation", {})

        metrics = evaluation.get("metrics", {})
        
        # Finer uses token-level accuracy as primary metric
        token_accuracy = metrics.get("accuracy", 0.0)
        is_correct = token_accuracy == 1.0
        
        return {
            "id": sample.get("id"),
            "question": sample.get("question"),
            "llm_answer": llm_output.get("final_answer"),
            "target": sample.get("ground_truth"),
            "is_correct": is_correct,
        }

    def load_samples(self, path: str, limit: int = 10, random_sample: bool = False, shuffle: bool = False) -> list[Sample]:
        """Load samples from the benchmark.

        Args:
            path: Path to the data file to load
            limit: Maximum number of samples to load
            random_sample: If True, randomly sample limit items; if False, take first limit items
            shuffle: If True, shuffle the order of loaded samples (useful for mini-batching)

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
                    context=FINER_CONTEXT,
                    ground_truth=data["target"],
                    extras={},
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

    def _finer_answer_is_correct(
        self, predicted: str, ground_truth: str, return_counts: bool = False
    ) -> bool | tuple[int, int]:
        """
        XBRL dataset specific answer correctness check.
        """
        pred = predicted.split(",")
        pred = [val.lower().strip() for val in pred]
        label = ground_truth.split(",")
        label = [val.lower().strip() for val in label]
        count = 0

        if len(pred) != len(label):
            if len(pred) > len(label):
                pred = pred[: len(label)]
            else:
                padding_needed = len(label) - len(pred)
                pred += [""] * padding_needed

        for prediction, ground_truth in zip(pred, label):
            try:
                ground_truth = eval(ground_truth)
                prediction = eval(prediction.replace(",", "").replace("$", ""))
            except:
                pass
            if ground_truth == prediction:
                count += 1

        score = count / len(pred) if pred else 0
        if return_counts:
            return count, len(pred)
        return score == 1

    async def aevaluate(
        self, sample: Sample, generator_output: str
    ) -> EnvironmentResult:
        ground_truth_str = sample.ground_truth

        # Use identical logic from data_processor.py
        correct_count, total_count = self._finer_answer_is_correct(
            generator_output, ground_truth_str, return_counts=True
        )

        # Token-level accuracy (count / total) - matches ACE framework's main metric
        accuracy = correct_count / total_count if total_count > 0 else 0.0

        if accuracy == 1.0:
            feedback = "Predicted answer matches ground truth"
        else:
            feedback = "Predicted answer does not match ground truth"

        return EnvironmentResult(
            feedback=feedback,
            ground_truth=sample.ground_truth,
            metrics={
                "accuracy": accuracy,
            },
        )