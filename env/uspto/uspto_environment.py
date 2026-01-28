import json
import os

from env import EnvironmentResult, Sample, TaskEnvironment



class USPTOEnvironment(TaskEnvironment):
    def __init__(self):
        """Initialize USPTOEnvironment for retrosynthesis prediction."""
        pass

    def get_primary_metric_name(self) -> str:
        """Return the primary metric name for USPTO environment."""
        return "accuracy"

    async def get_generator_prompt(self, sample: Sample, playbook_context: str) -> str:
        """
        Build a specialized prompt for USPTO retrosynthesis prediction.
        
        Args:
            sample: The USPTO retrosynthesis sample
            playbook_context: Retrieved context/instructions for this sample
        
        Returns:
            Formatted prompt string optimized for retrosynthesis reasoning
        """
        prompt = f"""You are an expert organic chemist specializing in retrosynthesis analysis.

Retrosynthesis Problem:
{sample.question}

Strategic Context:
{playbook_context}

Instructions:
- Analyze the product structure and identify key functional groups and bonds
- Consider the reaction type and typical disconnection strategies
- Think through the retrosynthetic analysis step-by-step
- Propose the most likely precursor reactants based on the reaction mechanism
- Output SMILES strings separated by periods (.) for multiple reactants
- Ignore atom mapping numbers in your analysis

You MUST respond with a valid JSON object containing exactly two fields:
1. "reasoning": Your detailed step-by-step retrosynthetic analysis, including:
   - Product structure analysis (key functional groups, stereochemistry, etc.)
   - Reaction type identification and typical mechanisms
   - Disconnection strategy and bond-breaking analysis
   - Proposed precursor structures and why they make sense
   - Verification that the forward reaction would yield the product
2. "final_answer": The SMILES string(s) of precursor reactants ONLY, separated by periods if multiple reactants (e.g., "CC(=O)Cl.c1ccccc1O")

Example response format:
{{
  "reasoning": "Your step-by-step retrosynthetic analysis... (less than 200 words)",
  "final_answer": "O=C=O.c1ccc(CO)cc1.C1CNCC1O"
}}"""
        return prompt

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

    def _normalize_smiles(self, smiles: str) -> str:
        """Normalize SMILES string for comparison."""
        # Remove whitespace and convert to lowercase for comparison
        return smiles.strip().lower()

    def _parse_reactants(self, smiles_string: str) -> set[str]:
        """Parse reactants from SMILES string separated by periods."""
        reactants = smiles_string.split(".")
        return {self._normalize_smiles(r) for r in reactants if r.strip()}

    async def aevaluate(
        self, sample: Sample, generator_output
    ) -> EnvironmentResult:
        """Evaluate predicted reactants against ground truth.
        
        For retrosynthesis, we check if the predicted reactants match the ground truth.
        Since reactants can be in any order, we compare them as sets.
        """
        # Extract final answer from generator output
        if isinstance(generator_output, str):
            predicted_smiles = generator_output
        elif hasattr(generator_output, 'final_answer'):
            predicted_smiles = generator_output.final_answer
        else:
            predicted_smiles = str(generator_output)
        
        ground_truth_str = sample.ground_truth
        
        # Parse predicted and ground truth reactants
        predicted_reactants = self._parse_reactants(predicted_smiles)
        ground_truth_reactants = self._parse_reactants(ground_truth_str)
        
        # Check if sets match exactly
        exact_match = predicted_reactants == ground_truth_reactants
        
        # Calculate partial credit: intersection / union (Jaccard similarity)
        if len(predicted_reactants) == 0 and len(ground_truth_reactants) == 0:
            jaccard_similarity = 1.0
        elif len(predicted_reactants) == 0 or len(ground_truth_reactants) == 0:
            jaccard_similarity = 0.0
        else:
            intersection = len(predicted_reactants & ground_truth_reactants)
            union = len(predicted_reactants | ground_truth_reactants)
            jaccard_similarity = intersection / union if union > 0 else 0.0
        
        if exact_match:
            feedback = "Predicted reactants match ground truth exactly"
        else:
            feedback = f"Predicted reactants do not match ground truth. Jaccard similarity: {jaccard_similarity:.2f}"
        
        return EnvironmentResult(
            feedback=feedback,
            ground_truth=sample.ground_truth,
            metrics={
                "accuracy": 1.0 if exact_match else 0.0,
                "jaccard_similarity": jaccard_similarity,
            },
        )

    def format_result_for_training(self, item: dict) -> dict:
        """
        Format a single evaluation result for training data.
        
        For USPTO retrosynthesis, we include reasoning since it's a reasoning-heavy task
        where the step-by-step retrosynthetic analysis is crucial for learning.
        
        Args:
            item: Raw evaluation result with nested structure:
                {
                    "sample": {id, question, context, ground_truth, ...extras},
                    "llm_output": {reasoning, final_answer, ...},
                    "evaluation": {playbook_context, feedback, metrics}
                }
        
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
        
        return {
            "id": sample.get("id"),
            "question": sample.get("question"),
            "reasoning": llm_output.get("reasoning"),
            "llm_answer": llm_output.get("final_answer"),
            "target": sample.get("ground_truth"),
            "is_correct": is_correct,
            "jaccard_similarity": metrics.get("jaccard_similarity", 0.0),
        }

