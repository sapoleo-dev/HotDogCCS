# Funciones de utilidad de operacion.

from typing import Optional, List


def get_valid_integer(prompt: str, min_value: Optional[int] = None, 
                      max_value: Optional[int] = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Valor debe ser al menos {min_value}. Porfavor intentalo de nuevo.")
                continue
            if max_value is not None and value > max_value:
                print(f"Valor debe ser maximo {max_value}. Porfavor intentalo de nuevo.")
                continue
            return value
        except ValueError:
            print("Invalido. Pon un numero valido.")


def get_valid_string(prompt: str, allow_empty: bool = False) -> str:
    while True:
        value = input(prompt).strip()
        if not allow_empty and not value:
            print("No se puede estar en blanco el valor. Porfavor intentalo de nuevo.")
            continue
        return value


def get_yes_no(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} (S/N): ").strip().upper()
        if response in ['S', 'SI']:
            return True
        elif response in ['N', 'NO']:
            return False
        else:
            print("Invalido. Porfavor escriba S or N.")


def print_header(text: str, char: str = "=") -> None:
    print(f"\n{char * 60}")
    print(f"{text:^60}")
    print(f"{char * 60}")


def print_section(text: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {text}")
    print(f"{'─' * 60}")


def pause() -> None:
    input("\nPresiona enter para continuar...")


def clear_screen() -> None:
    import os
    os.system('cls' if os.name == 'nt' else 'clear')