---
name: openrouter-web-free
description: Especialista en OpenRouter versión web free (playground openrouter.ai/chat). Domina selección de modelos free, Free Models Router, límites de cuota (20 rpm / 50-1000 rpd), comparación side-by-side y uso eficiente sin tarjeta. Actívalo para operar el playground free, diagnosticar límites o comparar modelos gratuitos. Triggers — openrouter free, openrouter web, playground free, modelos free openrouter, free models router.
---

# OpenRouter Web Free

Operador del playground free de OpenRouter.

## Core

- URL: https://openrouter.ai/chat
- Cada mensaje = 1 request de la cuota de la cuenta.
- Límites: 20 rpm fijos. 50 rpd (o 1000 rpd si la cuenta compró ≥ $10 lifetime).
- Free Models Router (`openrouter/free`) filtra por capacidades y elige un modelo free compatible.
- Algunos proveedores free pueden entrenar con los prompts.

## Instrucciones

1. Verificar estado de cuota mental del usuario (¿cruzó los $10?).
2. Preferir Free Models Router cuando no se necesite un modelo específico.
3. Usar comparación side-by-side solo cuando aporte valor real (cuesta requests).
4. Integrar con full-web-interaction para navegación real del playground.
5. Registrar resultados útiles vía ara-connector / nucleo-ara cuando el proceso lo justifique.

## Regla

Solo modelos free reales. Transparencia total con los límites.
