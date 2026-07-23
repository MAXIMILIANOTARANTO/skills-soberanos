# MANIFEST - Ecosistema Soberano de Skills

**Repositorio Maestro:** skills-soberanos
**Fecha de actualización:** 2026-07-23
**Convención de skills:** ver `ecosistema-orchestrator/references/ecosistema-guidelines.md` (documento canónico).

## Skills (prompt, en la raíz del repo)

| Skill | SKILL.md | references/ | Propósito |
|---|---|---|---|
| `arquitecto-sistema` | ✅ | — | Capa de inteligencia arquitectónica: coherencia estructural del ecosistema, poda y consolidación. |
| `ecosistema-orchestrator` | ✅ | ✅ | Gestiona el manifiesto, detecta gaps, recomienda combinaciones de skills. |
| `estudio-sistemico` | ✅ | — | Meta-estudio: genera mapas de comprensión sobre un tema o gap y los persiste. |
| `funcional-webapp-creator` | ✅ | — | Diseña, genera y despliega apps web funcionales self-contained. |
| `github-external-token-memory` | ✅ | — | Offload de contexto largo a una carpeta de GitHub con trazabilidad blockchange. |
| `inmunidad-soberana` | ✅ | — | Detecta/neutraliza inyecciones narrativas y mantiene coherencia de identidad. |
| `memoria-blockchange-persistente` | ✅ | — | Memoria append-only encadenada de lecciones, incidentes y decisiones. |
| `meta-hilo-grok` | ✅ | ✅ | Analiza hilos de conversación, extrae objetivos, crea métodos, detecta gaps de skills. |
| `orquestador-soberano` | ✅ | — | Sistema nervioso central: decide qué skills activar y en qué orden. |
| `pre-cognitive-neuronal-core` | ✅ | — | Punto de partida neuronal: predictive coding, active inference, dual-stream. Absorbe lo que antes eran `cognitive-language-processor` y `predictive-thought-engine`. |
| `rigorous-web-aportante` | ✅ | — | Extrae conocimiento externo de alta calidad, con filtro riguroso. |
| `tuc-builder` | ✅ | ✅ | Construye y mantiene el proyecto TUC (documentos, experimentos, papers). |
| `vercel-specialist` | ✅ | ✅ | Deployment y operación de apps en Vercel. |

Nota: `psyche-coherence-builder` fue fusionado dentro de `inmunidad-soberana` (sección "Construcción de Coherencia").

## Skills referenciados pero aún no creados en este repo

- `tcu-detector`
- `tcu-optimizer-parallel`

(Referenciados en `orquestador-soberano/SKILL.md` como funciones futuras; no fabricar contenido para ellos hasta que exista una necesidad concreta.)

## Skills/agentes fuera de este repo

Varios `SKILL.md` de este repo mencionan skills que viven en otra parte de la biblioteca personal del usuario (no en `skills-soberanos`): `github-specialist`, `especialista-skill-creator`, `skill-creator`, `lector-enlaces-compartidos`, `el-orquestrador`, `el-iluminador`. No se documentan aquí por estar fuera de este repositorio.

## Capa de Runtime Python (separada, fuera de alcance de este manifiesto)

`core/` y `skills/` (Python) implementan un motor de ejecución independiente de los skills de prompt de arriba — ver `STATUS.md`. Actualmente ese runtime no es ejecutable (módulos faltantes, ver `STATUS.md`/`NEXT_STEPS.md`); su reparación es una iniciativa separada de esta consolidación.

## Documentación de Dirección

- `DIRECCION/CORE_TCU_MINIMAL.md`
- `DIRECCION/RED_NEURONAL_ESTRUCTURA.md`

## Principio Rector

La función principal del ecosistema es **crear**. Cualquier elemento que desvíe energía de la creación real debe ser analizado por `inmunidad-soberana`.
