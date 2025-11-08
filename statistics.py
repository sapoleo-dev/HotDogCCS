"""
Module 5: Statistics Module (Bonus)
Generates graphs showing trends from sales history.
Requires at least 2 sales days.
"""

from typing import List
from models import SalesDay
from data_manager import DataManager
from utils import print_header, pause

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class StatisticsManager:
    """
    Generates statistical graphs from sales history.
    """
    
    def __init__(self, data_manager: DataManager):
        """
        Initialize the statistics manager.
        
        Args:
            data_manager: DataManager instance
        """
        self.data_manager = data_manager
    
    def can_show_statistics(self) -> bool:
        """Check if statistics can be shown (need 2+ days)."""
        return len(self.data_manager.get_sales_history()) >= 2
    
    def show_statistics(self) -> None:
        """Display statistics menu and generate graphs."""
        if not MATPLOTLIB_AVAILABLE:
            print("\n❌ Matplotlib is not installed.")
            print("   Install it with: pip install matplotlib")
            pause()
            return
        
        sales_history = self.data_manager.get_sales_history()
        
        if not self.can_show_statistics():
            print(f"\n❌ Need at least 2 sales days to show statistics.")
            print(f"   Current days recorded: {len(sales_history)}")
            pause()
            return
        
        print_header("SALES STATISTICS")
        
        print("\n1. Clients overview")
        print("2. Sales overview")
        print("3. Best-selling hot dogs")
        print("4. Inventory issues")
        print("5. All graphs")
        print("6. Back")
        
        from utils import get_valid_integer
        choice = get_valid_integer("\nEnter choice: ", 1, 6)
        
        if choice == 1:
            self._show_clients_overview(sales_history)
        elif choice == 2:
            self._show_sales_overview(sales_history)
        elif choice == 3:
            self._show_best_sellers(sales_history)
        elif choice == 4:
            self._show_inventory_issues(sales_history)
        elif choice == 5:
            self._show_all_graphs(sales_history)
        elif choice == 6:
            return
    
    def _show_clients_overview(self, history: List[SalesDay]) -> None:
        """Show client-related statistics."""
        dates = [sd.date for sd in history]
        total_clients = [sd.total_clients for sd in history]
        changed_opinion = [sd.clients_changed_opinion for sd in history]
        could_not_buy = [sd.clients_could_not_buy for sd in history]
        served = [sd.total_clients - sd.clients_changed_opinion - sd.clients_could_not_buy 
                  for sd in history]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Client Statistics Over Time', fontsize=16, fontweight='bold')
        
        # Total clients
        axes[0, 0].plot(dates, total_clients, marker='o', linewidth=2, color='blue')
        axes[0, 0].set_title('Total Clients per Day')
        axes[0, 0].set_ylabel('Number of Clients')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Clients changed opinion
        axes[0, 1].plot(dates, changed_opinion, marker='s', linewidth=2, color='orange')
        axes[0, 1].set_title('Clients Who Changed Opinion')
        axes[0, 1].set_ylabel('Number of Clients')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Clients could not buy
        axes[1, 0].plot(dates, could_not_buy, marker='^', linewidth=2, color='red')
        axes[1, 0].set_title('Clients Who Could Not Buy')
        axes[1, 0].set_ylabel('Number of Clients')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Clients served
        axes[1, 1].plot(dates, served, marker='D', linewidth=2, color='green')
        axes[1, 1].set_title('Clients Successfully Served')
        axes[1, 1].set_ylabel('Number of Clients')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def _show_sales_overview(self, history: List[SalesDay]) -> None:
        """Show sales-related statistics."""
        dates = [sd.date for sd in history]
        hotdogs_sold = [sd.total_hotdogs_sold for sd in history]
        sides_sold = [sd.total_sides_sold for sd in history]
        
        # Calculate average per client
        avg_per_client = []
        for sd in history:
            served = sd.total_clients - sd.clients_changed_opinion - sd.clients_could_not_buy
            if served > 0:
                avg_per_client.append(sd.total_hotdogs_sold / served)
            else:
                avg_per_client.append(0)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Sales Statistics Over Time', fontsize=16, fontweight='bold')
        
        # Hot dogs sold
        axes[0, 0].bar(dates, hotdogs_sold, color='brown', alpha=0.7)
        axes[0, 0].set_title('Hot Dogs Sold per Day')
        axes[0, 0].set_ylabel('Number of Hot Dogs')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Sides sold
        axes[0, 1].bar(dates, sides_sold, color='gold', alpha=0.7)
        axes[0, 1].set_title('Sides Sold per Day')
        axes[0, 1].set_ylabel('Number of Sides')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Average hot dogs per client
        axes[1, 0].plot(dates, avg_per_client, marker='o', linewidth=2, color='purple')
        axes[1, 0].set_title('Average Hot Dogs per Client')
        axes[1, 0].set_ylabel('Average')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # Combined view
        axes[1, 1].plot(dates, hotdogs_sold, marker='o', linewidth=2, 
                       label='Hot Dogs', color='brown')
        axes[1, 1].plot(dates, sides_sold, marker='s', linewidth=2, 
                       label='Sides', color='gold')
        axes[1, 1].set_title('Hot Dogs vs Sides')
        axes[1, 1].set_ylabel('Quantity')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _show_best_sellers(self, history: List[SalesDay]) -> None:
        """Show best-selling hot dogs."""
        from collections import Counter
        
        best_sellers = Counter()
        for sd in history:
            if sd.best_selling_hotdog:
                best_sellers[sd.best_selling_hotdog] += 1
        
        if not best_sellers:
            print("\n❌ No sales data available.")
            pause()
            return
        
        # Get top 10
        top_sellers = best_sellers.most_common(10)
        names = [name for name, _ in top_sellers]
        counts = [count for _, count in top_sellers]
        
        plt.figure(figsize=(12, 6))
        plt.bar(names, counts, color='darkred', alpha=0.7)
        plt.title('Top Selling Hot Dogs (Days as Best Seller)', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Hot Dog Name')
        plt.ylabel('Number of Days as Best Seller')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()
    
    def _show_inventory_issues(self, history: List[SalesDay]) -> None:
        """Show inventory-related issues."""
        from collections import Counter
        
        problem_hotdogs = Counter()
        problem_ingredients = Counter()
        
        for sd in history:
            for hd in sd.hotdogs_causing_loss:
                problem_hotdogs[hd] += 1
            for ing in sd.ingredients_causing_loss:
                problem_ingredients[ing] += 1
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Inventory Issues', fontsize=16, fontweight='bold')
        
        # Problem hot dogs
        if problem_hotdogs:
            top_problem_hd = problem_hotdogs.most_common(10)
            names = [name for name, _ in top_problem_hd]
            counts = [count for _, count in top_problem_hd]
            
            axes[0].barh(names, counts, color='orangered', alpha=0.7)
            axes[0].set_title('Hot Dogs Causing Client Loss')
            axes[0].set_xlabel('Number of Occurrences')
            axes[0].grid(True, alpha=0.3, axis='x')
        else:
            axes[0].text(0.5, 0.5, 'No data', ha='center', va='center')
            axes[0].set_title('Hot Dogs Causing Client Loss')
        
        # Problem ingredients
        if problem_ingredients:
            top_problem_ing = problem_ingredients.most_common(10)
            names = [name for name, _ in top_problem_ing]
            counts = [count for _, count in top_problem_ing]
            
            axes[1].barh(names, counts, color='crimson', alpha=0.7)
            axes[1].set_title('Missing Ingredients')
            axes[1].set_xlabel('Number of Occurrences')
            axes[1].grid(True, alpha=0.3, axis='x')
        else:
            axes[1].text(0.5, 0.5, 'No data', ha='center', va='center')
            axes[1].set_title('Missing Ingredients')
        
        plt.tight_layout()
        plt.show()
    
    def _show_all_graphs(self, history: List[SalesDay]) -> None:
        """Show all graphs sequentially."""
        self._show_clients_overview(history)
        self._show_sales_overview(history)
        self._show_best_sellers(history)
        self._show_inventory_issues(history)