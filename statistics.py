#Genera graficos de el historial de ventas.
#Requiere dos dias de ventas.

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
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def can_show_statistics(self) -> bool:
        return len(self.data_manager.get_sales_history()) >= 2
    
    def show_statistics(self) -> None:
        if not MATPLOTLIB_AVAILABLE:
            print("\nMatplotlib no instalado.")
            print("   Instalalo con: pip install matplotlib")
            pause()
            return
        
        sales_history = self.data_manager.get_sales_history()
        
        if not self.can_show_statistics():
            print(f"\nSe requieren a al menos dos dias de ventas.")
            print(f"   Dias guardados: {len(sales_history)}")
            pause()
            return
        
        print_header("ESTADISTICAS DE VENTAS")
        
        print("\n1. Vista de clientes")
        print("2. Vista de ventas")
        print("3. Perro calientes mas vendidos")
        print("4. Problemas de inventario")
        print("5. Todos los graficos")
        print("6. Volver")
        
        from utils import get_valid_integer
        choice = get_valid_integer("\nElije: ", 1, 6)
        
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
        dates = [sd.date for sd in history]
        total_clients = [sd.total_clients for sd in history]
        changed_opinion = [sd.clients_changed_opinion for sd in history]
        could_not_buy = [sd.clients_could_not_buy for sd in history]
        served = [sd.total_clients - sd.clients_changed_opinion - sd.clients_could_not_buy 
                  for sd in history]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Estadisticas de clientes por el tiempo', fontsize=16, fontweight='bold')
        
        axes[0, 0].plot(dates, total_clients, marker='o', linewidth=2, color='blue')
        axes[0, 0].set_title('Clientes totales por dia')
        axes[0, 0].set_ylabel('Numero de clientes')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        axes[0, 1].plot(dates, changed_opinion, marker='s', linewidth=2, color='orange')
        axes[0, 1].set_title('Clients Who Changed Opinion')
        axes[0, 1].set_ylabel('Numero de clientes')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        axes[1, 0].plot(dates, could_not_buy, marker='^', linewidth=2, color='red')
        axes[1, 0].set_title('Clientes que no pudieron comprar')
        axes[1, 0].set_ylabel('Numero de clientes')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        axes[1, 1].plot(dates, served, marker='D', linewidth=2, color='green')
        axes[1, 1].set_title('Clientes servidos')
        axes[1, 1].set_ylabel('Numero de clientes')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def _show_sales_overview(self, history: List[SalesDay]) -> None:
        dates = [sd.date for sd in history]
        hotdogs_sold = [sd.total_hotdogs_sold for sd in history]
        sides_sold = [sd.total_sides_sold for sd in history]
        
        avg_per_client = []
        for sd in history:
            served = sd.total_clients - sd.clients_changed_opinion - sd.clients_could_not_buy
            if served > 0:
                avg_per_client.append(sd.total_hotdogs_sold / served)
            else:
                avg_per_client.append(0)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Estadisticas de ventas por el tiempo', fontsize=16, fontweight='bold')
        
        axes[0, 0].bar(dates, hotdogs_sold, color='brown', alpha=0.7)
        axes[0, 0].set_title('Perro calientes vendidos por dia')
        axes[0, 0].set_ylabel('Numero de perro calientes')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        axes[0, 1].bar(dates, sides_sold, color='gold', alpha=0.7)
        axes[0, 1].set_title('Acompañantes vendidos por dia')
        axes[0, 1].set_ylabel('Numero de acompañantes')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        axes[1, 0].plot(dates, avg_per_client, marker='o', linewidth=2, color='purple')
        axes[1, 0].set_title('Promedio de perro calientes por clientes')
        axes[1, 0].set_ylabel('Promedio')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        axes[1, 1].plot(dates, hotdogs_sold, marker='o', linewidth=2, 
                       label='Perro calientes', color='brown')
        axes[1, 1].plot(dates, sides_sold, marker='s', linewidth=2, 
                       label='Acompañantes', color='gold')
        axes[1, 1].set_title('Perro calientes vs Acompañantes')
        axes[1, 1].set_ylabel('Cantidad')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _show_best_sellers(self, history: List[SalesDay]) -> None:
        from collections import Counter
        
        best_sellers = Counter()
        for sd in history:
            if sd.best_selling_hotdog:
                best_sellers[sd.best_selling_hotdog] += 1
        
        if not best_sellers:
            print("\nNo hay data de ventas disponibles.")
            pause()
            return
        
        top_sellers = best_sellers.most_common(10)
        names = [name for name, _ in top_sellers]
        counts = [count for _, count in top_sellers]
        
        plt.figure(figsize=(12, 6))
        plt.bar(names, counts, color='darkred', alpha=0.7)
        plt.title('Perro calientes mas vendidos (dias siendo mas vendido)', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Nombre de perro calientes')
        plt.ylabel('dias siendo mas vendido')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()
    
    def _show_inventory_issues(self, history: List[SalesDay]) -> None:
        from collections import Counter
        
        problem_hotdogs = Counter()
        problem_ingredients = Counter()
        
        for sd in history:
            for hd in sd.hotdogs_causing_loss:
                problem_hotdogs[hd] += 1
            for ing in sd.ingredients_causing_loss:
                problem_ingredients[ing] += 1
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Problemas de inventarios', fontsize=16, fontweight='bold')
        
        if problem_hotdogs:
            top_problem_hd = problem_hotdogs.most_common(10)
            names = [name for name, _ in top_problem_hd]
            counts = [count for _, count in top_problem_hd]
            
            axes[0].barh(names, counts, color='orangered', alpha=0.7)
            axes[0].set_title('Perro calientes casuando perdida de clientes')
            axes[0].set_xlabel('Numero de ocurrencias')
            axes[0].grid(True, alpha=0.3, axis='x')
        else:
            axes[0].text(0.5, 0.5, 'No data', ha='center', va='center')
            axes[0].set_title('Perro calientes casuando perdida de clientes')
        
        if problem_ingredients:
            top_problem_ing = problem_ingredients.most_common(10)
            names = [name for name, _ in top_problem_ing]
            counts = [count for _, count in top_problem_ing]
            
            axes[1].barh(names, counts, color='crimson', alpha=0.7)
            axes[1].set_title('Faltan Ingredientes')
            axes[1].set_xlabel('Numero de ocurrencias')
            axes[1].grid(True, alpha=0.3, axis='x')
        else:
            axes[1].text(0.5, 0.5, 'No data', ha='center', va='center')
            axes[1].set_title('Faltan Ingredientes')
        
        plt.tight_layout()
        plt.show()
    
    def _show_all_graphs(self, history: List[SalesDay]) -> None:
        self._show_clients_overview(history)
        self._show_sales_overview(history)
        self._show_best_sellers(history)
        self._show_inventory_issues(history)