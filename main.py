# Hot Dog CCS - Main

import sys
from data_manager import DataManager
from ingredient_manager import IngredientManager
from inventory_manager import InventoryManager
from menu_manager import MenuManager
from simulation import SalesSimulation
from statistics import StatisticsManager
from utils import get_valid_integer, print_header, pause, clear_screen


def print_welcome():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print(r"""
    ╦ ╦╔═╗╔╦╗  ╔╦╗╔═╗╔═╗  ╔═╗╔═╗╔═╗
    ╠═╣║ ║ ║    ║║║ ║║ ╦  ║  ║  ╚═╗
    ╩ ╩╚═╝ ╩   ═╩╝╚═╝╚═╝  ╚═╝╚═╝╚═╝
    """)
    print("    Manegador para venta de perro calientes")
    print("=" * 60)


def initialize_system():
    print_header("SYSTEM INITIALIZATION")
    
    github_repo = "https://github.com/FernandoSapient/BPTSP05_2526-1"
    
    data_manager = DataManager(github_repo)
    
    data_manager.load_all_data()
    
    ingredient_manager = IngredientManager(data_manager)
    inventory_manager = InventoryManager(data_manager, ingredient_manager)
    menu_manager = MenuManager(data_manager, ingredient_manager, inventory_manager)
    simulation = SalesSimulation(data_manager, menu_manager, inventory_manager)
    statistics = StatisticsManager(data_manager)
    
    return (data_manager, ingredient_manager, inventory_manager, 
            menu_manager, simulation, statistics)


def show_main_menu(data_manager, ingredient_manager, inventory_manager,
                   menu_manager, simulation, statistics):
    while True:
        print_header("HOT DOG CCS - MENU PRINCIPAL")
        
        print("\nMODULOS")
        print("  1. Manegador de ingredientes")
        print("  2. Manegador de inventario")
        print("  3. Manegador del menu")
        
        print("\nSIMULACION Y ANALITICAS")
        print("  4. Correr simulacion de ventas del dia")
        
        if statistics.can_show_statistics():
            print("  5. Ver estadisticas y graficos")
            max_choice = 7
        else:
            days = len(data_manager.get_sales_history())
            print(f"  5. Ver estadisticas (Necesita {2-days} dias de ventas mas)")
            max_choice = 7
        
        print("\nSISTEMA")
        print("  6. Guardar data")
        print("  7. Salir")
        
        choice = get_valid_integer("\nElije: ", 1, max_choice)
        
        if choice == 1:
            ingredient_manager.show_menu(menu_manager)
        elif choice == 2:
            inventory_manager.show_menu()
        elif choice == 3:
            menu_manager.show_menu()
        elif choice == 4:
            simulation.simulate_day()
        elif choice == 5:
            if statistics.can_show_statistics():
                statistics.show_statistics()
            else:
                print("\nSe necesitan al menos dos dias para ver las estadisticas.")
                pause()
        elif choice == 6:
            print("\nGuardando...")
            if data_manager.save_to_local():
                print("La data se guardo exitosamente!")
            else:
                print("Error guardando data!")
            pause()
        elif choice == 7:
            print("\nGuardando antes de salir...")
            data_manager.save_to_local()
            print("\nGracias por usar Hot Dog CCS!")
            print("=" * 60)
            sys.exit(0)


def main():
    try:
        print_welcome()
        pause()
        
        managers = initialize_system()
        
        pause()
        
        show_main_menu(*managers)
        
    except KeyboardInterrupt:
        print("\n\nAplicacion interumpida por usuario.")
        print("Adios!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError critico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()