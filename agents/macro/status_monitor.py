"""
Status Monitor — Agente macro que rastrea el estado de ejecución del ecosistema.

Responsabilidades:
- Registrar cada ciclo de orquestación (intent, resultados, Q impact).
- Detectar tendencias de error o degradación.
- Proveer resúmenes de salud del ecosistema.
- Sincronizar con el-iluminador-nucleo-soberano (si disponible).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base_macro_agent import BaseMacroAgent
from ..protocol import TaskResult, utc_now_iso


class StatusMonitor(BaseMacroAgent):
    """
    Monitor de Estado — rastrea la ejecución y salud del ecosistema de agentes.

    Integración cross-repo:
    - Puede sincronizar estado con `el-iluminador-nucleo-soberano` para auditoría.
    - Expone métricas que el CoherenceMeter puede usar para calcular Q(t).
    """

    def __init__(self):
        super().__init__(
            agent_id="macro:status-monitor",
            description="Rastrea ejecución, resultados y salud del ecosistema.",
        )
        self.runs: List[Dict[str, Any]] = []

    def handle(
        self, intent: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Devolver el resumen de estado actual."""
        return self.get_summary()

    def record_run(
        self,
        intent: str,
        results: List[TaskResult],
    ) -> None:
        """
        Registrar el resultado de un ciclo de orquestación.

        Args:
            intent  : intención que disparó el ciclo.
            results : lista de TaskResult del ciclo.
        """
        successful = sum(1 for r in results if r.succeeded)
        total_q = sum(r.q_impact for r in results)

        entry = {
            "timestamp": utc_now_iso(),
            "intent": intent[:200],
            "total_tasks": len(results),
            "successful": successful,
            "errors": len(results) - successful,
            "total_q_impact": round(total_q, 4),
            "error_rate": round((len(results) - successful) / max(1, len(results)), 3),
            "agents_used": [r.agent_id for r in results],
        }
        self.runs.append(entry)
        self._log("run_recorded", entry)

    def get_summary(self, last_n: int = 10) -> Dict[str, Any]:
        """Resumen de los últimos N ciclos de orquestación."""
        recent = self.runs[-last_n:]
        if not recent:
            return {
                "agent_id": self.agent_id,
                "total_runs": 0,
                "message": "Sin datos aún.",
            }

        avg_error_rate = sum(r["error_rate"] for r in recent) / len(recent)
        avg_q_impact = sum(r["total_q_impact"] for r in recent) / len(recent)

        health = "CRITICAL" if avg_error_rate > 0.5 else (
            "WARNING" if avg_error_rate > 0.2 else "HEALTHY"
        )

        return {
            "agent_id": self.agent_id,
            "total_runs": len(self.runs),
            "recent_runs": len(recent),
            "avg_error_rate": round(avg_error_rate, 3),
            "avg_q_impact": round(avg_q_impact, 4),
            "health": health,
            "last_run": recent[-1]["timestamp"] if recent else None,
        }

    def is_degraded(self, threshold: float = 0.4) -> bool:
        """Retorna True si el error rate reciente supera el threshold."""
        summary = self.get_summary()
        return summary.get("avg_error_rate", 0.0) > threshold
