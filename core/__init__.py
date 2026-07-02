"""
Ecosistema Soberano - Paquete principal
Importa todos los módulos y skills del ecosistema.
"""

__version__ = "1.0.0"
__author__ = "Maximiliano Taranto"
__description__ = "Sistema IA autónomo y soberano basado en GitHub"

# Core imports
from core.llm_engine import EcosystemLLM
from core.memory_github_manager import MemoryGitHubManager
from core.coherence_meter import QuantitativeCoherenceMeter
from core.orchestrator_engine import OrchestratorEngine
from core.coherence_router import CoherenceRouter
from core.skill_base import Skill

__all__ = [
    "EcosystemLLM",
    "MemoryGitHubManager",
    "QuantitativeCoherenceMeter",
    "OrchestratorEngine",
    "CoherenceRouter",
    "Skill",
]
