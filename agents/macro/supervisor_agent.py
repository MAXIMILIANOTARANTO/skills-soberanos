"""
Supervisor Agent — Agente macro supervisor principal del ecosistema.

Responsabilidades:
1. Recibir intenciones de alto nivel.
2. Calcular resonancia de micro-agentes con la intención.
3. Activar los micro-agentes más resonantes (via ResourceOrchestrator).
4. Sintetizar resultados y reportar estado al usuario.
5. Guardar resultados en memoria (via MemoryManagerAgent si disponible).

Conecta con todos los repositorios del ecosistema a través del registry.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base_macro_agent import BaseMacroAgent
from ..protocol import (
    TaskResult,
    make_task_request,
    utc_now_iso,
)


class SupervisorAgent(BaseMacroAgent):
    """
    Supervisor Principal — coordina el flujo general del ecosistema.

    Integración cross-repo:
    - Activa CoherencePulseAgent → consulta Q(t) desde tcu-unified-coherence-theory.
    - Activa MemoryManagerAgent  → persiste en el-dador-de-suenos-nucleus.
    - Activa MetaHiloGrokAgent   → enriquece con insights de grok-nodo-iluminado.
    - Reporta a ia-specialist-agent (si configurado) para tareas complejas.
    """

    MIN_RESONANCE_THRESHOLD = 0.2

    def __init__(
        self,
        micro_agents: Optional[List[Any]] = None,
        resource_orchestrator: Optional[Any] = None,
        status_monitor: Optional[Any] = None,
        priority_manager: Optional[Any] = None,
    ):
        super().__init__(
            agent_id="macro:supervisor",
            description="Supervisor Principal — coordina el flujo general del ecosistema.",
        )
        self.micro_agents: List[Any] = micro_agents or []
        self.resource_orchestrator = resource_orchestrator
        self.status_monitor = status_monitor
        self.priority_manager = priority_manager

    def handle(
        self, intent: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Procesar una intención de alto nivel:
        1. Evaluar resonancia de micro-agentes.
        2. Filtrar candidatos.
        3. Activar micro-agentes (directamente o via ResourceOrchestrator).
        4. Sintetizar resultados.

        Args:
            intent : intención/solicitud de alto nivel.
            context: recursos del ecosistema (llm_engine, memory, coherence_meter…).

        Returns:
            Dict con resultados sintetizados, errores y métricas.
        """
        context = context or {}
        self._log("handle_start", {"intent": intent[:200]})
        timestamp_start = utc_now_iso()

        # PASO 1 — Evaluar resonancia
        scored = self._score_agents(intent)
        candidates = [
            (agent, score)
            for agent, score in scored
            if score >= self.MIN_RESONANCE_THRESHOLD
        ]

        # Al menos uno si hay agentes disponibles
        if not candidates and scored:
            candidates = [scored[0]]

        # PASO 2 — Activar via ResourceOrchestrator (si disponible) o directo
        if self.resource_orchestrator:
            results = self.resource_orchestrator.activate(
                candidates=[agent for agent, _ in candidates],
                intent=intent,
                context=context,
            )
        else:
            results = self._activate_direct(
                candidates=[agent for agent, _ in candidates],
                intent=intent,
                context=context,
            )

        # PASO 3 — Reportar a StatusMonitor (si disponible)
        if self.status_monitor:
            self.status_monitor.record_run(intent=intent, results=results)

        # PASO 4 — Sintetizar
        successful = [r for r in results if r.succeeded]
        errors = [r for r in results if not r.succeeded]
        total_q_impact = sum(r.q_impact for r in results)

        response = {
            "timestamp": timestamp_start,
            "intent": intent[:200],
            "agents_scored": [
                {"agent_id": a.agent_id, "resonance": round(s, 3)}
                for a, s in scored[:10]
            ],
            "agents_activated": [r.agent_id for r in results],
            "results": [r.to_dict() for r in results],
            "successful": len(successful),
            "errors": len(errors),
            "total_q_impact": round(total_q_impact, 4),
            "status": "success" if not errors else ("partial" if successful else "error"),
        }

        self._log("handle_end", {"status": response["status"]})
        return response

    # ------------------------------------------------------------------ #
    # HELPERS                                                              #
    # ------------------------------------------------------------------ #

    def _score_agents(self, intent: str) -> List[tuple]:
        """Calcular resonancia de todos los micro-agentes con la intención."""
        scored = [
            (agent, agent.get_resonance_score(intent))
            for agent in self.micro_agents
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def _activate_direct(
        self,
        candidates: List[Any],
        intent: str,
        context: Dict[str, Any],
    ) -> List[TaskResult]:
        """Activar micro-agentes directamente sin ResourceOrchestrator."""
        results: List[TaskResult] = []
        for agent in candidates:
            request = make_task_request(
                intent=intent,
                skill_target=agent.skill_name,
                context=context,
                requester_id=self.agent_id,
            )
            result = agent.handle(request)
            results.append(result)
        return results

    def add_micro_agent(self, agent: Any) -> None:
        """Agregar un micro-agente al supervisor en tiempo de ejecución."""
        self.micro_agents.append(agent)

    def remove_micro_agent(self, agent_id: str) -> bool:
        """Remover un micro-agente por su agent_id. Retorna True si fue encontrado."""
        before = len(self.micro_agents)
        self.micro_agents = [a for a in self.micro_agents if a.agent_id != agent_id]
        return len(self.micro_agents) < before
