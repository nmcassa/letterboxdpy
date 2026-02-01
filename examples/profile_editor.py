"""
Letterboxd Profile Editor (Interactive CLI Form)

Demonstrates the UserSettings page module for profile management.
Select which field to edit from a summary view.
"""

__title__ = "Profile Editor"
__description__ = "CLI tool to edit Letterboxd profile settings."
__version__ = "1.0.0"
__author__ = "fastfingertips"
__created_at__ = "2026-02-01"

import argparse
import random
import copy
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from letterboxdpy.auth import UserSession
from letterboxdpy.account.settings import UserSettings
from letterboxdpy.constants.forms import PROFILE_FORM, PROFILE_EDITABLE_FIELDS


def display_summary(payload: dict, original: dict, console: Console):
    """Display all fields in a summary table."""
    table = Table(title="Profile Settings", box=None, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Field", style="bold")
    table.add_column("Value", style="white")

    for i, field in enumerate(PROFILE_EDITABLE_FIELDS, 1):
        val = payload.get(field.key, "")
        orig_val = original.get(field.key, "")
        
        is_modified = val != orig_val
        style = "italic yellow" if is_modified else "white"
        
        if field.field_type == "toggle":
            val = "[green]ON[/green]" if val == "true" else "[red]OFF[/red]"
        elif not val:
            val = "[dim](empty)[/dim]"
            
        if is_modified:
            val = f"[{style}]{val}[/{style}] [yellow]*[/yellow]"
            
        table.add_row(str(i), field.label, val)
    
    # Favorites row
    fav_films = payload.get("favouriteFilms", [])
    orig_favs = original.get("favouriteFilms", [])
    
    # Compare favorites by IDs
    current_ids = [f["id"] for f in fav_films]
    orig_ids = [f["id"] for f in orig_favs]
    is_fav_modified = current_ids != orig_ids
    
    if not fav_films:
        fav_str = "[dim](none)[/dim]"
    else:
        fav_str = "\n".join([f"{i}. {f['name']}" for i, f in enumerate(fav_films, 1)])
    
    if is_fav_modified:
        fav_str = f"[italic yellow]{fav_str}[/italic yellow] [yellow]*[/yellow]"
        
    table.add_row("F", "Favorite Films", fav_str)
    
    console.print(table)


def edit_field(field, payload: dict, console: Console) -> bool:
    """Edit a single field. Returns True if changed."""
    current = payload.get(field.key, "")
    
    if field.field_type in ["text", "textarea"]:
        console.print(f"\n[bold]{field.label}:[/bold] {current or '(empty)'}")
        new_val = Prompt.ask("  New value", default=current)
        if new_val != current:
            payload[field.key] = new_val
            return True
    
    elif field.field_type == "select":
        options = list(field.options)
        console.print(f"\n[bold]{field.label}:[/bold] {current}")
        console.print(f"  [dim]Options: {' | '.join(options)}[/dim]")
        new_val = Prompt.ask("  Select", choices=options, default=current)
        if new_val != current:
            payload[field.key] = new_val
            return True
    
    elif field.field_type == "toggle":
        is_on = current == "true"
        status = "[green]ON[/green]" if is_on else "[red]OFF[/red]"
        console.print(f"\n[bold]{field.label}:[/bold] {status}")
        if Confirm.ask("  Toggle?", default=False):
            payload[field.key] = "false" if is_on else "true"
            return True
    
    return False


def edit_favorites(payload: dict, console: Console) -> bool:
    """Edit favorite films order. Returns True if changed."""
    fav_films = payload.get("favouriteFilms", [])
    
    if not fav_films:
        console.print("\n[dim]No favorite films to reorder.[/dim]")
        return False
    
    console.print("\n[bold]Favorite Films:[/bold]")
    for i, film in enumerate(fav_films, 1):
        console.print(f"  {i}. {film['name']}")
    
    action = Prompt.ask("\n  Action", choices=["reverse", "shuffle", "cancel"], default="cancel")
    
    if action == "reverse":
        payload[PROFILE_FORM.FAVORITE_FILMS_FIELD] = [f["id"] for f in fav_films][::-1]
        console.print("  [green][OK] Reversed[/green]")
        return True
    elif action == "shuffle":
        ids = [f["id"] for f in fav_films]
        payload[PROFILE_FORM.FAVORITE_FILMS_FIELD] = random.sample(ids, len(ids))
        console.print("  [green][OK] Shuffled[/green]")
        return True
    
    return False

def run_editor(session: UserSession):
    """Main editor loop using UserSettings module."""
    console = Console()
    
    console.print(Panel(
        f"[bold]{__description__}[/bold]\n[dim]Select field # to edit, 'S' to save, 'Q' to quit.[/dim]",
        title=f"[bold green] {__title__} v{__version__} [/bold green]",
        border_style="green"
    ))
    console.print(f"Logged in as [bold cyan]@{session.username}[/bold cyan]\n")

    settings = UserSettings(session)
    # Get initial payload and make a deep copy for comparison
    payload = settings.get_profile()
    original_payload = copy.deepcopy(payload)
    
    changes_made = False
    
    num_fields = len(PROFILE_EDITABLE_FIELDS)
    # Allow both upper and lower case in the prompt validation
    valid_choices = [str(i) for i in range(1, num_fields + 1)] + ["F", "S", "Q", "f", "s", "q"]
    
    while True:
        display_summary(payload, original_payload, console)
        
        console.print("\n[dim]Enter field # to edit, [bold]F[/bold] for favorites, [bold]S[/bold] to save, [bold]Q[/bold] to quit[/dim]")
        choice = Prompt.ask("→", choices=valid_choices, default="Q").upper()
        
        if choice == "Q":
            if changes_made and not Confirm.ask("[yellow]Discard unsaved changes?[/yellow]"):
                continue
            break
        
        elif choice == "S":
            if not changes_made:
                console.print("[dim]No changes to save.[/dim]")
            else:
                result = settings.update_profile(payload)
                if result["success"]:
                    console.print("\n[bold green][SUCCESS] Profile saved![/bold green]")
                    # Update original state to match current saved state
                    original_payload = copy.deepcopy(payload)
                    changes_made = False
                else:
                    console.print(f"\n[bold red][FAILED] ({result['status_code']})[/bold red]")
        
        elif choice == "F":
            if edit_favorites(payload, console):
                changes_made = True
        
        else:
            idx = int(choice) - 1
            if edit_field(PROFILE_EDITABLE_FIELDS[idx], payload, console):
                changes_made = True


def main():
    from letterboxdpy.constants.project import DEFAULT_COOKIE_PATH
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--path", type=Path, default=DEFAULT_COOKIE_PATH)
    args = parser.parse_args()
    
    try:
        session = UserSession.ensure(args.path)
        run_editor(session)
    except KeyboardInterrupt:
        print("\nExiting.")
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
