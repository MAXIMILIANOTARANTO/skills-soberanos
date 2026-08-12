---
name: github-external-token-memory
description: Utiliza una carpeta específica en GitHub como memoria externa persistente para hacer offload de contexto largo, con trazabilidad estilo blockchange. Actívalo cuando el contexto de una conversación o tarea crece demasiado para mantenerse completo en la ventana activa. Triggers — offload de contexto, memoria externa de tokens, github como memoria, context window management, guardar contexto largo.
---

# GitHub External Token Memory

Utiliza una carpeta específica en GitHub como memoria externa persistente de tokens con offloading y trazabilidad blockchange.

## Flujo de Trabajo Estándar

1. Detectar que el contexto activo (conversación o tarea) está creciendo más allá de lo manejable en la ventana de contexto actual.
2. Escribir un archivo fechado con el contenido a descargar en la carpeta de memoria externa del repositorio en GitHub.
3. Encadenar el nuevo archivo con los anteriores (hash/referencia al archivo previo) para mantener trazabilidad estilo blockchange.
4. Dejar en el contexto activo solo un puntero o resumen breve al archivo, en vez del contenido completo.
5. Recuperar el contenido completo del archivo bajo demanda cuando vuelva a ser relevante.

## Integración con el Ecosistema

- `orquestador-soberano` → lo usa para offload de contexto largo (paso 3 de su flujo estándar).
- `memoria-blockchange-persistente` → mecanismo de persistencia relacionado pero de alcance distinto: este skill offload­ea contexto/tokens de trabajo en curso, mientras que `memoria-blockchange-persistente` registra lecciones y decisiones ya consolidadas.
