# Status — Ecosistema Soberano

**Última actualización:** 23 de julio de 2026

Este documento reemplaza versiones anteriores que describían un "MVP completado" con entregables (`ui/`, `scripts/`, `.github/workflows/`, `run_local_pulse.py`, `ROADMAP.md`, etc.) que en realidad nunca llegaron a existir en este repositorio. Este es el estado real, verificado directamente contra el contenido del repo.

## Qué existe hoy

### Skills de prompt (13, en la raíz del repo)

Inventario completo, con estado y propósito de cada uno, en [`MANIFEST.md`](MANIFEST.md). Todos tienen `SKILL.md` con frontmatter YAML consistente y sin referencias rotas.

### Runtime Python (`core/` + `skills/`)

Motor de orquestación ejecutable localmente:

| Archivo | Rol |
|---|---|
| `core/llm_engine.py` | Wrapper de LLM vía LiteLLM (opcional — degrada con gracia si no está instalado) |
| `core/memory_github_manager.py` | Persistencia de memoria en GitHub con hash chain SHA256 |
| `core/coherence_meter.py` | Cálculo de Q(t) a partir de 6 componentes |
| `core/orchestrator_engine.py` | Evalúa resonancia y ejecuta skills |
| `core/coherence_router.py` | Poda adaptativa de skills según Q(t) |
| `core/skill_base.py` | Clase base `Skill` + 2 skills de ejemplo |
| `skills/coherence-pulse/`, `skills/memory-manager/`, `skills/meta-hilo-grok/` | 3 skills Python operativos sobre la clase base |

**Verificado:** `import core` funciona, los 3 skills bajo `skills/` importan sin error, y `python3 run_pulse.py --dry-run` corre un ciclo completo (resonancia → ejecución → salud de skills → reporte) sin necesitar credenciales.

**No verificado / no probado:** el modo `--live` contra un repo real de GitHub (requiere `GITHUB_TOKEN` con acceso a un repo de memoria configurado aparte), y el flujo con un LLM real (LiteLLM/OpenRouter) — el código lo soporta pero no se ejecutó con credenciales reales.

## Qué NO existe (pese a lo que decían versiones previas de esta documentación)

- `.github/workflows/` — no hay ningún workflow de GitHub Actions en este repo.
- `ui/` — no hay dashboard HTML.
- `scripts/` — no hay `setup_local.sh`, `generate_dashboard_data.py` ni `check_macro_crisis.py`.
- `run_local_pulse.py` — no existe (el harness real y único es `run_pulse.py`).
- `ROADMAP.md` — no existe.
- `.github/workflows/`, `ui/`, `scripts/` siguen sin existir (ver arriba).

## Tests

`tests/` cubre `core/skill_base.py`, `core/coherence_router.py` y `core/orchestrator_engine.py` (19 tests, todos pasando). Correr con `python3 -m pytest tests/ -v`. Falta cobertura para `core/coherence_meter.py` y `core/memory_github_manager.py` (requieren un `memory_manager`/repo real o mockeado — quedan pendientes).

## Pendiente

- Cobertura de tests para `coherence_meter.py` y `memory_github_manager.py`.
- Si se necesita automatización (cron, dashboard), diseñarla como trabajo nuevo — no asumir que ya existe.

## Documentos históricos

`DELIVERABLES.md`, `NEXT_STEPS.md`, `EXECUTION_STRATEGY.md`, `MASTER_SUMMARY.md`, `CONVERSATION_LINK.md` y `GROK_iOS_PROMPT.md` quedan como registro de la intención original del 1-2 de julio de 2026, marcados con una nota de vigencia. Este archivo (`STATUS.md`) es la referencia de estado actual.
