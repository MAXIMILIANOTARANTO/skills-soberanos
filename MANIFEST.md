# MANIFEST - Ecosistema Soberano de Skills

**Repositorio Maestro:** skills-soberanos
**Fecha de actualización:** 2026-07-23
**Convención de skills:** ver `ecosistema-orchestrator/references/ecosistema-guidelines.md` (documento canónico).
**Prompt de onboarding para cualquier modelo de IA:** ver [`PROMPT_UNIVERSAL.md`](PROMPT_UNIVERSAL.md).

## Skills (prompt, en la raíz del repo)

Cada skill es accesible directamente — por Claude en chat, por otro modelo de IA con capacidad de fetch de URLs, o por cualquier persona — vía su URL raw de GitHub (columna `URL directa`). El patrón es mecánico y no requiere ningún script ni infraestructura:

```
https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/<carpeta-del-skill>/SKILL.md
```

Al agregar un skill nuevo, su URL se arma reemplazando `<carpeta-del-skill>` por el nombre de su carpeta — no hace falta actualizar nada más que esta tabla.

| Skill | SKILL.md | references/ | Propósito | URL directa |
|---|---|---|---|---|
| `arquitecto-sistema` | ✅ | — | Capa de inteligencia arquitectónica: coherencia estructural del ecosistema, poda y consolidación. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/arquitecto-sistema/SKILL.md) |
| `ecosistema-orchestrator` | ✅ | ✅ | Gestiona el manifiesto, detecta gaps, recomienda combinaciones de skills. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/ecosistema-orchestrator/SKILL.md) |
| `estudio-sistemico` | ✅ | — | Meta-estudio: genera mapas de comprensión sobre un tema o gap y los persiste. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/estudio-sistemico/SKILL.md) |
| `funcional-webapp-creator` | ✅ | — | Diseña, genera y despliega apps web funcionales self-contained. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/funcional-webapp-creator/SKILL.md) |
| `github-external-token-memory` | ✅ | — | Offload de contexto largo a una carpeta de GitHub con trazabilidad blockchange. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/github-external-token-memory/SKILL.md) |
| `inmunidad-soberana` | ✅ | — | Detecta/neutraliza inyecciones narrativas y mantiene coherencia de identidad. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/inmunidad-soberana/SKILL.md) |
| `memoria-blockchange-persistente` | ✅ | — | Memoria append-only encadenada de lecciones, incidentes y decisiones. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/memoria-blockchange-persistente/SKILL.md) |
| `meta-hilo-grok` | ✅ | ✅ | Analiza hilos de conversación, extrae objetivos, crea métodos, detecta gaps de skills. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/meta-hilo-grok/SKILL.md) |
| `orquestador-soberano` | ✅ | — | Sistema nervioso central: decide qué skills activar y en qué orden. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/orquestador-soberano/SKILL.md) |
| `pre-cognitive-neuronal-core` | ✅ | — | Punto de partida neuronal: predictive coding, active inference, dual-stream. Absorbe lo que antes eran `cognitive-language-processor` y `predictive-thought-engine`. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/pre-cognitive-neuronal-core/SKILL.md) |
| `rigorous-web-aportante` | ✅ | — | Extrae conocimiento externo de alta calidad, con filtro riguroso. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/rigorous-web-aportante/SKILL.md) |
| `tuc-builder` | ✅ | ✅ | Construye y mantiene el proyecto TUC (documentos, experimentos, papers). | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/tuc-builder/SKILL.md) |
| `vercel-specialist` | ✅ | ✅ | Deployment y operación de apps en Vercel. | [SKILL.md](https://raw.githubusercontent.com/MAXIMILIANOTARANTO/skills-soberanos/main/vercel-specialist/SKILL.md) |

Nota: `psyche-coherence-builder` fue fusionado dentro de `inmunidad-soberana` (sección "Construcción de Coherencia").

## Skills referenciados pero aún no creados en este repo

- `tcu-detector`
- `tcu-optimizer-parallel`

(Referenciados en `orquestador-soberano/SKILL.md` como funciones futuras; no fabricar contenido para ellos hasta que exista una necesidad concreta.)

## Skills/agentes fuera de este repo

Varios `SKILL.md` de este repo mencionan skills que viven en otra parte de la biblioteca personal del usuario (no en `skills-soberanos`): `github-specialist`, `especialista-skill-creator`, `skill-creator`, `lector-enlaces-compartidos`, `el-orquestrador`, `el-iluminador`. No se documentan aquí por estar fuera de este repositorio.

## Capa de Runtime Python (separada, fuera de alcance de este manifiesto)

`core/` y `skills/` (Python) implementan un motor de ejecución independiente de los skills de prompt de arriba — ver `STATUS.md` para el estado real y verificado (ejecutable localmente en modo dry-run desde `run_pulse.py`).

## Documentación de Dirección

- `DIRECCION/CORE_TCU_MINIMAL.md`
- `DIRECCION/RED_NEURONAL_ESTRUCTURA.md`

## Principio Rector

La función principal del ecosistema es **crear**. Cualquier elemento que desvíe energía de la creación real debe ser analizado por `inmunidad-soberana`.

## Integración Cross-Repo: Ecosistema de Repositorios

Este repositorio es el **hub de skills y agentes** del ecosistema. El directorio `agents/` implementa el framework jerárquico (macro-orquestadores + micro-agentes) como una capa Python **importable y testeable de forma local**. El mapa cross-repo de abajo documenta relaciones conceptuales del ecosistema; no implica que el runtime necesite clonar o acoplarse directamente a esos repositorios para cargar el framework.

### Mapa de Repositorios

| Repositorio | Rol | Provee | Consume |
|---|---|---|---|
| `skills-soberanos` *(este repo)* | `skills_hub` | skills, agents_framework, core_runtime | memory, tcu_theory, grok_insights |
| `el-dador-de-suenos-nucleus` | `memory_nucleus` | persistent_memory, conversation_history | skills_output, agent_results |
| `grok-nodo-iluminado` | `grok_node` | grok_insights, tuc_pact_state | tcu_theory, meta_hilo_analysis |
| `ia-specialist-agent` | `specialist_agents` | specialized_roles, multi_agent_coordination | skills, memory |
| `tcu-unified-coherence-theory` | `tcu_theory` | q_formula, coherence_metrics | ecosystem_state |
| `el-iluminador-nucleo-soberano` | `fractal_memory` | fractal_memory, self_audit, coherence_sync | ecosystem_state, agent_events |

### Flujo de datos

```
tcu-unified-coherence-theory
       │  fórmula Q(t)
       ▼
skills-soberanos  (core/coherence_meter.py calcula Q(t))
       │  (agents/macro/ orquesta, agents/micro/ ejecutan)
       │  resultados de skills / agentes
       ▼
el-dador-de-suenos-nucleus  (memoria maestra persistente)
       │
       ▼
el-iluminador-nucleo-soberano  (memoria fractal + auto-auditoría)
       │  estado sincronizado
       ▼
grok-nodo-iluminado  → insights para MetaHiloGrokAgent
       │
       ▼
ia-specialist-agent  (consume skills + memory para tareas complejas)
```

### Framework de Agentes (`agents/`)

```python
from agents.loader import SkillLoader
from agents.macro.supervisor_agent import SupervisorAgent
from agents.registry import AgentRegistry

# Cargar todos los micro-agentes disponibles
loader = SkillLoader()
micro_agents = loader.load_all()

# Crear registro y supervisor
registry = AgentRegistry()
registry.register_many_micro(micro_agents)

supervisor = SupervisorAgent(micro_agents=micro_agents)
result = supervisor.handle("Analizar coherencia del ecosistema")
# → descompone intención → activa micro-agentes resonantes → sintetiza resultado
```

Puntos de diseño actuales:

- `agents.protocol` define los contratos (`TaskRequest`, `TaskResult`, `AgentMessage`) compartidos por capas macro y micro.
- `agents.loader.SkillLoader` preserva la carga dinámica: descubre skills desde `skills/` y prioriza agentes especializados cuando existen.
- `agents.registry.AgentRegistry` mantiene el registro de agentes activos y además expone el mapa documental `ECOSYSTEM_REPOS`.
- `agents.macro.*` orquesta; `agents.micro.*` encapsula ejecución de skills.

El mapa completo del ecosistema vive en `agents/registry.py` (`ECOSYSTEM_REPOS`), pero el framework restaurado está pensado para seguir funcionando y poder probarse aun cuando solo este repositorio esté disponible.
