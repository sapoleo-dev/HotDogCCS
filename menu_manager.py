"""
Module 3: Menu Management
Manages the list of hot dogs offered for sale.
"""

from typing import Dict, List, Optional
from models import HotDog, Ingredient
from data_manager import DataManager
from ingredient_manager import IngredientManager
from inventory_manager import InventoryManager
from utils import (get_valid_integer, get_valid_string, get_yes_no,
                   print_header, print_section, pause)
import uuid


class MenuManager:
    """
    Manages the hot dog menu.
    """
    
    def __init__(self, data_manager: DataManager, 
                 ingredient_manager: IngredientManager,
                 inventory_manager: InventoryManager):
        """
        Initialize the menu manager.
        
        Args:
            data_manager: DataManager instance
            ingredient_manager: IngredientManager instance
            inventory_manager: InventoryManager instance
        """
        self.data_manager = data_manager
        self.ingredient_manager = ingredient_manager
        self.inventory_manager = inventory_manager
    
    def get_hotdogs(self) -> Dict[str, HotDog]:
        """Get all hot dogs."""
        return self.data_manager.get_hotdogs()
    
    def get_hotdog_by_id(self, hotdog_id: str) -> Optional[HotDog]:
        """Get hot dog by ID."""
        return self.get_hotdogs().get(hotdog_id)
    
    def get_hotdogs_using_ingredient(self, ingredient_id: str) -> List[HotDog]:
        """
        Get all hot dogs that use a specific ingredient.
        
        Args:
            ingredient_id: Ingredient ID to search for
        
        Returns:
            List of hot dogs using that ingredient
        """
        return [hd for hd in self.get_hotdogs().values() 
                if ingredient_id in hd.get_all_ingredient_ids()]
    
    def display_hotdog_details(self, hotdog: HotDog) -> None:
        """
        Display detailed information about a hot dog.
        
        Args:
            hotdog: HotDog instance
        """
        print(f"\n🌭 {hotdog.name}")
        print(f"   ID: {hotdog.id}")
        
        # Pan
        pan = self.ingredient_manager.get_ingredient_by_id(hotdog.pan_id)
        print(f"   📦 Pan: {pan.name if pan else 'Unknown'}")
        
        # Salchicha
        salchicha = self.ingredient_manager.get_ingredient_by_id(hotdog.salchicha_id)
        print(f"   🌭 Salchicha: {salchicha.name if salchicha else 'Unknown'}")
        
        # Toppings
        if hotdog.topping_ids:
            print(f"   🥗 Toppings:")
            for tid in hotdog.topping_ids:
                topping = self.ingredient_manager.get_ingredient_by_id(tid)
                print(f"      • {topping.name if topping else 'Unknown'}")
        
        # Salsas
        if hotdog.salsa_ids:
            print(f"   🍅 Salsas:")
            for sid in hotdog.salsa_ids:
                salsa = self.ingredient_manager.get_ingredient_by_id(sid)
                print(f"      • {salsa.name if salsa else 'Unknown'}")
        
        # Acompañante
        if hotdog.acompañante_id:
            acomp = self.ingredient_manager.get_ingredient_by_id(hotdog.acompañante_id)
            print(f"   🍟 Side: {acomp.name if acomp else 'Unknown'}")
    
    def view_menu(self) -> None:
        """Display all hot dogs on the menu."""
        print_header("HOT DOG MENU")
        
        hotdogs = self.get_hotdogs()
        
        if not hotdogs:
            print("\n❌ No hot dogs on the menu yet.")
            return
        
        print(f"\n📋 Total: {len(hotdogs)} hot dog(s)\n")
        
        for hd in sorted(hotdogs.values(), key=lambda x: x.name):
            self.display_hotdog_details(hd)
    
    def check_hotdog_availability(self) -> None:
        """Check if there's enough inventory to sell a specific hot dog."""
        print_header("CHECK HOT DOG AVAILABILITY")
        
        hotdogs = self.get_hotdogs()
        
        if not hotdogs:
            print("\n❌ No hot dogs on the menu.")
            return
        
        # Display menu
        hd_list = list(hotdogs.values())
        print("\nSelect a hot dog:")
        for i, hd in enumerate(hd_list, 1):
            print(f"  {i}. {hd.name}")
        
        choice = get_valid_integer("\nEnter choice: ", 1, len(hd_list))
        hotdog = hd_list[choice - 1]
        
        # Check availability
        requirements = {ing_id: 1 for ing_id in hotdog.get_all_ingredient_ids()}
        available, missing = self.inventory_manager.check_multiple_availability(requirements)
        
        print(f"\n🌭 {hotdog.name}")
        
        if available:
            print("✅ CAN BE SOLD - All ingredients available!")
        else:
            print("❌ CANNOT BE SOLD - Missing ingredients:")
            for item in missing:
                print(f"   • {item['name']}: Need {item['required']}, Have {item['available']}")
    
    def select_ingredient_from_category(self, category: str, 
                                       allow_cancel: bool = True,
                                       allow_multiple: bool = False) -> Optional[List[str]]:
        """
        Let user select ingredient(s) from a category.
        
        Args:
            category: Category to select from
            allow_cancel: Whether to allow cancellation
            allow_multiple: Whether to allow multiple selections
        
        Returns:
            List of selected ingredient IDs, or None if cancelled
        """
        items = self.ingredient_manager.get_by_category(category)
        
        if not items:
            print(f"\n❌ No {category} ingredients available.")
            if allow_cancel:
                return None
            return []
        
        print(f"\nSelect {category}:")
        for i, ing in enumerate(items, 1):
            qty = self.inventory_manager.get_quantity(ing.id)
            status = "✅" if qty > 0 else "❌"
            print(f"  {i}. {ing.name} (Stock: {qty}) {status}")
        
        if allow_cancel:
            print(f"  {len(items) + 1}. Cancel")
        
        if allow_multiple:
            print("\nEnter numbers separated by commas (e.g., 1,3,4) or 0 to skip:")
            selection = input("> ").strip()
            
            if selection == "0":
                return []
            
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                selected_ids = []
                for idx in indices:
                    if 1 <= idx <= len(items):
                        selected_ids.append(items[idx - 1].id)
                return selected_ids
            except ValueError:
                print("❌ Invalid input.")
                return self.select_ingredient_from_category(category, allow_cancel, allow_multiple)
        else:
            max_choice = len(items) + 1 if allow_cancel else len(items)
            choice = get_valid_integer("\nEnter choice: ", 1, max_choice)
            
            if allow_cancel and choice == len(items) + 1:
                return None
            
            return [items[choice - 1].id]
    
    def add_hotdog(self) -> None:
        """Add a new hot dog to the menu with validations."""
        print_header("ADD NEW HOT DOG")
        
        name = get_valid_string("\nEnter hot dog name: ")
        
        # Select Pan (required)
        print_section("Select Bread (Pan)")
        pan_ids = self.select_ingredient_from_category('Pan', allow_cancel=True)
        if pan_ids is None:
            print("❌ Operation cancelled.")
            return
        pan_id = pan_ids[0]
        pan = self.ingredient_manager.get_ingredient_by_id(pan_id)
        
        # Select Salchicha (required)
        print_section("Select Sausage (Salchicha)")
        salchicha_ids = self.select_ingredient_from_category('Salchicha', allow_cancel=True)
        if salchicha_ids is None:
            print("❌ Operation cancelled.")
            return
        salchicha_id = salchicha_ids[0]
        salchicha = self.ingredient_manager.get_ingredient_by_id(salchicha_id)
        
        # Length validation
        if pan and salchicha and pan.length and salchicha.length:
            if pan.length != salchicha.length:
                print(f"\n⚠️  WARNING: Length mismatch!")
                print(f"   Pan length: {pan.length}")
                print(f"   Salchicha length: {salchicha.length}")
                
                if not get_yes_no("Do you want to proceed anyway?"):
                    print("❌ Operation cancelled.")
                    return
        
        # Select Toppings (multiple, optional)
        print_section("Select Toppings (Optional, Multiple)")
        topping_ids = self.select_ingredient_from_category('Topping', 
                                                           allow_cancel=False,
                                                           allow_multiple=True)
        
        # Select Salsas (multiple, optional)
        print_section("Select Salsas (Optional, Multiple)")
        salsa_ids = self.select_ingredient_from_category('Salsa', 
                                                         allow_cancel=False,
                                                         allow_multiple=True)
        
        # Select Acompañante (single, optional)
        print_section("Select Side Dish (Acompañante) - Optional")
        print("Would you like to add a side dish?")
        if get_yes_no("Add side?"):
            acomp_ids = self.select_ingredient_from_category('Acompañante', allow_cancel=True)
            acompañante_id = acomp_ids[0] if acomp_ids else None
        else:
            acompañante_id = None
        
        # Check inventory for all ingredients
        all_ingredient_ids = [pan_id, salchicha_id] + topping_ids + salsa_ids
        if acompañante_id:
            all_ingredient_ids.append(acompañante_id)
        
        zero_stock = []
        for ing_id in all_ingredient_ids:
            if self.inventory_manager.get_quantity(ing_id) == 0:
                ing = self.ingredient_manager.get_ingredient_by_id(ing_id)
                zero_stock.append(ing.name if ing else ing_id)
        
        if zero_stock:
            print("\n⚠️  WARNING: The following ingredients have 0 stock:")
            for ing_name in zero_stock:
                print(f"   • {ing_name}")
            print("\nYou can still add this hot dog, but it cannot be sold until restocked.")
        
        # Create hot dog
        hotdog_id = str(uuid.uuid4())
        hotdog = HotDog(
            id=hotdog_id,
            name=name,
            pan_id=pan_id,
            salchicha_id=salchicha_id,
            topping_ids=topping_ids,
            salsa_ids=salsa_ids,
            acompañante_id=acompañante_id
        )
        
        # Add to menu
        self.data_manager.add_hotdog(hotdog)
        
        print(f"\n✅ Hot dog '{name}' added to menu successfully!")
    
    def delete_hotdog_by_id(self, hotdog_id: str, skip_confirmation: bool = False) -> None:
        """
        Delete a hot dog by ID.
        
        Args:
            hotdog_id: Hot dog ID
            skip_confirmation: Skip confirmation prompt
        """
        hotdog = self.get_hotdog_by_id(hotdog_id)
        if not hotdog:
            return
        
        if not skip_confirmation:
            # Check if all ingredients are available
            requirements = {ing_id: 1 for ing_id in hotdog.get_all_ingredient_ids()}
            available, missing = self.inventory_manager.check_multiple_availability(requirements)
            
            if available:
                print(f"\n⚠️  WARNING: There is enough inventory to sell '{hotdog.name}'!")
                if not get_yes_no("Are you sure you want to delete it?"):
                    print("❌ Operation cancelled.")
                    return
        
        self.data_manager.remove_hotdog(hotdog_id)
        if not skip_confirmation:
            print(f"\n✅ Hot dog '{hotdog.name}' deleted successfully!")
    
    def delete_hotdog(self) -> None:
        """Delete a hot dog from the menu."""
        print_header("DELETE HOT DOG")
        
        hotdogs = self.get_hotdogs()
        
        if not hotdogs:
            print("\n❌ No hot dogs on the menu.")
            return
        
        # Display menu
        hd_list = list(hotdogs.values())
        print("\nSelect hot dog to delete:")
        for i, hd in enumerate(hd_list, 1):
            print(f"  {i}. {hd.name}")
        print(f"  {len(hd_list) + 1}. Cancel")
        
        choice = get_valid_integer("\nEnter choice: ", 1, len(hd_list) + 1)
        
        if choice == len(hd_list) + 1:
            print("❌ Operation cancelled.")
            return
        
        hotdog = hd_list[choice - 1]
        self.delete_hotdog_by_id(hotdog.id)
    
    def show_menu(self) -> None:
        """Display menu management menu."""
        while True:
            print_header("MENU MANAGEMENT")
            print("\n1. View menu")
            print("2. Check hot dog availability")
            print("3. Add new hot dog")
            print("4. Delete hot dog")
            print("5. Back to main menu")
            
            choice = get_valid_integer("\nEnter your choice: ", 1, 5)
            
            if choice == 1:
                self.view_menu()
                pause()
            elif choice == 2:
                self.check_hotdog_availability()
                pause()
            elif choice == 3:
                self.add_hotdog()
                pause()
            elif choice == 4:
                self.delete_hotdog()
                pause()
            elif choice == 5:
                break