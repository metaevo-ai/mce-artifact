"""
Trajectory collector for sequential tasks with generation-reflection-regeneration loops.
"""

import json
import logging
import asyncio
from typing import Any, Dict, List
from pydantic import BaseModel, Field

from env.base import Sample, Trajectory, TaskEnvironment, EnvironmentResult

logger = logging.getLogger(__name__)


class GeneratorSchema(BaseModel):
    """Schema for Generator output."""
    reasoning: str = Field(description="Your step-by-step analysis and calculations")
    final_answer: str = Field(description="Your concise final answer")


class TrajectoryCollector:
    """
    Collect reasoning trajectories through generation-reflection-regeneration loops.
    
    For each sample:
    1. Generator produces reasoning + answer
    2. Environment evaluates (provides accuracy feedback)
    3. If correct (acc == 1.0), record success trajectory
    4. If incorrect and iterations remain:
       - Reflector analyzes the error and provides improvement guidance
       - Loop back to step 1 with history
    5. If max iterations reached, record failure trajectory
    """
    
    def __init__(
        self,
        env: TaskEnvironment,
        generator_llm,
        reflector_llm,
        max_iterations: int = 3,
    ):
        """
        Initialize trajectory collector.
        
        Args:
            env: Task environment for evaluation
            generator_llm: LLM client for generating answers
            reflector_llm: LLM client for reflection and guidance
            max_iterations: Maximum number of generation-reflection iterations
        """
        raise NotImplementedError("TrajectoryCollector is not implemented yet")
        self.env = env
        self.generator = generator_llm
        self.reflector = reflector_llm
        self.max_iterations = max_iterations
    
    async def collect_single(
        self,
        sample: Sample,
        playbook_context: str,
    ) -> Trajectory:
        """
        Collect a single trajectory for a sample.
        
        Args:
            sample: Sample to solve
            playbook_context: Context retrieved for this sample
            
        Returns:
            Trajectory with steps, final answer, and correctness
        """
        steps = []
        history = []  # Conversation history for multi-turn
        final_answer = ""
        final_acc = 0.0
        
        for i in range(self.max_iterations):
            try:
                # 1. Generator produces reasoning + answer (timeout handled in LLM client)
                prompt = await self._build_generator_prompt(sample, playbook_context, history)
                output = await self.generator.ainvoke(
                    prompt,
                    parse_function=self.env.parse_structured_output
                )
                result: EnvironmentResult = await self.env.aevaluate(sample, output.final_answer)
                acc = result.metrics.get("accuracy", 0.0)
                
                step = {
                    "iteration": i,
                    "reasoning": output.reasoning,
                    "answer": output.final_answer,
                    "accuracy": acc,
                    "feedback": result.feedback,
                }
                
                final_answer = output.final_answer
                final_acc = acc
                
                # 3. Check if correct
                if acc == 1.0:
                    steps.append(step)
                    return Trajectory(
                        steps=steps,
                        final_answer=final_answer,
                        is_correct=True,
                        reward=1.0,
                    )
                
                # 4. Reflector analyzes and provides guidance (timeout handled in LLM client)
                reflection = await self._reflect(sample, output, result)
                step["reflection"] = reflection
                steps.append(step)
                
                # 5. Update history for next iteration
                history.append(step)
                
            except Exception as e:
                logger.error(f"❌ Error at iteration {i} for sample {sample.id}: {e}")
                # Record error step and continue to next iteration
                step = {
                    "iteration": i,
                    "reasoning": f"Error: {str(e)}",
                    "answer": "",
                    "accuracy": 0.0,
                    "feedback": f"Error occurred: {str(e)}",
                    "reflection": "Error occurred, skipping this iteration",
                }
                steps.append(step)
                continue
        
        # Max iterations reached without success
        return Trajectory(
            steps=steps,
            final_answer=final_answer,
            is_correct=False,
            reward=final_acc,
        )
    
    async def _build_generator_prompt(
        self,
        sample: Sample,
        playbook_context: str,
        history: List[Dict[str, Any]],
    ) -> str:
        """
        Build prompt for generator with context and history.
        
        Args:
            sample: Sample to solve
            playbook_context: Retrieved context
            history: Previous attempts with feedback and reflections
            
        Returns:
            Prompt string
        """
        # If no history, use environment's base prompt
        if not history:
            return await self.env.get_generator_prompt(sample, playbook_context)
        
        # With history, build on top of environment's base prompt structure
        prompt_parts = [
            "You are an expert domain problem solver.",
            "",
            "Task Context:",
            sample.context,
            "",
            "Instructional Context:",
            playbook_context,
            "",
        ]
        
        # Add history
        prompt_parts.append("Previous Attempts:")
        for h in history:
            prompt_parts.append(f"\n--- Attempt {h['iteration'] + 1} ---")
            prompt_parts.append(f"Your reasoning: {h['reasoning']}")
            prompt_parts.append(f"Your answer: {h['answer']}")
            prompt_parts.append(f"Feedback: {h['feedback']} (Accuracy: {h['accuracy']:.2f})")
            if h.get('reflection'):
                prompt_parts.append(f"Reflection: {h['reflection']}")
        prompt_parts.append("")
        prompt_parts.append("Based on the feedback and reflection above, try again with improvements.")
        prompt_parts.append("")
        
        prompt_parts.extend([
            f"Question: {sample.question}",
            "",
            "You MUST respond with a valid JSON object containing exactly two fields:",
            "1. \"reasoning\": Your step-by-step analysis (string)",
            "2. \"final_answer\": Your concise final answer (string)",
        ])
        
        return "\n".join(prompt_parts)
    
    async def _reflect(
        self,
        sample: Sample,
        generator_output: Any,
        eval_result: EnvironmentResult,
    ) -> str:
        """
        Use reflector to analyze the error and provide improvement guidance.
        
        Args:
            sample: Sample being solved
            generator_output: Generator's output
            eval_result: Environment evaluation result
            
        Returns:
            Reflection string with improvement guidance
        """
        reflection_prompt = f"""You are a reflective agent analyzing a failed attempt at solving a problem.

Question: {sample.question}
Ground Truth: {sample.ground_truth}

Previous Attempt:
- Reasoning: {generator_output.reasoning}
- Answer: {generator_output.final_answer}
- Accuracy: {eval_result.metrics.get('accuracy', 0.0):.2f}
- Feedback: {eval_result.feedback}

Analyze what went wrong and provide specific guidance on how to improve the answer.
Focus on:
1. What errors were made in the reasoning or answer?
2. What should be done differently in the next attempt?
3. Any patterns or rules that were missed?

Only output the guidance (less than 150 words), no other text."""
        
        try:
            # Timeout handled in LLM client
            reflection = await self.reflector.ainvoke(reflection_prompt)
            # Return text response directly
            return reflection
        except Exception as e:
            logger.warning(f"⚠️ Reflector failed for sample {sample.id}: {e}")
            return f"Reflection error: {str(e)}"



