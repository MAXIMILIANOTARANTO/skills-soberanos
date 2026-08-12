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

import importlib
import importlib.util
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from core.skill_base import Skill
from ..protocol import (
    AgentTier,
    TaskRequest,
    TaskResult,
    TaskStatus,
    make_success_result,
    make_error_result,
    utc_now_iso,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_skill_instance(
    *,
    class_name: str,
    module_candidates: Iterable[str] = (),
    relative_file: Optional[str] = None,
) -> Skill:
    """
    Resolver una clase de skill por módulo importable o por archivo relativo.

    Esto permite mantener agentes especializados aunque los directorios reales
    de `skills/` usen guiones en lugar de nombres importables de paquete.
    """

    for module_name in module_candidates:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue

        skill_cls = getattr(module, class_name, None)
        if isinstance(skill_cls, type) and issubclass(skill_cls, Skill):
            return skill_cls()

    if relative_file:
        skill_path = _PROJECT_ROOT / relative_file
        if skill_path.exists():
            module_name = f"_agents_skill_{skill_path.stem}_{class_name}"
            spec = importlib.util.spec_from_file_location(module_name, skill_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)  # type: ignore[union-attr]
                skill_cls = getattr(module, class_name, None)
                if isinstance(skill_cls, type) and issubclass(skill_cls, Skill):
                    return skill_cls()

    raise ImportError(f"No se pudo resolver el skill {class_name!r}")


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
        self.created_at: str = utc_now_iso()
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
            normalized_output = self._normalize_output(raw_result)

            duration_ms = int(time.time() * 1000) - start_ms
            error_message = self._extract_error(normalized_output)
            if error_message:
                return make_error_result(
                    task_id=request.task_id,
                    agent_id=self.agent_id,
                    error=error_message,
                    duration_ms=duration_ms,
                )

            q_impact = float(normalized_output.get("q_impact", 0.0))

            self.successful_tasks += 1
            return make_success_result(
                task_id=request.task_id,
                agent_id=self.agent_id,
                output=normalized_output,
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

    def _normalize_output(self, raw_result: Any) -> Dict[str, Any]:
        """Normalizar la salida del skill a un diccionario serializable."""
        if isinstance(raw_result, dict):
            return raw_result
        return {"result": raw_result}

    def _extract_error(self, output: Dict[str, Any]) -> Optional[str]:
        """Detectar errores declarativos devueltos por el skill."""
        status = str(output.get("status", "")).lower()
        if status in {TaskStatus.ERROR.value, "failed", "failure"}:
            return str(output.get("error") or f"{self.skill_name} devolvió status={status}")

        if output.get("succeeded") is False:
            return str(output.get("error") or f"{self.skill_name} devolvió succeeded=False")

        return None

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
