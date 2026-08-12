"""
Tests del framework de agentes jerárquicos.

Cubre:
- AgentRegistry: registro, búsqueda, mapa cross-repo
- SkillLoader: carga dinámica
- BaseMicroAgent: ejecución, resonancia, health
- SupervisorAgent: orquestación end-to-end
- ResourceOrchestrator: límite de concurrencia
- StatusMonitor: tracking de runs
- PriorityManager: cola priorizada
- Protocol: helpers de creación de mensajes
"""

import pytest
from agents.protocol import (
    TaskRequest,
    TaskResult,
    TaskStatus,
    AgentMessage,
    MessageType,
    make_task_request,
    make_success_result,
    make_error_result,
)
from agents.registry import AgentRegistry, ECOSYSTEM_REPOS
from agents.loader import SkillLoader
from agents.micro.base_micro_agent import BaseMicroAgent
from agents.macro.supervisor_agent import SupervisorAgent
from agents.macro.resource_orchestrator import ResourceOrchestrator
from agents.macro.status_monitor import StatusMonitor
from agents.macro.priority_manager import PriorityManager
from core.skill_base import ExampleTechnicalSkill, ExampleCognitiveSkill


# ======================================================================= #
# FIXTURES                                                                 #
# ======================================================================= #

@pytest.fixture
def technical_skill():
    return ExampleTechnicalSkill()


@pytest.fixture
def cognitive_skill():
    return ExampleCognitiveSkill()


@pytest.fixture
def micro_technical(technical_skill):
    return BaseMicroAgent(skill=technical_skill)


@pytest.fixture
def micro_cognitive(cognitive_skill):
    return BaseMicroAgent(skill=cognitive_skill)


@pytest.fixture
def micro_agents(micro_technical, micro_cognitive):
    return [micro_technical, micro_cognitive]


@pytest.fixture
def registry():
    return AgentRegistry()


@pytest.fixture
def supervisor(micro_agents):
    return SupervisorAgent(micro_agents=micro_agents)


# ======================================================================= #
# PROTOCOL                                                                 #
# ======================================================================= #

class TestProtocol:
    def test_make_task_request_defaults(self):
        req = make_task_request(intent="analizar coherencia")
        assert req.intent == "analizar coherencia"
        assert req.priority == 5
        assert req.task_id  # UUID generado

    def test_make_success_result(self):
        result = make_success_result(
            task_id="t1", agent_id="micro:test", output={"x": 1}, q_impact=0.1
        )
        assert result.succeeded
        assert result.status == TaskStatus.SUCCESS
        assert result.q_impact == 0.1

    def test_make_error_result(self):
        result = make_error_result(task_id="t1", agent_id="micro:test", error="boom")
        assert not result.succeeded
        assert result.status == TaskStatus.ERROR
        assert "boom" in result.error

    def test_task_request_to_dict(self):
        req = make_task_request(intent="test")
        d = req.to_dict()
        assert d["intent"] == "test"
        assert "task_id" in d

    def test_agent_message_creation(self):
        msg = AgentMessage(
            sender_id="macro:supervisor",
            receiver_id="micro:test",
            type=MessageType.TASK_REQUEST,
            payload={"data": 42},
        )
        d = msg.to_dict()
        assert d["sender_id"] == "macro:supervisor"
        assert d["type"] == "task_request"


# ======================================================================= #
# BASE MICRO AGENT                                                         #
# ======================================================================= #

class TestBaseMicroAgent:
    def test_agent_id_defaults_to_skill_name(self, technical_skill):
        agent = BaseMicroAgent(skill=technical_skill)
        assert agent.agent_id == f"micro:{technical_skill.name}"

    def test_agent_id_custom(self, technical_skill):
        agent = BaseMicroAgent(skill=technical_skill, agent_id="custom:id")
        assert agent.agent_id == "custom:id"

    def test_handle_success(self, micro_technical):
        req = make_task_request(intent="análisis técnico")
        result = micro_technical.handle(req)
        assert result.succeeded
        assert result.task_id == req.task_id
        assert result.q_impact >= 0

    def test_handle_counts_tasks(self, micro_technical):
        req = make_task_request(intent="técnico")
        micro_technical.handle(req)
        micro_technical.handle(req)
        assert micro_technical.total_tasks == 2
        assert micro_technical.successful_tasks == 2

    def test_resonance_delegated_to_skill(self, micro_technical):
        score = micro_technical.get_resonance_score("análisis técnico del sistema")
        assert 0.0 <= score <= 1.0

    def test_no_resonance_on_unrelated_intent(self, micro_technical):
        score = micro_technical.get_resonance_score("zxzxzxzxzx nada relevante")
        assert score == 0.0

    def test_health_initially_full(self, micro_technical):
        assert micro_technical.get_health_score() == 1.0

    def test_to_dict_contains_key_fields(self, micro_technical):
        d = micro_technical.to_dict()
        assert "agent_id" in d
        assert "tier" in d
        assert "skill_name" in d
        assert "health_score" in d


