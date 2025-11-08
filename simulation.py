"""
Module 4: Sales Day Simulation
Simulates a day of sales to test the system.
"""

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
    """
    Simulates a sales day with random customers.
    """
    
    def __init__(self, data_manager: DataManager,
                 menu_manager: MenuManager,
                 inventory_manager: InventoryManager):
        """
        Initialize the sales simulation.
        
        Args:
            data_manager: DataManager instance
            menu_manager: MenuManager instance
            inventory_manager: InventoryManager instance
        """
        self.data_manager = data_manager
        self.menu_manager = menu_manager
        self.inventory_manager = inventory_manager
    
    def simulate_day(self) -> None:
        """Run a full day simulation."""
        print_header("SALES DAY SIMULATION", "=")
        
        hotdogs = self.menu_manager.get_hotdogs()
        
        if not hotdogs:
            print("\n❌ Cannot simulate - no hot dogs on menu!")
            pause()
            return
        
        # Initialize tracking variables
        num_clients = random.randint(0, 200)
        clients_changed_opinion = 0
        clients_could_not_buy = 0
        clients_served = 0
        total_hotdogs_sold = 0
        hotdog_sales_counter = Counter()
        hotdogs_causing_loss = []
        ingredients_causing_loss = []
        total_sides_sold = 0
        
        print(f"\n🎲 Generated {num_clients} clients for today\n")
        print("=" * 60)
        
        # Simulate each client
        for client_num in range(1, num_clients + 1):
            num_hotdogs = random.randint(0, 5)
            
            # Client changed their mind
            if num_hotdogs == 0:
                print(f"\n👤 Client {client_num}: Changed their opinion")
                clients_changed_opinion += 1
                continue
            
            # Build client's order
            order = []
            order_requirements = Counter()
            
            for _ in range(num_hotdogs):
                # Select random hot dog
                hotdog = random.choice(list(hotdogs.values()))
                order.append(hotdog)
                
                # Add ingredients to requirements
                for ing_id in hotdog.get_all_ingredient_ids():
                    order_requirements[ing_id] += 1
                
                # Randomly add extra side
                if random.random() < 0.3:  # 30% chance
                    from ingredient_manager import IngredientManager
                    # Get all sides
                    sides = [ing for ing in self.data_manager.get_ingredients().values()
                            if ing.category == 'Acompañante']
                    if sides:
                        extra_side = random.choice(sides)
                        order_requirements[extra_side.id] += 1
            
            # Check if order can be fulfilled
            available, missing = self.inventory_manager.check_multiple_availability(
                dict(order_requirements)
            )
            
            if available:
                # Fulfill order
                print(f"\n✅ Client {client_num}: Bought {num_hotdogs} hot dog(s)")
                for i, hd in enumerate(order, 1):
                    print(f"   {i}. {hd.name}")
                    hotdog_sales_counter[hd.name] += 1
                    total_hotdogs_sold += 1
                
                # Count sides
                for hd in order:
                    if hd.acompañante_id:
                        total_sides_sold += 1
                
                # Count extra sides
                for ing_id, count in order_requirements.items():
                    ing = self.data_manager.get_ingredients().get(ing_id)
                    if ing and ing.category == 'Acompañante':
                        # Subtract sides that came with hotdogs
                        combo_sides = sum(1 for hd in order if hd.acompañante_id == ing_id)
                        extra_sides = count - combo_sides
                        total_sides_sold += extra_sides
                
                # Consume inventory
                self.inventory_manager.consume_ingredients(dict(order_requirements))
                clients_served += 1
                
            else:
                # Order cannot be fulfilled
                print(f"\n❌ Client {client_num}: LEFT WITHOUT BUYING")
                print(f"   Wanted {num_hotdogs} hot dog(s) but missing:")
                
                for item in missing:
                    print(f"   • {item['name']}: Need {item['required']}, Have {item['available']}")
                    
                    if item['name'] not in ingredients_causing_loss:
                        ingredients_causing_loss.append(item['name'])
                
                # Track which hotdogs caused the loss
                for hd in order:
                    if hd.name not in hotdogs_causing_loss:
                        hotdogs_causing_loss.append(hd.name)
                
                clients_could_not_buy += 1
        
        # End of day report
        print("\n" + "=" * 60)
        print_header("END OF DAY REPORT", "=")
        
        print(f"\n📊 Client Statistics:")
        print(f"   Total clients: {num_clients}")
        print(f"   Clients changed opinion (0 hot dogs): {clients_changed_opinion}")
        print(f"   Clients who could not buy: {clients_could_not_buy}")
        print(f"   Clients served: {clients_served}")
        
        print(f"\n🌭 Sales Statistics:")
        print(f"   Total hot dogs sold: {total_hotdogs_sold}")
        
        if clients_served > 0:
            avg_hotdogs = total_hotdogs_sold / clients_served
            print(f"   Average hot dogs per client: {avg_hotdogs:.2f}")
        else:
            print(f"   Average hot dogs per client: 0.00")
        
        if hotdog_sales_counter:
            best_seller = hotdog_sales_counter.most_common(1)[0]
            print(f"   Best-selling hot dog: {best_seller[0]} ({best_seller[1]} sold)")
            best_selling_name = best_seller[0]
        else:
            print(f"   Best-selling hot dog: None")
            best_selling_name = ""
        
        print(f"   Total sides sold: {total_sides_sold}")
        
        if hotdogs_causing_loss:
            print(f"\n⚠️  Hot dogs that caused clients to leave:")
            for hd_name in hotdogs_causing_loss:
                print(f"   • {hd_name}")
        
        if ingredients_causing_loss:
            print(f"\n⚠️  Ingredients that were missing:")
            for ing_name in ingredients_causing_loss:
                print(f"   • {ing_name}")
        
        # Save to sales history
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
        
        print("\n✅ Sales day completed and saved to history!")
        pause()