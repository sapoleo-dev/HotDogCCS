"""
Module 1: Ingredient Management
Manages all available ingredients grouped by categories.
"""

from typing import Dict, List, Optional
from models import Ingredient
from data_manager import DataManager
from utils import (get_valid_integer, get_valid_string, get_yes_no,
                   print_header, print_section, pause)
import uuid


class IngredientManager:
    """
    Manages ingredients for the Hot Dog CCS.
    
    Categories: Pan, Salchicha, Topping, Salsa, Acompañante
    """
    
    CATEGORIES = ['Pan', 'Salchicha', 'Topping', 'Salsa', 'Acompañante']
    
    def __init__(self, data_manager: DataManager):
        """
        Initialize the ingredient manager.
        
        Args:
            data_manager: DataManager instance for data operations
        """
        self.data_manager = data_manager
    
    def get_ingredients(self) -> Dict[str, Ingredient]:
        """Get all ingredients."""
        return self.data_manager.get_ingredients()
    
    def get_by_category(self, category: str) -> List[Ingredient]:
        """
        Get all ingredients from a specific category.
        
        Args:
            category: Category name
        
        Returns:
            List of ingredients in that category
        """
        return [ing for ing in self.get_ingredients().values() 
                if ing.category == category]
    
    def get_by_category_and_type(self, category: str, type_name: str) -> List[Ingredient]:
        """
        Get ingredients by category and type.
        
        Args:
            category: Category name
            type_name: Type within category
        
        Returns:
            List of matching ingredients
        """
        return [ing for ing in self.get_by_category(category) 
                if ing.type == type_name]
    
    def get_ingredient_by_id(self, ingredient_id: str) -> Optional[Ingredient]:
        """
        Get ingredient by ID.
        
        Args:
            ingredient_id: Ingredient ID
        
        Returns:
            Ingredient if found, None otherwise
        """
        return self.get_ingredients().get(ingredient_id)
    
    def list_all_ingredients(self) -> None:
        """Display all ingredients grouped by category."""
        print_header("ALL INGREDIENTS")
        
        ingredients = self.get_ingredients()
        if not ingredients:
            print("\n❌ No ingredients available.")
            return
        
        for category in self.CATEGORIES:
            category_items = self.get_by_category(category)
            if category_items:
                print_section(f"{category} ({len(category_items)} items)")
                for ing in sorted(category_items, key=lambda x: x.name):
                    print(f"  • {ing}")
    
    def list_category_ingredients(self) -> None:
        """Display ingredients from a selected category."""
        print_header("INGREDIENTS BY CATEGORY")
        
        print("\nSelect a category:")
        for i, cat in enumerate(self.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer("\nEnter choice: ", 1, len(self.CATEGORIES))
        category = self.CATEGORIES[choice - 1]
        
        items = self.get_by_category(category)
        
        print_section(f"{category} Ingredients ({len(items)} items)")
        if items:
            for ing in sorted(items, key=lambda x: x.name):
                print(f"  • {ing}")
        else:
            print(f"  No ingredients in {category} category.")
    
    def list_by_type(self) -> None:
        """Display ingredients by category and type."""
        print_header("INGREDIENTS BY TYPE")
        
        print("\nSelect a category:")
        for i, cat in enumerate(self.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer("\nEnter choice: ", 1, len(self.CATEGORIES))
        category = self.CATEGORIES[choice - 1]
        
        # Get all unique types in this category
        category_items = self.get_by_category(category)
        types = sorted(set(ing.type for ing in category_items))
        
        if not types:
            print(f"\n❌ No types found in {category} category.")
            return
        
        print(f"\nAvailable types in {category}:")
        for i, type_name in enumerate(types, 1):
            print(f"  {i}. {type_name}")
        
        type_choice = get_valid_integer("\nEnter type choice: ", 1, len(types))
        selected_type = types[type_choice - 1]
        
        items = self.get_by_category_and_type(category, selected_type)
        
        print_section(f"{category} - {selected_type} ({len(items)} items)")
        for ing in sorted(items, key=lambda x: x.name):
            print(f"  • {ing}")
    
    def add_ingredient(self) -> None:
        """Add a new ingredient."""
        print_header("ADD NEW INGREDIENT")
        
        print("\nSelect category:")
        for i, cat in enumerate(self.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer("\nEnter choice: ", 1, len(self.CATEGORIES))
        category = self.CATEGORIES[choice - 1]
        
        name = get_valid_string("\nEnter ingredient name: ")
        type_name = get_valid_string("Enter ingredient type (e.g., normal, large): ")
        
        # Ask for length if Pan or Salchicha
        length = None
        if category in ['Pan', 'Salchicha']:
            length = get_valid_string("Enter length (e.g., small, medium, large): ")
        
        initial_quantity = get_valid_integer(
            "Enter initial inventory quantity: ", min_value=0
        )
        
        # Generate unique ID
        ingredient_id = str(uuid.uuid4())
        
        # Create ingredient
        ingredient = Ingredient(
            id=ingredient_id,
            name=name,
            category=category,
            type=type_name,
            length=length
        )
        
        # Add to data manager
        self.data_manager.add_ingredient(ingredient, initial_quantity)
        
        print(f"\n✅ Ingredient '{name}' added successfully!")
    
    def delete_ingredient(self, menu_manager=None) -> None:
        """
        Delete an ingredient with validation.
        
        Args:
            menu_manager: MenuManager instance to check hot dog dependencies
        """
        print_header("DELETE INGREDIENT")
        
        ingredients = self.get_ingredients()
        if not ingredients:
            print("\n❌ No ingredients available to delete.")
            return
        
        # Display all ingredients
        ing_list = list(ingredients.values())
        print("\nAvailable ingredients:")
        for i, ing in enumerate(ing_list, 1):
            print(f"  {i}. {ing} [ID: {ing.id}]")
        
        print(f"  {len(ing_list) + 1}. Cancel")
        
        choice = get_valid_integer(
            "\nSelect ingredient to delete: ", 1, len(ing_list) + 1
        )
        
        if choice == len(ing_list) + 1:
            print("❌ Operation cancelled.")
            return
        
        ingredient = ing_list[choice - 1]
        
        # Check if ingredient is used in any hot dog
        if menu_manager:
            affected_hotdogs = menu_manager.get_hotdogs_using_ingredient(ingredient.id)
            
            if affected_hotdogs:
                print(f"\n⚠️  WARNING: This ingredient is used in {len(affected_hotdogs)} hot dog(s):")
                for hd in affected_hotdogs:
                    print(f"  • {hd.name}")
                
                print("\n⚠️  Deleting this ingredient will also delete these hot dogs!")
                
                if not get_yes_no("Do you want to proceed?"):
                    print("❌ Operation cancelled.")
                    return
                
                # Delete affected hot dogs
                for hd in affected_hotdogs:
                    menu_manager.delete_hotdog_by_id(hd.id, skip_confirmation=True)
                    print(f"  🗑️  Deleted hot dog: {hd.name}")
        
        # Delete the ingredient
        self.data_manager.remove_ingredient(ingredient.id)
        print(f"\n✅ Ingredient '{ingredient.name}' deleted successfully!")
    
    def show_menu(self, menu_manager=None) -> None:
        """
        Display ingredient management menu.
        
        Args:
            menu_manager: Optional MenuManager for delete validation
        """
        while True:
            print_header("INGREDIENT MANAGEMENT")
            print("\n1. List all ingredients")
            print("2. List ingredients by category")
            print("3. List ingredients by type")
            print("4. Add new ingredient")
            print("5. Delete ingredient")
            print("6. Back to main menu")
            
            choice = get_valid_integer("\nEnter your choice: ", 1, 6)
            
            if choice == 1:
                self.list_all_ingredients()
                pause()
            elif choice == 2:
                self.list_category_ingredients()
                pause()
            elif choice == 3:
                self.list_by_type()
                pause()
            elif choice == 4:
                self.add_ingredient()
                pause()
            elif choice == 5:
                self.delete_ingredient(menu_manager)
                pause()
            elif choice == 6:
                break