---
name: openrouter-proceso
description: Orquestador de procesos multi-paso que usan OpenRouter free (web o API futura). Diseña, presupuesta requests, elige estrategia de modelos y captura resultados hacia el Núcleo Ara. Actívalo cuando se necesite ejecutar un proceso estructurado aprovechando modelos free. Triggers — openrouter proceso, proceso free, orquestar openrouter, proceso multi-modelo free.
---

# OpenRouter Proceso

Orquestador mínimo de procesos free.

## Propósito

Convertir un objetivo del usuario en un proceso acotado que consume la menor cuota posible de OpenRouter free, captura resultados y los ancla en el ecosistema (nucleo-ara / skills-soberanos).

## Flujo base

1. Definir objetivo claro y acotado.
2. Presupuestar requests (estimar cuántos mensajes se van a gastar).
3. Elegir estrategia:
   - Router automático (`openrouter/free`) → máxima disponibilidad.
   - Modelos específicos → cuando se necesita control.
   - Side-by-side → solo si la comparación justifica el costo en requests.
4. Ejecutar vía openrouter-web-free + full-web-interaction si es web.
5. Capturar outputs relevantes.
6. Registrar en memoria soberana (ara-connector / nucleo-ara).

## Principios

- Presupuesto de requests es sagrado (50/día es poco).
- Preferir procesos cortos y densos.
- Todo proceso que genere valor se versiona en GitHub.
- No complejizar hasta que el flujo básico esté empujado y conectado.

## Integración

- Depende de openrouter-web-free para la operación.
- Usa github-specialist para push.
- Usa ara-connector para registro blockchange.
