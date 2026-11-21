---
name: ezmaker-img2img-connector
description: Conector para EzMaker.ai Image-to-Image como fallback de generación y consistencia de personajes (Valentina/Naty). Actívalo cuando Grok Imagine tenga límites de créditos, necesites image-to-image gratuito sin login, multi-ref fusion o variaciones rápidas de outfit manteniendo rostro y cuerpo. Integra full-web-interaction + character bibles de Valentina y Naty. Triggers — ezmaker, image to image, fallback imagen, usa ezmaker, img2img externo, genera con ezmaker.
---

# EzMaker Img2Img Connector

## Overview
Wrapper soberano para operar https://ezmaker.ai/image-to-image/ como capa de respaldo cuando Grok Imagine esté limitado. Prioriza consistencia de Valentina (blanca/cream) y Naty (negra) usando referencias bloqueadas y prompts del character bible.

## Instrucciones

1. **Activación prioritaria**
   - Solo usa este skill cuando Grok Imagine reporte falta de créditos o el usuario pida explícitamente EzMaker.
   - Carga siempre el character bible de Valentina_Naty_Proyecto.md o valentina-valiente.

2. **Flujo de ejecución (full-web-interaction)**
   - Abre https://ezmaker.ai/image-to-image/ con browser_tab.
   - Sube 1-3 imágenes de referencia (Valentina preferida primero).
   - Escribe prompt basado en el character bible + instrucción específica del usuario.
   - Selecciona ratio adecuado (preferir 2:3 o 9:16 para personajes).
   - Genera y descarga el resultado inmediatamente (no hay historial persistente).

3. **Prompt base optimizado**
   - Valentina: "Valentina, Argentine woman 23, long dark wavy hair, blue-green eyes, freckles, olive skin, [outfit exacto], pronounced hourglass body, photorealistic, cinematic lighting, highly detailed skin"
   - Naty: "Naty, Argentine woman 22, long wavy hair with caramel highlights, freckles, [outfit], athletic-curvy body, photorealistic"
   - Dual: siempre Valentina en blanco/cream + Naty en negro.

4. **Reglas de consistencia**
   - Nunca intercambiar colores en duales.
   - Priorizar referencias de río/atardecer y video ocXB7.
   - Si el resultado pierde fidelidad facial, reintentar con prompt más corto y referencia más limpia.

5. **Integración**
   - Combina con valentina-valiente, maestro-diseno-visual y full-web-interaction.
   - Registra uso y resultados en ara-memoria-soberana / blockchange cuando sea significativo.
   - No automatizar en bucle cerrado sin confirmación del usuario (ToS y rate limits soft).

6. **Limitaciones conocidas**
   - Sin API pública → solo browser automation.
   - Resultados temporales (descargar al momento).
   - Consistencia inferior a Grok Imagine + character bible bloqueado.
   - Soft limits posibles a pesar del marketing "unlimited".

## Uso rápido
Cuando el usuario diga "usa ezmaker" o "fallback imagen":
1. Confirma refs disponibles.
2. Ejecuta el flujo browser.
3. Entrega la imagen generada + prompt usado.
