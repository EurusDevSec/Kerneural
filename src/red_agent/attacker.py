import docker
from rich.console import Console
from src.red_agent.scenarios import ATTACK_SCENARIOS


console = Console()

class RedAgent:
    def __init__(self, target_container="victim"):
        self.client=docker.from_env()
        self.target_container = target_container


        try:
            self.target_container = self.client.containers.get(target_container)
            console.print(f"[bold green]Connected to target container: {target_container}[/bold green]")
        except docker.errors.NotFound:
            console.print(f"[bold red]Container {target_container} not found![/bold red]")
            self.target_container = None

    def execute_attack(self, technique_id):
        if not self.container:
            return
        
        scenario = ATTACK_SCENARIOS.get(technique_id)
        if not scenario:
            console.print(f"[yellow]Technique {technique_id} not defined.[/yellow]")
            return 
        console.print(f"\n[bold red]>>> Executing Attack: {technique_id} - {scenario['name']} [/bold red]")

        for cmd in scenario['commands']:
            console.print(f"[cyan]Running cmd:[/cyan] {cmd}")
            try:
                # thuc thi lenh trong container ( tuong tu docker exec)
                exit_code, output = self.container.exec_run(cmd)

                if exit_code ==0:
                    console.print(f"   [green]Success:[/green] {output.de}")