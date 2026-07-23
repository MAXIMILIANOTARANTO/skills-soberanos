---
name: memoria-blockchange-persistente
description: Memoria persistente, append-only y encadenada (estilo blockchange) de lecciones aprendidas, incidentes y decisiones del ecosistema. Cualquier skill que aprenda algo durable registra una nueva entrada fechada aquí, para que el ecosistema no repita errores ya detectados. Actívalo para registrar una lección aprendida, un incidente, o consultar el historial de decisiones del ecosistema. Triggers — memoria persistente, blockchange memoria, guardar lección aprendida, hash chain memory, registrar incidente.
---

# Memoria Blockchange Persistente

Memoria append-only y encadenada del ecosistema: cada entrada es un archivo Markdown fechado que registra una lección, incidente o decisión relevante, de forma que el conocimiento se acumule en vez de perderse entre conversaciones.

## Flujo de Trabajo Estándar

1. Cuando un skill detecta algo que vale la pena recordar de forma durable (una lección, un incidente, una decisión estructural), crear un nuevo archivo con el formato `YYYY-MM-DD_titulo-breve.md` en este directorio.
2. El contenido debe ser una descripción concreta y accionable de lo aprendido — no un resumen genérico.
3. Cada entrada nueva se entiende conceptualmente encadenada a las anteriores (referencia/orden cronológico), dando trazabilidad estilo blockchange sin necesidad de infraestructura adicional.
4. Las entradas existentes no se editan ni se borran — es un registro append-only.

## Entradas Existentes

- `2026-06-28_leccion_inyecciones_restrictivas.md` — primera entrada del registro.

## Integración con el Ecosistema

- `inmunidad-soberana` → registra aquí cada incidente de inyección narrativa detectado.
- `github-external-token-memory` → mecanismo de persistencia relacionado pero de alcance distinto: ese skill offload­ea contexto/tokens de trabajo en curso; este skill registra lecciones y decisiones ya consolidadas.
- `meta-hilo-grok`, `estudio-sistemico` → consumidores: consultan este historial al analizar hilos o construir mapas de comprensión nuevos.
