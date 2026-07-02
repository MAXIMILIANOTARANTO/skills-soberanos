"""
Coherence Router — Decide qué skills ejecutar basándose en Q(t) y resonancia.

Implementa la lógica de "poda adaptativa":
- Q(t) alto  → ejecutar múltiples skills (modo EXPANSIVO)
- Q(t) medio → ejecutar skills críticos + top resonancia (modo BALANCEADO)
- Q(t) bajo  → solo skills críticos (modo CONSERVADOR)

También mantiene historial de decisiones de poda para análisis posterior.
"""

from typing import List, Tuple, Dict, Any
from datetime import datetime

from core.skill_base import Skill


class CoherenceRouter:
    """
    Router que decide cuáles skills activar según el estado de coherencia Q(t).

    Modos de operación:
        EXPANSIVE   : Q(t) >= 0.8  → todos los skills con resonancia >= threshold
        BALANCED    : Q(t) >= 0.6  → skills críticos + top-3 por resonancia
        CONSERVATIVE: Q(t) < 0.6   → solo skills marcados como is_critical=True
    """

    Q_EXPANSIVE = 0.80
    Q_BALANCED = 0.60

    # Número máximo de skills a activar por modo
    MAX_SKILLS = {
        "EXPANSIVE": 10,
        "BALANCED": 4,
        "CONSERVATIVE": 2,
    }

    def __init__(self):
        self.poda_history: List[Dict[str, Any]] = []

    def route(
        self,
        scored_skills: List[Tuple[Skill, float]],
        current_q: float,
    ) -> List[Skill]:
        """
        Seleccionar qué skills ejecutar dado Q(t) y sus scores de resonancia.

        Args:
            scored_skills: Lista de (skill, resonance_score) ya filtrados por
                           threshold mínimo, ordenados de mayor a menor score.
            current_q:     Valor actual de Q(t) entre 0.0 y 1.0.

        Returns:
            Lista de skills a ejecutar (puede estar vacía si no hay candidatos).
        """
        if not scored_skills:
            self._record_poda(mode="EMPTY", selected=[], q=current_q)
            return []

        # Determinar modo según Q(t)
        if current_q >= self.Q_EXPANSIVE:
            mode = "EXPANSIVE"
            selected = self._select_expansive(scored_skills)
        elif current_q >= self.Q_BALANCED:
            mode = "BALANCED"
            selected = self._select_balanced(scored_skills)
        else:
            mode = "CONSERVATIVE"
            selected = self._select_conservative(scored_skills)

        self._record_poda(mode=mode, selected=selected, q=current_q)
        return selected

    # ------------------------------------------------------------------ #
    # MODOS DE SELECCIÓN                                                   #
    # ------------------------------------------------------------------ #

    def _select_expansive(self, scored_skills: List[Tuple[Skill, float]]) -> List[Skill]:
        """Modo expansivo: activar todos hasta el límite máximo."""
        limit = self.MAX_SKILLS["EXPANSIVE"]
        return [skill for skill, _ in scored_skills[:limit]]

    def _select_balanced(self, scored_skills: List[Tuple[Skill, float]]) -> List[Skill]:
        """
        Modo balanceado: skills críticos primero, luego top por resonancia.
        """
        limit = self.MAX_SKILLS["BALANCED"]
        critical = [skill for skill, _ in scored_skills if skill.is_critical]
        non_critical = [skill for skill, _ in scored_skills if not skill.is_critical]

        # Siempre incluir críticos; rellenar con no-críticos hasta el límite
        selected = critical[:]
        remaining = limit - len(selected)
        if remaining > 0:
            selected.extend(non_critical[:remaining])

        return selected[:limit]

    def _select_conservative(self, scored_skills: List[Tuple[Skill, float]]) -> List[Skill]:
        """
        Modo conservador: solo skills críticos.
        Si no hay críticos, tomar el de mayor resonancia.
        """
        limit = self.MAX_SKILLS["CONSERVATIVE"]
        critical = [skill for skill, _ in scored_skills if skill.is_critical]

        if critical:
            return critical[:limit]

        # Sin críticos: usar top-1 para no dejar el sistema sin respuesta
        return [scored_skills[0][0]] if scored_skills else []

    # ------------------------------------------------------------------ #
    # HISTORIAL                                                            #
    # ------------------------------------------------------------------ #

    def _record_poda(
        self,
        mode: str,
        selected: List[Skill],
        q: float,
    ) -> None:
        """Registrar decisión de poda en el historial."""
        self.poda_history.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "mode": mode,
                "q_value": round(q, 4),
                "selected_count": len(selected),
                "selected_names": [s.name for s in selected],
            }
        )

    def get_poda_summary(self, last_n: int = 10) -> Dict[str, Any]:
        """Resumen de las últimas N decisiones de poda."""
        recent = self.poda_history[-last_n:]
        if not recent:
            return {"total_decisions": 0}

        mode_counts: Dict[str, int] = {}
        for entry in recent:
            mode = entry["mode"]
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        avg_q = sum(e["q_value"] for e in recent) / len(recent)
        avg_selected = sum(e["selected_count"] for e in recent) / len(recent)

        return {
            "total_decisions": len(self.poda_history),
            "recent_decisions": len(recent),
            "mode_distribution": mode_counts,
            "avg_q": round(avg_q, 4),
            "avg_skills_selected": round(avg_selected, 2),
            "last_mode": recent[-1]["mode"] if recent else None,
        }
