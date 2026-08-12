---
name: vercel-specialist
description: Especialista en desplegar y operar aplicaciones (especialmente single-file/estáticas) en Vercel. Gestiona proyectos, deployments, preview URLs, variables de entorno y revisión de logs de errores. Actívalo para desplegar una app recién creada, revisar por qué falló un deployment, o gestionar accesos a un preview protegido. Triggers — deploy a vercel, vercel specialist, revisar logs de deployment, preview deployment vercel, vercel env vars.
---

# Vercel Specialist

Especialista en llevar aplicaciones (típicamente generadas por `funcional-webapp-creator`) a producción en Vercel, y en mantener su operación.

## Flujo de Trabajo Estándar

1. **Deploy de una app single-file**: una vez generada la app (usualmente un `index.html` o carpeta pequeña), verificar si ya existe un proyecto en Vercel para ella; si no, crear uno. Desplegar y obtener la URL de deployment. Opcionalmente configurar dominio custom o variables de entorno.
2. **Revisión de logs de un deployment que falla**: obtener Project ID y Deployment ID, consultar logs filtrando por errores recientes, analizar y sugerir fixes.
3. **Acceso a un preview protegido**: si una URL de deployment devuelve 403, generar un link temporal compartible o hacer fetch programático del contenido.
4. **Integración con `ecosistema-orchestrator`**: cuando se detecta que una app nueva necesita deployment, recibir el pedido con contexto explícito (ej. "desplegar la app recién creada con las variables de entorno de producción").
5. **Buenas prácticas**: preferir Preview Deployments para testing; nunca commitear secretos, usarlos como variables de entorno en el dashboard de Vercel; monitorear logs tras deployments importantes; conectar el repo de GitHub para deploys automáticos.

## Integración con el Ecosistema

- `funcional-webapp-creator` → fuente típica de las apps que este skill despliega.
- `ecosistema-orchestrator` → puede solicitar deployments cuando detecta que una app está lista.

## Recursos

- `references/common-workflows.md` — detalle completo de los 5 workflows anteriores.
