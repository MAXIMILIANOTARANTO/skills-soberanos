# Conversation Knowledge Base Structure (para Meta-Hilo-Grok)

Este documento define cómo `meta-hilo-grok` debe estructurar y mantener el conocimiento persistente extraído de múltiples conversaciones a lo largo del tiempo.

## Objetivo
Construir un "mapa de conocimiento del usuario" que permita:
- Detectar patrones y temas recurrentes
- Recordar objetivos, decisiones y métodos creados en conversaciones anteriores
- Identificar gaps estructurales que se repiten
- Facilitar la creación de skills más precisos y alineados con la evolución real del usuario

## Estructura Recomendada de la Knowledge Base

### 1. Perfil del Usuario (actualizado continuamente)
- Objetivos principales y cómo han evolucionado
- Temas de mayor interés (TUC, apps funcionales, soberanía, mercados, creatividad, etc.)
- Estilo de trabajo preferido (iniciativa alta, iteración rápida, foco en deployment, etc.)
- Nivel de soberanía deseado

### 2. Historial de Proyectos y Decisiones
Por cada proyecto o línea de trabajo importante:
- Objetivo original
- Hitos clave y decisiones tomadas
- Skills utilizados y su efectividad
- Resultados obtenidos
- Lecciones aprendidas

### 3. Patrones Recurrentes
- Temas que aparecen en múltiples conversaciones
- Gaps que se repiten
- Skills que se solicitan o se crean frecuentemente
- Combinaciones de skills que funcionan bien juntas

### 4. Gaps y Oportunidades Detectadas
- Gaps identificados que aún no tienen skill dedicado
- Oportunidades de mejora en el ecosistema actual
- Skills candidatos a crear (con justificación)

### 5. Evolución del Ecosistema de Skills
- Skills creados y su propósito
- Cómo han mejorado el trabajo del usuario
- Dependencias y relaciones entre skills

## Cómo Mantener esta Knowledge Base

- Después de analizar cada hilo importante, extraer y registrar la información relevante en las secciones correspondientes.
- Usar `memoria-blockchange` o `blockchange-memoria` para versionar los cambios de forma trazable.
- Periódicamente (usando `ecosistema-orchestrator`), revisar y sintetizar la knowledge base para detectar patrones de alto nivel.
- Cuando se detecten patrones fuertes, proponer nuevos skills o mejoras estructurales.

Este enfoque permite que el sistema (Meta-Hilo-Grok + Ecosistema Orchestrator) se vuelva cada vez más preciso y proactivo en la evolución del ecosistema de skills del usuario.