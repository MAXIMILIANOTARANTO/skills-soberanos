"""
Priority Manager — Agente macro que gestiona la cola de tareas con prioridades.

Responsabilidades:
- Mantener una cola priorizada de TaskRequests pendientes.
- Despachar al Supervisor/ResourceOrchestrator según prioridad.
- Evitar inanición de tareas de baja prioridad.
"""

from __future__ import annotations

import heapq
from datetime import datetime
from typing import Any, Dict, List, Optional

from agents.macro.base_macro_agent import BaseMacroAgent
from agents.protocol import TaskRequest


class PriorityManager(BaseMacroAgent):
    """
    Gestor de Prioridades — cola de tareas ordenada por prioridad (1=alta … 10=baja).

    Uso típico:
        pm = PriorityManager()
        pm.enqueue(TaskRequest(intent="...", priority=1))
        request = pm.dequeue()  # devuelve la de mayor prioridad
    """

    def __init__(self):
        super().__init__(
            agent_id="macro:priority-manager",
            description="Cola priorizada de tareas para el ecosistema de agentes.",
        )
        # heap: (priority, counter, TaskRequest)
        # counter rompe empates en prioridad de forma FIFO
        self._heap: List[tuple] = []
        self._counter: int = 0
        self._dispatched: int = 0

    def handle(
        self, intent: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Devolver el estado actual de la cola."""
        return self.queue_status()

    def enqueue(self, request: TaskRequest) -> None:
        """
        Agregar una tarea a la cola con su prioridad.
        Prioridad 1 = más alta; 10 = más baja.
        """
        heapq.heappush(self._heap, (request.priority, self._counter, request))
        self._counter += 1
        self._log(
            "enqueue",
            {"task_id": request.task_id, "priority": request.priority, "intent": request.intent[:80]},
        )

    def dequeue(self) -> Optional[TaskRequest]:
        """
        Extraer la tarea de mayor prioridad (menor número).
        Retorna None si la cola está vacía.
        """
        if not self._heap:
            return None
        _, _, request = heapq.heappop(self._heap)
        self._dispatched += 1
        self._log(
            "dequeue",
            {"task_id": request.task_id, "priority": request.priority},
        )
        return request

    def peek(self) -> Optional[TaskRequest]:
        """Ver la próxima tarea sin extraerla."""
        if not self._heap:
            return None
        return self._heap[0][2]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def queue_status(self) -> Dict[str, Any]:
        """Estado actual de la cola."""
        return {
            "agent_id": self.agent_id,
            "queued": len(self._heap),
            "dispatched": self._dispatched,
            "next_priority": self._heap[0][0] if self._heap else None,
            "next_intent": self._heap[0][2].intent[:80] if self._heap else None,
        }

    def drain_all(self) -> List[TaskRequest]:
        """
        Extraer todas las tareas de la cola en orden de prioridad.
        Útil para flush o shutdown controlado.
        """
        results: List[TaskRequest] = []
        while not self.is_empty():
            req = self.dequeue()
            if req:
                results.append(req)
        return results
