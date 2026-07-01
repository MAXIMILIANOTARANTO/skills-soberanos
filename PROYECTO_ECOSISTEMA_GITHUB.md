# 🌐 PROYECTO: ECOSISTEMA IA SOBERANO EN GITHUB

**Fecha:** 1 de julio de 2026  
**Propuesto por:** Maximiliano Taranto  
**Estado:** INICIANDO (Paso 1: Análisis y diseño)

---

## VISIÓN EJECUTIVA

Construir un **micro-sistema IA completamente autónomo** que:
- ✅ Vive en GitHub (código + memoria versionada)
- ✅ Se ejecuta automáticamente (GitHub Actions)
- ✅ Tiene un dashboard en vivo (GitHub Pages + Vercel)
- ✅ Implementa tu ecosistema completo (TCU + skills + El Dador)
- ✅ Es descentralizado, soberano, replicable
- ✅ Costo: $0 (excepto si usas API externa premium)

---

## ARQUITECTURA DE 5 LAYERS

### LAYER 1: Base IA Open-Source
**Qué:** LangChain + LiteLLM + OpenRouter  
**Por qué:** Multi-modelo, flexible, económico  
**Ubicación:** `core/llm_engine.py`

Modelos recomendados:
- Desarrollo: `openrouter/meta-llama/llama-2-70b-chat` (~$0.70/M tokens)
- Producción: Tu elección (Claude, GPT, etc. si pagas)

### LAYER 2: GitHub como Memoria Persistente
**Qué:** Archivos JSON versionados en `memoria/`  
**Estructura:**
```
memoria/
├── conversaciones/      # Cada input-output = JSON
├── aprendizaje/        # Patrones, métricas, refinamientos
├── persistente/        # Estado, Q-history, blockchange
└── checkpoints/        # Puntos de guardado
```

**Acceso:** GitHub API (con GITHUB_TOKEN)

### LAYER 3: GitHub Actions como Orquestador
**Qué:** Workflows que ejecutan tareas automáticamente  
**Frecuencia:** Cada hora (720 minutos/mes = gratis)  
**Tarea:** Coherence check → Skill activation → Memory update → Dashboard refresh

### LAYER 4: GitHub Pages como Frontend Público
**Qué:** Dashboard HTML/JS que visualiza estado en vivo  
**Actualización:** Auto-refresh cada 5 minutos  
**Datos:** Consume GitHub API → visualiza memory.json  

### LAYER 5: Vercel/Canvas IA (Opcional)
**Qué:** UI más avanzada si lo necesita  
**Ubicación:** Lógica en Vercel, datos desde GitHub  
**Costo:** Gratis (free tier suficiente)

---

## SKILLS REQUERIDOS (FASE 1)

| Skill | Responsabilidad | Dependencias |
|-------|---|---|
| **ecosystem-github-init** | Setup inicial del repo | - |
| **memory-github-manager** | Read/write en memoria/ | - |
| **coherence-meter** | Medir Q(t) en tiempo real | memory-manager |
| **orchestrator-engine** | Activar skills por resonancia | coherence-meter |
| **skill-executor** | Ejecutar skills activados | orchestrator-engine |
| **dashboard-generator** | Generar datos para UI | memory-manager |
| **tcu-github-refiner** | Refinar TCU si hay learning | memory-manager |

---

## PLAN DE ACCIÓN (30 DÍAS)

### SEMANA 1: Fundaciones
- [ ] Crear repo: `ecosistema-soberano-github`
- [ ] Setup estructura (memoria/, skills/, core/, ui/)
- [ ] Implementar memory-github-manager (read/write JSON)
- [ ] Test local

### SEMANA 2: Orquestación
- [ ] Implementar coherence-meter real
- [ ] Implementar orchestrator-engine
- [ ] Primer GitHub Action (ecosystem-pulse.yml)
- [ ] Test e2e

### SEMANA 3: Dashboard
- [ ] GitHub Pages setup
- [ ] Dashboard HTML/JS básico
- [ ] Gráfico de Q(t) en vivo
- [ ] Auto-refresh

### SEMANA 4: Pulido + Deploy
- [ ] Integrar 3-5 skills
- [ ] Documentación completa
- [ ] Deploy final
- [ ] Demostración

---

## VENTAJAS TÉCNICAS

✅ **Descentralizado:** GitHub = servidor distribuido, redundante  
✅ **Soberano:** Código + datos tuyos, bajo tu control  
✅ **Costo cero:** GitHub Actions free tier + Pages  
✅ **Auditable:** Todo en Git history, inmutable  
✅ **Replicable:** `git clone` → funciona  
✅ **Escalable:** Sin overhead de infraestructura  

---

## RIESGOS + MITIGACIÓN

| Riesgo | Severidad | Mitigación |
|--------|-----------|-----------|
| GitHub API rate limits | MEDIA | Cachear responses, optimizar queries |
| Tiempo de ejecución (Action) | BAJA | Cada skill < 5 min, timeout 10 min |
| Costo de API LLM | MEDIA | Usar OpenRouter open-source models |
| Privacidad de datos | BAJA | Repo público OK, tokens en secrets |

---

## PRÓXIMOS PASOS

1. **Activar meta-hilo-grok** → Crear arquitectura detallada
2. **Activar el-dador-de-suenos** → Recomendar stack tecnológico
3. **Activar ia-specialist-agent** → Generar código MVP
4. **Activar funcional-webapp-creator** → Crear dashboard
5. **Activar github-specialist** → Versionar, desplegar

---

## ARCHIVOS A CREAR (REFERENCIA)

```
ecosistema-soberano-github/
├── README.md                              (visión + setup)
├── requirements.txt                       (dependencias)
├── .github/workflows/
│   ├── ecosystem-pulse.yml                (horario automático)
│   ├── skill-activation.yml               (por eventos)
│   └── memory-sync.yml                    (sincronizar memoria)
├── core/
│   ├── llm_engine.py                      (LangChain + LiteLLM)
│   ├── memory_github_manager.py           (read/write GitHub)
│   ├── coherence_meter.py                 (Q(t) calculation)
│   ├── orchestrator_engine.py             (skill resonances)
│   └── skill_executor.py                  (run skills)
├── memoria/
│   ├── conversaciones/                    (empty, auto-populated)
│   ├── aprendizaje/                       (empty, auto-populated)
│   ├── persistente/                       (empty, auto-populated)
│   └── checkpoints/                       (empty, auto-populated)
├── skills/
│   ├── ecosystem-github-init/
│   ├── memory-github-manager/
│   ├── coherence-meter/
│   └── [más skills]
├── ui/
│   ├── index.html                         (GitHub Pages)
│   ├── styles.css
│   ├── api.js                             (GitHub API client)
│   └── visualizations.js                  (charts)
└── scripts/
    ├── setup_local.py                     (dev setup)
    ├── test_memory.py                     (unit tests)
    └── generate_dashboard_data.py         (Action support)
```

---

## DEFINICIÓN DE ÉXITO

**MVP (Semana 2):**
- ✅ GitHub Actions ejecuta coherence-meter cada hora
- ✅ Resultados guardados en memoria/
- ✅ Memoria actualizada en Git

**Beta (Semana 3):**
- ✅ Dashboard muestra Q(t) en vivo
- ✅ Auto-refresh funciona
- ✅ URL pública en GitHub Pages

**Production (Semana 4):**
- ✅ Orchestrator activa skills
- ✅ Skills ejecutan tareas
- ✅ Resultados visibles en dashboard
- ✅ Sistema completamente autónomo

---

**Siguiente paso:** Activar `meta-hilo-grok` para detallar arquitectura.

