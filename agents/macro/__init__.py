"""
Macro Agents — Paquete de agentes macro orquestadores.

Los macro-agentes coordinan la activación de micro-agentes (skills),
gestionan el flujo general del ecosistema y reportan al supervisor principal.
"""

from agents.macro.base_macro_agent import BaseMacroAgent
from agents.macro.supervisor_agent import SupervisorAgent
from agents.macro.resource_orchestrator import ResourceOrchestrator
from agents.macro.status_monitor import StatusMonitor
from agents.macro.priority_manager import PriorityManager

__all__ = [
    "BaseMacroAgent",
    "SupervisorAgent",
    "ResourceOrchestrator",
    "StatusMonitor",
    "PriorityManager",
]
