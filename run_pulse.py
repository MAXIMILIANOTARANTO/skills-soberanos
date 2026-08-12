#!/usr/bin/env python3
"""
Run Pulse — Test harness local del ecosistema
Ejecuta un ciclo completo: Resonance → Skills → Memory → Q(t) → Report

Uso:
    python run_pulse.py                          # dry-run (no guarda)
    python run_pulse.py --live                   # guarda en GitHub
    python run_pulse.py --intent "tu intención"  # custom intent
    python run_pulse.py --dry-run                # explícito dry-run
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict

# Imports del ecosistema
try:
    from core.memory_github_manager import MemoryGitHubManager
    from core.coherence_meter import QuantitativeCoherenceMeter
    from core.orchestrator_engine import OrchestratorEngine
    from core.llm_engine import EcosystemLLM
    from core.skill_base import ExampleTechnicalSkill, ExampleCognitiveSkill
except ImportError as e:
    print(f"❌ Error de import: {e}")
    print("Asegúrate de estar en el directorio raíz del proyecto")
    sys.exit(1)


class EcosystemPulse:
    """Gestor del pulse del ecosistema"""
    
    def __init__(self, github_token: str = None, openrouter_key: str = None, dry_run: bool = True):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN", "")
        self.openrouter_key = openrouter_key or os.getenv("OPENROUTER_API_KEY", "")
        self.dry_run = dry_run
        
        # Componentes
        self.llm = None
        self.memory = None
        self.coherence_meter = None
        self.orchestrator = None
        
        # Report
        self.report = {}
        
        print(f"🌐 EcosystemPulse inicializado (dry_run={dry_run})")
    
    def initialize(self) -> bool:
        """Inicializar todos los componentes"""
        try:
            # 1. LLM Engine
            print("  → Inicializando LLM...")
            self.llm = EcosystemLLM(model_type="balanced")
            
            # 2. Memory Manager
            print("  → Inicializando Memory Manager...")
            if not self.github_token:
                print("    ⚠️  GITHUB_TOKEN no configurado. Funcionará en modo local.")
                self.memory = None
            else:
                try:
                    from github import Github
                    gh_client = Github(self.github_token)
                    repo = gh_client.get_repo("MAXIMILIANOTARANTO/ecosistema-soberano-github")
                    self.memory = MemoryGitHubManager(repo=repo)
                except Exception as e:
                    print(f"    ⚠️  No se pudo conectar al repo de memoria en GitHub ({e}). Funcionará en modo local.")
                    self.memory = None
            
            # 3. Coherence Meter
            print("  → Inicializando Coherence Meter...")
            self.coherence_meter = QuantitativeCoherenceMeter(self.memory) if self.memory else None
            
            # 4. Skills
            print("  → Cargando skills...")
            skills = [
                ExampleTechnicalSkill(),
                ExampleCognitiveSkill()
            ]
            # TODO: Agregar más skills aquí (coherence-pulse, meta-hilo-grok, etc)
            
            # 5. Orchestrator
            print("  → Inicializando Orchestrator...")
            self.orchestrator = OrchestratorEngine(
                skills=skills,
                llm_engine=self.llm,
                memory_manager=self.memory,
                coherence_meter=self.coherence_meter
            )
            
            print("✅ Todos los componentes inicializados correctamente\n")
            return True
        
        except Exception as e:
            print(f"❌ Error en inicialización: {e}")
            return False
    
    def run(self, intent: str = "Analizar estado actual del ecosistema") -> Dict:
        """
        Ejecutar un pulse completo
        
        Args:
            intent: Intención del pulse
        
        Returns:
            Dict con resultados
        """
        print(f"\n{'='*70}")
        print(f"🌀 ECOSYSTEM PULSE — {datetime.utcnow().isoformat()}")
        print(f"{'='*70}\n")
        
        if not self.orchestrator:
            print("❌ Orchestrator no inicializado. Llamar a initialize() primero.")
            return {}
        
        # STEP 1: Ejecutar orchestrator
        print(f"📍 Intención: {intent}\n")
        print("Step 1: Evaluando resonancia de skills...")
        
        try:
            # Construir contexto
            context = {
                "summary": "Estado del ecosistema soberano en GitHub",
                "current_q": 0.75 if self.coherence_meter is None else None
            }
            
            # Ejecutar
            orch_result = self.orchestrator.route_and_execute(
                intent=intent,
                context=context,
                dry_run=self.dry_run
            )
            
            print(f"  ✅ {len(orch_result['activated_skills'])} skills activados")
            resonance_display = [f"{s['skill']}({s['resonance']})" for s in orch_result['resonance_scores'][:3]]
            print(f"     Resonancia: {resonance_display}\n")
            
        except Exception as e:
            print(f"  ❌ Error en orquestación: {e}")
            orch_result = {"error": str(e), "activated_skills": []}
        
        # STEP 2: Calcular Q(t) si es posible
        print("Step 2: Calculando coherencia Q(t)...")
        
        if self.coherence_meter:
            try:
                q_result = self.coherence_meter.calculate_q()
                print(f"  ✅ Q(t) = {q_result['q_value']}")
                print(f"     Estado: {q_result['status']}")
                print(f"     Componentes: skill_resonance={q_result['components']['skill_resonance']}, " +
                      f"memory_health={q_result['components']['memory_health']}\n")
            except Exception as e:
                print(f"  ⚠️  No se pudo calcular Q(t): {e}\n")
                q_result = None
        else:
            print("  ⚠️  Coherence Meter no disponible (memory no configurada)\n")
            q_result = None
        
        # STEP 3: Análisis de skills
        print("Step 3: Analizando salud de skills...")
        
        try:
            skills_health = self.orchestrator.analyze_skills_health()
            healthy_count = skills_health["healthy_count"]
            total_count = skills_health["total_skills"]
            print(f"  ✅ {healthy_count}/{total_count} skills saludables")
            print(f"     Skills críticos: {skills_health['critical_skills']}\n")
        except Exception as e:
            print(f"  ⚠️  Error analizando health: {e}\n")
            skills_health = None
        
        # STEP 4: Detectar crisis
        print("Step 4: Detectando crisis...")
        
        crisis_detected = False
        if q_result:
            if q_result['status'] == 'CRITICAL':
                print(f"  🔴 CRISIS DETECTADA: Coherencia crítica")
                crisis_detected = True
            else:
                print(f"  ✅ No hay crisis macro detectada")
        print()
        
        # STEP 5: Guardar si no es dry-run
        print("Step 5: Persistencia...")
        
        if self.dry_run:
            print("  ℹ️  DRY-RUN: No se guarda en GitHub")
        else:
            if self.memory:
                try:
                    previous_hash = self.memory.get_last_hash()
                    self.memory.save_conversation(intent, orch_result, previous_hash)
                    print("  ✅ Conversación guardada en GitHub")
                except Exception as e:
                    print(f"  ❌ Error guardando memoria: {e}")
            else:
                print("  ⚠️  Memory manager no disponible")
        print()
        
        # COMPILAR REPORTE
        self.report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "intent": intent,
            "dry_run": self.dry_run,
            "orchestrator": orch_result,
            "coherence": q_result,
            "skills_health": skills_health,
            "crisis_detected": crisis_detected,
            "status": "SUCCESS" if not crisis_detected else "WARNING"
        }
        
        # RESUMEN FINAL
        print(f"{'='*70}")
        print(f"📊 PULSE SUMMARY")
        print(f"{'='*70}")
        print(f"Status: {self.report['status']}")
        print(f"Intención: {intent}")
        print(f"Skills activados: {len(orch_result.get('activated_skills', []))}")
        if q_result:
            print(f"Q(t): {q_result['q_value']}")
        print(f"Dry-run: {self.dry_run}")
        print(f"Timestamp: {self.report['timestamp']}\n")
        
        return self.report
    
    def save_report(self, filename: str = "pulse_report.json"):
        """Guardar reporte en JSON"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.report, f, indent=2, default=str)
            print(f"✅ Reporte guardado: {filename}")
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="Ecosystem Pulse — Test harness local del ecosistema"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Guardar cambios en GitHub (default: dry-run)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explícitamente dry-run (no guarda)"
    )
    parser.add_argument(
        "--intent",
        default="Analizar estado actual del ecosistema",
        help="Intención personalizada"
    )
    parser.add_argument(
        "--report",
        default="pulse_report.json",
        help="Archivo de salida del reporte"
    )
    
    args = parser.parse_args()
    
    # Determinar dry-run
    dry_run = not args.live if not args.dry_run else True
    
    # Crear y ejecutar pulse
    pulse = EcosystemPulse(dry_run=dry_run)
    
    if not pulse.initialize():
        sys.exit(1)
    
    pulse.run(intent=args.intent)
    pulse.save_report(args.report)
    
    print("\n✅ Pulse completado!")


if __name__ == "__main__":
    main()
