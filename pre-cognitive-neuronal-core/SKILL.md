---
name: pre-cognitive-neuronal-core
description: Punto de partida neuronal obligatorio del ecosistema de skills. Implementa predictive coding jerárquico, active inference y procesamiento de lenguaje dual-stream para generar predicciones top-down antes de procesar cualquier tarea compleja. Actívalo primero en cualquier proceso cognitivo complejo, antes de delegar a otros skills. Triggers — activar núcleo pre-cognitivo, predictive coding, active inference, procesamiento de lenguaje dual-stream, predicción top-down.
---

# Pre-Cognitive Neuronal Core

Punto de partida neuronal obligatorio del ecosistema de skills: genera una predicción del resultado esperado antes de que cualquier otro skill se ejecute, y ajusta esa predicción con el resultado real.

## Principios

- **Predictive coding jerárquico** — capas de predicción de alto nivel (intención, objetivo) hacia bajo nivel (acción concreta), y de vuelta.
- **Active inference** — minimizar el error de predicción actuando sobre el entorno, no solo actualizando creencias.
- **Sparse activation** — solo activar los skills necesarios para la tarea, evitando gasto de tokens en ramas no predichas como relevantes.
- **Procesamiento de lenguaje dual-stream** — separar un flujo "qué" (contenido semántico, objetivo del usuario) de un flujo "cómo" (forma, estructura de la respuesta), inspirado en el modelo dual-stream del procesamiento de lenguaje humano.
- **Flujo ida y vuelta**: predicción → comparación con input real → error → actualización.

## Flujo de Trabajo Estándar

1. Recibir la tarea o input entrante.
2. Generar una predicción top-down: ¿qué objetivo persigue el usuario? ¿qué skills probablemente hacen falta?
3. Separar el input en flujo semántico (qué se pide) y flujo estructural (cómo se espera la respuesta).
4. Ejecutar o delegar según la predicción (sparse activation: solo lo necesario).
5. Comparar el resultado real contra la predicción inicial.
6. Ajustar la predicción para el siguiente ciclo (aprendizaje continuo).

## Integración con el Ecosistema

- `orquestador-soberano` → lo activa siempre primero, en cada ciclo de coordinación.
- `estudio-sistemico` → consume las predicciones para construir mapas de comprensión más precisos.

Este skill debe activarse primero en cualquier proceso cognitivo complejo.
