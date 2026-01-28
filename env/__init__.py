from .base import EnvironmentResult, Sample, TaskEnvironment
from .registry import EnvironmentRegistry, get_environment, get_task_instruction

# Register environments
from .finer import FinerEnvironment
from .uspto import USPTOEnvironment
from .aegis2 import Aegis2Environment
from .crime_prediction import CrimePredictionEnvironment
from .symptom_diagnosis import SymptomDiagnosisEnvironment

EnvironmentRegistry.register("finer", FinerEnvironment)
EnvironmentRegistry.register("uspto", USPTOEnvironment)
EnvironmentRegistry.register("aegis2", Aegis2Environment)
EnvironmentRegistry.register("crime_prediction", CrimePredictionEnvironment)
EnvironmentRegistry.register("symptom_diagnosis", SymptomDiagnosisEnvironment)
__all__ = [
    "EnvironmentResult",
    "Sample", 
    "TaskEnvironment",
    "get_environment",
    "get_task_instruction",
]
