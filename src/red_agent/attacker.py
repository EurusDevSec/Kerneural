import subprocess
from rich.console import Console
from src.red_agent.scenarios import ATTACK_SCENARIOS

console = Console()

class RedAgent:
    def __init__(self, target_container="victim"):
        self.target_container = target_container
        # Check if container exists using docker inspect
        try:
            subprocess.run(
                ["docker", "inspect", target_container],
                capture_output=True,
                check=True
            )
            console.print(f"[bold green]Connected to target container: {target_container}[/bold green]")
        except subprocess.CalledProcessError:
            console.print(f"[bold red]Container {target_container} not found![/bold red]")
            self.target_container = None

    def execute_attack(self, technique_id):
        if not self.target_container:
            return
        
        scenario = ATTACK_SCENARIOS.get(technique_id)
        if not scenario:
            console.print(f"[yellow]Technique {technique_id} not defined.[/yellow]")
            return

        console.print(f"\n[bold red]>>> Executing Attack: {technique_id} - {scenario['name']}[/bold red]")
        
        for cmd in scenario['commands']:
            console.print(f"[cyan]Running cmd:[/cyan] {cmd}")
            try:
                # Execute command in container using docker exec
                # We use sh -c to handle shell commands properly
                full_cmd = ["docker", "exec", self.target_container, "sh", "-c", cmd]
                
                result = subprocess.run(
                    full_cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    console.print(f"   [green]Success:[/green] {result.stdout.strip()}")
                else:
                    console.print(f"   [red]Failed (Code {result.returncode}):[/red] {result.stderr.strip()}")
            except Exception as e:
                console.print(f"   [bold red]Error:[/bold red] {str(e)}")