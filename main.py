"""
Hot Dog CCS - Main Application
Complete console-based hot dog stand management system.
"""

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
    print("    Complete Console-based Stand Management")
    print("=" * 60)


def initialize_system():
    """
    Initialize the system and load data.
    
    Returns:
        Tuple of all manager instances
    """
    print_header("SYSTEM INITIALIZATION")
    
    # GitHub repository URL
    github_repo = "https://github.com/FernandoSapient/BPTSP05_2526-1"
    
    # Initialize data manager
    data_manager = DataManager(github_repo)
    
    # Load data from GitHub and local file
    data_manager.load_all_data()
    
    # Initialize managers
    ingredient_manager = IngredientManager(data_manager)
    inventory_manager = InventoryManager(data_manager, ingredient_manager)
    menu_manager = MenuManager(data_manager, ingredient_manager, inventory_manager)
    simulation = SalesSimulation(data_manager, menu_manager, inventory_manager)
    statistics = StatisticsManager(data_manager)
    
    return (data_manager, ingredient_manager, inventory_manager, 
            menu_manager, simulation, statistics)


def show_main_menu(data_manager, ingredient_manager, inventory_manager,
                   menu_manager, simulation, statistics):
    """
    Display and handle main menu.
    
    Args:
        data_manager: DataManager instance
        ingredient_manager: IngredientManager instance
        inventory_manager: InventoryManager instance
        menu_manager: MenuManager instance
        simulation: SalesSimulation instance
        statistics: StatisticsManager instance
    """
    while True:
        print_header("HOT DOG CCS - MAIN MENU")
        
        print("\n📋 MANAGEMENT MODULES")
        print("  1. Ingredient Management")
        print("  2. Inventory Management")
        print("  3. Menu Management")
        
        print("\n🎲 SIMULATION & ANALYTICS")
        print("  4. Run Sales Day Simulation")
        
        # Show statistics option only if available
        if statistics.can_show_statistics():
            print("  5. View Statistics & Graphs ✨")
            max_choice = 7
        else:
            days = len(data_manager.get_sales_history())
            print(f"  5. View Statistics (Need {2-days} more sales day(s))")
            max_choice = 7
        
        print("\n⚙️  SYSTEM")
        print("  6. Save Data")
        print("  7. Exit")
        
        choice = get_valid_integer("\n👉 Enter your choice: ", 1, max_choice)
        
        if choice == 1:
            # Pass menu_manager for delete validation
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
                print("\n❌ Need at least 2 sales days to view statistics.")
                pause()
        elif choice == 6:
            print("\n💾 Saving data...")
            if data_manager.save_to_local():
                print("✅ Data saved successfully!")
            else:
                print("❌ Error saving data!")
            pause()
        elif choice == 7:
            # Save before exit
            print("\n💾 Saving data before exit...")
            data_manager.save_to_local()
            print("\n👋 Thank you for using Hot Dog CCS!")
            print("=" * 60)
            sys.exit(0)


def main():
    """Main application entry point."""
    try:
        # Print welcome banner
        print_welcome()
        pause()
        
        # Initialize system
        managers = initialize_system()
        
        pause()
        
        # Run main menu
        show_main_menu(*managers)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user.")
        print("👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()