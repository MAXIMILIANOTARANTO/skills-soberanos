"""
Meta Hilo Grok Agent — Agente micro que envuelve MetaHiloGrokSkill.

Responsabilidad: análisis cognitivo de patrones, extracción de insights,
recomendaciones estratégicas.
Conecta con `grok-nodo-iluminado` para enriquecer el análisis con insights Grok.
"""

from __future__ import annotations

from typing import Any, Dict

from .base_micro_agent import BaseMicroAgent, load_skill_instance
from ..protocol import TaskRequest


class MetaHiloGrokAgent(BaseMicroAgent):
    """
    Agente micro especializado en análisis cognitivo y meta-orquestación.

    Integración cross-repo:
    - Lee insights de `grok-nodo-iluminado` para enriquecer el análisis.
    - Consume historial de `el-dador-de-suenos-nucleus` para detectar patrones.
    - Propone mejoras a la teoría en `tcu-unified-coherence-theory`.
    - Reporta al supervisor con recomendaciones de activación de skills.

    Requiere LLM (context["llm_engine"]).
    """

    def __init__(self, skill: Any = None):
        super().__init__(
            skill=skill
            or load_skill_instance(
                class_name="MetaHiloGrokSkill",
                module_candidates=("skills.meta_hilo_grok.meta_hilo_grok_skill",),
                relative_file="skills/meta-hilo-grok/meta_hilo_grok_skill.py",
            ),
            agent_id="micro:meta-hilo-grok",
        )

    def _build_context(self, request: TaskRequest) -> Dict[str, Any]:
        ctx = super()._build_context(request)
        # Días de análisis por defecto: 7
        ctx.setdefault("days_back", 7)
        return ctx


def create_meta_hilo_grok_agent() -> MetaHiloGrokAgent:
    """Factory — crea y devuelve un MetaHiloGrokAgent listo para usar."""
    return MetaHiloGrokAgent()
