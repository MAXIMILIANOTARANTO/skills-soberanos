"""
Base Macro Agent — Clase base para todos los agentes macro orquestadores.

Un macro-agente:
- Recibe solicitudes de alto nivel (intenciones del usuario).
- Las descompone en TaskRequests dirigidas a micro-agentes.
- Recopila y sintetiza TaskResults.
- Mantiene estado de la sesión de orquestación.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.protocol import TaskRequest, TaskResult, AgentTier


class BaseMacroAgent(ABC):
    """
    Clase base abstracta para agentes macro orquestadores.

    Subclases deben implementar `handle()`.
    """

    tier: AgentTier = AgentTier.MACRO

    def __init__(self, agent_id: str, description: str = ""):
        self.agent_id: str = agent_id
        self.description: str = description
        self.created_at: str = datetime.utcnow().isoformat() + "Z"
        self.session_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------ #
    # INTERFAZ OBLIGATORIA                                                 #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def handle(self, intent: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesar una intención de alto nivel.

        Args:
            intent : descripción de lo que se quiere lograr.
            context: recursos adicionales (llm_engine, memory, etc.)

        Returns:
            Dict con el resultado sintetizado de la orquestación.
        """

    # ------------------------------------------------------------------ #
    # LOGGING DE SESIÓN                                                    #
    # ------------------------------------------------------------------ #

    def _log(self, event: str, data: Optional[Dict[str, Any]] = None) -> None:
        self.session_log.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "agent_id": self.agent_id,
                "event": event,
                "data": data or {},
            }
        )

    # ------------------------------------------------------------------ #
    # REPRESENTACIÓN                                                       #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "tier": self.tier.value,
            "description": self.description,
            "session_events": len(self.session_log),
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        return f"<MacroAgent id={self.agent_id!r}>"
