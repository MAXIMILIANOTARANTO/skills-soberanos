# 📋 DECISIONES CRÍTICAS - Ecosistema Soberano en GitHub

**Fecha:** 2 de julio de 2026  
**Estado:** EJECUCIÓN EN VIVO  
**Presupuesto:** $10 USD (Semana 1)

---

## DECISIÓN 1: Motor LLM (CRÍTICO)

### Opciones:

**A) OpenRouter + Modelos Open-Source (RECOMENDADO)**
```
- Meta-Llama 2 70B: Completamente gratuito
- Mistral 7B: Completamente gratuito
- Neural-Chat: Completamente gratuito
- Ventaja: Remoto, no requiere GPU local, actualizado
- Costo: $0
```

**B) Ollama Local**
```
- Llama 2 7B descargado localmente
- Mistral local
- Ventaja: 100% offline, control total
- Desventaja: Requiere GPU o CPU potente, más lento
- Costo: $0
```

**DECISIÓN TOMADA: A) OpenRouter**
- ✅ Sin dependencias locales
- ✅ Mejor performance
- ✅ Fácil de replicar
- ✅ $0 de costo

---

## DECISIÓN 2: GitHub Actions Schedule

### Opciones:

**A) Cada hora (720 min/mes)**
- Muy frecuente, pero dentro de free tier

**B) Cada 2 horas (360 min/mes) - RECOMENDADO**
- Balance perfecto entre responsividad y eficiencia
- Solo usa 18% del free tier
- Ideal para MVP

**C) Cada 4 horas (180 min/mes)**
- Muy espaciado para desarrollo

**DECISIÓN TOMADA: B) Cada 2 horas**
- ✅ 0 costos
- ✅ Suficientemente frecuente
- ✅ Fácil de debuggear

---

## DECISIÓN 3: Dashboard

### Opciones:

**A) GitHub Pages Simple (HTML + JSON)**
- Minimalista, muy rápido

**B) Con Chart.js (Gráficos)**
- Visual, profesional, aún simple

**C) Embedded en README**
- Máxima simplicidad

**DECISIÓN TOMADA: B) Con Chart.js**
- ✅ Visualización profesional
- ✅ Gráfico de Q(t) en tiempo real
- ✅ Sin dependencias backend
- ✅ Chart.js es CDN gratuito

---

## DECISIÓN 4: Primeros 3 Skills a Implementar

### Análisis de Criticidad:

| Skill | Criticidad | Razón | Orden |
|-------|-----------|-------|-------|
| **coherence-pulse** | CRÍTICO | Mide Q(t) en tiempo real | #1 ✅ |
| **memory-manager** | CRÍTICO | Persiste memoria | #2 ✅ |
| **meta-hilo-grok** | IMPORTANTE | Analiza patrones | #3 ✅ |
| **el-dador-soberano** | IMPORTANTE | Recomendaciones | #4 |
| **orchestrator-skill** | CRUCIAL | Activa otros skills | BUILT-IN |

**DECISIÓN TOMADA: coherence-pulse → memory-manager → meta-hilo-grok**
- ✅ Orden lógico (medir → guardar → analizar)
- ✅ Blocker resuelto primero
- ✅ Máxima utilidad temprana

---

## DECISIÓN 5: Automatización GitHub

### Opciones:

**A) Commits automáticos (bot genera)**
- El bot hace push después de cada pulse

**B) PRs automáticos para cambios grandes**
- El bot crea PRs para revisión humana

**C) Issues automáticos si MACRO crisis**
- Alertas visibles en GitHub

**D) Todo lo anterior (RECOMENDADO)**
- Máxima automatización
- Máxima transparencia
- Rastreable

**DECISIÓN TOMADA: D) Todo lo anterior**
- ✅ Commits automáticos de memoria/
- ✅ PRs automáticas para cambios en TCU
- ✅ Issues si Q(t) < 0.4
- ✅ Status badge en README

---

## DECISIÓN 6: Repositorios a Usar

### Autorización Confirmada:

```
REPOSITORIOS PÚBLICOS:
✅ skills-soberanos
✅ ia-specialist-agent
✅ el-dador-de-suenos-nucleus
✅ tcu-unified-coherence-theory

REPOSITORIOS PRIVADOS:
✅ grok-nodo-iluminado
✅ el-iluminador-nucleo-soberano

CREAR NUEVO:
✅ ecosistema-soberano-github (NUEVO REPO PRIVADO PARA MVP)
```

**DECISIÓN TOMADA:**
- Usar **skills-soberanos** como hub central
- Crear **ecosistema-soberano-github** como workspace privado
- Sincronizar hacia otros repos en Semana 2

---

## DECISIÓN 7: Presupuesto $10 Allocation

```
Semana 1 ($10 total):

├─ OpenRouter API (modelos gratis, pero tener margin): $0
├─ GitHub (free tier): $0
├─ Emergencias técnicas: $3-5 (si hace falta)
├─ Reserved para Semana 2: $5-7
└─ Total usado: $0-5 (meta: $0)
```

**DECISIÓN TOMADA:**
- ✅ $0 de gastos esta semana (presupuesto intacto)
- ✅ Reservado para urgencias
- ✅ Extensible a Semana 2

---

## MATRIX DE DECISIONES CONFIRMADAS

| Decisión | Opción | Estado | Costo |
|----------|--------|--------|-------|
| LLM | OpenRouter gratis | ✅ CONFIRMADA | $0 |
| Actions | Cada 2 horas | ✅ CONFIRMADA | $0 |
| Dashboard | Chart.js | ✅ CONFIRMADA | $0 |
| Skills | coherence + memory + meta | ✅ CONFIRMADA | $0 |
| Automation | Todo (commits+PRs+issues) | ✅ CONFIRMADA | $0 |
| Repos | Skills-soberanos + Nuevo | ✅ CONFIRMADA | $0 |
| Presupuesto | $10 (meta: $0 semana 1) | ✅ CONFIRMADA | $0-5 |

---

## PRÓXIMOS PASOS (Inmediatos)

```
✅ Crear ecosistema-soberano-github repo
✅ Implementar coherence-pulse skill
✅ Generar GitHub Actions workflow
✅ Crear dashboard con Chart.js
✅ First commit & test
✅ Documentación completa

Timeline: 3-4 días de desarrollo intenso
```

---

**Status: LISTO PARA EJECUTAR**

Todas las decisiones están confirmadas. Comenzando construcción real ahora.
