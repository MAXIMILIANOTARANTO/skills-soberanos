"""Tests para core/coherence_router.py: poda adaptativa según Q(t)."""

from core.coherence_router import CoherenceRouter
from core.skill_base import Skill


class FakeSkill(Skill):
    def __init__(self, name, is_critical=False):
        super().__init__()
        self.name = name
        self.is_critical = is_critical

    def execute(self, context):
        return {"status": "success", "q_impact": 0.0}


def make_scored_skills():
    critical = FakeSkill("critical-skill", is_critical=True)
    a = FakeSkill("skill-a")
    b = FakeSkill("skill-b")
    c = FakeSkill("skill-c")
    d = FakeSkill("skill-d")
    e = FakeSkill("skill-e")
    f = FakeSkill("skill-f")
    g = FakeSkill("skill-g")
    # Ordenados de mayor a menor resonancia, como lo entrega evaluate_resonance().
    return [
        (critical, 0.9),
        (a, 0.8),
        (b, 0.7),
        (c, 0.6),
        (d, 0.5),
        (e, 0.4),
        (f, 0.3),
        (g, 0.2),
    ]


def test_critical_mode_only_selects_critical_skills():
    router = CoherenceRouter()
    scored = make_scored_skills()

    selected = router.route(scored, current_q=0.3)

    assert [s.name for s in selected] == ["critical-skill"]
    assert router.poda_history[-1]["mode"] == "CRITICAL"


def test_conservative_mode_adds_top_one_non_critical():
    router = CoherenceRouter()
    scored = make_scored_skills()

    selected = router.route(scored, current_q=0.55)

    assert [s.name for s in selected] == ["critical-skill", "skill-a"]
    assert router.poda_history[-1]["mode"] == "CONSERVATIVE"


def test_normal_mode_caps_at_max_normal():
    router = CoherenceRouter()
    scored = make_scored_skills()

    selected = router.route(scored, current_q=0.7)

    assert [s.name for s in selected] == ["critical-skill", "skill-a", "skill-b", "skill-c"]
    assert router.poda_history[-1]["mode"] == "NORMAL"


def test_expansive_mode_caps_at_max_expansive():
    router = CoherenceRouter()
    scored = make_scored_skills()

    selected = router.route(scored, current_q=0.9)

    assert len(selected) == 1 + CoherenceRouter.MAX_EXPANSIVE
    assert router.poda_history[-1]["mode"] == "EXPANSIVE"


def test_route_appends_to_poda_history_each_call():
    router = CoherenceRouter()
    scored = make_scored_skills()

    router.route(scored, current_q=0.3)
    router.route(scored, current_q=0.9)

    assert len(router.poda_history) == 2
    assert router.poda_history[0]["skills_considered"] == len(scored)


def test_route_never_duplicates_a_skill():
    router = CoherenceRouter()
    critical = FakeSkill("only-skill", is_critical=True)
    scored = [(critical, 0.9)]

    selected = router.route(scored, current_q=0.9)

    assert len(selected) == 1
