"""
Coherence Router - Decide qué skills ejecutar dado su score de resonancia
y el Q(t) actual del ecosistema. Implementa poda adaptativa: cuanto más baja
la coherencia, más conservador el filtro de activación.
"""

from typing import List, Tuple, Dict, Any
from datetime import datetime

from core.skill_base import Skill


class CoherenceRouter:
    """
    A partir de una lista de (skill, resonance_score) ya filtrada por threshold
    mínimo, decide cuáles skills ejecutar según el nivel de coherencia Q(t) actual.

    Modos de poda (más agresivos cuanto más baja la coherencia):
    - CRITICAL (Q < 0.5): solo skills críticos (is_critical=True).
    - CONSERVATIVE (0.5 <= Q < 0.65): críticos + el skill de mayor resonancia.
    - NORMAL (0.65 <= Q < 0.8): críticos + hasta MAX_NORMAL skills de mayor resonancia.
    - EXPANSIVE (Q >= 0.8): críticos + hasta MAX_EXPANSIVE skills de mayor resonancia.
    """

    Q_CRITICAL = 0.5
    Q_WARNING = 0.65
    Q_OPTIMAL = 0.8

    MAX_NORMAL = 3
    MAX_EXPANSIVE = 6

    def __init__(self):
        self.poda_history: List[Dict[str, Any]] = []

    def route(self, scored_skills: List[Tuple[Skill, float]], current_q: float) -> List[Skill]:
        """
        Args:
            scored_skills: lista de (skill, resonance_score), ordenada de mayor a menor.
            current_q: Q(t) actual del ecosistema.

        Returns:
            Lista de skills a ejecutar, sin duplicados, preservando el orden de resonancia.
        """
        critical = [s for s, _ in scored_skills if s.is_critical]
        non_critical = [s for s, _ in scored_skills if not s.is_critical]

        if current_q < self.Q_CRITICAL:
            mode = "CRITICAL"
            selected = critical
        elif current_q < self.Q_WARNING:
            mode = "CONSERVATIVE"
            selected = critical + non_critical[:1]
        elif current_q < self.Q_OPTIMAL:
            mode = "NORMAL"
            selected = critical + non_critical[:self.MAX_NORMAL]
        else:
            mode = "EXPANSIVE"
            selected = critical + non_critical[:self.MAX_EXPANSIVE]

        seen = set()
        deduped = []
        for s in selected:
            if id(s) not in seen:
                seen.add(id(s))
                deduped.append(s)

        self.poda_history.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "mode": mode,
            "current_q": current_q,
            "skills_selected": [s.name for s in deduped],
            "skills_considered": len(scored_skills),
        })

        return deduped


def create_coherence_router() -> CoherenceRouter:
    """Factory para crear CoherenceRouter"""
    return CoherenceRouter()
