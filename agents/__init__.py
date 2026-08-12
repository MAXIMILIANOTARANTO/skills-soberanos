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

from .protocol import (
    AgentEvent,
    AgentMessage,
    AgentTier,
    MessageType,
    TaskRequest,
    TaskResult,
    TaskStatus,
    make_error_result,
    make_success_result,
    make_task_request,
)
from .registry import AgentRegistry, ECOSYSTEM_REPOS, get_global_registry
from .loader import SkillLoader
from .micro import (
    BaseMicroAgent,
    CoherencePulseAgent,
    MemoryManagerAgent,
    MetaHiloGrokAgent,
)
from .macro import (
    BaseMacroAgent,
    PriorityManager,
    ResourceOrchestrator,
    StatusMonitor,
    SupervisorAgent,
)

__all__ = [
    # Protocol
    "AgentMessage",
    "AgentEvent",
    "MessageType",
    "TaskRequest",
    "TaskResult",
    "TaskStatus",
    "AgentTier",
    "make_task_request",
    "make_success_result",
    "make_error_result",
    # Registry & Loader
    "AgentRegistry",
    "ECOSYSTEM_REPOS",
    "get_global_registry",
    "SkillLoader",
    # Micro
    "BaseMicroAgent",
    "CoherencePulseAgent",
    "MemoryManagerAgent",
    "MetaHiloGrokAgent",
    # Macro
    "BaseMacroAgent",
    "SupervisorAgent",
    "ResourceOrchestrator",
    "StatusMonitor",
    "PriorityManager",
]
