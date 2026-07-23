# WORKFLOW - Ecosistema de Investigación TUC

**Versión:** 1.0  
**Fecha:** 23 de julio de 2026  
**Propósito:** Definir el flujo de trabajo práctico entre los skills del ecosistema de investigación de la Teoría Unificada de la Coherencia (TUC).

---

## Principios del Flujo

1. **Ciclo iterativo**: El ecosistema funciona en ciclos de investigación que pueden ser completos o parciales.
2. **Calidad sobre velocidad**: Nunca se salta validación estadística ni revisión crítica.
3. **Trazabilidad**: Todo paso queda registrado en `blockchange-memoria`.
4. **Flexibilidad**: El flujo puede adaptarse según el contexto y los resultados intermedios.
5. **Propósito claro**: Todo ciclo debe terminar entregando valor a `tuc-builder`.

---

## Flujo Estándar de Investigación TUC

### Fase 1: Detección
- **Skill principal**: `tcu-detector`
- **Objetivo**: Identificar patrones, bifurcaciones, cambios de régimen o estados de coherencia relevantes.
- **Output**: Detecciones estructuradas con parámetros y contexto metodológico.

### Fase 2: Validación Estadística
- **Skill principal**: `tuc-statistician`
- **Objetivo**: Evaluar significancia, robustez y confiabilidad de las detecciones.
- **Output**: Evaluación de robustez + métricas estadísticas + limitaciones.

### Fase 3: Reflexión y Generación de Hipótesis
- **Skill principal**: `tuc-reflexion`
- **Objetivo**: Analizar los hallazgos, generar hipótesis y proponer mejoras o extensiones a TUC.
- **Output**: Hipótesis, reflexiones y propuestas de refinamiento de la teoría.

### Fase 4: Crítica y Control de Calidad
- **Skill principal**: `tuc-critic`
- **Objetivo**: Revisar críticamente los hallazgos y las hipótesis antes de avanzar.
- **Output**: Observaciones críticas, detección de debilidades y sugerencias de mejora.

### Fase 5: Validación Aplicada (Opcional)
- **Skill principal**: `tuc-field-feedback`
- **Objetivo**: Contrastar los hallazgos con evidencia del mundo real o contextos aplicados.
- **Output**: Observaciones de campo + brechas entre teoría y práctica.

### Fase 6: Síntesis y Consolidación
- **Skill principal**: `tuc-synthesizer`
- **Objetivo**: Integrar todo el ciclo en un reporte o actualización coherente.
- **Output**: Documento sintetizado listo para `tuc-builder`.

### Fase 7: Actualización de la Teoría
- **Skill principal**: `tuc-builder`
- **Objetivo**: Incorporar los resultados del ciclo al estado actual de TUC.
- **Output**: Estado actualizado de la teoría + registro de cambios.

---

## Rol del Orquestador

**Skill**: `tuc-research-orchestrator`

Este skill es responsable de:

- Decidir qué flujo ejecutar (completo o parcial).
- Activar los skills en el orden correcto.
- Manejar resultados intermedios y posibles reintentos.
- Registrar todo el ciclo en memoria persistente.
- Entregar el resultado final a `tuc-builder`.

---

## Ejemplos de Uso

### Ejemplo 1: Ciclo Completo de Investigación
```
tuc-research-orchestrator → ciclo completo
```
Ejecuta: Detección → Validación → Reflexión → Crítica → Síntesis → Actualización de TUC.

### Ejemplo 2: Solo Análisis y Reflexión
```
tuc-research-orchestrator → solo reflexión
```
Ejecuta: Detección → Validación → Reflexión (sin crítica ni actualización).

### Ejemplo 3: Validación de Campo
```
tuc-research-orchestrator → con feedback de campo
```
Ejecuta el flujo completo + activa `tuc-field-feedback`.

---

## Notas de Implementación

- El orquestador puede ejecutarse de forma manual o ser activado por `el-iluminador` / `ecosistema-orchestrator` cuando se detecte necesidad de investigación TUC.
- Todos los outputs intermedios deben quedar registrados en `blockchange-memoria`.
- El flujo es **iterativo**: después de actualizar `tuc-builder`, puede volver a empezar si se identifican nuevos gaps.

---

**Documento creado como parte del ecosistema de investigación TUC**  
**Integrado con**: `tuc-research-orchestrator`, `tuc-reflexion`, `tuc-builder` y `blockchange-memoria`