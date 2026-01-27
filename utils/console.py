"""
Console utilities for the Cinema Ticket project.

Provides functions for:
- Clearing the screen
- Printing formatted menus and messages
"""

import os
import platform
from typing import List, Optional

def clear_screen() -> None:
    """Clears the terminal screen"""

    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)


def print_title(title: str) -> None:
    """Print a centered title with decorative lines."""

    clear_screen()
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)
    print()


def print_menu(options: list[str], title: Optional[str] = None) -> None:
    """Prints a numbered menu."""

    if title:
        print_title(title)
    else:
        clear_screen()

    for i, option in enumerate(options, 1):
        print(f"    {i}. {option}")

    print()
    print("-" * 60)


def get_choice(max_choice: int, prompt: str = "your choice: ") -> int:
    """Gets a valid numeric choice from user."""

    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= max_choice:
                return choice
            else:
                print("Enter a valid number!")

        except ValueError:
            print("Enter a valid input")


def get_input(prompt: str, required: bool =True) -> str:
    """Gets string input from users and returns str: User input (stripped)."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("Empty input not allowed!")


def print_success(message: str) -> None:
    """Prints a success message in green (if supported)."""
    print(f"\n✅ {message}\n")


def print_error(message: str) -> None:
    """Prints an error message in red (if supported)."""
    print(f"\n❌ {message}\n")


def print_info(message: str) -> None:
    """Prints an info message."""
    print(f"\nℹ️  {message}\n")





