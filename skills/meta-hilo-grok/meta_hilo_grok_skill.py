"""
Meta-Hilo-Grok Skill — Análisis cognitivo de patrones del ecosistema
Tercer skill: analiza memoria, detecta patrones, genera insights.

Responsabilidades:
- Analizar tendencias de Q(t)
- Detectar patrones en activaciones de skills
- Generar recomendaciones estratégicas
- Proponer mejoras a TCU
- Identificar skills problematicos
"""

from core.skill_base import Skill
from datetime import datetime
from typing import Dict, Any, List, Optional


class MetaHiloGrokSkill(Skill):
    """
    Skill cognitivo de análisis profundo.
    
    Características:
    - requires_llm = True (usa LLM para análisis)
    - is_critical = False (puede podarse si crisis)
    - impact_on_q = 0.15 (impacto moderado en decisiones)
    """
    
    def __init__(self):
        super().__init__()
        self.name = "meta-hilo-grok"
        self.purpose = "Analizar patrones cognitivos del ecosistema y generar insights"
        self.version = "1.0"
        self.requires_llm = True
        self.resonance_keywords = [
            "analizar", "patrón", "meta", "grok", "insight", "estrategia",
            "tendencia", "predicción", "mejora", "evolución", "reflexión"
        ]
        self.impact_on_q = 0.15  # Impacto moderado
        self.is_critical = False  # Puede podarse
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecutar análisis metacognitivo del ecosistema.
        
        Context:
        - memory: MemoryGitHubManager (para cargar historial)
        - coherence_meter: Para acceder a Q(t)
        - llm_engine: Para análisis cognitivo
        - days_back: Cuántos días analizar (default: 7)
        
        Returns:
        Dict con:
        - patterns: Patrones detectados
        - insights: Análisis profundo
        - predictions: Predicciones
        - recommendations: Mejoras propuestas
        """
        
        try:
            memory = context.get("memory")
            coherence_meter = context.get("coherence_meter")
            llm_engine = context.get("llm_engine")
            days_back = context.get("days_back", 7)
            
            # Validación
            if not llm_engine:
                return {
                    "status": "error",
                    "error": "LLM engine not available",
                    "q_impact": 0.0
                }
            
            timestamp_start = datetime.utcnow().isoformat() + "Z"
            
            # PASO 1: Recolectar datos
            patterns = self._detect_patterns(memory, coherence_meter, days_back)
            
            # PASO 2: Análisis cognitivo vía LLM
            insights = self._generate_insights(llm_engine, patterns)
            
            # PASO 3: Predicciones
            predictions = self._generate_predictions(patterns, coherence_meter)
            
            # PASO 4: Recomendaciones
            recommendations = self._generate_recommendations(insights, predictions)
            
            # Resultado
            result = {
                "status": "success",
                "timestamp": timestamp_start,
                "analysis_depth": "meta-cognitive",
                "patterns": patterns,
                "insights": insights,
                "predictions": predictions,
                "recommendations": recommendations,
                "action_items": len(recommendations),
                "q_impact": 0.15
            }
            
            self.update_health(True, result)
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "q_impact": 0.0
            }
            self.update_health(False, error_result)
            return error_result
    
    def _detect_patterns(self, memory, coherence_meter, days_back: int) -> Dict:
        """Detectar patrones en memoria e historial de Q(t)"""
        
        patterns = {
            "time_period_days": days_back,
            "patterns_found": []
        }
        
        # Patrón 1: Tendencia de Q(t)
        if coherence_meter:
            try:
                trend = coherence_meter.get_trend_summary(days_back=days_back)
                
                if trend.get("net_change", 0) > 0.1:
                    patterns["patterns_found"].append({
                        "name": "improving_coherence",
                        "description": "Sistema mejorando gradualmente",
                        "strength": abs(trend.get("net_change", 0))
                    })
                elif trend.get("net_change", 0) < -0.1:
                    patterns["patterns_found"].append({
                        "name": "declining_coherence",
                        "description": "Sistema degradando",
                        "strength": abs(trend.get("net_change", 0))
                    })
            except:
                pass
        
        # Patrón 2: Memoria (si disponible)
        if memory:
            try:
                memories = memory.load_memory(days_back=days_back)
                
                if len(memories) > 10:
                    patterns["patterns_found"].append({
                        "name": "high_activity",
                        "description": f"Alta actividad: {len(memories)} conversaciones",
                        "strength": min(1.0, len(memories) / 50)
                    })
            except:
                pass
        
        return patterns
    
    def _generate_insights(self, llm_engine, patterns: Dict) -> str:
        """Generar insights cognitivos vía LLM"""
        
        prompt = f"""
Analiza estos patrones del ecosistema y genera 2-3 insights profundos:

Patrones detectados:
{patterns}

Genera insights que expliquen:
1. Por qué ocurren estos patrones
2. Qué significan para la coherencia del sistema
3. Cómo se relacionan con la autonomía del ecosistema

Responde brevemente, máximo 3 puntos.
"""
        
        try:
            insights = llm_engine.think(prompt, model_type="balanced")
            return insights
        except:
            return "No insights available (LLM error)"
    
    def _generate_predictions(self, patterns: Dict, coherence_meter) -> List[str]:
        """Generar predicciones sobre el futuro del sistema"""
        
        predictions = []
        
        patterns_found = patterns.get("patterns_found", [])
        
        # Predicción 1: Basada en tendencia
        for p in patterns_found:
            if p["name"] == "improving_coherence":
                predictions.append(
                    "🟢 Se espera que Q(t) continúe mejorando en próximas 24h"
                )
            elif p["name"] == "declining_coherence":
                predictions.append(
                    "🔴 Se espera degradación - trigger poda adaptativa recomendado"
                )
            elif p["name"] == "high_activity":
                predictions.append(
                    "📈 Alta actividad sostenida sugiere sistema robusto"
                )
        
        if not predictions:
            predictions.append("ℹ️  Datos insuficientes para predicciones")
        
        return predictions
    
    def _generate_recommendations(self, insights: str, predictions: List) -> List[Dict]:
        """Generar recomendaciones basadas en análisis"""
        
        recommendations = []
        
        # Recomendación genérica
        if insights and "mejor" in insights.lower():
            recommendations.append({
                "priority": "LOW",
                "action": "maintain_current_strategy",
                "reasoning": "Sistema está mejorando - mantener configuración actual"
            })
        elif insights and "degrad" in insights.lower():
            recommendations.append({
                "priority": "HIGH",
                "action": "review_skill_configuration",
                "reasoning": "Degradación detectada - revisar skills activos"
            })
        else:
            recommendations.append({
                "priority": "MEDIUM",
                "action": "monitor_trends",
                "reasoning": "Continuar monitoreo de patrones"
            })
        
        return recommendations


# === FACTORY ===

def create_meta_hilo_grok_skill() -> MetaHiloGrokSkill:
    """Factory para crear MetaHiloGrokSkill"""
    return MetaHiloGrokSkill()
