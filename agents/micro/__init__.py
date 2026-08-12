"""
Micro Agents — Paquete de agentes micro especializados.

Cada agente micro envuelve un skill soberano y expone la interfaz
estándar de TaskRequest/TaskResult para interactuar con los agentes macro.
"""

from agents.micro.base_micro_agent import BaseMicroAgent
from agents.micro.coherence_pulse_agent import CoherencePulseAgent
from agents.micro.memory_manager_agent import MemoryManagerAgent
from agents.micro.meta_hilo_grok_agent import MetaHiloGrokAgent

__all__ = [
    "BaseMicroAgent",
    "CoherencePulseAgent",
    "MemoryManagerAgent",
    "MetaHiloGrokAgent",
]
