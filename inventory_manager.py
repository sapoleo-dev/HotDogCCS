"""
Module 2: Inventory Management
Tracks the quantity (stock) of each ingredient.
"""

from typing import Dict
from data_manager import DataManager
from ingredient_manager import IngredientManager
from utils import (get_valid_integer, get_valid_string, 
                   print_header, print_section, pause)


class InventoryManager:
    """
    Manages inventory quantities for all ingredients.
    """
    
    def __init__(self, data_manager: DataManager, ingredient_manager: IngredientManager):
        """
        Initialize the inventory manager.
        
        Args:
            data_manager: DataManager instance
            ingredient_manager: IngredientManager instance
        """
        self.data_manager = data_manager
        self.ingredient_manager = ingredient_manager
    
    def get_inventory(self) -> Dict[str, int]:
        """Get current inventory."""
        return self.data_manager.get_inventory()
    
    def get_quantity(self, ingredient_id: str) -> int:
        """
        Get quantity of a specific ingredient.
        
        Args:
            ingredient_id: Ingredient ID
        
        Returns:
            Quantity (0 if not found)
        """
        return self.get_inventory().get(ingredient_id, 0)
    
    def update_quantity(self, ingredient_id: str, quantity: int) -> None:
        """
        Update quantity of an ingredient.
        
        Args:
            ingredient_id: Ingredient ID
            quantity: New quantity
        """
        self.data_manager.update_inventory(ingredient_id, quantity)
    
    def add_quantity(self, ingredient_id: str, amount: int) -> None:
        """
        Add to existing quantity.
        
        Args:
            ingredient_id: Ingredient ID
            amount: Amount to add (can be negative)
        """
        current = self.get_quantity(ingredient_id)
        new_quantity = max(0, current + amount)  # Don't go below 0
        self.update_quantity(ingredient_id, new_quantity)
    
    def check_availability(self, ingredient_id: str, required_amount: int = 1) -> bool:
        """
        Check if enough quantity is available.
        
        Args:
            ingredient_id: Ingredient ID
            required_amount: Required quantity
        
        Returns:
            True if available, False otherwise
        """
        return self.get_quantity(ingredient_id) >= required_amount
    
    def check_multiple_availability(self, requirements: Dict[str, int]) -> tuple:
        """
        Check availability for multiple ingredients.
        
        Args:
            requirements: Dict of {ingredient_id: required_quantity}
        
        Returns:
            Tuple of (all_available: bool, missing_items: list)
        """
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
        """
        Consume (subtract) ingredients from inventory.
        
        Args:
            requirements: Dict of {ingredient_id: quantity_to_consume}
        
        Returns:
            True if successful, False if not enough inventory
        """
        # First check if all are available
        all_available, missing = self.check_multiple_availability(requirements)
        
        if not all_available:
            return False
        
        # Consume all ingredients
        for ing_id, quantity in requirements.items():
            self.add_quantity(ing_id, -quantity)
        
        return True
    
    def view_full_inventory(self) -> None:
        """Display the complete inventory."""
        print_header("COMPLETE INVENTORY")
        
        ingredients = self.ingredient_manager.get_ingredients()
        inventory = self.get_inventory()
        
        if not ingredients:
            print("\n❌ No ingredients in system.")
            return
        
        for category in self.ingredient_manager.CATEGORIES:
            category_items = self.ingredient_manager.get_by_category(category)
            if category_items:
                print_section(f"{category}")
                for ing in sorted(category_items, key=lambda x: x.name):
                    quantity = inventory.get(ing.id, 0)
                    status = "✅" if quantity > 10 else "⚠️ " if quantity > 0 else "❌"
                    print(f"  {status} {ing.name:30} | Qty: {quantity:5}")
    
    def search_ingredient_quantity(self) -> None:
        """Search and display quantity of a specific ingredient."""
        print_header("SEARCH INGREDIENT QUANTITY")
        
        search_term = get_valid_string("\nEnter ingredient name to search: ")
        
        ingredients = self.ingredient_manager.get_ingredients()
        inventory = self.get_inventory()
        
        matches = [ing for ing in ingredients.values() 
                   if search_term.lower() in ing.name.lower()]
        
        if not matches:
            print(f"\n❌ No ingredients found matching '{search_term}'")
            return
        
        print(f"\n✅ Found {len(matches)} match(es):")
        for ing in matches:
            quantity = inventory.get(ing.id, 0)
            print(f"  • {ing.name:30} | Qty: {quantity:5}")
    
    def list_category_inventory(self) -> None:
        """Display inventory for a specific category."""
        print_header("INVENTORY BY CATEGORY")
        
        print("\nSelect a category:")
        for i, cat in enumerate(self.ingredient_manager.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer(
            "\nEnter choice: ", 1, len(self.ingredient_manager.CATEGORIES)
        )
        category = self.ingredient_manager.CATEGORIES[choice - 1]
        
        items = self.ingredient_manager.get_by_category(category)
        inventory = self.get_inventory()
        
        print_section(f"{category} Inventory")
        if items:
            for ing in sorted(items, key=lambda x: x.name):
                quantity = inventory.get(ing.id, 0)
                status = "✅" if quantity > 10 else "⚠️ " if quantity > 0 else "❌"
                print(f"  {status} {ing.name:30} | Qty: {quantity:5}")
        else:
            print(f"  No ingredients in {category} category.")
    
    def update_ingredient_quantity(self) -> None:
        """Update the quantity of a specific ingredient."""
        print_header("UPDATE INGREDIENT QUANTITY")
        
        search_term = get_valid_string("\nEnter ingredient name to search: ")
        
        ingredients = self.ingredient_manager.get_ingredients()
        matches = [ing for ing in ingredients.values() 
                   if search_term.lower() in ing.name.lower()]
        
        if not matches:
            print(f"\n❌ No ingredients found matching '{search_term}'")
            return
        
        if len(matches) > 1:
            print(f"\nFound {len(matches)} matches. Select one:")
            for i, ing in enumerate(matches, 1):
                current_qty = self.get_quantity(ing.id)
                print(f"  {i}. {ing.name} (Current: {current_qty})")
            
            choice = get_valid_integer("\nEnter choice: ", 1, len(matches))
            ingredient = matches[choice - 1]
        else:
            ingredient = matches[0]
        
        current_qty = self.get_quantity(ingredient.id)
        print(f"\nCurrent quantity of '{ingredient.name}': {current_qty}")
        
        print("\n1. Set new quantity")
        print("2. Add to current quantity")
        print("3. Subtract from current quantity")
        
        action = get_valid_integer("\nSelect action: ", 1, 3)
        
        if action == 1:
            new_qty = get_valid_integer("Enter new quantity: ", min_value=0)
            self.update_quantity(ingredient.id, new_qty)
            print(f"\n✅ Quantity updated: {current_qty} → {new_qty}")
        elif action == 2:
            amount = get_valid_integer("Enter amount to add: ", min_value=0)
            self.add_quantity(ingredient.id, amount)
            new_qty = self.get_quantity(ingredient.id)
            print(f"\n✅ Quantity updated: {current_qty} → {new_qty}")
        else:  # action == 3
            amount = get_valid_integer("Enter amount to subtract: ", min_value=0)
            self.add_quantity(ingredient.id, -amount)
            new_qty = self.get_quantity(ingredient.id)
            print(f"\n✅ Quantity updated: {current_qty} → {new_qty}")
    
    def show_menu(self) -> None:
        """Display inventory management menu."""
        while True:
            print_header("INVENTORY MANAGEMENT")
            print("\n1. View full inventory")
            print("2. Search ingredient quantity")
            print("3. View inventory by category")
            print("4. Update ingredient quantity")
            print("5. Back to main menu")
            
            choice = get_valid_integer("\nEnter your choice: ", 1, 5)
            
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