"""Tests para core/skill_base.py: Skill (base) y los skills de ejemplo."""

from core.skill_base import Skill, ExampleTechnicalSkill, ExampleCognitiveSkill


class DummySkill(Skill):
    def __init__(self, is_critical=False):
        super().__init__()
        self.name = "dummy-skill"
        self.resonance_keywords = ["alfa", "beta", "gamma", "delta"]
        self.is_critical = is_critical

    def execute(self, context):
        result = {"status": "success", "q_impact": 0.0}
        self.update_health(True, result)
        return result


def test_skill_execute_not_implemented_by_default():
    skill = Skill()
    try:
        skill.execute({})
        assert False, "se esperaba NotImplementedError"
    except NotImplementedError:
        pass


def test_resonance_score_no_intent_or_no_keywords():
    skill = DummySkill()
    assert skill.get_resonance_score("") == 0.0

    skill_no_keywords = Skill()
    assert skill_no_keywords.get_resonance_score("cualquier cosa") == 0.0


def test_resonance_score_no_matches_is_zero():
    skill = DummySkill()
    assert skill.get_resonance_score("texto sin relación alguna") == 0.0


def test_resonance_score_scales_with_matches():
    skill = DummySkill()
    one_match = skill.get_resonance_score("hablemos de alfa")
    two_matches = skill.get_resonance_score("hablemos de alfa y beta")

    assert 0.0 < one_match <= 1.0
    assert two_matches > one_match


def test_health_score_defaults_to_one_with_no_executions():
    skill = DummySkill()
    assert skill.get_health_score() == 1.0
    assert skill.is_healthy() is True


def test_update_health_tracks_success_rate():
    skill = DummySkill()

    skill.update_health(True, {"status": "success"})
    skill.update_health(False, {"status": "error"})

    assert skill.execution_count == 2
    assert skill.success_count == 1
    assert skill.get_health_score() == 0.5
    assert skill.last_executed_at is not None


def test_is_healthy_respects_threshold_unless_critical():
    non_critical = DummySkill(is_critical=False)
    non_critical.update_health(False, {"status": "error"})
    non_critical.update_health(False, {"status": "error"})
    assert non_critical.is_healthy() is False

    critical = DummySkill(is_critical=True)
    critical.update_health(False, {"status": "error"})
    critical.update_health(False, {"status": "error"})
    assert critical.is_healthy() is True


def test_example_skills_execute_successfully():
    for skill in (ExampleTechnicalSkill(), ExampleCognitiveSkill()):
        result = skill.execute({})
        assert result["status"] == "success"
        assert skill.execution_count == 1
        assert skill.success_count == 1
