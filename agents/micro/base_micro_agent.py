"""
Base Micro Agent — Agente micro que envuelve un skill soberano.

Un micro-agente:
- Tiene exactamente un Skill asociado.
- Recibe TaskRequest desde un macro-agente.
- Delega la ejecución al Skill.execute() con el contexto apropiado.
- Devuelve un TaskResult.
- Puede ser activado independientemente o bajo la dirección de un macro.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Dict, Optional

from core.skill_base import Skill
from agents.protocol import (
    TaskRequest,
    TaskResult,
    TaskStatus,
    AgentTier,
    make_success_result,
    make_error_result,
)


class BaseMicroAgent:
    """
    Agente micro que envuelve un Skill soberano.

    Responsabilidades:
    - Traducir TaskRequest → contexto para Skill.execute()
    - Ejecutar el skill y capturar errores
    - Devolver TaskResult al macro-agente llamador
    - Reportar resonancia con una intención dada
    """

    tier: AgentTier = AgentTier.MICRO

    def __init__(self, skill: Skill, agent_id: Optional[str] = None):
        """
        Args:
            skill     : instancia de Skill que este agente envuelve.
            agent_id  : identificador único; por defecto usa el nombre del skill.
        """
        self.skill = skill
        self.agent_id: str = agent_id or f"micro:{skill.name}"
        self.skill_name: str = skill.name
        self.created_at: str = datetime.utcnow().isoformat() + "Z"
        self.total_tasks: int = 0
        self.successful_tasks: int = 0

    # ------------------------------------------------------------------ #
    # EJECUCIÓN                                                            #
    # ------------------------------------------------------------------ #

    def handle(self, request: TaskRequest) -> TaskResult:
        """
        Procesar una TaskRequest y devolver un TaskResult.

        El contexto del TaskRequest se pasa directamente al skill;
        las subclases pueden sobreescribir `_build_context()` para adaptar.
        """
        self.total_tasks += 1
        start_ms = int(time.time() * 1000)

        try:
            context = self._build_context(request)
            raw_result = self.skill.execute(context)

            duration_ms = int(time.time() * 1000) - start_ms
            q_impact = float(raw_result.get("q_impact", 0.0))

            self.successful_tasks += 1
            return make_success_result(
                task_id=request.task_id,
                agent_id=self.agent_id,
                output=raw_result,
                q_impact=q_impact,
                duration_ms=duration_ms,
            )

        except Exception as exc:  # noqa: BLE001
            duration_ms = int(time.time() * 1000) - start_ms
            return make_error_result(
                task_id=request.task_id,
                agent_id=self.agent_id,
                error=str(exc),
                duration_ms=duration_ms,
            )

    # ------------------------------------------------------------------ #
    # RESONANCIA                                                           #
    # ------------------------------------------------------------------ #

    def get_resonance_score(self, intent: str) -> float:
        """Delegar al skill el cálculo de resonancia con la intención."""
        return self.skill.get_resonance_score(intent)

    # ------------------------------------------------------------------ #
    # SALUD                                                                #
    # ------------------------------------------------------------------ #

    def is_healthy(self) -> bool:
        """El agente micro está sano si su skill subyacente está sano."""
        return self.skill.is_healthy()

    def get_health_score(self) -> float:
        return self.skill.get_health_score()

    # ------------------------------------------------------------------ #
    # HELPERS                                                              #
    # ------------------------------------------------------------------ #

    def _build_context(self, request: TaskRequest) -> Dict[str, Any]:
        """
        Construir el contexto para Skill.execute() a partir de la TaskRequest.
        Subclases pueden extender para inyectar recursos adicionales.
        """
        ctx = dict(request.context)
        ctx["intent"] = request.intent
        ctx["task_id"] = request.task_id
        ctx["requester_id"] = request.requester_id
        return ctx

    # ------------------------------------------------------------------ #
    # REPRESENTACIÓN                                                       #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "tier": self.tier.value,
            "skill_name": self.skill_name,
            "health_score": round(self.get_health_score(), 3),
            "total_tasks": self.total_tasks,
            "successful_tasks": self.successful_tasks,
            "success_rate": (
                round(self.successful_tasks / self.total_tasks, 3)
                if self.total_tasks
                else None
            ),
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        return (
            f"<MicroAgent id={self.agent_id!r} skill={self.skill_name!r} "
            f"health={self.get_health_score():.2f}>"
        )
