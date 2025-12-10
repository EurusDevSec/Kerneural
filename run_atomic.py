import argparse
import sys
import time
from src.red_agent.atomic_client import AtomicClient
from src.utils.docker_helper import DockerHelper
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Run Atomic Red Team tests in Kerneural Victim")
    parser.add_argument("technique_id", help="MITRE ATT&CK Technique ID (e.g., T1059.004)")
    args = parser.parse_args()

    client = AtomicClient()
    console.print(f"[bold blue]Fetching Atomic Tests for {args.technique_id}...[/bold blue]")
    
    tests = client.fetch_technique(args.technique_id)
    
    if not tests:
        console.print("[bold red]No Linux tests found or technique not found.[/bold red]")
        sys.exit(1)

    # Check if victim is running
    if not DockerHelper.is_container_running("victim"):
        console.print("[bold red]Error: 'victim' container is not running. Please start the environment first.[/bold red]")
        sys.exit(1)

    table = Table(title=f"Available Tests for {args.technique_id}")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Name", style="magenta")
    table.add_column("Description")
    
    for i, test in enumerate(tests):
        desc = test['description'].replace('\n', ' ').strip()
        if len(desc) > 60:
            desc = desc[:57] + "..."
        table.add_row(str(i+1), test['name'], desc)
    
    console.print(table)
    
    # Ask user which test to run
    choice = console.input("[bold yellow]Enter test number to run (or 'all', 'q' to quit): [/bold yellow]")
    
    if choice.lower() == 'q':
        sys.exit(0)
        
    tests_to_run = []
    if choice.lower() == 'all':
        tests_to_run = tests
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tests):
                tests_to_run = [tests[idx]]
            else:
                console.print("[red]Invalid selection.[/red]")
                sys.exit(1)
        except ValueError:
            console.print("[red]Invalid input.[/red]")
            sys.exit(1)

    for test in tests_to_run:
        console.print(f"\n[bold green]Running Test: {test['name']}[/bold green]")
        console.print(f"[dim]Command: {test['commands']}[/dim]")
        
        # Execute
        console.print("[bold cyan]Executing in 'victim' container...[/bold cyan]")
        code, output = DockerHelper.exec_command("victim", test['commands'])
        
        if code == 0:
            console.print("[bold green]Execution Successful![/bold green]")
        else:
            console.print(f"[bold red]Execution Failed (Exit Code {code})[/bold red]")
        
        console.print(Panel(output.strip(), title="Container Output", border_style="blue"))
        
        # Cleanup
        if test['cleanup']:
            console.print("[italic]Running cleanup...[/italic]")
            DockerHelper.exec_command("victim", test['cleanup'])
            
        time.sleep(1)

if __name__ == "__main__":
    main()
