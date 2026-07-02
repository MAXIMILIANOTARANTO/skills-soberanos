"""
Agents — Sistema jerárquico de agentes soberanos.

Estructura:
    agents/
    ├── protocol.py          — Mensajes y eventos entre agentes
    ├── registry.py          — Registro central de agentes
    ├── loader.py            — Carga dinámica de skills como micro-agentes
    ├── micro/               — Agentes micro (uno por skill)
    │   ├── base_micro_agent.py
    │   ├── coherence_pulse_agent.py
    │   ├── memory_manager_agent.py
    │   └── meta_hilo_grok_agent.py
    └── macro/               — Agentes macro orquestadores
        ├── base_macro_agent.py
        ├── supervisor_agent.py
        ├── resource_orchestrator.py
        ├── status_monitor.py
        └── priority_manager.py

Uso rápido:
    from agents.loader import SkillLoader
    from agents.macro.supervisor_agent import SupervisorAgent

    loader = SkillLoader()
    micro_agents = loader.load_all()
    supervisor = SupervisorAgent(micro_agents=micro_agents)
    result = supervisor.handle("Analizar coherencia del ecosistema")
"""

from agents.protocol import AgentMessage, AgentEvent, TaskRequest, TaskResult
from agents.registry import AgentRegistry
from agents.loader import SkillLoader
from agents.micro.base_micro_agent import BaseMicroAgent
from agents.macro.base_macro_agent import BaseMacroAgent
from agents.macro.supervisor_agent import SupervisorAgent
from agents.macro.resource_orchestrator import ResourceOrchestrator
from agents.macro.status_monitor import StatusMonitor
from agents.macro.priority_manager import PriorityManager

__all__ = [
    # Protocol
    "AgentMessage",
    "AgentEvent",
    "TaskRequest",
    "TaskResult",
    # Registry & Loader
    "AgentRegistry",
    "SkillLoader",
    # Micro
    "BaseMicroAgent",
    # Macro
    "BaseMacroAgent",
    "SupervisorAgent",
    "ResourceOrchestrator",
    "StatusMonitor",
    "PriorityManager",
]
