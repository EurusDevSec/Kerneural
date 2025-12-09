import time
import json
import os
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from rich.align import Align
from datetime import datetime, timedelta

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
        self.last_generated_rule = None
        self.start_time = datetime.now()

    def format_time(self, time_str):
        """Convert UTC timestamp from Falco logs to Local Time (System Time)"""
        try:
            # Falco time string example: "2025-12-09T09:14:16.123456789Z"
            # We only care about up to seconds for display
            clean_time = time_str.split('.')[0].replace('Z', '')
            dt = datetime.strptime(clean_time, "%Y-%m-%dT%H:%M:%S")
            
            # Calculate local offset
            now = time.time()
            if time.localtime(now).tm_isdst and time.daylight:
                offset_sec = -time.altzone
            else:
                offset_sec = -time.timezone
            
            local_dt = dt + timedelta(seconds=offset_sec)
            return local_dt.strftime("%H:%M:%S")
        except Exception:
            return time_str[:19]

    def make_layout(self) -> Layout:
        layout = Layout(name="root")
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["main"].split_row(
            Layout(name="left_panel", ratio=6),
            Layout(name="right_panel", ratio=4)
        )
        layout["right_panel"].split_column(
            Layout(name="status", size=10),
            Layout(name="neural_core", ratio=1)
        )
        return layout

    def generate_header(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right", ratio=1)
        
        grid.add_row(
            "🛡️ Kerneural v1.0",
            "[bold white]AUTOMATED PURPLE TEAMING SYSTEM[/bold white]",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return Panel(grid, style="white on blue")

    def generate_alert_table(self) -> Panel:
        table = Table(expand=True, border_style="dim", header_style="bold white")
        table.add_column("Time", style="cyan", no_wrap=True, width=10)
        table.add_column("Lvl", style="bold", width=8)
        table.add_column("Rule / Event", style="white")
        table.add_column("Container", style="green", width=15)

        # Show last 15 alerts
        for alert in reversed(self.alerts[-15:]):
            priority = alert.get('priority', 'UNKNOWN')
            
            # Color coding for priority
            p_style = "white"
            if priority in ['Critical', 'Error']:
                p_style = "bold red"
            elif priority in ['Warning']:
                p_style = "bold yellow"
            elif priority in ['Notice', 'Info']:
                p_style = "blue"

            table.add_row(
                self.format_time(alert.get('time', 'N/A')),
                Text(priority, style=p_style),
                alert.get('rule', 'Unknown Rule'),
                alert.get('output_fields', {}).get('container.name', 'N/A')
            )
            
        return Panel(
            table, 
            title="[bold red]🚨 Live Threat Feed[/bold red]", 
            border_style="red",
            padding=(0, 1)
        )

    def generate_status_panel(self) -> Panel:
        # Calculate uptime
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]

        status_color = "green"
        status_icon = "🟢"
        if self.status != "Monitoring":
            status_color = "yellow"
            status_icon = "⚠️"

        grid = Table.grid(expand=True)
        grid.add_column(style="bold white")
        grid.add_column(justify="right")

        grid.add_row("System Status:", Text(f"{status_icon} {self.status}", style=f"bold {status_color}"))
        grid.add_row("Uptime:", uptime_str)
        grid.add_row("Total Alerts:", str(len(self.alerts)))
        grid.add_row("Last Action:", Text(self.last_action, style="italic cyan"))

        return Panel(
            grid, 
            title="[bold blue]📊 System Stats[/bold blue]", 
            border_style="blue"
        )

    def generate_neural_panel(self) -> Panel:
        content = None
        if self.last_generated_rule:
            content = Syntax(self.last_generated_rule, "yaml", theme="monokai", line_numbers=True)
        else:
            content = Align.center(
                Text("\n\nWaiting for threats...\nNeural Core is idle.", style="dim white"),
                vertical="middle"
            )

        return Panel(
            content,
            title="[bold magenta]🧠 Neural Core Activity (Gemini)[/bold magenta]",
            border_style="magenta"
        )

    def start(self):
        layout = self.make_layout()
        layout["footer"].update(Panel(Text("Press Ctrl+C to exit | Powered by eBPF & LLM", justify="center", style="italic grey50")))

        with Live(layout, refresh_per_second=4, screen=True) as live:
            # Open log file and seek to end
            if not os.path.exists(self.log_file):
                open(self.log_file, 'w').close()
                
            with open(self.log_file, 'r') as f:
                f.seek(0, os.SEEK_END)
                
                while True:
                    # Update UI Components
                    layout["header"].update(self.generate_header())
                    layout["left_panel"].update(self.generate_alert_table())
                    layout["status"].update(self.generate_status_panel())
                    layout["neural_core"].update(self.generate_neural_panel())
                    
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
            self.last_action = f"Analyzing: {log_entry.get('rule')[:30]}..."
            
            # Generate Rule
            new_rule = self.brain.analyze_log_and_generate_rule(json.dumps(log_entry))
            
            if new_rule:
                self.status = "GENERATING VACCINE"
                self.last_action = "Applying new Falco rule..."
                self.last_generated_rule = new_rule # Save for display
                
                self.rule_manager.add_rule(new_rule)
                self.rule_manager.reload_falco()
                
                self.last_action = "System Immunized!"
                self.status = "Monitoring"

if __name__ == "__main__":
    dashboard = KerneuralDashboard()
    dashboard.start()
