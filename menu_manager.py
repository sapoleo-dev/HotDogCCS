#Manega la lista de perro calientes a la venta.

from typing import Dict, List, Optional
from models import HotDog, Ingredient
from data_manager import DataManager
from ingredient_manager import IngredientManager
from inventory_manager import InventoryManager
from utils import (get_valid_integer, get_valid_string, get_yes_no,
                   print_header, print_section, pause)
import uuid


class MenuManager:
    
    def __init__(self, data_manager: DataManager, 
                 ingredient_manager: IngredientManager,
                 inventory_manager: InventoryManager):
        self.data_manager = data_manager
        self.ingredient_manager = ingredient_manager
        self.inventory_manager = inventory_manager
    
    def get_hotdogs(self) -> Dict[str, HotDog]:
        return self.data_manager.get_hotdogs()
    
    def get_hotdog_by_id(self, hotdog_id: str) -> Optional[HotDog]:
        return self.get_hotdogs().get(hotdog_id)
    
    def get_hotdogs_using_ingredient(self, ingredient_id: str) -> List[HotDog]:
        return [hd for hd in self.get_hotdogs().values() 
                if ingredient_id in hd.get_all_ingredient_ids()]
    
    def display_hotdog_details(self, hotdog: HotDog) -> None:
        print(f"\nPerro caliente: {hotdog.name}")
        print(f"   ID: {hotdog.id}")
        
        pan = self.ingredient_manager.get_ingredient_by_id(hotdog.pan_id)
        print(f"   Pan: {pan.name if pan else 'Unknown'}")
        
        salchicha = self.ingredient_manager.get_ingredient_by_id(hotdog.salchicha_id)
        print(f"   Salchicha: {salchicha.name if salchicha else 'Unknown'}")
        
        # Toppings
        if hotdog.topping_ids:
            print(f"   Aderezos:")
            for tid in hotdog.topping_ids:
                topping = self.ingredient_manager.get_ingredient_by_id(tid)
                print(f"      • {topping.name if topping else 'Unknown'}")
        
        # Salsas
        if hotdog.salsa_ids:
            print(f"   Salsas:")
            for sid in hotdog.salsa_ids:
                salsa = self.ingredient_manager.get_ingredient_by_id(sid)
                print(f"      • {salsa.name if salsa else 'Unknown'}")
        
        # Acompañante
        if hotdog.acompañante_id:
            acomp = self.ingredient_manager.get_ingredient_by_id(hotdog.acompañante_id)
            print(f"   Acompañante: {acomp.name if acomp else 'Unknown'}")
    
    def view_menu(self) -> None:
        print_header("MENU PERRO CALIENTE")
        
        hotdogs = self.get_hotdogs()
        
        if not hotdogs:
            print("\nTodavia no hay perro calientes en el menu.")
            return
        
        print(f"\nTotal: {len(hotdogs)} perro caliente(s)\n")
        
        for hd in sorted(hotdogs.values(), key=lambda x: x.name):
            self.display_hotdog_details(hd)
    
    def check_hotdog_availability(self) -> None:
        print_header("DISPONIBILIDAD PERRO CALIENTE")
        
        hotdogs = self.get_hotdogs()
        
        if not hotdogs:
            print("\nNo hay perro calientes en el menu.")
            return
        
        hd_list = list(hotdogs.values())
        print("\nSeleccionar perro caliente:")
        for i, hd in enumerate(hd_list, 1):
            print(f"  {i}. {hd.name}")
        
        choice = get_valid_integer("\nElije: ", 1, len(hd_list))
        hotdog = hd_list[choice - 1]
        
        requirements = {ing_id: 1 for ing_id in hotdog.get_all_ingredient_ids()}
        available, missing = self.inventory_manager.check_multiple_availability(requirements)
        
        print(f"\nPerro caliente: {hotdog.name}")
        
        if available:
            print("Puede venderse - Todos los ingredientes disponibles!")
        else:
            print("No se puede vender - Faltan ingredientes:")
            for item in missing:
                print(f"   • {item['name']}: Se necesita {item['required']}, Se tiene {item['available']}")
    
    def select_ingredient_from_category(self, category: str, 
                                       allow_cancel: bool = True,
                                       allow_multiple: bool = False) -> Optional[List[str]]:
        items = self.ingredient_manager.get_by_category(category)
        
        if not items:
            print(f"\nNo hay ingredientes de {category} disponible.")
            if allow_cancel:
                return None
            return []
        
        print(f"\nSelecciona {category}:")
        for i, ing in enumerate(items, 1):
            qty = self.inventory_manager.get_quantity(ing.id)
            status = "✓" if qty > 0 else "X"
            print(f"  {i}. {ing.name} (Stock: {qty}) {status}")
        
        if allow_cancel:
            print(f"  {len(items) + 1}. Cancelar")
        
        if allow_multiple:
            print("\nPon numeros separados por comas (e.g., 1,3,4) o 0 para saltar:")
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
                print("Invalido.")
                return self.select_ingredient_from_category(category, allow_cancel, allow_multiple)
        else:
            max_choice = len(items) + 1 if allow_cancel else len(items)
            choice = get_valid_integer("\nElije: ", 1, max_choice)
            
            if allow_cancel and choice == len(items) + 1:
                return None
            
            return [items[choice - 1].id]
    
    def add_hotdog(self) -> None:
        print_header("AÑADIR NUEVO PERRO CALIENTE")
        
        name = get_valid_string("\nPon nombre del perro caliente: ")
        
        print_section("Seleccionar Pan")
        pan_ids = self.select_ingredient_from_category('Pan', allow_cancel=True)
        if pan_ids is None:
            print("Operacion cancelada.")
            return
        pan_id = pan_ids[0]
        pan = self.ingredient_manager.get_ingredient_by_id(pan_id)
        
        print_section("Selecciona Salchicha)")
        salchicha_ids = self.select_ingredient_from_category('Salchicha', allow_cancel=True)
        if salchicha_ids is None:
            print("Operacion cancelada.")
            return
        salchicha_id = salchicha_ids[0]
        salchicha = self.ingredient_manager.get_ingredient_by_id(salchicha_id)
        
        if pan and salchicha and pan.length and salchicha.length:
            if pan.length != salchicha.length:
                print(f"\nEl largo no es igual!")
                print(f"   Largo del pan: {pan.length}")
                print(f"   Largo de la salchicha: {salchicha.length}")
                
                if not get_yes_no("Continuar igual?"):
                    print("Operacion cancelada.")
                    return
        
        print_section("Seleccionar aderezos (Opcional, Multiples)")
        topping_ids = self.select_ingredient_from_category('Aderezo', 
                                                           allow_cancel=False,
                                                           allow_multiple=True)
        
        print_section("Seleccionar Salsas (Opcional, Multiples)")
        salsa_ids = self.select_ingredient_from_category('Salsa', 
                                                         allow_cancel=False,
                                                         allow_multiple=True)
        
        print_section("Seleccionar acompañante - Opcional")
        print("Quisieras añadir un acompañante?")
        if get_yes_no("Añadir acompañante?"):
            acomp_ids = self.select_ingredient_from_category('Acompañante', allow_cancel=True)
            acompañante_id = acomp_ids[0] if acomp_ids else None
        else:
            acompañante_id = None
        
        all_ingredient_ids = [pan_id, salchicha_id] + topping_ids + salsa_ids
        if acompañante_id:
            all_ingredient_ids.append(acompañante_id)
        
        zero_stock = []
        for ing_id in all_ingredient_ids:
            if self.inventory_manager.get_quantity(ing_id) == 0:
                ing = self.ingredient_manager.get_ingredient_by_id(ing_id)
                zero_stock.append(ing.name if ing else ing_id)
        
        if zero_stock:
            print("\nHay 0 de los siguientes ingredientes en el stock:")
            for ing_name in zero_stock:
                print(f"   • {ing_name}")
            print("\nIgual puedes añadir este perro caliente, pero no se puede vender hasta que hallan los ingredientes requeridos.")
        
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
        
        self.data_manager.add_hotdog(hotdog)
        
        print(f"\nPerro caliente '{name}' se añadio al menu exitosamente!")
    
    def delete_hotdog_by_id(self, hotdog_id: str, skip_confirmation: bool = False) -> None:
        hotdog = self.get_hotdog_by_id(hotdog_id)
        if not hotdog:
            return
        
        if not skip_confirmation:
            requirements = {ing_id: 1 for ing_id in hotdog.get_all_ingredient_ids()}
            available, missing = self.inventory_manager.check_multiple_availability(requirements)
            
            if available:
                print(f"\nTodavia hay inventario para vender '{hotdog.name}'!")
                if not get_yes_no("Igual lo deseas borrar?"):
                    print("Operacion cancelada.")
                    return
        
        self.data_manager.remove_hotdog(hotdog_id)
        if not skip_confirmation:
            print(f"\nPerro caliente '{hotdog.name}' se borro exitosamente!")
    
    def delete_hotdog(self) -> None:
        print_header("BORRAR PERRO CALIENTE")
        
        hotdogs = self.get_hotdogs()
        
        if not hotdogs:
            print("\nNo hay perro calientes en el menu.")
            return
        
        # Display menu
        hd_list = list(hotdogs.values())
        print("\nSeleccionar perro caliente para borrar:")
        for i, hd in enumerate(hd_list, 1):
            print(f"  {i}. {hd.name}")
        print(f"  {len(hd_list) + 1}. Cancelar")
        
        choice = get_valid_integer("\nElije: ", 1, len(hd_list) + 1)
        
        if choice == len(hd_list) + 1:
            print("Operacion cancelada.")
            return
        
        hotdog = hd_list[choice - 1]
        self.delete_hotdog_by_id(hotdog.id)
    
    def show_menu(self) -> None:
        while True:
            print_header("MANEGADOR DE MENU")
            print("\n1. Ver menu")
            print("2. Ver disponibilidad de perro caliente")
            print("3. Añadir perro caliente nuevo")
            print("4. Borrar perro caliente")
            print("5. Volver")
            
            choice = get_valid_integer("\nElije: ", 1, 5)
            
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