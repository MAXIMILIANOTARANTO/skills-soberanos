"""
Skill Base - Clase base para todos los skills ejecutables del ecosistema.
Define la interfaz común de resonancia, ejecución y salud que usan
OrchestratorEngine y CoherenceRouter, más dos skills de ejemplo para pruebas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class Skill:
    """
    Clase base de la que heredan todos los skills ejecutables del ecosistema.

    Subclases deben, en su propio __init__ (llamando primero a super().__init__()):
    - Setear name, purpose, version, requires_llm, resonance_keywords, impact_on_q, is_critical
    - Sobreescribir execute()
    """

    def __init__(self):
        self.name: str = self.__class__.__name__
        self.purpose: str = ""
        self.version: str = "1.0"
        self.requires_llm: bool = False
        self.resonance_keywords: List[str] = []
        self.impact_on_q: float = 0.0
        self.is_critical: bool = False

        self.execution_count: int = 0
        self.success_count: int = 0
        self.last_result: Optional[Dict[str, Any]] = None
        self.last_executed_at: Optional[str] = None

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar el skill. Las subclases deben sobreescribir este método."""
        raise NotImplementedError(f"{self.name} no implementa execute()")

    def get_resonance_score(self, intent: str, intent_embedding=None) -> float:
        """
        Score de resonancia 0.0-1.0 entre este skill y una intención.
        Implementación base: coincidencia de keywords (case-insensitive).
        Subclases pueden sobreescribir para lógica más rica.
        """
        if not intent or not self.resonance_keywords:
            return 0.0

        intent_lower = intent.lower()
        matches = sum(1 for kw in self.resonance_keywords if kw.lower() in intent_lower)

        if matches == 0:
            return 0.0

        return min(1.0, (matches / len(self.resonance_keywords)) + 0.2)

    def update_health(self, success: bool, result: Dict[str, Any]) -> None:
        """Registrar el resultado de una ejecución para el tracking de salud del skill."""
        self.execution_count += 1
        if success:
            self.success_count += 1
        self.last_result = result
        self.last_executed_at = datetime.utcnow().isoformat() + "Z"

    def get_health_score(self) -> float:
        """
        Score de salud 0.0-1.0 basado en tasa de éxito histórica.
        Sin ejecuciones previas, se asume salud neutral (1.0).
        """
        if self.execution_count == 0:
            return 1.0
        return self.success_count / self.execution_count

    def is_healthy(self, threshold: float = 0.5) -> bool:
        """Un skill crítico siempre se considera saludable (nunca se poda)."""
        if self.is_critical:
            return True
        return self.get_health_score() >= threshold


class ExampleTechnicalSkill(Skill):
    """Skill de ejemplo técnico, usado por run_pulse.py como placeholder de prueba."""

    def __init__(self):
        super().__init__()
        self.name = "example-technical-skill"
        self.purpose = "Skill de ejemplo para pruebas técnicas del orquestador"
        self.requires_llm = False
        self.resonance_keywords = ["técnico", "sistema", "código", "análisis técnico"]
        self.impact_on_q = 0.05
        self.is_critical = False

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "status": "success",
            "message": "Example technical skill ejecutado",
            "q_impact": self.impact_on_q,
        }
        self.update_health(True, result)
        return result


class ExampleCognitiveSkill(Skill):
    """Skill de ejemplo cognitivo, usado por run_pulse.py como placeholder de prueba."""

    def __init__(self):
        super().__init__()
        self.name = "example-cognitive-skill"
        self.purpose = "Skill de ejemplo para pruebas de razonamiento del orquestador"
        self.requires_llm = True
        self.resonance_keywords = ["reflexión", "análisis", "insight", "cognitivo"]
        self.impact_on_q = 0.1
        self.is_critical = False

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "status": "success",
            "message": "Example cognitive skill ejecutado",
            "q_impact": self.impact_on_q,
        }
        self.update_health(True, result)
        return result
