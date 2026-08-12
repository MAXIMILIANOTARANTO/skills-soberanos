"""Tests para core/orchestrator_engine.py: resonancia, routing y ejecución."""

from core.orchestrator_engine import OrchestratorEngine
from core.skill_base import Skill


class HighResonanceSkill(Skill):
    def __init__(self):
        super().__init__()
        self.name = "high-resonance-skill"
        self.resonance_keywords = ["coherencia", "estado", "ecosistema"]
        self.impact_on_q = 0.1

    def execute(self, context):
        result = {"status": "success", "q_impact": self.impact_on_q}
        self.update_health(True, result)
        return result


class LowResonanceSkill(Skill):
    def __init__(self):
        super().__init__()
        self.name = "low-resonance-skill"
        self.resonance_keywords = ["algo-que-no-aparece-nunca"]

    def execute(self, context):
        result = {"status": "success", "q_impact": 0.0}
        self.update_health(True, result)
        return result


class FailingSkill(Skill):
    def __init__(self):
        super().__init__()
        self.name = "failing-skill"
        self.resonance_keywords = ["coherencia"]

    def execute(self, context):
        raise RuntimeError("fallo simulado")


def test_evaluate_resonance_orders_by_score_descending():
    engine = OrchestratorEngine(skills=[LowResonanceSkill(), HighResonanceSkill()])

    scores = engine.evaluate_resonance("Analizar estado de coherencia del ecosistema")

    assert scores[0][0].name == "high-resonance-skill"
    assert scores[0][1] >= scores[1][1]


def test_route_and_execute_activates_above_threshold_skill():
    engine = OrchestratorEngine(skills=[HighResonanceSkill(), LowResonanceSkill()])

    response = engine.route_and_execute(
        "Analizar estado de coherencia del ecosistema",
        context={"current_q": 0.7},
        dry_run=True,
    )

    assert "high-resonance-skill" in response["activated_skills"]
    assert "low-resonance-skill" not in response["activated_skills"]
    assert response["errors"] is None


def test_route_and_execute_falls_back_to_top_skill_when_none_above_threshold():
    engine = OrchestratorEngine(skills=[LowResonanceSkill()])

    response = engine.route_and_execute(
        "un intent que no resuena con nada",
        context={"current_q": 0.7},
        dry_run=True,
    )

    assert response["activated_skills"] == ["low-resonance-skill"]


def test_route_and_execute_records_errors_without_crashing():
    engine = OrchestratorEngine(skills=[FailingSkill()])

    response = engine.route_and_execute(
        "Analizar estado de coherencia del ecosistema",
        context={"current_q": 0.7},
        dry_run=True,
    )

    assert response["errors"] is not None
    assert response["errors"][0]["skill"] == "failing-skill"
    assert response["execution_results"][0]["status"] == "error"


def test_analyze_skills_health_reports_all_skills():
    skill = HighResonanceSkill()
    engine = OrchestratorEngine(skills=[skill])

    engine.route_and_execute("coherencia del ecosistema", context={"current_q": 0.7}, dry_run=True)
    health = engine.analyze_skills_health()

    assert health["total_skills"] == 1
    assert health["skills_detail"][0]["name"] == "high-resonance-skill"
    assert health["skills_detail"][0]["executions"] == 1
