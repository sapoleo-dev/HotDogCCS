# Busqueda del stock de cada ingrediente.

from typing import Dict
from data_manager import DataManager
from ingredient_manager import IngredientManager
from utils import (get_valid_integer, get_valid_string, 
                   print_header, print_section, pause)


class InventoryManager:
    
    def __init__(self, data_manager: DataManager, ingredient_manager: IngredientManager):
        self.data_manager = data_manager
        self.ingredient_manager = ingredient_manager
    
    def get_inventory(self) -> Dict[str, int]:
        return self.data_manager.get_inventory()
    
    def get_quantity(self, ingredient_id: str) -> int:
        return self.get_inventory().get(ingredient_id, 0)
    
    def update_quantity(self, ingredient_id: str, quantity: int) -> None:
        self.data_manager.update_inventory(ingredient_id, quantity)
    
    def add_quantity(self, ingredient_id: str, amount: int) -> None:
        current = self.get_quantity(ingredient_id)
        new_quantity = max(0, current + amount)
        self.update_quantity(ingredient_id, new_quantity)
    
    def check_availability(self, ingredient_id: str, required_amount: int = 1) -> bool:
        return self.get_quantity(ingredient_id) >= required_amount
    
    def check_multiple_availability(self, requirements: Dict[str, int]) -> tuple:
        missing = []
        for ing_id, required in requirements.items():
            if not self.check_availability(ing_id, required):
                available = self.get_quantity(ing_id)
                ingredient = self.ingredient_manager.get_ingredient_by_id(ing_id)
                ing_name = ingredient.name if ingredient else ing_id
                missing.append({
                    'id': ing_id,
                    'name': ing_name,
                    'required': required,
                    'available': available
                })
        
        return (len(missing) == 0, missing)
    
    def consume_ingredients(self, requirements: Dict[str, int]) -> bool:
        all_available, missing = self.check_multiple_availability(requirements)
        
        if not all_available:
            return False
        
        for ing_id, quantity in requirements.items():
            self.add_quantity(ing_id, -quantity)
        
        return True
    
    def view_full_inventory(self) -> None:
        print_header("INVENTARIO COMPLETO")
        
        ingredients = self.ingredient_manager.get_ingredients()
        inventory = self.get_inventory()
        
        if not ingredients:
            print("\nNo hay ingredientes en el sistema.")
            return
        
        for category in self.ingredient_manager.CATEGORIES:
            category_items = self.ingredient_manager.get_by_category(category)
            if category_items:
                print_section(f"{category}")
                for ing in sorted(category_items, key=lambda x: x.name):
                    quantity = inventory.get(ing.id, 0)
                    status = "✓" if quantity > 10 else "!" if quantity > 0 else "X"
                    print(f"  {status} {ing.name:30} | Cantidad: {quantity:5}")
    
    def search_ingredient_quantity(self) -> None:
        print_header("CANTIDAD DE INGREDIENTES")
        
        search_term = get_valid_string("\nIngrediente para buscar: ")
        
        ingredients = self.ingredient_manager.get_ingredients()
        inventory = self.get_inventory()
        
        matches = [ing for ing in ingredients.values() 
                   if search_term.lower() in ing.name.lower()]
        
        if not matches:
            print(f"\nNo se encontraron ingredientes '{search_term}'")
            return
        
        print(f"\nSe encontro {len(matches)} ingrediente(s):")
        for ing in matches:
            quantity = inventory.get(ing.id, 0)
            print(f"  • {ing.name:30} | Cantidad: {quantity:5}")
    
    def list_category_inventory(self) -> None:
        print_header("INVENTARIO POR CATEGORIA")
        
        print("\nSelecciona una categoria:")
        for i, cat in enumerate(self.ingredient_manager.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer(
            "\nElije: ", 1, len(self.ingredient_manager.CATEGORIES)
        )
        category = self.ingredient_manager.CATEGORIES[choice - 1]
        
        items = self.ingredient_manager.get_by_category(category)
        inventory = self.get_inventory()
        
        print_section(f"Inventario de {category}")
        if items:
            for ing in sorted(items, key=lambda x: x.name):
                quantity = inventory.get(ing.id, 0)
                status = "✓" if quantity > 10 else "!" if quantity > 0 else "X"
                print(f"  {status} {ing.name:30} | Qty: {quantity:5}")
        else:
            print(f"No hay ingredientes en la categoria {category}.")
    
    def update_ingredient_quantity(self) -> None:
        print_header("ACTUALIZAR CANTIDAD DE INGREDIENTES")
        
        search_term = get_valid_string("\nIngrediente para buscar: ")
        
        ingredients = self.ingredient_manager.get_ingredients()
        matches = [ing for ing in ingredients.values() 
                   if search_term.lower() in ing.name.lower()]
        
        if not matches:
            print(f"\nNo se encontraron ingredientes '{search_term}'")
            return
        
        if len(matches) > 1:
            print(f"\nSe encontro {len(matches)} ingrediente(s). Selecciona uno:")
            for i, ing in enumerate(matches, 1):
                current_qty = self.get_quantity(ing.id)
                print(f"  {i}. {ing.name} (Cantidad actual: {current_qty})")
            
            choice = get_valid_integer("\nElije: ", 1, len(matches))
            ingredient = matches[choice - 1]
        else:
            ingredient = matches[0]
        
        current_qty = self.get_quantity(ingredient.id)
        print(f"\nCantidad actual de '{ingredient.name}': {current_qty}")
        
        print("\n1. Poner nueva cantidad")
        print("2. añadir a cantidad actual")
        print("3. Substraer de cantidad actual")
        
        action = get_valid_integer("\nSeleccionar accion: ", 1, 3)
        
        if action == 1:
            new_qty = get_valid_integer("Nueva cantidad: ", min_value=0)
            self.update_quantity(ingredient.id, new_qty)
            print(f"\nCantidad actualizada: {current_qty} → {new_qty}")
        elif action == 2:
            amount = get_valid_integer("Cantidad para añadir: ", min_value=0)
            self.add_quantity(ingredient.id, amount)
            new_qty = self.get_quantity(ingredient.id)
            print(f"\nCantidad actualizada: {current_qty} → {new_qty}")
        else:
            amount = get_valid_integer("Cantidad para substraer: ", min_value=0)
            self.add_quantity(ingredient.id, -amount)
            new_qty = self.get_quantity(ingredient.id)
            print(f"\nCantidad actualizada: {current_qty} → {new_qty}")
    
    def show_menu(self) -> None:
        while True:
            print_header("MANEJO DE INVENTARIO")
            print("\n1. Ver inventario completo")
            print("2. Buscar cantidad de ingrediente")
            print("3. Ver inventario por categoria")
            print("4. Actualizar cantidad de ingrediente")
            print("5. Volver")
            
            choice = get_valid_integer("\nElije: ", 1, 5)
            
            if choice == 1:
                self.view_full_inventory()
                pause()
            elif choice == 2:
                self.search_ingredient_quantity()
                pause()
            elif choice == 3:
                self.list_category_inventory()
                pause()
            elif choice == 4:
                self.update_ingredient_quantity()
                pause()
            elif choice == 5:
                break