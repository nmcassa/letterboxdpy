import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from letterboxdpy.auth import UserSession
from letterboxdpy.account.settings import UserSettings
from letterboxdpy.constants.forms.notifications import NOTIFICATIONS_FORM, NOTIFICATION_GROUPS

__title__ = "Notification Manager"
__description__ = "CLI tool to manage Letterboxd notification settings"
__version__ = "1.0.0"
__author__ = "fastfingertips"
__created_at__ = "2026-02-02"

def display_menu(states, console):
    table = Table(title="Letterboxd Notifications", show_header=True, header_style="bold magenta")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Category/Setting", style="white")
    table.add_column("Status", justify="center")

    idx = 1
    mapping = {}
    
    for group_name, fields in NOTIFICATION_GROUPS.items():
        table.add_section()
        table.add_row("", f"[bold yellow]{group_name}[/bold yellow]", "")
        for label, key in fields:
            status = states.get(key, False)
            status_str = "[bold green]ON[/bold green]" if status else "[bold red]OFF[/bold red]"
            table.add_row(str(idx), label, status_str)
            mapping[idx] = key
            idx += 1
            
    console.clear()
    console.print(Panel(
        f"[bold]{__description__}[/bold]",
        title=f"[bold green] {__title__} v{__version__} [/bold green]",
        border_style="green"
    ))
    console.print(table)
    return mapping

def display_pending_changes(pending_changes: dict, console: Console):
    """Shows a list of unsaved modifications."""
    if not pending_changes:
        return

    console.print("\n[bold yellow]Pending Changes:[/bold yellow]")
    for key, val in pending_changes.items():
        # Find label for key in groups
        label = key
        for _, fields in NOTIFICATION_GROUPS.items():
            for l, k in fields:
                if k == key:
                    label = l
                    break
        
        status = "[green]ON[/green]" if val else "[red]OFF[/red]"
        console.print(f"  • {label}: {status}")

def handle_save(settings: UserSettings, pending_changes: dict, console: Console) -> list:
    """Updates notification settings and returns results."""
    with console.status("[bold green]Saving changes..."):
        results = settings.update_notifications(pending_changes)
    
    success_count = sum(1 for r in results if r["success"])
    console.print(f"\n[bold green]Successfully updated {success_count}/{len(results)} settings![/bold green]")
    Prompt.ask("\nPress Enter to continue")
    return results

def handle_choice(choice: str, states: dict, original_states: dict, pending_changes: dict, mapping: dict, settings: UserSettings, console: Console) -> bool:
    """Handles user menu selection. Returns False to exit the loop."""
    if choice == "Q":
        if pending_changes and not Confirm.ask("[yellow]Discard unsaved changes?[/yellow]"):
            return True
        return False
    
    if choice == "S":
        if not pending_changes:
            console.print("[dim]No changes to save.[/dim]")
            return True
        
        handle_save(settings, pending_changes, console)
        original_states.update(states) # Sync original state after save
        pending_changes.clear()
        return True
    
    # Toggle setting
    idx = int(choice)
    key = mapping[idx]
    states[key] = not states[key]
    
    if states[key] == original_states[key]:
        pending_changes.pop(key, None)
    else:
        pending_changes[key] = states[key]
    
    return True

def main():
    from letterboxdpy.constants.project import DEFAULT_COOKIE_PATH
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--path", type=Path, default=DEFAULT_COOKIE_PATH, help="Path to cookie file")
    args = parser.parse_args()

    console = Console()
    try:
        session = UserSession.ensure(cookie_path=args.path)
        settings = UserSettings(session)
        
        with console.status("[bold cyan]Fetching current settings..."):
            states = settings.get_notifications()
        
        original_states = states.copy()
        pending_changes = {}

        while True:
            mapping = display_menu(states, console)
            num_options = len(mapping)
            
            console.print(f"\n[dim]Logged in as: @{session.username}[/dim]")
            
            display_pending_changes(pending_changes, console)

            console.print("\n[dim]Enter # to toggle, [bold green]S[/bold green] to save changes, [bold red]Q[/bold red] to quit.[/dim]")
            
            choice = Prompt.ask("→", choices=[str(i) for i in range(1, num_options + 1)] + ["S", "Q"], default="Q").upper()
            
            if not handle_choice(choice, states, original_states, pending_changes, mapping, settings, console):
                break

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
