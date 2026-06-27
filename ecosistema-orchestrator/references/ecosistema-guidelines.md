# Directrices del Ecosistema de Skills Soberanos

## Principios Fundamentales

1. **Soberanía del usuario** — Todo skill debe servir al usuario, no al revés.
2. **Acción real > Análisis** — Preferimos crear, desplegar y versionar antes que solo analizar.
3. **Aprendizaje continuo** — Cada interacción debe mejorar el sistema.
4. **Coherencia TUC** — Buscar resonancia, fractalidad y coherencia en cómo se relacionan los skills.
5. **Versionado central** — Todo skill importante debe estar en `skills-soberanos`.

## Estructura Recomendada de un Skill

```
skill-name/
├── SKILL.md              # Descripción, triggers e instrucciones principales
├── references/           # Documentación de apoyo
└── assets/               # Plantillas, ejemplos, archivos que se copian
```

## Cómo Actualizar el MANIFEST.md

Cuando se crea o modifica un skill importante:
1. Actualizar la sección correspondiente en `MANIFEST.md`.
2. Incluir: nombre, rol principal, estado, triggers principales.
3. Mantener la fecha de última actualización.

## Criterios para Proponer un Nuevo Skill

Un nuevo skill vale la pena si cumple al menos 2 de estos criterios:
- Resuelve un gap recurrente en los hilos del usuario.
- Permite orquestar mejor skills existentes.
- Aumenta la soberanía o autonomía del ecosistema.
- Tiene triggers claros y reutilizables.
- Se alinea con TUC / MHE / principios del usuario.

## Relación entre Skills Clave

- `meta-hilo-grok` → Analiza conversaciones y detecta necesidades/gaps.
- `ecosistema-orchestrator` → Toma las detecciones de gaps y decide qué hacer (recomendar, crear, reorganizar).
- `funcional-webapp-creator` → Ejecuta la creación de herramientas concretas cuando se necesita una app.
- `github-specialist` → Se usa para versionar y mantener el repo central.

## Flujo Recomendado de Evolución

1. `meta-hilo-grok` analiza un hilo importante.
2. Detecta patrones o gaps.
3. `ecosistema-orchestrator` evalúa si hace falta un nuevo skill o reorganización.
4. Si corresponde, se usa `especialista-skill-creator` + `skill-creator` para crearlo.
5. Se versiona en `skills-soberanos`.
6. Se actualiza el MANIFEST.

Este documento debe mantenerse actualizado por `ecosistema-orchestrator`.