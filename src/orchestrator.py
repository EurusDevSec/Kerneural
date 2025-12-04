import time
import json
import os
from rich.console import Console
from rich.live import Live
from rich.table import Table

from src.blue_agent.monitor import LogMonitor # Cần implement class này để tail file log
from src.blue_agent.rule_manager import RuleManager
from src.neural_core.gemini_client import NeuralBrain


console = Console()
class KerneuralOrchestrator:
    def __init__(self):
        self.brain = NeuralBrain()
        self.rule_manager = RuleManager()
        self.log_file = "logs/falco_events.json"

    def start(self):
        console.print("[bold green]Kerneural System Started...[/bold green]")



        with open(self.log_file,'r') as f:
            # di chuyen den cuoi file
            f.seek(0, os.SEEK_END)

            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                try:
                    log_entry = json.loads(line)
                    self.process_event(log_entry)
                except json.JSONDecodeError:
                    continue


    def process_event(self, log_entry):
        priority = log_entry.get('priority')
        rule_name=log_entry.get('rule')

        console.print(f"[red]ALERT:[/red] {rule_name} ({priority})")

        # chi xu ly cac canh bao quan trong va chu aco trong whitelist

        if priority in ['Warning', 'Error', 'Critical', 'Notice']:
            console.print("[yellow]Analyzing threat with Gemini...[/yellow]")

            #1. Gui Ai sinh rule
            new_rule=self.brain.analyze_log_and_generate_rule(json.dumps(log_entry))
            if new_rule:
                console.print(f"[cyan]Generated Vaccine:[/cyan]\n{new_rule}")

                #2. apply rule
                self.rule_manager.add_rule(new_rule)
                self.rule_manager.reload_falco()

                console.print("[bold green]System Immunized![/bold green]")


if __name__ == "__main__":
    app=KerneuralOrchestrator()
    app.start()