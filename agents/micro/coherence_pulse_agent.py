"""
Coherence Pulse Agent — Agente micro que envuelve CoherencePulseSkill.

Responsabilidad: medir Q(t) del ecosistema.
Se activa automáticamente en cada pulse del macro-supervisor.
Conecta con tcu-unified-coherence-theory para la fórmula base de Q(t).
"""

from __future__ import annotations

from typing import Any, Dict

from .base_micro_agent import BaseMicroAgent, load_skill_instance
from ..protocol import TaskRequest


class CoherencePulseAgent(BaseMicroAgent):
    """
    Agente micro especializado en medición de coherencia (Q(t)).

    Integración cross-repo:
    - Lee la fórmula Q(t) definida en `tcu-unified-coherence-theory`.
    - Guarda resultados en `el-dador-de-suenos-nucleus` (si memory disponible).
    - Comparte estado con `el-iluminador-nucleo-soberano` para sincronización.
    """

    def __init__(self, skill: Any = None):
        super().__init__(
            skill=skill
            or load_skill_instance(
                class_name="CoherencePulseSkill",
                module_candidates=("skills.coherence_pulse.coherence_pulse_skill",),
                relative_file="skills/coherence-pulse/coherence_pulse_skill.py",
            ),
            agent_id="micro:coherence-pulse",
        )

    def _build_context(self, request: TaskRequest) -> Dict[str, Any]:
        ctx = super()._build_context(request)
        # Asegurar que el CoherenceMeter esté disponible si viene en el contexto
        if "coherence_meter" not in ctx:
            ctx.setdefault("coherence_meter", None)
        return ctx


def create_coherence_pulse_agent() -> CoherencePulseAgent:
    """Factory — crea y devuelve un CoherencePulseAgent listo para usar."""
    return CoherencePulseAgent()
