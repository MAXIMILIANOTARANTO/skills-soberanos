"""
Cross-repository feedback bridge.

The bridge keeps integrations optional: each repository is represented by an
adapter callable supplied by the host application. This repository produces a
stable feedback envelope, while adapters decide how to persist or transport it.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Mapping

from .protocol import utc_now_iso


FeedbackAdapter = Callable[[Dict[str, Any]], Any]


class CrossRepoFeedback:
    """Build and publish feedback without coupling the runtime to GitHub APIs."""

    TARGETS = (
        "el-dador-de-suenos-nucleus",
        "grok-nodo-iluminado",
        "ia-specialist-agent",
        "tcu-unified-coherence-theory",
        "el-iluminador-nucleo-soberano",
    )

    def build_envelope(
        self,
        *,
        intent: str,
        response: Mapping[str, Any],
        status: Mapping[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Create the portable event consumed by cross-repo adapters."""
        return {
            "event_type": "skills_soberanos.execution_feedback",
            "timestamp": utc_now_iso(),
            "source_repo": "skills-soberanos",
            "intent": intent[:200],
            "status": dict(status or {}),
            "payload": {
                "activated_agents": list(response.get("agents_activated", [])),
                "successful": response.get("successful", 0),
                "errors": response.get("errors", 0),
                "total_q_impact": response.get("total_q_impact", 0.0),
                "results": list(response.get("results", [])),
            },
        }

    def publish(
        self,
        envelope: Mapping[str, Any],
        adapters: Mapping[str, FeedbackAdapter] | None = None,
    ) -> Dict[str, Any]:
        """
        Publish to configured targets and report each failure explicitly.

        Adapters are intentionally injected so production deployments can use
        GitHub, queues, or local stores without making them dependencies here.
        """
        adapters = adapters or {}
        published = []
        errors = []

        for target, adapter in adapters.items():
            if target not in self.TARGETS:
                errors.append({"target": target, "error": "unsupported feedback target"})
                continue
            if not callable(adapter):
                errors.append({"target": target, "error": "adapter is not callable"})
                continue
            try:
                adapter(dict(envelope))
                published.append(target)
            except Exception as exc:  # adapter boundary: isolate and report it
                errors.append({"target": target, "error": str(exc)})

        return {
            "published": published,
            "errors": errors,
            "configured_targets": sorted(adapters),
        }

