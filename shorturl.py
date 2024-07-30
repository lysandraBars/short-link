import requests
from urllib.parse import urlparse
from requests.exceptions import RequestException, HTTPError, ConnectionError
import time
import os
import json
import pyperclip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from rich.syntax import Syntax
from pyfiglet import Figlet

# Configuration
HISTORY_FILE = "url_history.json"
MAX_HISTORY_SIZE = 5 # maximun of short link save on history
SHORTENER_API = "http://tinyurl.com/api-create.php?url="

console = Console()

def is_valid_url(url):
    """Check if the URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def print_ascii_title():
    """Print the title in ASCII art."""
    figlet = Figlet(font='slant')
    ascii_title = figlet.renderText('SHORT LINK')
    console.print(ascii_title, style="bold cyan")

def get_short_url(api_url, long_url):
    """Call the API to shorten the URL and return the result."""
    try:
        response = requests.get(api_url + long_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.text
    except HTTPError as http_err:
        return f"HTTP Error: {http_err}"
    except ConnectionError as conn_err:
        return f"Connection Error: {conn_err}"
    except RequestException as req_err:
        return f"Request Error: {req_err}"

def shorten_url(long_url):
    """Shorten the URL and return the shortened URL or an error message."""
    if not is_valid_url(long_url):
        return "Invalid URL format."

    for _ in range(3):  # Try up to 3 times
        short_url = get_short_url(SHORTENER_API, long_url)
        if "Error" not in short_url:
            return short_url
        time.sleep(1)  # Wait one second before trying again

    return short_url

def save_to_history(long_url, short_url, custom_name=None, expiry_seconds=None):
    """Save URL information to history."""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)
    
    expiry_timestamp = time.time() + expiry_seconds if expiry_seconds else None
    
    history.append({
        "long_url": long_url,
        "short_url": short_url,
        "timestamp": time.ctime(),
        "custom_name": custom_name,
        "expiry_timestamp": expiry_timestamp
    })
    
    if len(history) > MAX_HISTORY_SIZE:
        history = history[-MAX_HISTORY_SIZE:]
    
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def show_history():
    """Display the history of shortened URLs."""
    if not os.path.exists(HISTORY_FILE):
        console.print("[bold red]History not found.[/bold red]", style="bold red")
        return

    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)
    
    if not history:
        console.print("[bold red]No history available.[/bold red]")
    else:
        table = Table(title="[bold cyan]URL History[/bold cyan]", style="bold cyan", border_style="bold magenta", show_lines=True)
        table.add_column("Name", style="bold green")
        table.add_column("Long URL", style="bold white")
        table.add_column("Short URL", style="bold yellow")
        table.add_column("Timestamp", style="bold blue")
        table.add_column("Expiry", style="bold red")
        
        current_time = time.time()
        for entry in history:
            if entry.get("expiry_timestamp") and current_time > entry["expiry_timestamp"]:
                continue  # Skip expired entries
            table.add_row(
                entry.get('custom_name', 'N/A'),
                entry['long_url'],
                entry['short_url'],
                entry['timestamp'],
                time.ctime(entry['expiry_timestamp']) if entry.get('expiry_timestamp') else 'Never'
            )
        console.print(table)

def delete_expired_links():
    """Delete expired links from history."""
    if not os.path.exists(HISTORY_FILE):
        console.print("[bold red]History not found.[/bold red]", style="bold red")
        return

    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)
    
    current_time = time.time()
    history = [entry for entry in history if not (entry.get("expiry_timestamp") and current_time > entry["expiry_timestamp"])]
    
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def update_link(custom_name, new_long_url=None, new_expiry_seconds=None):
    """Update an existing link in history."""
    if not os.path.exists(HISTORY_FILE):
        console.print("[bold red]History not found.[/bold red]", style="bold red")
        return

    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)

    updated = False
    for entry in history:
        if entry.get('custom_name') == custom_name:
            if new_long_url:
                if is_valid_url(new_long_url):
                    entry['long_url'] = new_long_url
                    entry['short_url'] = shorten_url(new_long_url)
                else:
                    console.print("[bold red]New URL is not valid.[/bold red]", style="bold red")
                    return
            if new_expiry_seconds is not None:
                entry['expiry_timestamp'] = time.time() + new_expiry_seconds
            updated = True
            break
    
    if updated:
        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)
        console.print("[bold green]Link updated successfully.[/bold green]", style="bold green")
    else:
        console.print("[bold red]Link not found.[/bold red]", style="bold red")

def shorten_url_from_clipboard():
    """Shorten the URL from the clipboard."""
    long_url = pyperclip.paste()
    if not is_valid_url(long_url):
        console.print("[bold red]Clipboard does not contain a valid URL.[/bold red]", style="bold red")
        return
    
    short_url = shorten_url(long_url)
    console.print(f"[bold cyan]Shortened URL: {short_url}[/bold cyan]")
    if "Error" not in short_url:
        save_to_history(long_url, short_url)

def remind_expiring_links():
    """Remind about links that are about to expire."""
    if not os.path.exists(HISTORY_FILE):
        console.print("[bold red]History not found.[/bold red]", style="bold red")
        return

    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)

    current_time = time.time()
    for entry in history:
        expiry_timestamp = entry.get("expiry_timestamp")
        if expiry_timestamp and (expiry_timestamp - current_time) <= 3600:  # 1 hour
            console.print(f"[bold yellow]Reminder: Link '{entry['short_url']}' is about to expire.[/bold yellow]")
            console.print(f"[bold white]Long URL: {entry['long_url']}[/bold white]")
            console.print(f"[bold red]Expires at: {time.ctime(expiry_timestamp)}[/bold red]")
            console.print("-" * 40)

def show_about():
    """Display information about the application."""
    console.print(Panel(
        "[bold bright_cyan]URL Shortener Code\nContact me: https://github.com/lysandraBars\nAuthor: T7C\nDescription: This code helps to shorten URLs and manage the history of shortened links.[/bold bright_cyan]",
        title="[bold bright_magenta]About[/bold bright_magenta]",
        border_style="bold bright_magenta",
        padding=(1, 2),
        expand=True
    ))

def get_file():
    """Display the file path of the history."""
    if os.path.exists(HISTORY_FILE):
        console.print(f"[bold bright_cyan]History saved at: {os.path.abspath(HISTORY_FILE)}[/bold bright_cyan]")
    else:
        console.print("[bold red]History not found.[/bold red]", style="bold red")

def usega():
    """Display a placeholder message for 'Usega' functionality."""
    console.print("[bold bright_cyan]Usega functionality not implemented in this version.[/bold bright_cyan]")

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        console.print(Panel(
            "[bold bright_cyan][1] Shorten URL\n[2] View History\n[3] Update Link\n[4] Delete Expired Links\n[5] Shorten URL from Clipboard\n[6] Remind About Expiring Links\n[7] Other\n[8] Exit[/bold bright_cyan]",
            title="[bold bright_magenta]URL SHORTENER - @T7C[/bold bright_magenta]",
            border_style="bold bright_magenta",
            padding=(1, 2),
            expand=True
        ))

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            while True:
                long_url = input("Enter URL to shorten: ").strip()
                if long_url and is_valid_url(long_url):
                    break
                elif not long_url:
                    console.print("[bold red]URL cannot be empty.[/bold red]", style="bold red")
                else:
                    console.print("[bold red]Invalid URL format.[/bold red]", style="bold red")
            
            custom_name = input("Enter custom name (optional): ").strip() or None
            expiry_seconds = input("Enter expiry time in seconds (optional): ").strip()
            expiry_seconds = int(expiry_seconds) if expiry_seconds.isdigit() else None
            
            short_url = shorten_url(long_url)
            console.print(f"[bold cyan]Shortened URL: {short_url}[/bold cyan]")
            if "Error" not in short_url:
                save_to_history(long_url, short_url, custom_name, expiry_seconds)

        elif choice == "2":
            show_history()

        elif choice == "3":
            custom_name = input("Enter the custom name of the link to update: ").strip()
            if custom_name:
                new_long_url = input("Enter new long URL (optional): ").strip() or None
                new_expiry_seconds = input("Enter new expiry time in seconds (optional): ").strip()
                new_expiry_seconds = int(new_expiry_seconds) if new_expiry_seconds.isdigit() else None
                update_link(custom_name, new_long_url, new_expiry_seconds)
            else:
                console.print("[bold red]Custom name cannot be empty.[/bold red]", style="bold red")

        elif choice == "4":
            delete_expired_links()

        elif choice == "5":
            shorten_url_from_clipboard()

        elif choice == "6":
            remind_expiring_links()

        elif choice == "7":
            while True:
                console.print(Panel(
                    "[bold bright_cyan][1] View About\n[2] Get File Path\n[3] Usega\n[4] Back to Main Menu[/bold bright_cyan]",
                    title="[bold bright_magenta]Other[/bold bright_magenta]",
                    border_style="bold bright_magenta",
                    padding=(1, 2),
                    expand=True
                ))

                sub_choice = input("Enter your choice: ").strip()

                if sub_choice == "1":
                    show_about()

                elif sub_choice == "2":
                    get_file()

                elif sub_choice == "3":
                    usega()

                elif sub_choice == "4":
                    break

                else:
                    console.print("[bold red]Invalid choice, please try again.[/bold red]", style="bold red")

        elif choice == "8":
            console.print("[bold green]Exiting the application...[/bold green]")
            break

        else:
            console.print("[bold red]Invalid choice, please try again.[/bold red]", style="bold red")

if __name__ == "__main__":
    print_ascii_title()
    main_menu()
