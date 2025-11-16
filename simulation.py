# Simula un dia de venta para probar el sistema.

import random
from typing import Dict, List
from datetime import datetime
from collections import Counter
from models import SalesDay, HotDog
from data_manager import DataManager
from menu_manager import MenuManager
from inventory_manager import InventoryManager
from utils import print_header, print_section, pause


class SalesSimulation:
    
    def __init__(self, data_manager: DataManager,
                 menu_manager: MenuManager,
                 inventory_manager: InventoryManager):
        self.data_manager = data_manager
        self.menu_manager = menu_manager
        self.inventory_manager = inventory_manager
    
    def simulate_day(self) -> None:
        print_header("SIMULACION DE VENTA", "=")
        
        hotdogs = self.menu_manager.get_hotdogs()
        
        if not hotdogs:
            print("\nNo se puede simular - no hay perro calientes en el menu!")
            pause()
            return
        
        num_clients = random.randint(0, 200)
        clients_changed_opinion = 0
        clients_could_not_buy = 0
        clients_served = 0
        total_hotdogs_sold = 0
        hotdog_sales_counter = Counter()
        hotdogs_causing_loss = []
        ingredients_causing_loss = []
        total_sides_sold = 0
        
        print(f"\nSe generaron {num_clients} clientes para hoy\n")
        print("=" * 60)
        
        for client_num in range(1, num_clients + 1):
            num_hotdogs = random.randint(0, 5)
            
            if num_hotdogs == 0:
                print(f"\nCliente {client_num}: Cambio de opinion")
                clients_changed_opinion += 1
                continue
            
            order = []
            order_requirements = Counter()
            
            for _ in range(num_hotdogs):
                hotdog = random.choice(list(hotdogs.values()))
                order.append(hotdog)
                
                for ing_id in hotdog.get_all_ingredient_ids():
                    order_requirements[ing_id] += 1
                
                if random.random() < 0.3:
                    from ingredient_manager import IngredientManager
                    sides = [ing for ing in self.data_manager.get_ingredients().values()
                            if ing.category == 'Acompañante']
                    if sides:
                        extra_side = random.choice(sides)
                        order_requirements[extra_side.id] += 1
            
            available, missing = self.inventory_manager.check_multiple_availability(
                dict(order_requirements)
            )
            
            if available:
                print(f"\nCliente {client_num}: Compro {num_hotdogs} perro caliente(s)")
                for i, hd in enumerate(order, 1):
                    print(f"   {i}. {hd.name}")
                    hotdog_sales_counter[hd.name] += 1
                    total_hotdogs_sold += 1
                
                for hd in order:
                    if hd.acompañante_id:
                        total_sides_sold += 1
                
                for ing_id, count in order_requirements.items():
                    ing = self.data_manager.get_ingredients().get(ing_id)
                    if ing and ing.category == 'Acompañante':
                        combo_sides = sum(1 for hd in order if hd.acompañante_id == ing_id)
                        extra_sides = count - combo_sides
                        total_sides_sold += extra_sides
                
                self.inventory_manager.consume_ingredients(dict(order_requirements))
                clients_served += 1
                
            else:
                print(f"\nCliente {client_num}: Se fue sin comprar")
                print(f"   Queria {num_hotdogs} perro caliente(s) pero faltaban:")
                
                for item in missing:
                    print(f"   • {item['name']}: Se necesita {item['required']}, Se tiene {item['available']}")
                    
                    if item['name'] not in ingredients_causing_loss:
                        ingredients_causing_loss.append(item['name'])
                
                for hd in order:
                    if hd.name not in hotdogs_causing_loss:
                        hotdogs_causing_loss.append(hd.name)
                
                clients_could_not_buy += 1
        
        print("\n" + "=" * 60)
        print_header("REPORTE DEL FINAL DEL DIA", "=")
        
        print(f"\nEstadisticas del Cliente:")
        print(f"   Clientes totales: {num_clients}")
        print(f"   Clientes que cambiaron de opinion (0 perro calientes): {clients_changed_opinion}")
        print(f"   Clientes que no pudieron comprar: {clients_could_not_buy}")
        print(f"   Clientes servidos: {clients_served}")
        
        print(f"\nEstadisticas de venta:")
        print(f"   Perro calientes totales vendidos: {total_hotdogs_sold}")
        
        if clients_served > 0:
            avg_hotdogs = total_hotdogs_sold / clients_served
            print(f"   Promedio de perro calientes comprados por clientes: {avg_hotdogs:.2f}")
        else:
            print(f"   Promedio de perro calientes comprados por clientes: 0.00")
        
        if hotdog_sales_counter:
            best_seller = hotdog_sales_counter.most_common(1)[0]
            print(f"   Perro caliente mejor vendido: {best_seller[0]} ({best_seller[1]} vendidos)")
            best_selling_name = best_seller[0]
        else:
            print(f"   Perro caliente mejor vendido: None")
            best_selling_name = ""
        
        print(f"   Acompañantes vendidos: {total_sides_sold}")
        
        if hotdogs_causing_loss:
            print(f"\nPerro calientes que causaron que los clientes se fueran:")
            for hd_name in hotdogs_causing_loss:
                print(f"   • {hd_name}")
        
        if ingredients_causing_loss:
            print(f"\nIngredientes que faltaron:")
            for ing_name in ingredients_causing_loss:
                print(f"   • {ing_name}")
        
        sales_day = SalesDay(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            clients_changed_opinion=clients_changed_opinion,
            clients_could_not_buy=clients_could_not_buy,
            total_clients=num_clients,
            total_hotdogs_sold=total_hotdogs_sold,
            best_selling_hotdog=best_selling_name,
            hotdogs_causing_loss=hotdogs_causing_loss,
            ingredients_causing_loss=ingredients_causing_loss,
            total_sides_sold=total_sides_sold
        )
        
        self.data_manager.add_sales_day(sales_day)
        
        print("\nDia de ventas completado, y guardado!")
        pause()