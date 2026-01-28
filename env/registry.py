"""Centralized environment registry for MCE."""

from typing import Dict, Type
from .base import TaskEnvironment


class EnvironmentRegistry:
    """Registry for task environments."""
    
    _registry: Dict[str, Type[TaskEnvironment]] = {}
    
    @classmethod
    def register(cls, name: str, env_class: Type[TaskEnvironment]):
        """Register an environment class."""
        cls._registry[name] = env_class
    
    @classmethod
    def get(cls, name: str) -> TaskEnvironment:
        """Get an environment instance by name."""
        if name not in cls._registry:
            raise ValueError(f"Unknown environment: {name}. Available: {list(cls._registry.keys())}")
        return cls._registry[name]()
    
    @classmethod
    def list_environments(cls) -> list:
        """List all registered environment names."""
        return list(cls._registry.keys())


def get_environment(name: str) -> TaskEnvironment:
    """Get an environment instance by name."""
    return EnvironmentRegistry.get(name)


def get_task_instruction(env_name: str) -> str:
    """Get task instruction for an environment."""
    if env_name == "finer":
        from .finer.task_instruction import task_instruction
    elif env_name == "uspto":
        from .uspto.task_instruction import task_instruction
    elif env_name == "aegis2":
        from .aegis2.task_instruction import task_instruction
    elif env_name == "crime_prediction":
        from .crime_prediction.task_instruction import task_instruction
    elif env_name == "symptom_diagnosis":
        from .symptom_diagnosis.task_instruction import task_instruction
    else:
        raise ValueError(f"Unknown environment: {env_name}")
    return task_instruction

