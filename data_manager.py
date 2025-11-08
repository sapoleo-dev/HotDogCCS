"""
Data manager for handling GitHub API data and local JSON file.
Manages loading, merging, and saving data.
"""

import json
import os
import requests
from typing import Dict, List, Optional
from models import Ingredient, HotDog, SalesDay


class DataManager:
    """
    Manages data from GitHub API and local JSON file.
    
    Attributes:
        github_repo: GitHub repository URL
        local_file: Path to local JSON file
        data: Current application data
    """
    
    def __init__(self, github_repo: str, local_file: str = "local_data.json"):
        """
        Initialize the data manager.
        
        Args:
            github_repo: GitHub repository URL or API endpoint
            local_file: Path to local JSON file
        """
        self.github_repo = github_repo
        self.local_file = local_file
        self.data = {
            'ingredients': {},
            'hotdogs': {},
            'inventory': {},
            'sales_history': []
        }
    
    def load_all_data(self) -> bool:
        """
        Load data from both GitHub API and local file.
        
        Returns:
            True if successful, False otherwise
        """
        print("\n🔄 Loading data...")
        
        # Load from GitHub API
        api_success = self._load_from_github()
        
        # Load from local file (overrides/extends API data)
        local_success = self._load_from_local()
        
        if api_success or local_success:
            print("✅ Data loaded successfully!")
            return True
        else:
            print("⚠️  No data sources available. Starting with empty data.")
            return False
    
    def _load_from_github(self) -> bool:
        """
        Load data from GitHub repository.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # GitHub API endpoint for repository contents
            # Format: https://api.github.com/repos/{owner}/{repo}/contents/{path}
            repo_parts = self.github_repo.replace('https://github.com/', '').strip('/')
            api_url = f"https://api.github.com/repos/{repo_parts}/contents"
            
            print(f"  📡 Fetching from GitHub API: {repo_parts}")
            
            # Get list of files in repository
            response = requests.get(api_url, timeout=10)
            
            if response.status_code != 200:
                print(f"  ⚠️  GitHub API returned status code {response.status_code}")
                return False
            
            files = response.json()
            json_files = [f for f in files if f['name'].endswith('.json')]
            
            if not json_files:
                print("  ⚠️  No JSON files found in repository")
                return False
            
            # Load each JSON file
            for file_info in json_files:
                file_name = file_info['name']
                download_url = file_info['download_url']
                
                print(f"  📥 Loading {file_name}...")
                file_response = requests.get(download_url, timeout=10)
                
                if file_response.status_code == 200:
                    file_data = file_response.json()
                    self._merge_api_data(file_data, file_name)
                else:
                    print(f"  ⚠️  Failed to load {file_name}")
            
            print("  ✅ GitHub data loaded")
            return True
            
        except requests.RequestException as e:
            print(f"  ⚠️  Network error: {e}")
            return False
        except Exception as e:
            print(f"  ⚠️  Error loading from GitHub: {e}")
            return False
    
    def _merge_api_data(self, file_data: dict, file_name: str) -> None:
        """
        Merge data from a GitHub API file into the main data structure.
        
        Args:
            file_data: Data from JSON file
            file_name: Name of the source file
        """
        # Handle different possible file structures
        if 'ingredients' in file_data:
            for ing_data in file_data['ingredients']:
                ingredient = Ingredient.from_dict(ing_data)
                self.data['ingredients'][ingredient.id] = ingredient
                # Initialize inventory with default quantity
                if ingredient.id not in self.data['inventory']:
                    self.data['inventory'][ingredient.id] = 50
        
        if 'hotdogs' in file_data:
            for hd_data in file_data['hotdogs']:
                hotdog = HotDog.from_dict(hd_data)
                self.data['hotdogs'][hotdog.id] = hotdog
        
        if 'inventory' in file_data:
            self.data['inventory'].update(file_data['inventory'])
    
    def _load_from_local(self) -> bool:
        """
        Load data from local JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(self.local_file):
            print(f"  ℹ️  No local file found ({self.local_file})")
            return False
        
        try:
            print(f"  📂 Loading from {self.local_file}...")
            with open(self.local_file, 'r', encoding='utf-8') as f:
                local_data = json.load(f)
            
            # Merge ingredients
            if 'ingredients' in local_data:
                for ing_data in local_data['ingredients']:
                    ingredient = Ingredient.from_dict(ing_data)
                    self.data['ingredients'][ingredient.id] = ingredient
            
            # Merge hot dogs
            if 'hotdogs' in local_data:
                for hd_data in local_data['hotdogs']:
                    hotdog = HotDog.from_dict(hd_data)
                    self.data['hotdogs'][hotdog.id] = hotdog
            
            # Merge inventory
            if 'inventory' in local_data:
                self.data['inventory'].update(local_data['inventory'])
            
            # Load sales history
            if 'sales_history' in local_data:
                self.data['sales_history'] = [
                    SalesDay.from_dict(sd) for sd in local_data['sales_history']
                ]
            
            print("  ✅ Local data loaded")
            return True
            
        except Exception as e:
            print(f"  ⚠️  Error loading local file: {e}")
            return False
    
    def save_to_local(self) -> bool:
        """
        Save current data to local JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for serialization
            save_data = {
                'ingredients': [ing.to_dict() for ing in self.data['ingredients'].values()],
                'hotdogs': [hd.to_dict() for hd in self.data['hotdogs'].values()],
                'inventory': self.data['inventory'],
                'sales_history': [sd.to_dict() for sd in self.data['sales_history']]
            }
            
            # Save to file
            with open(self.local_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving to local file: {e}")
            return False
    
    def get_ingredients(self) -> Dict[str, Ingredient]:
        """Get all ingredients."""
        return self.data['ingredients']
    
    def get_hotdogs(self) -> Dict[str, HotDog]:
        """Get all hot dogs."""
        return self.data['hotdogs']
    
    def get_inventory(self) -> Dict[str, int]:
        """Get inventory."""
        return self.data['inventory']
    
    def get_sales_history(self) -> List[SalesDay]:
        """Get sales history."""
        return self.data['sales_history']
    
    def add_ingredient(self, ingredient: Ingredient, initial_quantity: int = 0) -> None:
        """Add a new ingredient."""
        self.data['ingredients'][ingredient.id] = ingredient
        self.data['inventory'][ingredient.id] = initial_quantity
        self.save_to_local()
    
    def remove_ingredient(self, ingredient_id: str) -> None:
        """Remove an ingredient."""
        if ingredient_id in self.data['ingredients']:
            del self.data['ingredients'][ingredient_id]
        if ingredient_id in self.data['inventory']:
            del self.data['inventory'][ingredient_id]
        self.save_to_local()
    
    def add_hotdog(self, hotdog: HotDog) -> None:
        """Add a new hot dog."""
        self.data['hotdogs'][hotdog.id] = hotdog
        self.save_to_local()
    
    def remove_hotdog(self, hotdog_id: str) -> None:
        """Remove a hot dog."""
        if hotdog_id in self.data['hotdogs']:
            del self.data['hotdogs'][hotdog_id]
        self.save_to_local()
    
    def update_inventory(self, ingredient_id: str, quantity: int) -> None:
        """Update inventory quantity."""
        self.data['inventory'][ingredient_id] = quantity
        self.save_to_local()
    
    def add_sales_day(self, sales_day: SalesDay) -> None:
        """Add a sales day to history."""
        self.data['sales_history'].append(sales_day)
        self.save_to_local()