# Estado Actual del Proyecto TUC (resumen vivo - junio 2026)

## Fortalezas Consolidadas

- **Taxonomía SHOCK / MACRO**: Separación estadística clara (p=0.007-0.016) entre crisis exógenas rápidas y deterioro macro gradual. Es uno de los hallazgos más sólidos.
- **Protocolo de validación E3 + E4**: IAAFT surrogates como test bloqueante de causalidad + walk-forward con embargo es metodológicamente robusto.
- **Enfoque de corroboración histórica**: Usar repositorios públicos ya existentes (Yahoo Finance, PhysioNet, PAGES2k, NOAA, etc.) en lugar de predecir futuro desconocido es una de las mejores decisiones del proyecto. Aumenta rigor y reproducibilidad.
- **Transparencia honesta**: El proyecto reconoce abiertamente limitaciones (n=3 para MACRO, AR1 ≈ Q pero no idéntico, ventana-dependencia de τ_m^field). Esto es valioso.

## Gaps Principales (priorizados)

1. **n pequeño para crisis MACRO** (crítico)
   - Solo 3 eventos identificados.
   - Necesita o bien más eventos históricos o validación out-of-sample robusta en período posterior.

2. **Validación en dominios no-financieros** (alto impacto)
   - EEG / seizures es el más prometedor y accesible (PhysioNet CHB-MIT ya existe).
   - Ecología (Peter Lake / Cascade Project) también accesible.
   - Si funciona en 2-3 dominios adicionales, el claim de "mecanismo plausiblemente universal" se fortalece enormemente.

3. **Cuantificación más allá de clasificación binaria**
   - Actualmente el sistema hace "detecta / no detecta".
   - Falta estimación de timing (cuándo) y magnitud aproximada del evento.

4. **Robustez de τ_m^field**
   - Muy sensible a elección de ventana.
   - Necesita o bien justificación teórica fuerte de la ventana elegida o método adaptativo (E2).

5. **Derivación / fundamentación de la ecuación maestra**
   - Sigue siendo fenomenológica.
   - Sería valioso explicitar claramente qué asunciones se hacen y qué no se deriva de microestructura.

## Estado de los Experimentos Clave

- **E3 (IAAFT Surrogates)**: Implementado y con resultados. Es el test más importante de causalidad vs artefacto.
- **E4 (Walk-forward)**: Implementado. Muestra robustez temporal.
- **E2 (Calibración W = 5τ_m)**: Resultados mixtos / marginales. No parece aportar ganancia significativa sobre W=21 fijo en los datos probados.
- **Corroboración histórica con repositorios públicos**: Muy bien conceptualizado, parcialmente ejecutado en finanzas. Debe expandirse a otros dominios.

## Recomendación de Prioridades Inmediatas (junio-julio 2026)

1. **Fortalecer falsabilidad** (out-of-sample + E3 completo en más eventos).
2. **Iniciar validación EEG** (PhysioNet CHB-MIT) — alto impacto si funciona.
3. **Formalizar el "TUC Reproducible Validation Protocol v1.0"** combinando E3 + E4 + corroboración histórica.
4. **Actualizar narrativa del paper**: Pasar de "predicción" a "corroboración histórica con datos públicos ya existentes".

Este estado debe actualizarse cada vez que se complete un experimento o se identifique un nuevo gap relevante.