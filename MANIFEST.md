# MANIFEST - Ecosistema Soberano de Skills

**Repositorio Maestro:** skills-soberanos
**Fecha de actualización:** 2026-07-23
**Convención de skills:** ver `ecosistema-orchestrator/references/ecosistema-guidelines.md` (documento canónico).

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