if __name__ == "__main__":
    
    async def main():
        from env.formula import FormulaEnvironment
        
        # Load actual formula data
        env = FormulaEnvironment()
        samples = env.load_samples(path="env/formula/data/test.jsonl", limit=20)
        
        for sample in samples:
            print("TESTING TRAJECTORY COLLECTOR")            
            # Initialize collector
            from mce.llm_client import LLMClient
            llm = LLMClient(model="deepseek/deepseek-chat-v3.1")
            collector = TrajectoryCollector(
                env=env,
                generator_llm=llm,
                reflector_llm=llm,
                max_iterations=3,
            )
            
            # Collect trajectory
            print("🔄 Collecting trajectory...")
            traj = await collector.collect_single(sample, playbook_context="")
            
            # Pretty print trajectory
            print("\n" + "=" * 80)
            print("TRAJECTORY RESULTS")
            print("=" * 80)
            print(f"\n✅ Success: {traj.is_correct}")
            print(f"🎯 Final Answer: {traj.final_answer}")
            print(f"📊 Reward: {traj.reward}")
            print(f"🔢 Number of Iterations: {len(traj.steps)}")
            
            print(f"\n📋 Step-by-Step Process:")
            for i, step in enumerate(traj.steps, 1):
                print(f"\n  {'─' * 76}")
                print(f"  Iteration {step['iteration'] + 1}:")
                print(f"  {'─' * 76}")
                print(f"  💭 Reasoning: {step['reasoning'][:200]}...")
                print(f"  💡 Answer: {step['answer']}")
                print(f"  📈 Accuracy: {step['accuracy']:.2f}")
                print(f"  📢 Feedback: {step['feedback']}")
                if step.get('reflection'):
                    print(f"  🔍 Reflection: {step['reflection'][:200]}...")
            
            print("\n" + "=" * 80)

        return "✅ Test completed"

    res = asyncio.run(main())
    print(f"\n{res}")