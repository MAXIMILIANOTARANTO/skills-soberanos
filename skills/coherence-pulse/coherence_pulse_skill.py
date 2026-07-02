"""
Coherence Pulse Skill — Primer skill operativo del ecosistema
Ejecuta medición de Q(t) cada pulse automático.

Responsabilidades:
- Medir coherencia actual (Q(t))
- Detectar crisis MACRO vs SHOCK
- Registrar tendencias
- Recomendar acciones
- Trigger poda adaptativa si necesario
"""

from core.skill_base import Skill
from core.coherence_meter import QuantitativeCoherenceMeter
from datetime import datetime
from typing import Dict, Any, Optional


class CoherencePulseSkill(Skill):
    """
    Skill técnico crítico que mide la coherencia del ecosistema en tiempo real.
    Se ejecuta en CADA pulse automáticamente.
    
    Atributos especiales:
    - is_critical = True (nunca se poda)
    - requires_llm = False (puro cálculo)
    - impact_on_q = 0.0 (no impacta Q, solo lo mide)
    """
    
    def __init__(self):
        super().__init__()
        self.name = "coherence-pulse"
        self.purpose = "Medir coherencia del ecosistema en tiempo real"
        self.version = "1.0"
        self.requires_llm = False
        self.resonance_keywords = [
            "coherencia", "q(t)", "medir", "pulse", "estado", 
            "análisis", "sincronización", "estabilidad"
        ]
        self.impact_on_q = 0.0  # No impacta, solo mide
        self.is_critical = True  # NUNCA se poda
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecutar medición de coherencia.
        
        Context requerido:
        - memory: MemoryGitHubManager (para cargar historial)
        - coherence_meter: QuantitativeCoherenceMeter (para calcular Q)
        
        Returns:
        Dict con:
        - q_value: Coherencia actual 0.0-1.0
        - components: Desglose de cada métrica
        - crisis: Detección de crisis
        - trend: Tendencia de últimos 7 días
        - recommendations: Acciones recomendadas
        """
        
        try:
            # Extraer componentes del contexto
            memory = context.get("memory")
            coherence_meter = context.get("coherence_meter")
            
            if not coherence_meter:
                return {
                    "status": "error",
                    "error": "CoherenceMeter not available in context",
                    "q_impact": 0.0
                }
            
            timestamp_start = datetime.utcnow().isoformat() + "Z"
            
            # PASO 1: Calcular Q(t) actual
            q_result = coherence_meter.calculate_q(timestamp=timestamp_start)
            
            # PASO 2: Detectar crisis
            macro_crisis = coherence_meter.detect_macro_crisis()
            shock_crisis = coherence_meter.detect_shock_crisis()
            
            # PASO 3: Analizar tendencia
            trend = coherence_meter.get_trend_summary(days_back=7)
            
            # PASO 4: Generar recomendaciones
            recommendations = self._generate_recommendations(
                q_result=q_result,
                macro_crisis=macro_crisis,
                shock_crisis=shock_crisis,
                trend=trend
            )
            
            # PASO 5: Preparar reporte
            result = {
                "status": "success",
                "timestamp": timestamp_start,
                "q_value": q_result["q_value"],
                "q_status": q_result["status"],
                "components": q_result["components"],
                "crisis": {
                    "macro_detected": macro_crisis.get("crisis_detected", False),
                    "shock_detected": shock_crisis.get("shock_detected", False),
                    "severity": max(
                        macro_crisis.get("severity", 0),
                        shock_crisis.get("severity", 0)
                    )
                },
                "trend_7days": trend,
                "recommendations": recommendations,
                "action_required": len(recommendations) > 0,
                "q_impact": 0.0  # No impacta
            }
            
            # Registrar ejecución exitosa
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
    
    def _generate_recommendations(self, 
                                  q_result: Dict,
                                  macro_crisis: Dict,
                                  shock_crisis: Dict,
                                  trend: Dict) -> list:
        """
        Generar recomendaciones de acciones basadas en Q(t) y crisis.
        """
        recommendations = []
        q_value = q_result["q_value"]
        
        # Recomendación 1: Crisis MACRO
        if macro_crisis.get("crisis_detected"):
            recommendations.append({
                "priority": "CRITICAL",
                "action": "trigger_adaptive_poda",
                "reason": f"MACRO crisis detected - Q declining {macro_crisis.get('avg_daily_decline'):.3f} per day",
                "actions": [
                    "🔴 Pause non-critical skills immediately",
                    "🔴 Clear memory of low-quality entries",
                    "🔴 Reset skill activation weights",
                    "🔴 Create GitHub Issue for manual review"
                ]
            })
        
        # Recomendación 2: Crisis SHOCK
        elif shock_crisis.get("shock_detected"):
            recommendations.append({
                "priority": "HIGH",
                "action": "investigate_last_skill",
                "reason": f"SHOCK detected - Q dropped {shock_crisis.get('severity'):.1%}",
                "action": "Check logs of last executed skill for errors"
            })
        
        # Recomendación 3: Q muy bajo
        if q_value < 0.5:
            recommendations.append({
                "priority": "HIGH",
                "action": "activate_recovery_mode",
                "reason": f"Coherence critically low (Q={q_value:.3f})",
                "actions": [
                    "Activate only critical skills",
                    "Review memory for corrupted entries",
                    "Verify skill health scores"
                ]
            })
        
        # Recomendación 4: Q bajo pero no crítico
        elif q_value < 0.65:
            recommendations.append({
                "priority": "MEDIUM",
                "action": "review_skill_health",
                "reason": f"Coherence warning (Q={q_value:.3f})",
                "actions": [
                    "Audit poorly performing skills",
                    "Consider temporary poda of low-resonance skills",
                    "Verify memory integrity"
                ]
            })
        
        # Recomendación 5: Tendencia negativa
        if trend.get("net_change", 0) < -0.1:
            recommendations.append({
                "priority": "MEDIUM",
                "action": "investigate_trend",
                "reason": f"Q declining over time (net change: {trend.get('net_change'):.3f})",
                "actions": [
                    "Analyze which skills are causing degradation",
                    "Check for memory corruption",
                    "Review skill execution logs"
                ]
            })
        
        # Recomendación 6: Oportunidad de mejora
        if q_value > 0.8 and len(recommendations) == 0:
            recommendations.append({
                "priority": "LOW",
                "action": "optimal_mode_active",
                "reason": f"Coherence optimal (Q={q_value:.3f})",
                "actions": [
                    "✅ System is coherent and responsive",
                    "Consider enabling experimental features",
                    "Monitor for sustainability"
                ]
            })
        
        return recommendations
    
    def get_resonance_score(self, intent: str, intent_embedding=None) -> float:
        """
        Coherence Pulse siempre tiene alta resonancia porque mide estado.
        Es meta-skill que debería ejecutarse en casi todos los pulses.
        """
        # Base: keywords
        base_score = super().get_resonance_score(intent, intent_embedding)
        
        # Bonus: siempre relevante (es meta-skill)
        return min(1.0, base_score + 0.3)


# === FACTORY ===

def create_coherence_pulse_skill() -> CoherencePulseSkill:
    """Factory para crear CoherencePulseSkill"""
    return CoherencePulseSkill()


if __name__ == "__main__":
    print("Coherence Pulse Skill - Test mode")
    print("Usa esta clase en core/orchestrator_engine.py")
    print("""
    Ejemplo:
    
    from skills.coherence_pulse.coherence_pulse_skill import CoherencePulseSkill
    from core.coherence_meter import QuantitativeCoherenceMeter
    from core.memory_github_manager import MemoryGitHubManager
    
    # Crear skill
    skill = CoherencePulseSkill()
    
    # Crear contexto
    context = {
        "coherence_meter": QuantitativeCoherenceMeter(memory),
        "memory": memory
    }
    
    # Ejecutar
    result = skill.execute(context)
    
    print(f"Q(t) = {result['q_value']}")
    print(f"Recommendations: {result['recommendations']}")
    """)
