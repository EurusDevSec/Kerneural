import time
import json
import os
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from datetime import datetime

from src.blue_agent.rule_manager import RuleManager
from src.neural_core.gemini_client import NeuralBrain

console = Console()

class KerneuralDashboard:
    def __init__(self):
        self.brain = NeuralBrain()
        self.rule_manager = RuleManager()
        self.log_file = "logs/falco_events.json"
        self.alerts = []
        self.status = "Monitoring"
        self.last_action = "System initialized"

    def make_layout(self) -> Layout:
        layout = Layout(name="root")
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["main"].split_row(
            Layout(name="alerts", ratio=2),
            Layout(name="actions", ratio=1)
        )
        return layout

    def generate_alert_table(self) -> Table:
        table = Table(title="🚨 Security Alerts", expand=True, border_style="red")
        table.add_column("Time", style="cyan", no_wrap=True)
        table.add_column("Priority", style="magenta")
        table.add_column("Rule", style="white")
        table.add_column("Container", style="green")

        # Show last 10 alerts
        for alert in self.alerts[-10:]:
            table.add_row(
                alert.get('time', 'N/A')[:19],
                alert.get('priority', 'UNKNOWN'),
                alert.get('rule', 'Unknown Rule'),
                alert.get('output_fields', {}).get('container.name', 'N/A')
            )
        return table

    def generate_status_panel(self) -> Panel:
        status_text = Text()
        status_text.append(f"Status: {self.status}\n", style="bold green" if self.status == "Monitoring" else "bold yellow")
        status_text.append(f"Last Action: {self.last_action}\n", style="white")
        status_text.append(f"Total Alerts: {len(self.alerts)}\n", style="cyan")
        
        return Panel(status_text, title="🛡️ System Status", border_style="blue")

    def start(self):
        layout = self.make_layout()
        layout["header"].update(Panel(Text("KERNEURAL - AI-Driven Purple Teaming System", justify="center", style="bold white"), style="on blue"))
        layout["footer"].update(Panel(Text("Press Ctrl+C to exit", justify="center", style="italic grey50")))

        with Live(layout, refresh_per_second=4, screen=True) as live:
            # Open log file and seek to end
            if not os.path.exists(self.log_file):
                open(self.log_file, 'w').close()
                
            with open(self.log_file, 'r') as f:
                f.seek(0, os.SEEK_END)
                
                while True:
                    # Update UI
                    layout["alerts"].update(self.generate_alert_table())
                    layout["actions"].update(self.generate_status_panel())
                    
                    # Read logs
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    
                    try:
                        log_entry = json.loads(line)
                        self.process_event(log_entry)
                    except json.JSONDecodeError:
                        continue

    def process_event(self, log_entry):
        self.alerts.append(log_entry)
        priority = log_entry.get('priority')
        
        if priority in ['Warning', 'Error', 'Critical', 'Notice']:
            self.status = "ANALYZING THREAT"
            self.last_action = f"Analyzing alert: {log_entry.get('rule')}"
            
            # Generate Rule
            new_rule = self.brain.analyze_log_and_generate_rule(json.dumps(log_entry))
            
            if new_rule:
                self.status = "GENERATING VACCINE"
                self.last_action = "Applying new Falco rule..."
                
                self.rule_manager.add_rule(new_rule)
                self.rule_manager.reload_falco()
                
                self.last_action = "System Immunized! Rule applied."
                self.status = "Monitoring"

if __name__ == "__main__":
    dashboard = KerneuralDashboard()
    dashboard.start()
