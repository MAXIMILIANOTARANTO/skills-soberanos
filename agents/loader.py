"""
Skill Loader — Descubrimiento y carga dinámica de skills como micro-agentes.

Carga automáticamente los skills de `skills/` y los envuelve en BaseMicroAgent,
más los tres skills pre-existentes (coherence-pulse, memory-manager, meta-hilo-grok).

Uso:
    loader = SkillLoader()
    micro_agents = loader.load_all()
    # → lista de BaseMicroAgent listos para registrar en AgentRegistry
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from core.skill_base import Skill, ExampleTechnicalSkill, ExampleCognitiveSkill
from .micro.base_micro_agent import BaseMicroAgent


# Ruta raíz del proyecto (donde vive este archivo: agents/loader.py → un nivel arriba)
_PROJECT_ROOT = Path(__file__).parent.parent


class SkillLoader:
    """
    Descubre y carga skills del ecosistema como micro-agentes.

    Orden de carga:
    1. Skills de `skills/` (directorios con *_skill.py).
    2. Skills de ejemplo (ExampleTechnicalSkill, ExampleCognitiveSkill).

    Las subclases concretas de micro-agentes (CoherencePulseAgent, etc.) se
    registran automáticamente si sus módulos están disponibles.
    """

    SKILLS_DIR: Path = _PROJECT_ROOT / "skills"

    # Mapeo explícito: nombre de skill → módulo Python + clase + agent class
    _EXPLICIT_AGENTS: List[Dict[str, str]] = [
        {
            "agent_module": "agents.micro.coherence_pulse_agent",
            "agent_class": "CoherencePulseAgent",
        },
        {
            "agent_module": "agents.micro.memory_manager_agent",
            "agent_class": "MemoryManagerAgent",
        },
        {
            "agent_module": "agents.micro.meta_hilo_grok_agent",
            "agent_class": "MetaHiloGrokAgent",
        },
    ]

    def __init__(self, include_examples: bool = True):
        """
        Args:
            include_examples: Si True, incluir skills de ejemplo (para testing).
        """
        self.include_examples = include_examples
        self._loaded: List[BaseMicroAgent] = []
        self._errors: List[Dict[str, str]] = []

    def load_all(self) -> List[BaseMicroAgent]:
        """
        Cargar todos los micro-agentes disponibles.

        Returns:
            Lista de BaseMicroAgent listos para usar.
        """
        self._loaded = []
        self._errors = []

        # 1. Cargar agentes concretos (CoherencePulseAgent, etc.)
        self._load_explicit_agents()

        # 2. Descubrimiento dinámico en skills/
        self._discover_skills()

        # 3. Skills de ejemplo (siempre disponibles para testing)
        if self.include_examples:
            self._load_example_skills()

        return self._loaded

    def load_by_skill_name(self, skill_name: str) -> Optional[BaseMicroAgent]:
        """Cargar un micro-agente específico por nombre de skill."""
        all_agents = self.load_all()
        for agent in all_agents:
            if agent.skill_name == skill_name:
                return agent
        return None

    # ------------------------------------------------------------------ #
    # HELPERS DE CARGA                                                     #
    # ------------------------------------------------------------------ #

    def _load_explicit_agents(self) -> None:
        """Intentar cargar los agentes micro pre-definidos."""
        for entry in self._EXPLICIT_AGENTS:
            try:
                agent_mod = importlib.import_module(entry["agent_module"])
                agent_cls: Type[BaseMicroAgent] = getattr(agent_mod, entry["agent_class"])
                self._loaded.append(agent_cls())
            except Exception as exc:  # noqa: BLE001
                self._errors.append(
                    {
                        "source": entry["agent_module"],
                        "error": str(exc),
                    }
                )

    def _discover_skills(self) -> None:
        """
        Descubrir dinámicamente skills en skills/ que no tienen un agente explícito.
        Busca archivos *_skill.py y los envuelve en BaseMicroAgent genérico.
        """
        if not self.SKILLS_DIR.exists():
            return

        already_loaded_skills = {a.skill_name for a in self._loaded}

        for skill_dir in sorted(self.SKILLS_DIR.iterdir()):
            if not skill_dir.is_dir():
                continue
            for skill_file in skill_dir.glob("*_skill.py"):
                try:
                    skill_instance = self._import_skill_from_file(skill_file)
                    if skill_instance and skill_instance.name not in already_loaded_skills:
                        self._loaded.append(BaseMicroAgent(skill=skill_instance))
                        already_loaded_skills.add(skill_instance.name)
                except Exception as exc:  # noqa: BLE001
                    self._errors.append(
                        {
                            "source": str(skill_file),
                            "error": str(exc),
                        }
                    )

    def _import_skill_from_file(self, path: Path) -> Optional[Skill]:
        """
        Importar un archivo Python de skill y devolver su instancia principal.
        Busca la primera subclase concreta de Skill definida en el módulo.
        """
        module_name = f"_dynamic_skill_{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, Skill)
                and attr is not Skill
                and not attr.__name__.startswith("Example")
            ):
                return attr()

        return None

    def _load_example_skills(self) -> None:
        """Agregar skills de ejemplo para testing."""
        already = {a.skill_name for a in self._loaded}
        for skill_cls in (ExampleTechnicalSkill, ExampleCognitiveSkill):
            instance = skill_cls()
            if instance.name not in already:
                self._loaded.append(BaseMicroAgent(skill=instance))

    # ------------------------------------------------------------------ #
    # DIAGNÓSTICO                                                          #
    # ------------------------------------------------------------------ #

    def get_errors(self) -> List[Dict[str, str]]:
        """Errores encontrados en la última llamada a load_all()."""
        return list(self._errors)

    def summary(self) -> Dict[str, Any]:
        return {
            "loaded": len(self._loaded),
            "errors": len(self._errors),
            "agent_ids": [a.agent_id for a in self._loaded],
            "error_details": self._errors,
        }
