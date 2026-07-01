"""
Orchestrator Engine v2 — Resonance Evaluator + Coherence Router
Orquestador inteligente que evalúa resonancia y decide ejecución de skills.

Flujo:
1. Input (intención del usuario o pulse automático)
2. Resonance Evaluator → calcula scores con todos los skills
3. Coherence Router → decide cuáles ejecutar según Q(t)
4. Execution → corre skills en paralelo/secuencial
5. Registry → guarda resultados en memoria
"""

from typing import Dict, Any, List, Tuple, Optional
import json
from datetime import datetime
from core.skill_base import Skill
from core.coherence_router import CoherenceRouter


class OrchestratorEngine:
    """
    Motor de orquestación que decide qué skills activar y ejecutar.
    Implementa lógica de resonancia + coherencia de TCU.
    """
    
    def __init__(self, 
                 skills: List[Skill], 
                 llm_engine=None, 
                 memory_manager=None,
                 coherence_meter=None):
        """
        Args:
            skills: Lista de skills disponibles
            llm_engine: EcosystemLLM instance (opcional)
            memory_manager: MemoryGitHubManager instance (opcional)
            coherence_meter: QuantitativeCoherenceMeter instance (opcional)
        """
        self.skills = skills
        self.llm_engine = llm_engine
        self.memory_manager = memory_manager
        self.coherence_meter = coherence_meter
        self.router = CoherenceRouter()
        
        self.min_resonance_threshold = 0.45
        self.execution_log = []
    
    def evaluate_resonance(self, intent: str) -> List[Tuple[Skill, float]]:
        """
        Paso 1: Evalúa resonancia de todos los skills con la intención.
        
        Args:
            intent: Intención/input del usuario o descripción del pulse
        
        Returns:
            Lista de (skill, score) ordenada por resonancia descendente
        """
        scores = []
        
        for skill in self.skills:
            score = skill.get_resonance_score(intent)
            scores.append((skill, score))
        
        # Ordenar de mayor a menor resonancia
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores
    
    def route_and_execute(self, 
                         intent: str, 
                         context: Optional[Dict[str, Any]] = None,
                         dry_run: bool = False) -> Dict[str, Any]:
        """
        Paso principal: Evalúa resonancia → Elige skills → Ejecuta → Registra.
        
        Args:
            intent: Input/intención
            context: Contexto adicional (memory, llm_engine, coherence_meter, etc)
            dry_run: Si True, no guarda en memoria
        
        Returns:
            Dict con resultados de ejecución
        """
        
        # Construir contexto si no se proporciona
        if not context:
            context = {}
        
        # Inyectar componentes en contexto
        context["llm_engine"] = self.llm_engine
        context["memory"] = self.memory_manager
        context["coherence_meter"] = self.coherence_meter
        context["current_q"] = context.get("current_q", 0.7)  # Default
        
        timestamp_start = datetime.utcnow().isoformat() + "Z"
        
        # PASO 1: Evaluar resonancia
        resonance_scores = self.evaluate_resonance(intent)
        
        # PASO 2: Filtrar por threshold mínimo
        above_threshold = [
            (skill, score) for skill, score in resonance_scores 
            if score >= self.min_resonance_threshold
        ]
        
        # Si no hay skills sobre threshold, usar el top
        if not above_threshold and resonance_scores:
            above_threshold = [resonance_scores[0]]
        
        # PASO 3: Coherence Router decide cuáles ejecutar
        current_q = context.get("current_q", 0.7)
        skills_to_execute = self.router.route(above_threshold, current_q)
        
        # PASO 4: Ejecutar skills
        execution_results = []
        total_q_impact = 0.0
        errors = []
        
        for skill in skills_to_execute:
            try:
                result = skill.execute(context)
                
                execution_results.append({
                    "skill": skill.name,
                    "status": result.get("status", "unknown"),
                    "result": result,
                    "health_after": skill.get_health_score()
                })
                
                total_q_impact += result.get("q_impact", 0)
                
            except Exception as e:
                error_msg = str(e)
                errors.append({
                    "skill": skill.name,
                    "error": error_msg
                })
                execution_results.append({
                    "skill": skill.name,
                    "status": "error",
                    "error": error_msg
                })
        
        # PASO 5: Preparar respuesta
        timestamp_end = datetime.utcnow().isoformat() + "Z"
        
        response = {
            "timestamp": timestamp_start,
            "intent": intent[:200],  # Limitar tamaño
            "resonance_scores": [
                {
                    "skill": s.name,
                    "resonance": round(score, 3),
                    "health": round(s.get_health_score(), 3)
                }
                for s, score in resonance_scores[:10]
            ],
            "activated_skills": [s.name for s in skills_to_execute],
            "execution_results": execution_results,
            "q_impact_total": round(total_q_impact, 3),
            "coherence_router_mode": self.router.poda_history[-1]["mode"] if self.router.poda_history else "UNKNOWN",
            "errors": errors if errors else None,
            "execution_time_ms": 0  # Calcular luego
        }
        
        # PASO 6: Guardar en memory (si no es dry-run)
        if not dry_run and self.memory_manager:
            try:
                previous_hash = self.memory_manager.get_last_hash()
                self.memory_manager.save_conversation(intent, response, previous_hash)
            except Exception as e:
                response["memory_save_error"] = str(e)
        
        # Guardar en log local
        self.execution_log.append(response)
        
        return response
    
    def get_execution_summary(self, last_n: int = 5) -> Dict[str, Any]:
        """Resumen de últimas N ejecuciones"""
        recent = self.execution_log[-last_n:]
        
        avg_q_impact = sum(r.get("q_impact_total", 0) for r in recent) / len(recent) if recent else 0
        error_count = sum(1 for r in recent if r.get("errors"))
        
        return {
            "executions_total": len(self.execution_log),
            "recent_executions": len(recent),
            "avg_q_impact": round(avg_q_impact, 3),
            "error_rate": round(error_count / len(recent), 2) if recent else 0.0,
            "recent_logs": [
                {
                    "timestamp": r["timestamp"],
                    "activated_count": len(r.get("activated_skills", [])),
                    "has_errors": bool(r.get("errors"))
                }
                for r in recent
            ]
        }
    
    def analyze_skills_health(self) -> Dict[str, Any]:
        """Análisis de salud de todos los skills"""
        return {
            "total_skills": len(self.skills),
            "healthy_count": sum(1 for s in self.skills if s.is_healthy()),
            "critical_skills": sum(1 for s in self.skills if s.is_critical),
            "skills_detail": [
                {
                    "name": s.name,
                    "health": round(s.get_health_score(), 3),
                    "executions": s.execution_count,
                    "success_rate": round(s.success_count / max(1, s.execution_count), 2),
                    "impact_on_q": s.impact_on_q
                }
                for s in self.skills
            ]
        }


# === FACTORY ===

def create_orchestrator(skills: List[Skill], llm_engine=None, memory_manager=None, coherence_meter=None) -> OrchestratorEngine:
    """Factory para crear OrchestratorEngine"""
    return OrchestratorEngine(skills, llm_engine, memory_manager, coherence_meter)
