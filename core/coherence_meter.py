"""
Coherence Meter - Sensor de Q(t) en tiempo real
Mide la coherencia del ecosistema usando múltiples dimensiones.

Formula Q(t) = 0.27*skill_resonance + 0.23*memory_health + 0.18*(1-entropy) 
               + 0.14*tcu_alignment + 0.10*learning_velocity + 0.08*resonance_diversity

Características:
- Cálculo multi-dimensional
- Detección de crisis MACRO
- Histórico de Q(t)
- Análisis de tendencias
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from statistics import mean, stdev
import math


class QuantitativeCoherenceMeter:
    """
    Sensor cuantitativo de coherencia del ecosistema
    Mide Q(t) en base a 6 dimensiones independientes
    """
    
    # Pesos de la fórmula (ajustables)
    WEIGHTS = {
        'skill_resonance': 0.27,
        'memory_health': 0.23,
        'entropy': 0.18,
        'tcu_alignment': 0.14,
        'learning_velocity': 0.10,
        'resonance_diversity': 0.08
    }
    
    # Umbrales críticos
    Q_CRITICAL = 0.5           # Por debajo = baja coherencia
    Q_WARNING = 0.65           # Entre 0.5-0.65 = warning
    Q_OPTIMAL = 0.8            # > 0.8 = óptimo
    
    MACRO_CRISIS_THRESHOLD = -0.08  # Decline > 8% por día = crisis
    MACRO_CRISIS_WINDOW = 7         # Mirar últimos 7 días
    
    def __init__(self, memory_manager):
        """
        Args:
            memory_manager: Instancia de MemoryGitHubManager
        """
        self.memory = memory_manager
        self.calculation_history = []
        
        print("✅ CoherenceMeter inicializado")
    
    # === CÁLCULO PRINCIPAL ===
    
    def calculate_q(self, timestamp: Optional[str] = None) -> Dict:
        """
        Calcular Q(t) actual
        
        Args:
            timestamp: Timestamp override (default: ahora)
            
        Returns:
            Dict con Q y componentes individuales
        """
        if not timestamp:
            timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Calcular cada métrica
        skill_resonance = self._calculate_skill_resonance()
        memory_health = self._calculate_memory_health()
        entropy = self._calculate_entropy()
        tcu_alignment = self._calculate_tcu_alignment()
        learning_velocity = self._calculate_learning_velocity()
        resonance_diversity = self._calculate_resonance_diversity()
        
        # Fórmula ponderada
        q_value = (
            skill_resonance * self.WEIGHTS['skill_resonance'] +
            memory_health * self.WEIGHTS['memory_health'] +
            (1 - entropy) * self.WEIGHTS['entropy'] +
            tcu_alignment * self.WEIGHTS['tcu_alignment'] +
            learning_velocity * self.WEIGHTS['learning_velocity'] +
            resonance_diversity * self.WEIGHTS['resonance_diversity']
        )
        
        # Clampear a 0-1
        q_value = max(0.0, min(1.0, q_value))
        
        result = {
            "timestamp": timestamp,
            "q_value": round(q_value, 4),
            "components": {
                "skill_resonance": round(skill_resonance, 4),
                "memory_health": round(memory_health, 4),
                "entropy": round(entropy, 4),
                "tcu_alignment": round(tcu_alignment, 4),
                "learning_velocity": round(learning_velocity, 4),
                "resonance_diversity": round(resonance_diversity, 4)
            },
            "status": self._classify_coherence(q_value),
            "crisis_detected": False
        }
        
        # Guardar en historial
        self.calculation_history.append(result)
        
        return result
    
    # === MÉTRICAS INDIVIDUALES ===
    
    def _calculate_skill_resonance(self) -> float:
        """
        Qué tan bien resuenan los skills activados con la intención del usuario
        
        Basado en: promedio de resonance scores de últimas conversaciones
        Range: 0.0 - 1.0
        """
        memories = self.memory.load_memory(days_back=1)
        
        if not memories:
            return 0.5  # Default si no hay datos
        
        # Extraer resonance scores (asumiendo que están en response)
        resonance_scores = []
        for mem in memories:
            response = mem.get("response", {})
            if "resonance_scores" in response:
                scores = response["resonance_scores"].values()
                resonance_scores.extend(scores)
        
        if not resonance_scores:
            return 0.5
        
        # Promedio de scores
        avg_resonance = mean(resonance_scores)
        return min(1.0, max(0.0, avg_resonance))
    
    def _calculate_memory_health(self) -> float:
        """
        Qué tan saludable es la memoria (sin ruido, con learning consistente)
        
        Basado en: % conversaciones que resultaron en learning
        Range: 0.0 - 1.0
        """
        memories = self.memory.load_memory(days_back=7)
        
        if not memories:
            return 0.5
        
        # Contar conversaciones con learning
        with_learning = sum(1 for m in memories if m.get("learning"))
        
        health = with_learning / len(memories)
        return min(1.0, health)
    
    def _calculate_entropy(self) -> float:
        """
        Qué tan caótico es el sistema
        
        Basado en: varianza de Q-values recientes
        Range: 0.0 - 1.0 (donde 0 = muy consistente, 1 = muy caótico)
        """
        memories = self.memory.load_memory(days_back=1)
        
        if len(memories) < 2:
            return 0.3  # Default bajo si no hay suficientes datos
        
        q_values = [m.get("q_value", 0.5) for m in memories]
        
        # Calcular varianza
        try:
            variance = stdev(q_values)
            # Normalizar a 0-1 (máxima varianza = 1.0)
            entropy = min(1.0, variance)
        except:
            entropy = 0.3
        
        return entropy
    
    def _calculate_tcu_alignment(self) -> float:
        """
        Qué tan alineado está el sistema con TCU
        
        Basado en:
        - ¿Existe poda adaptativa activa?
        - ¿Existe kernel de decaimiento?
        - ¿El sistema reporta incertidumbre honestamente?
        
        Range: 0.0 - 1.0
        """
        # Estas son checks booleanas que se pueden implementar
        # Por ahora, placeholder que busca evidencia en memoria
        
        memories = self.memory.load_memory(days_back=7)
        
        if not memories:
            return 0.5
        
        alignment_score = 0.0
        
        # Check 1: Poda adaptativa (¿hay skills removidos?)
        has_poda = any("poda" in str(m.get("learning", {})).lower() for m in memories)
        alignment_score += 0.33 if has_poda else 0.0
        
        # Check 2: Kernel decay (¿hay evidencia de memory decay?)
        has_decay = any("decay" in str(m.get("learning", {})).lower() for m in memories)
        alignment_score += 0.33 if has_decay else 0.0
        
        # Check 3: Incertidumbre (¿sistema expresa uncertainty?)
        has_uncertainty = any(
            "uncertain" in str(m.get("response", {})).lower() or 
            "confidence" in str(m.get("response", {})).lower()
            for m in memories
        )
        alignment_score += 0.34 if has_uncertainty else 0.0
        
        return min(1.0, alignment_score)
    
    def _calculate_learning_velocity(self) -> float:
        """
        Velocidad de aprendizaje (nuevos patrones por unidad de tiempo)
        
        Basado en: ratio de learnings en última semana vs dos semanas atrás
        Range: 0.0 - 1.0
        """
        memories_week1 = self.memory.load_memory(days_back=7)
        memories_week2 = self.memory.load_memory(days_back=14)
        
        if not memories_week1 or not memories_week2:
            return 0.5
        
        learnings_week1 = sum(1 for m in memories_week1 if m.get("learning"))
        learnings_week2 = sum(1 for m in memories_week2 if m.get("learning"))
        
        if learnings_week2 == 0:
            velocity = 0.5
        else:
            # Ratio de learnings week1 vs week2
            velocity = min(1.0, (learnings_week1 / learnings_week2) * 0.5 + 0.25)
        
        return velocity
    
    def _calculate_resonance_diversity(self) -> float:
        """
        Diversidad de skills resonando (evita over-specialization)
        
        Basado en: cuántos skills diferentes se activaron en últimas conversaciones
        Range: 0.0 - 1.0
        """
        memories = self.memory.load_memory(days_back=7)
        
        if not memories:
            return 0.5
        
        # Recolectar todos los skills únicos
        unique_skills = set()
        for mem in memories:
            skills = mem.get("skills_activated", [])
            unique_skills.update(skills)
        
        # Si no hay skills, baja diversidad
        if not unique_skills:
            return 0.3
        
        # Normalizar: entre 1-10 skills = buen rango
        num_skills = len(unique_skills)
        
        if num_skills < 2:
            diversity = 0.3
        elif num_skills > 8:
            diversity = 0.9
        else:
            # Escalar linealmente 2-8 → 0.5-0.9
            diversity = 0.5 + (num_skills - 2) * (0.4 / 6)
        
        return min(1.0, diversity)
    
    # === CLASIFICACIÓN & DETECCIÓN DE CRISIS ===
    
    def _classify_coherence(self, q_value: float) -> str:
        """Clasificar nivel de coherencia"""
        if q_value < self.Q_CRITICAL:
            return "CRITICAL"
        elif q_value < self.Q_WARNING:
            return "WARNING"
        elif q_value >= self.Q_OPTIMAL:
            return "OPTIMAL"
        else:
            return "STABLE"
    
    def detect_macro_crisis(self, history_window_days: int = None) -> Dict:
        """
        Detectar si Q está bajando progresivamente (MACRO crisis)
        
        Una MACRO crisis es una pérdida GRADUAL de coherencia durante días,
        no un pico momentáneo.
        
        Args:
            history_window_days: Días a analizar (default: MACRO_CRISIS_WINDOW)
            
        Returns:
            Dict con detección y severidad
        """
        window = history_window_days or self.MACRO_CRISIS_WINDOW
        
        # Obtener histórico de Q
        q_history = self.memory.get_coherence_history(days_back=window)
        
        if len(q_history) < 3:
            return {"crisis_detected": False, "reason": "Insufficient data"}
        
        # Extraer valores Q
        q_values = [h["q_value"] for h in q_history]
        
        # Calcular trend (decline por día)
        daily_changes = []
        for i in range(len(q_values) - 1):
            change = q_values[i+1] - q_values[i]
            daily_changes.append(change)
        
        if not daily_changes:
            return {"crisis_detected": False, "reason": "No trend data"}
        
        avg_daily_change = mean(daily_changes)
        
        # Crisis si decline > threshold
        if avg_daily_change < self.MACRO_CRISIS_THRESHOLD:
            return {
                "crisis_detected": True,
                "type": "MACRO",
                "severity": abs(avg_daily_change),
                "avg_daily_decline": round(avg_daily_change, 4),
                "current_q": q_values[0],
                "recommendation": "Trigger adaptive poda immediately",
                "actions": [
                    "🔴 Pause non-critical skills",
                    "🔴 Clear low-quality memories",
                    "🔴 Reset skill activations",
                    "🔴 Create GitHub Issue for manual review"
                ]
            }
        
        return {"crisis_detected": False, "avg_daily_change": round(avg_daily_change, 4)}
    
    def detect_shock_crisis(self) -> Dict:
        """
        Detectar si hay un SHOCK (caída abrupta de Q en una conversación)
        
        SHOCK = error técnico, bug, falla puntual
        MACRO = degradación gradual
        """
        memories = self.memory.load_memory(days_back=1)
        
        if len(memories) < 2:
            return {"shock_detected": False}
        
        q_values = [m.get("q_value", 0.5) for m in memories[-5:]]  # Últimas 5
        
        # Detectar caídas abruptas
        for i in range(len(q_values) - 1):
            drop = q_values[i] - q_values[i+1]
            if drop > 0.25:  # Caída > 25%
                return {
                    "shock_detected": True,
                    "type": "SHOCK",
                    "severity": drop,
                    "recommendation": "Check last skill execution for errors"
                }
        
        return {"shock_detected": False}
    
    # === ANÁLISIS DE TENDENCIA ===
    
    def get_q_trend(self, days_back: int = 7) -> List[Tuple[str, float]]:
        """
        Obtener tendencia de Q(t) durante N días
        
        Returns:
            Lista de (timestamp, q_value) ordenada cronológicamente
        """
        q_history = self.memory.get_coherence_history(days_back=days_back)
        
        # Ordenar por timestamp (más antiguo primero)
        q_history_sorted = sorted(q_history, key=lambda x: x["timestamp"])
        
        return [(h["timestamp"], h["q_value"]) for h in q_history_sorted]
    
    def get_trend_summary(self, days_back: int = 7) -> Dict:
        """
        Resumen cuantitativo de tendencia
        """
        trend = self.get_q_trend(days_back=days_back)
        
        if not trend:
            return {"error": "No trend data"}
        
        q_values = [v for _, v in trend]
        
        return {
            "period_days": days_back,
            "num_measurements": len(q_values),
            "min_q": round(min(q_values), 4),
            "max_q": round(max(q_values), 4),
            "avg_q": round(mean(q_values), 4),
            "first_q": round(q_values[0], 4),
            "last_q": round(q_values[-1], 4),
            "net_change": round(q_values[-1] - q_values[0], 4),
            "trend": "📈 Mejorando" if q_values[-1] > q_values[0] else "📉 Degradando" if q_values[-1] < q_values[0] else "➡️ Estable"
        }
    
    # === REPORTE COMPLETO ===
    
    def generate_report(self) -> Dict:
        """
        Generar reporte completo del estado del ecosistema
        """
        q_current = self.calculate_q()
        macro_crisis = self.detect_macro_crisis()
        shock_crisis = self.detect_shock_crisis()
        trend = self.get_trend_summary(days_back=7)
        stats = self.memory.get_memory_stats()
        
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "current_state": q_current,
            "macro_crisis": macro_crisis,
            "shock_crisis": shock_crisis,
            "trend_7days": trend,
            "memory_stats": stats,
            "overall_assessment": self._generate_assessment(q_current, macro_crisis)
        }
    
    def _generate_assessment(self, q_current: Dict, macro_crisis: Dict) -> str:
        """Generar assessment textual"""
        status = q_current["status"]
        
        if macro_crisis.get("crisis_detected"):
            return f"🔴 MACRO CRISIS - System coherence declining. Q={q_current['q_value']}. Severity: {macro_crisis.get('severity'):.3f}"
        elif status == "CRITICAL":
            return f"⚠️ CRITICAL - System coherence very low (Q={q_current['q_value']}). Immediate intervention needed."
        elif status == "WARNING":
            return f"🟡 WARNING - System coherence degrading (Q={q_current['q_value']}). Monitor closely."
        elif status == "STABLE":
            return f"🟢 STABLE - System coherence healthy (Q={q_current['q_value']})."
        else:
            return f"🟢 OPTIMAL - System coherence excellent (Q={q_current['q_value']})."


# === FACTORY ===

def create_coherence_meter(memory_manager):
    """Factory para crear CoherenceMeter"""
    return QuantitativeCoherenceMeter(memory_manager)


if __name__ == "__main__":
    print("Coherence Meter - Test mode")
    print("Usa esta clase en core/orchestrator.py o scripts/run_pulse.py")
    
    # Ejemplo de uso
    print("""
    Ejemplo:
    
    from core.memory_github_manager import MemoryGitHubManager
    from core.coherence_meter import QuantitativeCoherenceMeter
    
    memory = MemoryGitHubManager(repo)
    meter = QuantitativeCoherenceMeter(memory)
    
    # Calcular Q(t)
    q_result = meter.calculate_q()
    print(f"Q(t) = {q_result['q_value']}")
    
    # Detectar crisis
    crisis = meter.detect_macro_crisis()
    if crisis["crisis_detected"]:
        print("Crisis detectada!")
    
    # Generar reporte
    report = meter.generate_report()
    print(json.dumps(report, indent=2))
    """)