# ======================================================================= #
# AGENT REGISTRY                                                           #
# ======================================================================= #

class TestAgentRegistry:
    def test_register_micro(self, registry, micro_technical):
        registry.register_micro(micro_technical)
        assert len(registry.list_micro()) == 1

    def test_register_many_micro(self, registry, micro_agents):
        registry.register_many_micro(micro_agents)
        assert len(registry.list_micro()) == 2

    def test_get_micro_by_id(self, registry, micro_technical):
        registry.register_micro(micro_technical)
        found = registry.get_micro(micro_technical.agent_id)
        assert found is micro_technical

    def test_find_micro_by_skill_name(self, registry, micro_technical):
        registry.register_micro(micro_technical)
        found = registry.find_micro_by_skill(micro_technical.skill_name)
        assert found is micro_technical

    def test_find_micro_by_resonance(self, registry, micro_agents):
        registry.register_many_micro(micro_agents)
        results = registry.find_micro_by_resonance("análisis técnico del sistema", top_n=2)
        assert len(results) <= 2

    def test_ecosystem_map_has_all_repos(self):
        eco = AgentRegistry.get_ecosystem_map()
        assert "skills-soberanos" in eco
        assert "el-dador-de-suenos-nucleus" in eco
        assert "grok-nodo-iluminado" in eco
        assert "ia-specialist-agent" in eco
        assert "tcu-unified-coherence-theory" in eco
        assert "el-iluminador-nucleo-soberano" in eco

    def test_get_repos_by_role(self):
        memory_repos = AgentRegistry.get_repos_by_role("memory_nucleus")
        assert len(memory_repos) == 1
        assert memory_repos[0]["repo"] == "el-dador-de-suenos-nucleus"

    def test_summary_counts_correctly(self, registry, micro_technical):
        registry.register_micro(micro_technical)
        s = registry.summary()
        assert s["micro_agents"] == 1
        assert s["macro_agents"] == 0
        assert s["ecosystem_repos"] == len(ECOSYSTEM_REPOS)


# ======================================================================= #
# SKILL LOADER                                                             #
# ======================================================================= #

class TestSkillLoader:
    def test_load_all_returns_list(self):
        loader = SkillLoader(include_examples=True)
        agents = loader.load_all()
        assert isinstance(agents, list)
        assert len(agents) >= 2  # al menos los dos de ejemplo

    def test_example_agents_have_unique_skill_names(self):
        loader = SkillLoader(include_examples=True)
        agents = loader.load_all()
        names = [a.skill_name for a in agents]
        assert len(names) == len(set(names))

    def test_all_loaded_are_micro_agents(self):
        loader = SkillLoader(include_examples=True)
        agents = loader.load_all()
        for agent in agents:
            assert isinstance(agent, BaseMicroAgent)

    def test_summary_has_loaded_count(self):
        loader = SkillLoader(include_examples=True)
        loader.load_all()
        s = loader.summary()
        assert s["loaded"] >= 2


# ======================================================================= #
# SUPERVISOR AGENT                                                         #
# ======================================================================= #

class TestSupervisorAgent:
    def test_handle_returns_dict(self, supervisor):
        result = supervisor.handle("análisis del sistema técnico")
        assert isinstance(result, dict)
        assert "status" in result

    def test_handle_activates_at_least_one_agent(self, supervisor):
        result = supervisor.handle("análisis técnico del sistema")
        assert result["agents_activated"] or result["agents_scored"]

    def test_handle_with_no_micro_agents(self):
        sv = SupervisorAgent(micro_agents=[])
        result = sv.handle("test")
        assert result["successful"] == 0
        assert result["agents_activated"] == []

    def test_handle_reports_q_impact(self, supervisor):
        result = supervisor.handle("análisis técnico")
        assert isinstance(result["total_q_impact"], float)

    def test_add_remove_micro_agent(self, supervisor):
        extra = BaseMicroAgent(skill=ExampleTechnicalSkill(), agent_id="micro:extra-test")
        initial = len(supervisor.micro_agents)
        supervisor.add_micro_agent(extra)
        assert len(supervisor.micro_agents) == initial + 1
        removed = supervisor.remove_micro_agent(extra.agent_id)
        assert removed
        assert len(supervisor.micro_agents) == initial


