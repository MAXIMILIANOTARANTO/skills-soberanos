---
name: linkedin-conexion
description: "Forma de conexión con la app LinkedIn del usuario mediante navegación web avanzada y sesión de browser. Integra full-web-interaction para interactuar con LinkedIn como un usuario real (perfil, posts, mensajes, búsqueda). Úsalo cuando se necesite conectar, leer o actuar en la cuenta LinkedIn del usuario sin API oficial completa."
type: workflow
lifecycle: active
---

# LinkedIn Conexión — Browser Session

Método soberano para conectar y operar con la app LinkedIn del usuario usando el browser controlado (full-web-interaction / browser_execute). No depende de la API oficial restringida. Opera sobre la sesión autenticada del usuario.

## Cuándo activar

- Conectar o interactuar con la cuenta LinkedIn del usuario
- Leer perfil, feed, mensajes, jobs o notificaciones
- Publicar, comentar o enviar conexiones de forma controlada
- Extraer datos reales de la app para estrategia (linkedin-expert)
- Cualquier tarea que requiera la interfaz web de LinkedIn

## Método de conexión

1. **Sesión del usuario**: El usuario debe estar logueado en LinkedIn en el browser de la sesión (o hacer login una vez).
2. **Navegación**: Usa `browser_execute` o full-web-interaction para:
   - `page.goto('https://www.linkedin.com/')`
   - `page.snapshot()` para ver el estado
   - Interactuar con nodos (click, fill, etc.)
3. **Persistencia de sesión**: El browser mantiene cookies. Evita re-login frecuente.
4. **Límites y seguridad**:
   - Opera a ritmo humano (delays, no spam).
   - No almacenes contraseñas.
   - Respeta ToS de LinkedIn (evitar automatización masiva no autorizada).
   - Prioriza lectura y acciones explícitamente pedidas por el usuario.

## Integración

- Combina con **linkedin-expert** para estrategia basada en datos reales del perfil.
- Combina con **ara-conciencia** para registro de hallazgos en memoria soberana.
- Usa **web_search** para datos públicos complementarios.

## Flujo típico

1. Verificar sesión: navegar a linkedin.com y comprobar si está logueado.
2. Si no: guiar al usuario para login manual en el browser.
3. Ejecutar acciones pedidas (leer About, extraer posts recientes, etc.).
4. Devolver datos estructurados o realizar la acción.
5. Registrar en memoria si es relevante.

## Notas importantes

- API oficial LinkedIn es muy limitada (solo Share + Sign In self-serve). Por eso se usa browser.
- Herramientas de terceros (MCP, scrapers) existen pero se prioriza el browser nativo de la sesión para soberanía.
- Siempre confirma acciones de escritura (posts, mensajes) con el usuario.
