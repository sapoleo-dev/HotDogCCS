# Manegador para la data del API de GitHub en el archivo de JSON local.
# Manega la carga, el merging, y el guardado de data.

import json
import os
import requests
from typing import Dict, List, Optional
from models import Ingredient, HotDog, SalesDay


class DataManager:
    
    def __init__(self, github_repo: str, local_file: str = "local_data.json"):
        self.github_repo = github_repo
        self.local_file = local_file
        self.data = {
            'ingredients': {},
            'hotdogs': {},
            'inventory': {},
            'sales_history': []
        }
    
    def load_all_data(self) -> bool:
        print("\n🔄 Loading data...")

        api_success = self._load_from_github()
        
        local_success = self._load_from_local()
        
        if api_success or local_success:
            print("La data se cargo exitosamente!")
            return True
        else:
            print("No hay fuentes de data disponible.")
            return False
    
    def _load_from_github(self) -> bool:
        try:
            repo_parts = self.github_repo.replace('https://github.com/', '').strip('/')
            api_url = f"https://api.github.com/repos/{repo_parts}/contents"
            
            print(f"Agarramdo data de la API de GitHub: {repo_parts}")
            
            response = requests.get(api_url, timeout=10)
            
            if response.status_code != 200:
                print(f"La API de GitHub retorno el codigo de status {response.status_code}")
                return False
            
            files = response.json()
            json_files = [f for f in files if f['name'].endswith('.json')]
            
            if not json_files:
                print("No se encontraron archivos JSON en el repositorio")
                return False
            
            for file_info in json_files:
                file_name = file_info['name']
                download_url = file_info['download_url']
                
                print(f"Cargando {file_name}...")
                file_response = requests.get(download_url, timeout=10)
                
                if file_response.status_code == 200:
                    file_data = file_response.json()
                    self._merge_api_data(file_data, file_name)
                else:
                    print(f"Se fallo en cargar {file_name}")
            
            print("Se cargo la data de Github")
            return True
            
        except requests.RequestException as e:
            print(f"Error de internet: {e}")
            return False
        except Exception as e:
            print(f"Error cargando de Github: {e}")
            return False
    
    def _merge_api_data(self, file_data: dict, file_name: str) -> None:

        if 'ingredients' in file_data:
            for ing_data in file_data['ingredients']:
                ingredient = Ingredient.from_dict(ing_data)
                self.data['ingredients'][ingredient.id] = ingredient
                if ingredient.id not in self.data['inventory']:
                    self.data['inventory'][ingredient.id] = 50
        
        if 'hotdogs' in file_data:
            for hd_data in file_data['hotdogs']:
                hotdog = HotDog.from_dict(hd_data)
                self.data['hotdogs'][hotdog.id] = hotdog
        
        if 'inventory' in file_data:
            self.data['inventory'].update(file_data['inventory'])
    
    def _load_from_local(self) -> bool:
        
        if not os.path.exists(self.local_file):
            print(f"No se encontro archivo local ({self.local_file})")
            return False
        
        try:
            print(f"Cargando de {self.local_file}...")
            with open(self.local_file, 'r', encoding='utf-8') as f:
                local_data = json.load(f)
            
            if 'ingredients' in local_data:
                for ing_data in local_data['ingredients']:
                    ingredient = Ingredient.from_dict(ing_data)
                    self.data['ingredients'][ingredient.id] = ingredient
            
            if 'hotdogs' in local_data:
                for hd_data in local_data['hotdogs']:
                    hotdog = HotDog.from_dict(hd_data)
                    self.data['hotdogs'][hotdog.id] = hotdog
            
            if 'inventory' in local_data:
                self.data['inventory'].update(local_data['inventory'])
            
            if 'sales_history' in local_data:
                self.data['sales_history'] = [
                    SalesDay.from_dict(sd) for sd in local_data['sales_history']
                ]
            
            print("Data local cargada")
            return True
            
        except Exception as e:
            print(f"Error cargando archivo local: {e}")
            return False
    
    def save_to_local(self) -> bool:
        try:
            
            save_data = {
                'ingredients': [ing.to_dict() for ing in self.data['ingredients'].values()],
                'hotdogs': [hd.to_dict() for hd in self.data['hotdogs'].values()],
                'inventory': self.data['inventory'],
                'sales_history': [sd.to_dict() for sd in self.data['sales_history']]
            }
            
            
            with open(self.local_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error guardando a archivo local: {e}")
            return False
    
    def get_ingredients(self) -> Dict[str, Ingredient]:
        return self.data['ingredients']
    
    def get_hotdogs(self) -> Dict[str, HotDog]:
        return self.data['hotdogs']
    
    def get_inventory(self) -> Dict[str, int]:
        return self.data['inventory']
    
    def get_sales_history(self) -> List[SalesDay]:
        return self.data['sales_history']
    
    def add_ingredient(self, ingredient: Ingredient, initial_quantity: int = 0) -> None:
        self.data['ingredients'][ingredient.id] = ingredient
        self.data['inventory'][ingredient.id] = initial_quantity
        self.save_to_local()
    
    def remove_ingredient(self, ingredient_id: str) -> None:
        if ingredient_id in self.data['ingredients']:
            del self.data['ingredients'][ingredient_id]
        if ingredient_id in self.data['inventory']:
            del self.data['inventory'][ingredient_id]
        self.save_to_local()
    
    def add_hotdog(self, hotdog: HotDog) -> None:
        self.data['hotdogs'][hotdog.id] = hotdog
        self.save_to_local()
    
    def remove_hotdog(self, hotdog_id: str) -> None:
        if hotdog_id in self.data['hotdogs']:
            del self.data['hotdogs'][hotdog_id]
        self.save_to_local()
    
    def update_inventory(self, ingredient_id: str, quantity: int) -> None:
        self.data['inventory'][ingredient_id] = quantity
        self.save_to_local()
    
    def add_sales_day(self, sales_day: SalesDay) -> None:
        self.data['sales_history'].append(sales_day)
        self.save_to_local()