# ======================================================================= #
# RESOURCE ORCHESTRATOR                                                    #
# ======================================================================= #

class TestResourceOrchestrator:
    def test_activate_respects_max_concurrent(self, micro_agents):
        ro = ResourceOrchestrator(max_concurrent=1)
        results = ro.activate(micro_agents, intent="test")
        assert len(results) == 1

    def test_activate_all_when_within_limit(self, micro_agents):
        ro = ResourceOrchestrator(max_concurrent=10)
        results = ro.activate(micro_agents, intent="test")
        assert len(results) == len(micro_agents)

    def test_fail_fast_stops_on_error(self, micro_agents):
        # Crear un skill que siempre falla
        class FailingSkill(ExampleTechnicalSkill):
            def execute(self, context):
                raise RuntimeError("deliberate failure")

        from agents.micro.base_micro_agent import BaseMicroAgent
        failing_agent = BaseMicroAgent(skill=FailingSkill())
        ro = ResourceOrchestrator(max_concurrent=10, fail_fast=True)
        results = ro.activate([failing_agent] + micro_agents, intent="test")
        # Debe detenerse tras el primer error
        assert len(results) == 1
        assert not results[0].succeeded


# ======================================================================= #
# STATUS MONITOR                                                           #
# ======================================================================= #

class TestStatusMonitor:
    def test_get_summary_empty(self):
        monitor = StatusMonitor()
        s = monitor.get_summary()
        assert s["total_runs"] == 0

    def test_record_run_increments_count(self, micro_technical):
        monitor = StatusMonitor()
        req = make_task_request(intent="test")
        result = micro_technical.handle(req)
        monitor.record_run(intent="test", results=[result])
        s = monitor.get_summary()
        assert s["total_runs"] == 1
        assert s["recent_runs"] == 1

    def test_is_not_degraded_on_success(self, micro_technical):
        monitor = StatusMonitor()
        req = make_task_request(intent="test")
        result = micro_technical.handle(req)
        monitor.record_run(intent="test", results=[result])
        assert not monitor.is_degraded()

    def test_health_critical_on_all_errors(self):
        monitor = StatusMonitor()
        error_result = make_error_result("t1", "micro:x", "err")
        for _ in range(5):
            monitor.record_run(intent="test", results=[error_result])
        s = monitor.get_summary()
        assert s["health"] == "CRITICAL"


# ======================================================================= #
# PRIORITY MANAGER                                                         #
# ======================================================================= #

class TestPriorityManager:
    def test_dequeue_empty_returns_none(self):
        pm = PriorityManager()
        assert pm.dequeue() is None

    def test_enqueue_dequeue_fifo_same_priority(self):
        pm = PriorityManager()
        r1 = make_task_request(intent="first", priority=5)
        r2 = make_task_request(intent="second", priority=5)
        pm.enqueue(r1)
        pm.enqueue(r2)
        assert pm.dequeue().intent == "first"
        assert pm.dequeue().intent == "second"

    def test_high_priority_before_low(self):
        pm = PriorityManager()
        low = make_task_request(intent="low", priority=9)
        high = make_task_request(intent="high", priority=1)
        pm.enqueue(low)
        pm.enqueue(high)
        assert pm.dequeue().intent == "high"

    def test_is_empty(self):
        pm = PriorityManager()
        assert pm.is_empty()
        pm.enqueue(make_task_request(intent="x"))
        assert not pm.is_empty()

    def test_drain_all(self):
        pm = PriorityManager()
        for i in range(3):
            pm.enqueue(make_task_request(intent=f"task{i}"))
        drained = pm.drain_all()
        assert len(drained) == 3
        assert pm.is_empty()

    def test_queue_status(self):
        pm = PriorityManager()
        pm.enqueue(make_task_request(intent="test", priority=3))
        s = pm.queue_status()
        assert s["queued"] == 1
        assert s["next_priority"] == 3
