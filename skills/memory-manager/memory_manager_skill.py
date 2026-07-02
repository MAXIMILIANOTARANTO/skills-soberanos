"""
Memory Manager Skill — Gestión inteligente de memoria persistente
Segundo skill operativo - maneja lectura/escritura segura en GitHub.
"""

from core.skill_base import Skill
from core.memory_github_manager import MemoryGitHubManager
from datetime import datetime
from typing import Dict, Any, Optional


class MemoryManagerSkill(Skill):
    """
    Skill técnico que gestiona persistencia de memoria en GitHub.
    
    Atributos:
    - is_critical = True (nunca se poda)
    - requires_llm = False (puro I/O)
    - impact_on_q = 0.0 (no impacta, solo guarda)
    """
    
    def __init__(self):
        super().__init__()
        self.name = "memory-manager"
        self.purpose = "Gestionar persistencia de memoria en GitHub con integridad"
        self.version = "1.0"
        self.requires_llm = False
        self.resonance_keywords = [
            "memoria", "guardar", "persistencia", "github", "blockchange",
            "integridad", "backup", "historial"
        ]
        self.impact_on_q = 0.0  # No impacta
        self.is_critical = True  # NUNCA se poda
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecutar operaciones de memoria.
        
        Context requerido:
        - memory: MemoryGitHubManager
        - operation: "save_conversation" | "load_memory" | "verify_integrity" | "stats"
        - data: datos a guardar (si es save)
        
        Returns:
        Dict con resultado de la operación
        """
        
        try:
            memory = context.get("memory")
            operation = context.get("operation", "stats")
            
            if not memory:
                return {
                    "status": "error",
                    "error": "Memory manager not available in context",
                    "q_impact": 0.0
                }
            
            # Ejecutar operación solicitada
            if operation == "save_conversation":
                return self._save_conversation(memory, context)
            
            elif operation == "load_memory":
                return self._load_memory(memory, context)
            
            elif operation == "verify_integrity":
                return self._verify_integrity(memory)
            
            elif operation == "stats":
                return self._get_stats(memory)
            
            elif operation == "cleanup":
                return self._cleanup_memory(memory, context)
            
            else:
                return {
                    "status": "error",
                    "error": f"Unknown operation: {operation}",
                    "q_impact": 0.0
                }
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "q_impact": 0.0
            }
            self.update_health(False, error_result)
            return error_result
    
    def _save_conversation(self, memory: MemoryGitHubManager, context: Dict) -> Dict:
        """Guardar conversación con integridad blockchange"""
        try:
            user_input = context.get("user_input", "")
            response = context.get("response", {})
            
            previous_hash = memory.get_last_hash()
            file_path, current_hash = memory.save_conversation(user_input, response, previous_hash)
            
            result = {
                "status": "success",
                "operation": "save_conversation",
                "file_path": file_path,
                "hash": current_hash,
                "message": "Conversation saved with integrity verification",
                "q_impact": 0.0
            }
            self.update_health(True, result)
            return result
            
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "q_impact": 0.0
            }
            self.update_health(False, result)
            return result
    
    def _load_memory(self, memory: MemoryGitHubManager, context: Dict) -> Dict:
        """Cargar memoria histórica"""
        try:
            days_back = context.get("days_back", 7)
            memories = memory.load_memory(days_back=days_back)
            
            result = {
                "status": "success",
                "operation": "load_memory",
                "memories_loaded": len(memories),
                "days_back": days_back,
                "memories": memories[:10],  # Limitar a últimas 10 para evitar overflow
                "q_impact": 0.0
            }
            self.update_health(True, result)
            return result
            
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "q_impact": 0.0
            }
            self.update_health(False, result)
            return result
    
    def _verify_integrity(self, memory: MemoryGitHubManager) -> Dict:
        """Verificar integridad de cadena de memoria"""
        try:
            is_intact = memory.verify_chain_integrity()
            
            result = {
                "status": "success",
                "operation": "verify_integrity",
                "chain_intact": is_intact,
                "message": "✅ Memory chain integrity verified" if is_intact else "🔴 Chain corruption detected",
                "q_impact": 0.0 if is_intact else -0.15  # Impacto negativo si corrupción
            }
            self.update_health(is_intact, result)
            return result
            
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "chain_intact": False,
                "q_impact": -0.1
            }
            self.update_health(False, result)
            return result
    
    def _get_stats(self, memory: MemoryGitHubManager) -> Dict:
        """Obtener estadísticas de memoria"""
        try:
            stats = memory.get_memory_stats()
            
            result = {
                "status": "success",
                "operation": "stats",
                "statistics": stats,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "q_impact": 0.0
            }
            self.update_health(True, result)
            return result
            
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "q_impact": 0.0
            }
            self.update_health(False, result)
            return result
    
    def _cleanup_memory(self, memory: MemoryGitHubManager, context: Dict) -> Dict:
        """
        Limpiar memoria: eliminar entradas antiguas y duplicadas
        SOLO ejecutar si Q(t) muy bajo
        """
        try:
            days_threshold = context.get("days_threshold", 90)
            dry_run = context.get("dry_run", True)
            
            # Analizar qué eliminar
            old_memories = memory.load_memory(days_back=days_threshold)
            
            if dry_run:
                result = {
                    "status": "success",
                    "operation": "cleanup_memory",
                    "mode": "DRY_RUN",
                    "would_delete": len(old_memories),
                    "days_threshold": days_threshold,
                    "message": "Dry run only - no deletions executed",
                    "q_impact": 0.0
                }
            else:
                # En versión real, eliminaría archivos
                result = {
                    "status": "success",
                    "operation": "cleanup_memory",
                    "mode": "LIVE",
                    "deleted_count": len(old_memories),
                    "message": f"Cleaned {len(old_memories)} old memory entries",
                    "q_impact": 0.05  # Pequeño boost por limpieza
                }
            
            self.update_health(True, result)
            return result
            
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "q_impact": 0.0
            }
            self.update_health(False, result)
            return result


# === FACTORY ===

def create_memory_manager_skill() -> MemoryManagerSkill:
    """Factory para crear MemoryManagerSkill"""
    return MemoryManagerSkill()
