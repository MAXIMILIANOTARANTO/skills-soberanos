# 2026-10-15 — Q por defecto no ejecuta

`OrchestratorEngine.route_and_execute` ponía `current_q` en 0.7 si faltaba. `run_pulse.py` ponía 0.75 si no había medidor. Esos números no son una corrida AR1.

Si `current_q` no viene, el motor devuelve la resonancia y no ejecuta skills. `tcu-detector/SKILL.md` ya está en el repo; el orquestador decía que no existía.
