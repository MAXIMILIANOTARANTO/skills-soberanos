"""
Skill Base — Clase base para todos los skills del ecosistema soberano.
Define la interfaz estándar que deben implementar todos los skills.

Características:
- Interfaz uniforme para execute(), resonance, health
- Tracking de ejecuciones y éxitos
- Soporte para is_critical (nunca se poda)
- Compatibilidad con OrchestratorEngine y CoherenceRouter
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import math


class Skill(ABC):
    """
    Clase base abstracta para todos los skills soberanos.

    Subclases deben implementar:
        - execute(context) → Dict[str, Any]

    Atributos configurables en __init__ de la subclase:
        name            : identificador único del skill
        purpose         : descripción corta del propósito
        version         : versión semántica (ej. "1.0")
        requires_llm    : True si necesita un LLM para operar
        is_critical     : True = nunca se poda aunque Q(t) sea bajo
        impact_on_q     : contribución al Q(t) (-1.0 … 1.0)
        resonance_keywords: palabras clave para calcular resonancia
    """

    def __init__(self):
        # Metadatos — sobreescribir en subclases
        self.name: str = "base-skill"
        self.purpose: str = "Skill base abstracto"
        self.version: str = "1.0"
        self.requires_llm: bool = False
        self.is_critical: bool = False
        self.impact_on_q: float = 0.0
        self.resonance_keywords: List[str] = []

        # Tracking interno
        self.execution_count: int = 0
        self.success_count: int = 0
        self.error_count: int = 0
        self.last_execution: Optional[str] = None
        self.creation_date: str = datetime.utcnow().isoformat() + "Z"

    # ------------------------------------------------------------------ #
    # INTERFAZ OBLIGATORIA                                                 #
    # ------------------------------------------------------------------ #

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecutar la lógica del skill.

        Args:
            context: Diccionario con recursos del ecosistema.
                     Claves habituales: llm_engine, memory, coherence_meter,
                     current_q, operation, data, …

        Returns:
            Dict con al menos:
                status   : "success" | "error" | "partial"
                q_impact : float — efecto neto en Q(t)
        """

    # ------------------------------------------------------------------ #
    # RESONANCIA                                                           #
    # ------------------------------------------------------------------ #

    def get_resonance_score(self, intent: str) -> float:
        """
        Calcular qué tan relevante es este skill para la intención dada.

        Algoritmo simple basado en coincidencia de keywords.
        Subclases pueden sobreescribir para lógica semántica más sofisticada.

        Args:
            intent: Texto de intención/solicitud del usuario.

        Returns:
            Score entre 0.0 y 1.0.
        """
        if not intent or not self.resonance_keywords:
            return 0.0

        intent_lower = intent.lower()
        matches = sum(1 for kw in self.resonance_keywords if kw.lower() in intent_lower)

        # Normalizar con función logarítmica suavizada
        if matches == 0:
            return 0.0

        max_possible = len(self.resonance_keywords)
        raw = matches / max_possible
        # Suavizar: scores altos pero no lineales
        return round(min(1.0, raw + math.log1p(matches) * 0.1), 4)

    # ------------------------------------------------------------------ #
    # SALUD DEL SKILL                                                      #
    # ------------------------------------------------------------------ #

    def get_health_score(self) -> float:
        """
        Calcular la salud del skill basada en su historial de ejecuciones.

        Returns:
            Score entre 0.0 y 1.0.
        """
        if self.execution_count == 0:
            return 1.0  # Sin historial → asumimos saludable

        success_rate = self.success_count / self.execution_count
        # Penalizar levemente skills recién creados con pocos datos
        confidence = min(1.0, self.execution_count / 10.0)
        return round(success_rate * confidence + (1 - confidence) * 0.7, 4)

    def is_healthy(self) -> bool:
        """Retorna True si el skill está en condición operativa."""
        return self.get_health_score() >= 0.5

    # ------------------------------------------------------------------ #
    # TRACKING INTERNO                                                     #
    # ------------------------------------------------------------------ #

    def _record_execution(self, success: bool):
        """Registrar resultado de una ejecución."""
        self.execution_count += 1
        self.last_execution = datetime.utcnow().isoformat() + "Z"
        if success:
            self.success_count += 1
        else:
            self.error_count += 1

    # ------------------------------------------------------------------ #
    # REPRESENTACIÓN                                                       #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> Dict[str, Any]:
        """Serializar metadatos del skill."""
        return {
            "name": self.name,
            "purpose": self.purpose,
            "version": self.version,
            "requires_llm": self.requires_llm,
            "is_critical": self.is_critical,
            "impact_on_q": self.impact_on_q,
            "resonance_keywords": self.resonance_keywords,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "health_score": self.get_health_score(),
            "last_execution": self.last_execution,
            "creation_date": self.creation_date,
        }

    def __repr__(self) -> str:
        return (
            f"<Skill name={self.name!r} version={self.version!r} "
            f"health={self.get_health_score():.2f} critical={self.is_critical}>"
        )


# ======================================================================= #
# SKILLS DE EJEMPLO — para testing y demostración                         #
# ======================================================================= #

class ExampleTechnicalSkill(Skill):
    """Skill técnico de ejemplo para testing y demostración."""

    def __init__(self):
        super().__init__()
        self.name = "example-technical"
        self.purpose = "Skill técnico de demostración"
        self.version = "1.0"
        self.requires_llm = False
        self.is_critical = False
        self.impact_on_q = 0.05
        self.resonance_keywords = [
            "técnico", "sistema", "estado", "pulse", "análisis",
            "coherencia", "medir", "calcular", "diagnóstico"
        ]

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self._record_execution(success=True)
        return {
            "status": "success",
            "skill": self.name,
            "message": "Skill técnico ejecutado correctamente",
            "q_impact": self.impact_on_q,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }


class ExampleCognitiveSkill(Skill):
    """Skill cognitivo de ejemplo para testing y demostración."""

    def __init__(self):
        super().__init__()
        self.name = "example-cognitive"
        self.purpose = "Skill cognitivo de demostración"
        self.version = "1.0"
        self.requires_llm = True
        self.is_critical = False
        self.impact_on_q = 0.10
        self.resonance_keywords = [
            "cognitivo", "analizar", "patrón", "aprender", "insight",
            "reflexión", "meta", "estrategia", "tendencia", "mejora"
        ]

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self._record_execution(success=True)
        return {
            "status": "success",
            "skill": self.name,
            "message": "Skill cognitivo ejecutado correctamente",
            "q_impact": self.impact_on_q,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
