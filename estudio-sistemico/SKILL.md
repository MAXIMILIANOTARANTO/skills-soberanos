---
name: estudio-sistemico
description: Skill de meta-estudio y construcción de sistemas de pensamiento. Genera arquitecturas de comprensión sobre un tema o gap detectado, y las persiste con estructura blockchange. Actívalo cuando aparezca conocimiento nuevo que deba integrarse de forma estructurada al ecosistema. Triggers — estudio sistémico, meta-estudio, construir mapa de comprensión, analizar sistema complejo, integrar conocimiento nuevo.
---

# Estudio Sistémico

Skill de meta-estudio y construcción de sistemas de pensamiento. Genera arquitecturas de comprensión y las guarda en memoria persistente con estructura blockchange.

## Flujo de Trabajo Estándar

1. Recibir un tema, gap de conocimiento o pregunta a estudiar.
2. Descomponer el tema en sus componentes y relaciones clave (mapa de comprensión).
3. Identificar qué partes ya están cubiertas por skills o documentos existentes, y qué es genuinamente nuevo.
4. Producir un "mapa de comprensión": resumen estructurado del tema, sus partes, y cómo se relaciona con el resto del ecosistema.
5. Persistir el mapa de comprensión vía `memoria-blockchange-persistente` para que quede disponible en estudios futuros.

## Integración con el Ecosistema

- `orquestador-soberano` → lo consulta cuando detecta conocimiento nuevo que integrar (paso 2 de su flujo estándar).
- `arquitecto-sistema` → puede solicitar un estudio sistémico antes de proponer cambios estructurales de alto impacto.
- `memoria-blockchange-persistente` → destino de persistencia de cada mapa de comprensión generado.
