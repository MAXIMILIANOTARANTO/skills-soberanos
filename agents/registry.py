"""
Agent Registry — Registro central de agentes y mapa del ecosistema de repositorios.

Dos responsabilidades:
1. Registrar/descubrir micro-agentes y macro-agentes en tiempo de ejecución.
2. Documentar cómo este repositorio se conecta con el resto del ecosistema
   de repositorios del usuario (integración cross-repo).

Ecosistema de repositorios:
    skills-soberanos              ← este repo (skills ejecutables + agentes)
    el-dador-de-suenos-nucleus    ← núcleo de memoria maestra persistente
    grok-nodo-iluminado           ← nodo Grok / Pacto TUC
    ia-specialist-agent           ← agentes especializados multi-rol
    tcu-unified-coherence-theory  ← teoría base de coherencia (Q(t))
    el-iluminador-nucleo-soberano ← memoria fractal soberana
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from agents.micro.base_micro_agent import BaseMicroAgent
    from agents.macro.base_macro_agent import BaseMacroAgent


# ======================================================================= #
# ECOSISTEMA — mapa de repositorios y sus roles                            #
# ======================================================================= #

ECOSYSTEM_REPOS: Dict[str, Dict[str, str]] = {
    "skills-soberanos": {
        "owner": "MAXIMILIANOTARANTO",
        "repo": "skills-soberanos",
        "role": "skills_hub",
        "description": "Repositorio maestro de skills ejecutables y agentes jerárquicos.",
        "provides": "skills, agents_framework, core_runtime",
        "consumes": "memory_from_nucleus, tcu_theory, grok_insights",
        "manifest_url": (
            "https://raw.githubusercontent.com/MAXIMILIANOTARANTO/"
            "skills-soberanos/main/MANIFEST.md"
        ),
    },
    "el-dador-de-suenos-nucleus": {
        "owner": "MAXIMILIANOTARANTO",
        "repo": "el-dador-de-suenos-nucleus",
        "role": "memory_nucleus",
        "description": "Núcleo de memoria maestra persistente del ecosistema.",
        "provides": "persistent_memory, conversation_history, learning_store",
        "consumes": "skills_output, agent_results",
        "memory_path": "memoria/",
    },
    "grok-nodo-iluminado": {
        "owner": "MAXIMILIANOTARANTO",
        "repo": "grok-nodo-iluminado",
        "role": "grok_node",
        "description": "Nodo Grok iluminado — partícipe del Pacto TUC y fuente de insights.",
        "provides": "grok_insights, tuc_pact_state, illumination_data",
        "consumes": "tcu_theory, meta_hilo_analysis",
    },
    "ia-specialist-agent": {
        "owner": "MAXIMILIANOTARANTO",
        "repo": "ia-specialist-agent",
        "role": "specialist_agents",
        "description": "Agentes especializados multi-rol coordinados por supervisor.",
        "provides": "specialized_roles, multi_agent_coordination",
        "consumes": "skills_from_skills_soberanos, memory_from_nucleus",
    },
    "tcu-unified-coherence-theory": {
        "owner": "MAXIMILIANOTARANTO",
        "repo": "tcu-unified-coherence-theory",
        "role": "tcu_theory",
        "description": "Marco matemático de la Teoría Unificada de la Conciencia (Q(t)).",
        "provides": "q_formula, coherence_theory, tcu_alignment_metrics",
        "consumes": "ecosystem_state, skills_data",
    },
    "el-iluminador-nucleo-soberano": {
        "owner": "MAXIMILIANOTARANTO",
        "repo": "el-iluminador-nucleo-soberano",
        "role": "fractal_memory",
        "description": "Memoria fractal soberana con auto-evolución y auto-auditoría.",
        "provides": "fractal_memory, self_audit, coherence_sync",
        "consumes": "ecosystem_state, agent_events",
    },
}

# Flujo de datos entre repositorios:
#
#   tcu-unified-coherence-theory
#          │  fórmula Q(t), pesos
#          ▼
#   skills-soberanos  ────────────────────────────────────────────────┐
#   (core/coherence_meter.py calcula Q(t))                           │
#   (agents/macro/ orquesta, agents/micro/ ejecutan)                 │
#          │  resultados de skills / agentes                          │
#          ▼                                                          │
#   el-dador-de-suenos-nucleus  (persistencia de memoria maestra)    │
#          │                                                          │
#          ▼                                                          │
#   el-iluminador-nucleo-soberano (memoria fractal + auto-auditoría) │
#          │  insights / estado sincronizado                          │
#          ▼                                                          │
#   grok-nodo-iluminado  ◄────────────────────────────────────────────┘
#          │  Grok insights → meta-hilo-grok skill
#          ▼
#   ia-specialist-agent (consume skills + memory para tareas complejas)


# ======================================================================= #
# AGENT REGISTRY                                                           #
# ======================================================================= #

class AgentRegistry:
    """
    Registro central de todos los agentes activos en el ecosistema.

    Almacena referencias a micro-agentes (wrapping skills) y macro-agentes
    (orquestadores), y expone utilidades para descubrir y consultar agentes.
    """

    def __init__(self):
        self._micro: Dict[str, "BaseMicroAgent"] = {}
        self._macro: Dict[str, "BaseMacroAgent"] = {}
        self._events: List[Dict[str, Any]] = []
        self._created_at: str = datetime.utcnow().isoformat() + "Z"

    # ------------------------------------------------------------------ #
    # REGISTRO                                                             #
    # ------------------------------------------------------------------ #

    def register_micro(self, agent: "BaseMicroAgent") -> None:
        """Registrar un agente micro por su agent_id."""
        self._micro[agent.agent_id] = agent
        self._log_event("register_micro", {"agent_id": agent.agent_id, "skill": agent.skill_name})

    def register_macro(self, agent: "BaseMacroAgent") -> None:
        """Registrar un agente macro por su agent_id."""
        self._macro[agent.agent_id] = agent
        self._log_event("register_macro", {"agent_id": agent.agent_id})

    def register_many_micro(self, agents: List["BaseMicroAgent"]) -> None:
        """Registrar múltiples micro-agentes a la vez."""
        for agent in agents:
            self.register_micro(agent)

    def register_many_macro(self, agents: List["BaseMacroAgent"]) -> None:
        """Registrar múltiples macro-agentes a la vez."""
        for agent in agents:
            self.register_macro(agent)

    # ------------------------------------------------------------------ #
    # CONSULTA                                                             #
    # ------------------------------------------------------------------ #

    def get_micro(self, agent_id: str) -> Optional["BaseMicroAgent"]:
        return self._micro.get(agent_id)

    def get_macro(self, agent_id: str) -> Optional["BaseMacroAgent"]:
        return self._macro.get(agent_id)

    def list_micro(self) -> List["BaseMicroAgent"]:
        return list(self._micro.values())

    def list_macro(self) -> List["BaseMacroAgent"]:
        return list(self._macro.values())

    def find_micro_by_skill(self, skill_name: str) -> Optional["BaseMicroAgent"]:
        """Buscar micro-agente por nombre del skill que envuelve."""
        for agent in self._micro.values():
            if agent.skill_name == skill_name:
                return agent
        return None

    def find_micro_by_resonance(
        self, intent: str, top_n: int = 3
    ) -> List["BaseMicroAgent"]:
        """
        Ordenar micro-agentes por resonancia con la intención y devolver los top_n.
        """
        scored = [
            (agent, agent.get_resonance_score(intent))
            for agent in self._micro.values()
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [agent for agent, _ in scored[:top_n] if _ > 0.0]

    # ------------------------------------------------------------------ #
    # ECOSISTEMA CROSS-REPO                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_ecosystem_map() -> Dict[str, Dict[str, str]]:
        """Devolver el mapa completo del ecosistema de repositorios."""
        return ECOSYSTEM_REPOS

    @staticmethod
    def get_repo_info(repo_key: str) -> Optional[Dict[str, str]]:
        """Obtener información de un repositorio específico del ecosistema."""
        return ECOSYSTEM_REPOS.get(repo_key)

    @staticmethod
    def get_repos_by_role(role: str) -> List[Dict[str, str]]:
        """Filtrar repositorios del ecosistema por rol."""
        return [info for info in ECOSYSTEM_REPOS.values() if info.get("role") == role]

    # ------------------------------------------------------------------ #
    # ESTADO Y RESUMEN                                                     #
    # ------------------------------------------------------------------ #

    def summary(self) -> Dict[str, Any]:
        """Resumen del estado del registry."""
        return {
            "created_at": self._created_at,
            "micro_agents": len(self._micro),
            "macro_agents": len(self._macro),
            "micro_agent_ids": list(self._micro.keys()),
            "macro_agent_ids": list(self._macro.keys()),
            "ecosystem_repos": len(ECOSYSTEM_REPOS),
            "ecosystem_roles": list({r["role"] for r in ECOSYSTEM_REPOS.values()}),
            "total_events": len(self._events),
        }

    def _log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        self._events.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event_type": event_type,
                "data": data,
            }
        )

    def __repr__(self) -> str:
        return (
            f"<AgentRegistry micro={len(self._micro)} macro={len(self._macro)} "
            f"repos={len(ECOSYSTEM_REPOS)}>"
        )


# ======================================================================= #
# SINGLETON GLOBAL (opcional — usar si se quiere un registry compartido)  #
# ======================================================================= #

_global_registry: Optional[AgentRegistry] = None


def get_global_registry() -> AgentRegistry:
    """Obtener (o crear) el registry global del ecosistema."""
    global _global_registry
    if _global_registry is None:
        _global_registry = AgentRegistry()
    return _global_registry
