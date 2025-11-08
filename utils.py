"""
Utility functions for input validation and common operations.
"""

from typing import Optional, List


def get_valid_integer(prompt: str, min_value: Optional[int] = None, 
                      max_value: Optional[int] = None) -> int:
    """
    Get a valid integer from user input with optional range validation.
    
    Args:
        prompt: The prompt to display to the user
        min_value: Minimum acceptable value (inclusive)
        max_value: Maximum acceptable value (inclusive)
    
    Returns:
        Valid integer from user
    """
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"❌ Value must be at least {min_value}. Please try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"❌ Value must be at most {max_value}. Please try again.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")


def get_valid_string(prompt: str, allow_empty: bool = False) -> str:
    """
    Get a valid non-empty string from user input.
    
    Args:
        prompt: The prompt to display to the user
        allow_empty: Whether to allow empty strings
    
    Returns:
        Valid string from user
    """
    while True:
        value = input(prompt).strip()
        if not allow_empty and not value:
            print("❌ Input cannot be empty. Please try again.")
            continue
        return value


def get_yes_no(prompt: str) -> bool:
    """
    Get a yes/no answer from the user.
    
    Args:
        prompt: The prompt to display to the user
    
    Returns:
        True for yes, False for no
    """
    while True:
        response = input(f"{prompt} (Y/N): ").strip().upper()
        if response in ['Y', 'YES']:
            return True
        elif response in ['N', 'NO']:
            return False
        else:
            print("❌ Invalid input. Please enter Y or N.")


def print_header(text: str, char: str = "=") -> None:
    """
    Print a formatted header.
    
    Args:
        text: Header text
        char: Character to use for the border
    """
    print(f"\n{char * 60}")
    print(f"{text:^60}")
    print(f"{char * 60}")


def print_section(text: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'─' * 60}")
    print(f"  {text}")
    print(f"{'─' * 60}")


def pause() -> None:
    """Pause execution until user presses Enter."""
    input("\n⏸  Press Enter to continue...")


def clear_screen() -> None:
    """Clear the console screen (platform independent)."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')