"""
Memory Manager Agent — Agente micro que envuelve MemoryManagerSkill.

Responsabilidad: persistencia de memoria con integridad blockchange.
Conecta directamente con `el-dador-de-suenos-nucleus` como destino de memoria.
"""

from __future__ import annotations

from typing import Any, Dict

from agents.micro.base_micro_agent import BaseMicroAgent
from agents.protocol import TaskRequest


class MemoryManagerAgent(BaseMicroAgent):
    """
    Agente micro especializado en gestión de memoria persistente.

    Integración cross-repo:
    - Escribe/lee memoria en `el-dador-de-suenos-nucleus` (repo de memoria maestra).
    - Sincroniza estado con `el-iluminador-nucleo-soberano` (memoria fractal).
    - El macro-supervisor lo activa para guardar resultados de otros agentes.

    Operaciones soportadas (via context["operation"]):
        "save_conversation" — persistir conversación/resultado
        "load_memory"       — cargar historial reciente
        "verify_integrity"  — verificar hash chain
        "stats"             — obtener estadísticas de memoria
    """

    DEFAULT_OPERATION = "stats"

    def __init__(self):
        from skills.memory_manager.memory_manager_skill import MemoryManagerSkill  # type: ignore[import]
        super().__init__(skill=MemoryManagerSkill(), agent_id="micro:memory-manager")

    def _build_context(self, request: TaskRequest) -> Dict[str, Any]:
        ctx = super()._build_context(request)
        # Si no viene operación explícita, usar stats por defecto
        ctx.setdefault("operation", self.DEFAULT_OPERATION)
        return ctx


def create_memory_manager_agent() -> MemoryManagerAgent:
    """Factory — crea y devuelve un MemoryManagerAgent listo para usar."""
    return MemoryManagerAgent()
