"""
Resource Orchestrator — Agente macro que gestiona la activación de micro-agentes.

Responsabilidades:
- Recibir lista de micro-agentes candidatos del Supervisor.
- Aplicar límites de recursos (máx. paralelos, timeout).
- Activar los agentes en orden de prioridad.
- Devolver lista de TaskResults al Supervisor.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.macro.base_macro_agent import BaseMacroAgent
from agents.protocol import TaskResult, make_task_request


class ResourceOrchestrator(BaseMacroAgent):
    """
    Orquestador de Recursos — gestiona cuántos y cuáles micro-agentes se activan.

    Parámetros configurables:
        max_concurrent : máximo de agentes que se activan por ciclo.
        fail_fast      : si True, detener activaciones al primer error crítico.
    """

    def __init__(self, max_concurrent: int = 5, fail_fast: bool = False):
        super().__init__(
            agent_id="macro:resource-orchestrator",
            description="Gestiona la activación y recursos de micro-agentes.",
        )
        self.max_concurrent = max_concurrent
        self.fail_fast = fail_fast

    def handle(
        self, intent: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Implementación mínima de handle() para cumplir con la interfaz.
        En uso normal, llamar a activate() directamente desde el Supervisor.
        """
        return {"agent_id": self.agent_id, "message": "Usar activate() directamente."}

    def activate(
        self,
        candidates: List[Any],
        intent: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> List[TaskResult]:
        """
        Activar los micro-agentes candidatos respetando el límite de concurrencia.

        Args:
            candidates : lista de BaseMicroAgent a activar.
            intent     : intención de la tarea.
            context    : recursos del ecosistema.

        Returns:
            Lista de TaskResult (uno por agente activado).
        """
        context = context or {}
        limited = candidates[: self.max_concurrent]
        results: List[TaskResult] = []

        self._log(
            "activate_start",
            {"candidates": len(candidates), "activating": len(limited)},
        )

        for agent in limited:
            request = make_task_request(
                intent=intent,
                skill_target=agent.skill_name,
                context=context,
                requester_id=self.agent_id,
            )
            result = agent.handle(request)
            results.append(result)

            if self.fail_fast and not result.succeeded:
                self._log("fail_fast_stop", {"failed_agent": agent.agent_id})
                break

        self._log("activate_end", {"results": len(results)})
        return results
