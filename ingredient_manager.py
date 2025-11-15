# Manega todos los ingredientes agrupados por categorias.

from typing import Dict, List, Optional
from models import Ingredient
from data_manager import DataManager
from utils import (get_valid_integer, get_valid_string, get_yes_no,
                   print_header, print_section, pause)
import uuid


class IngredientManager:
    
    CATEGORIES = ['Pan', 'Salchicha', 'Topping', 'Salsa', 'Acompañante']
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def get_ingredients(self) -> Dict[str, Ingredient]:
        return self.data_manager.get_ingredients()
    
    def get_by_category(self, category: str) -> List[Ingredient]:
        return [ing for ing in self.get_ingredients().values() 
                if ing.category == category]
    
    def get_by_category_and_type(self, category: str, type_name: str) -> List[Ingredient]:
        return [ing for ing in self.get_by_category(category) 
                if ing.type == type_name]
    
    def get_ingredient_by_id(self, ingredient_id: str) -> Optional[Ingredient]:
        return self.get_ingredients().get(ingredient_id)
    
    def list_all_ingredients(self) -> None:
        print_header("TODOS LOS INGREDIENTES")
        
        ingredients = self.get_ingredients()
        if not ingredients:
            print("\nNo hay ingredientes disponibles")
            return
        
        for category in self.CATEGORIES:
            category_items = self.get_by_category(category)
            if category_items:
                print_section(f"{category} ({len(category_items)} objetos)")
                for ing in sorted(category_items, key=lambda x: x.name):
                    print(f"  • {ing}")
    
    def list_category_ingredients(self) -> None:
        print_header("INGREDIENTES POR CATEGORIA")
        
        print("\nSelecciona una categoria:")
        for i, cat in enumerate(self.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer("\nElije: ", 1, len(self.CATEGORIES))
        category = self.CATEGORIES[choice - 1]
        
        items = self.get_by_category(category)
        
        print_section(f"Ingrediente {category} ({len(items)} objetos)")
        if items:
            for ing in sorted(items, key=lambda x: x.name):
                print(f"  • {ing}")
        else:
            print(f"No hay ingredientes en la categoria {category}.")
    
    def list_by_type(self) -> None:
        print_header("INGREDIENTES POR CATEGORIA")
        
        print("\nSelecciona una categoria:")
        for i, cat in enumerate(self.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer("\nElije: ", 1, len(self.CATEGORIES))
        category = self.CATEGORIES[choice - 1]
        
        category_items = self.get_by_category(category)
        types = sorted(set(ing.type for ing in category_items))
        
        if not types:
            print(f"\nNo se encontraron tipos de ingredientes en la categoria {category}.")
            return
        
        print(f"\nTipos de ingredientes en {category}:")
        for i, type_name in enumerate(types, 1):
            print(f"  {i}. {type_name}")
        
        type_choice = get_valid_integer("\nElije un tipo: ", 1, len(types))
        selected_type = types[type_choice - 1]
        
        items = self.get_by_category_and_type(category, selected_type)
        
        print_section(f"{category} - {selected_type} ({len(items)} objetos)")
        for ing in sorted(items, key=lambda x: x.name):
            print(f"  • {ing}")
    
    def add_ingredient(self) -> None:
        print_header("AGREGA UN INGREDIENTE")
        
        print("\nSelecciona una categoria:")
        for i, cat in enumerate(self.CATEGORIES, 1):
            print(f"  {i}. {cat}")
        
        choice = get_valid_integer("\nElije: ", 1, len(self.CATEGORIES))
        category = self.CATEGORIES[choice - 1]
        
        name = get_valid_string("\nNombre de ingrediente: ")
        type_name = get_valid_string("Tipo de ingrediente (e.g., normal, grande): ")
        
        length = None
        if category in ['Pan', 'Salchicha']:
            length = get_valid_string("Tamaño (e.g., pequeño, mediano, grande): ")
        
        initial_quantity = get_valid_integer(
            "Cantidad de inventario principal: ", min_value=0
        )
        
        ingredient_id = str(uuid.uuid4())
        
        ingredient = Ingredient(
            id=ingredient_id,
            name=name,
            category=category,
            type=type_name,
            length=length
        )
        
        # Add to data manager
        self.data_manager.add_ingredient(ingredient, initial_quantity)
        
        print(f"\nIngrediente '{name}' se añadio exitosamente!")
    
    def delete_ingredient(self, menu_manager=None) -> None:
        print_header("BORRAR INGREDIENTE")
        
        ingredients = self.get_ingredients()
        if not ingredients:
            print("\nNo hay ingredientes para borrar.")
            return
        
        ing_list = list(ingredients.values())
        print("\nIngredientes disponibles:")
        for i, ing in enumerate(ing_list, 1):
            print(f"  {i}. {ing} [ID: {ing.id}]")
        
        print(f"  {len(ing_list) + 1}. Cancelar")
        
        choice = get_valid_integer(
            "\nSeleccionar ingredientes para borrar: ", 1, len(ing_list) + 1
        )
        
        if choice == len(ing_list) + 1:
            print("Operacion cancelada.")
            return
        
        ingredient = ing_list[choice - 1]
        
        if menu_manager:
            affected_hotdogs = menu_manager.get_hotdogs_using_ingredient(ingredient.id)
            
            if affected_hotdogs:
                print(f"\nEste ingrediente esta usado en {len(affected_hotdogs)} perro caliente(s):")
                for hd in affected_hotdogs:
                    print(f"  • {hd.name}")
                
                print("\nBorrar este ingrediente tambien borrara los perro calientes!")
                
                if not get_yes_no("Proceder?"):
                    print("Operacion cancelada.")
                    return
                
                for hd in affected_hotdogs:
                    menu_manager.delete_hotdog_by_id(hd.id, skip_confirmation=True)
                    print(f"Perro caliente borrado: {hd.name}")
        
        self.data_manager.remove_ingredient(ingredient.id)
        print(f"\nIngrediente '{ingredient.name}' se borro exitosamente!")
    
    def show_menu(self, menu_manager=None) -> None:
        while True:
            print_header("Manegar ingredientes")
            print("\n1. Todos los ingredientes")
            print("2. Ingredientes por categoria")
            print("3. Ingredientes por tipo")
            print("4. Añadir ingrediente")
            print("5. Borrar ingrediente")
            print("6. Volver")
            
            choice = get_valid_integer("\nElije: ", 1, 6)
            
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