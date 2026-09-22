import json
from datetime import datetime, timedelta

from core.memory_github_manager import MemoryGitHubManager


class FakeContent:
    def __init__(self, name, payload):
        self.name = name
        self.decoded_content = json.dumps(payload).encode("utf-8")


class FakeRepo:
    def __init__(self, memories):
        self.full_name = "demo/repo"
        self._memories = memories

    def get_contents(self, path):
        if path == "memoria/conversaciones":
            return [
                FakeContent(name, payload)
                for name, payload in self._memories.items()
            ]
        return []


def test_load_memory_filters_recent_entries_with_days_back():
    now = datetime.utcnow()
    recent_ts = (now - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    old_ts = (now - timedelta(days=12)).strftime("%Y-%m-%dT%H:%M:%SZ")

    repo = FakeRepo(
        {
            "2024-01-02T00-00-00Z.json": {"timestamp": old_ts, "q_value": 0.2},
            "2024-01-03T00-00-00Z.json": {"timestamp": recent_ts, "q_value": 0.8},
            "bad.json": {"timestamp": "not-a-date"},
        }
    )
    manager = MemoryGitHubManager(repo=repo)

    memories = manager.load_memory(days_back=7)

    assert len(memories) == 1
    assert memories[0]["q_value"] == 0.8
