"""
Memory GitHub Manager - Persistencia con integridad blockchange
Sistema de almacenamiento de memoria en GitHub con hash chain inmutable.

Características:
- Blockchange-style hashing (SHA256)
- Lock file para atomicidad
- Retry logic con backoff
- Integridad verificable
- Versionado automático en Git
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from pathlib import Path


class MemoryGitHubManager:
    """
    Gestor de memoria persistente en GitHub
    Cada conversación = archivo JSON con hash chain
    """
    
    def __init__(self, repo, base_path: str = "memoria"):
        """
        Args:
            repo: PyGithub Repository object
            base_path: Ruta base en el repo
        """
        self.repo = repo
        self.base_path = base_path
        self.lock_path = f"{base_path}/.lock"
        self.conversations_path = f"{base_path}/conversaciones"
        self.learning_path = f"{base_path}/aprendizaje"
        self.persistent_path = f"{base_path}/persistente"
        
        print(f"✅ MemoryGitHubManager inicializado para {repo.full_name}")
    
    # === HASHING & INTEGRIDAD ===
    
    @staticmethod
    def _calculate_hash(data: dict) -> str:
        """
        Calcula SHA256 del contenido JSON ordenado
        Garantiza que mismo contenido = mismo hash
        """
        # Ordenar keys para determinismo
        content = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    @staticmethod
    def _verify_hash(data: dict, expected_hash: str) -> bool:
        """Verifica que el hash de datos coincida con expected_hash"""
        calculated = MemoryGitHubManager._calculate_hash(data)
        return calculated == expected_hash
    
    # === LOCKING (Atomicidad) ===
    
    def _acquire_lock(self, max_retries: int = 8, wait_seconds: float = 2.0) -> bool:
        """
        Adquirir lock file para evitar race conditions
        
        Args:
            max_retries: Máximo intentos
            wait_seconds: Espera entre intentos
            
        Returns:
            True si consigue lock, False/Exception si no
        """
        for attempt in range(max_retries):
            try:
                self.repo.create_file(
                    path=self.lock_path,
                    message="🔒 LOCK: ecosystem pulse in progress",
                    content="locked"
                )
                print(f"✅ Lock acquired (attempt {attempt + 1})")
                return True
            
            except Exception as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"❌ Could not acquire memory lock after {max_retries} attempts: {e}")
                
                print(f"⏳ Lock busy, retrying in {wait_seconds}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_seconds)
        
        return False
    
    def _release_lock(self) -> bool:
        """Liberar lock file"""
        try:
            contents = self.repo.get_contents(self.lock_path)
            self.repo.delete_file(
                path=self.lock_path,
                message="🔓 UNLOCK: ecosystem pulse completed",
                sha=contents.sha
            )
            print("✅ Lock released")
            return True
        except Exception as e:
            print(f"⚠️ Lock release failed (may already be gone): {e}")
            return False
    
    # === GUARDAR CONVERSACIONES ===
    
    def save_conversation(self, user_input: str, response: dict, 
                         previous_hash: str = "") -> Tuple[str, str]:
        """
        Guardar conversación con integridad de cadena
        
        Args:
            user_input: Input del usuario
            response: Dict con respuesta (q_value, skills_activated, etc.)
            previous_hash: Hash del archivo anterior (para chain)
            
        Returns:
            Tupla (archivo_path, hash_actual)
        """
        timestamp_iso = datetime.utcnow().isoformat() + "Z"
        timestamp_file = timestamp_iso.replace(':', '-')
        
        # Construir data
        data = {
            "timestamp": timestamp_iso,
            "user_input": user_input[:500],  # Limitar tamaño
            "response": response,
            "q_value": response.get("q_value", 0.5),
            "skills_activated": response.get("skills_activated", []),
            "learning": response.get("learning", {}),
            "previous_hash": previous_hash,  # Chain link
        }
        
        # Calcular hash DESPUÉS de armar data (sin incluir current_hash)
        current_hash = self._calculate_hash(data)
        data["current_hash"] = current_hash
        
        # Path del archivo
        file_path = f"{self.conversations_path}/{timestamp_file}.json"
        
        try:
            self.repo.create_file(
                path=file_path,
                message=f"📝 Memory: {timestamp_iso} | Q={response.get('q_value', 0):.3f}",
                content=json.dumps(data, indent=2, ensure_ascii=False)
            )
            print(f"✅ Conversation saved: {file_path}")
            return (file_path, current_hash)
        
        except Exception as e:
            print(f"❌ Failed to save conversation: {e}")
            raise
    
    # === RECUPERAR MEMORIA ===
    
    def get_last_hash(self) -> str:
        """
        Obtiene el hash del último archivo de memoria
        Usado para encadenar próximas conversaciones
        """
        try:
            contents = self.repo.get_contents(self.conversations_path)
            
            if not contents or len(contents) == 0:
                return ""
            
            # Obtener el archivo más reciente (por nombre)
            files = sorted(contents, key=lambda x: x.name, reverse=True)
            last_file = files[0]
            
            data = json.loads(last_file.decoded_content)
            return data.get("current_hash", "")
        
        except Exception as e:
            print(f"⚠️ Could not retrieve last hash: {e}")
            return ""
    
    def load_memory(self, days_back: int = 7) -> List[dict]:
        """
        Cargar conversaciones de los últimos N días
        
        Args:
            days_back: Días hacia atrás a recuperar
            
        Returns:
            Lista de conversaciones (más recientes primero)
        """
        try:
            contents = self.repo.get_contents(self.conversations_path)
            
            if not contents:
                return []
            
            # Ordenar por nombre (timestamp)
            files = sorted(contents, key=lambda x: x.name, reverse=True)
            
            memories = []
            cutoff_time = datetime.utcnow().replace(
                day=datetime.utcnow().day - days_back
            )
            
            for file in files:
                try:
                    data = json.loads(file.decoded_content)
                    file_time = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
                    
                    if file_time >= cutoff_time:
                        memories.append(data)
                
                except Exception as e:
                    print(f"⚠️ Failed to parse {file.name}: {e}")
            
            return memories
        
        except Exception as e:
            print(f"❌ Failed to load memory: {e}")
            return []
    
    def get_coherence_history(self, days_back: int = 30) -> List[dict]:
        """
        Obtener histórico de Q(t) para gráficos
        
        Returns:
            Lista de {timestamp, q_value}
        """
        memories = self.load_memory(days_back=days_back)
        
        history = [
            {
                "timestamp": m["timestamp"],
                "q_value": m.get("q_value", 0.5)
            }
            for m in memories
        ]
        
        return history
    
    # === GUARDAR APRENDIZAJE ===
    
    def save_learning(self, finding: str, confidence: float, 
                     source: str = "ecosystem-ai") -> str:
        """
        Guardar nuevo aprendizaje del sistema
        
        Args:
            finding: Patrón o descubrimiento
            confidence: Score 0.0-1.0
            source: Origen del aprendizaje
            
        Returns:
            Path del archivo creado
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        learning_data = {
            "finding": finding,
            "confidence": confidence,
            "discovered_at": timestamp,
            "source": source,
            "hash": self._calculate_hash({"finding": finding, "confidence": confidence})
        }
        
        file_path = f"{self.learning_path}/{timestamp.replace(':', '-')}.json"
        
        try:
            self.repo.create_file(
                path=file_path,
                message=f"🧠 Learning: {finding[:50]}... (confidence: {confidence:.2f})",
                content=json.dumps(learning_data, indent=2, ensure_ascii=False)
            )
            print(f"✅ Learning saved: {file_path}")
            return file_path
        
        except Exception as e:
            print(f"❌ Failed to save learning: {e}")
            raise
    
    # === ESTADO PERSISTENTE ===
    
    def save_persistent_state(self, state_name: str, state_data: dict) -> str:
        """
        Guardar estado persistente (como checkpoints de TCU, estado del orquestador)
        
        Args:
            state_name: Nombre del estado (ej: "tcu_state_v1.0")
            state_data: Datos a persistir
            
        Returns:
            Path del archivo
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        file_path = f"{self.persistent_path}/{state_name}_{timestamp.replace(':', '-')}.json"
        
        state_data["persistent_at"] = timestamp
        state_data["hash"] = self._calculate_hash(state_data)
        
        try:
            self.repo.create_file(
                path=file_path,
                message=f"💾 Persistent state: {state_name}",
                content=json.dumps(state_data, indent=2, ensure_ascii=False)
            )
            print(f"✅ State saved: {file_path}")
            return file_path
        
        except Exception as e:
            print(f"❌ Failed to save state: {e}")
            raise
    
    # === VERIFICACIÓN DE INTEGRIDAD ===
    
    def verify_chain_integrity(self) -> bool:
        """
        Verifica que la cadena de hashes sea íntegra
        (cada archivo apunta correctamente al anterior)
        
        Returns:
            True si cadena es íntegra, False si hay corrupción
        """
        memories = self.load_memory(days_back=90)
        
        if not memories:
            print("⚠️ No memories to verify")
            return True
        
        # Recorrer de más antiguo a más nuevo
        memories_sorted = sorted(memories, key=lambda x: x["timestamp"])
        
        previous_hash = ""
        corrupted = []
        
        for memory in memories_sorted:
            if memory.get("previous_hash") != previous_hash:
                corrupted.append(memory["timestamp"])
            
            previous_hash = memory.get("current_hash", "")
        
        if corrupted:
            print(f"🔴 Chain corruption detected at: {corrupted}")
            return False
        
        print(f"✅ Chain integrity verified ({len(memories)} files)")
        return True
    
    # === ESTADÍSTICAS ===
    
    def get_memory_stats(self) -> dict:
        """Obtener estadísticas de memoria"""
        memories = self.load_memory(days_back=30)
        
        if not memories:
            return {"total_conversations": 0}
        
        q_values = [m.get("q_value", 0.5) for m in memories]
        
        return {
            "total_conversations": len(memories),
            "avg_q_value": sum(q_values) / len(q_values),
            "max_q_value": max(q_values),
            "min_q_value": min(q_values),
            "last_update": memories[0]["timestamp"] if memories else None
        }


# === FACTORY ===

def create_memory_manager(repo):
    """Factory para crear MemoryGitHubManager"""
    return MemoryGitHubManager(repo)


if __name__ == "__main__":
    print("Memory GitHub Manager - Test mode")
    print("Usa esta clase en core/orchestrator.py o core/coherence_meter.py")
