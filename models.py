"""
Data models for Hot Dog CCS application.
Contains classes for Ingredient, HotDog, and SalesDay.
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Ingredient:
    """
    Represents an ingredient with its properties.
    
    Attributes:
        id: Unique identifier for the ingredient
        name: Display name of the ingredient
        category: Category (Pan, Salchicha, Topping, Salsa, Acompañante)
        type: Type within category (e.g., normal, large)
        length: Optional length attribute for Pan and Salchicha
    """
    id: str
    name: str
    category: str
    type: str
    length: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert ingredient to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'type': self.type,
            'length': self.length
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Ingredient':
        """Create ingredient from dictionary."""
        return Ingredient(
            id=data.get('id', ''),
            name=data.get('name', ''),
            category=data.get('category', ''),
            type=data.get('type', ''),
            length=data.get('length')
        )
    
    def __str__(self) -> str:
        """String representation of ingredient."""
        length_info = f" (Length: {self.length})" if self.length else ""
        return f"{self.name} [{self.type}]{length_info}"


@dataclass
class HotDog:
    """
    Represents a hot dog menu item.
    
    Attributes:
        id: Unique identifier
        name: Name of the hot dog
        pan_id: ID of the bread ingredient
        salchicha_id: ID of the sausage ingredient
        topping_ids: List of topping ingredient IDs
        salsa_ids: List of salsa ingredient IDs
        acompañante_id: Optional side dish ingredient ID
    """
    id: str
    name: str
    pan_id: str
    salchicha_id: str
    topping_ids: List[str] = field(default_factory=list)
    salsa_ids: List[str] = field(default_factory=list)
    acompañante_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert hot dog to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'pan_id': self.pan_id,
            'salchicha_id': self.salchicha_id,
            'topping_ids': self.topping_ids,
            'salsa_ids': self.salsa_ids,
            'acompañante_id': self.acompañante_id
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'HotDog':
        """Create hot dog from dictionary."""
        return HotDog(
            id=data.get('id', ''),
            name=data.get('name', ''),
            pan_id=data.get('pan_id', ''),
            salchicha_id=data.get('salchicha_id', ''),
            topping_ids=data.get('topping_ids', []),
            salsa_ids=data.get('salsa_ids', []),
            acompañante_id=data.get('acompañante_id')
        )
    
    def get_all_ingredient_ids(self) -> List[str]:
        """Get all ingredient IDs used in this hot dog."""
        ids = [self.pan_id, self.salchicha_id]
        ids.extend(self.topping_ids)
        ids.extend(self.salsa_ids)
        if self.acompañante_id:
            ids.append(self.acompañante_id)
        return ids


@dataclass
class SalesDay:
    """
    Represents statistics from a single sales day.
    
    Attributes:
        date: Date of the sales day
        clients_changed_opinion: Number of clients who bought 0 hot dogs
        clients_could_not_buy: Number of clients who left due to missing inventory
        total_clients: Total number of clients
        total_hotdogs_sold: Total hot dogs sold
        best_selling_hotdog: Name of the best-selling hot dog
        hotdogs_causing_loss: List of hot dogs that caused clients to leave
        ingredients_causing_loss: List of ingredients that were missing
        total_sides_sold: Total number of sides sold
    """
    date: str
    clients_changed_opinion: int = 0
    clients_could_not_buy: int = 0
    total_clients: int = 0
    total_hotdogs_sold: int = 0
    best_selling_hotdog: str = ""
    hotdogs_causing_loss: List[str] = field(default_factory=list)
    ingredients_causing_loss: List[str] = field(default_factory=list)
    total_sides_sold: int = 0
    
    def to_dict(self) -> dict:
        """Convert sales day to dictionary for JSON serialization."""
        return {
            'date': self.date,
            'clients_changed_opinion': self.clients_changed_opinion,
            'clients_could_not_buy': self.clients_could_not_buy,
            'total_clients': self.total_clients,
            'total_hotdogs_sold': self.total_hotdogs_sold,
            'best_selling_hotdog': self.best_selling_hotdog,
            'hotdogs_causing_loss': self.hotdogs_causing_loss,
            'ingredients_causing_loss': self.ingredients_causing_loss,
            'total_sides_sold': self.total_sides_sold
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'SalesDay':
        """Create sales day from dictionary."""
        return SalesDay(
            date=data.get('date', ''),
            clients_changed_opinion=data.get('clients_changed_opinion', 0),
            clients_could_not_buy=data.get('clients_could_not_buy', 0),
            total_clients=data.get('total_clients', 0),
            total_hotdogs_sold=data.get('total_hotdogs_sold', 0),
            best_selling_hotdog=data.get('best_selling_hotdog', ''),
            hotdogs_causing_loss=data.get('hotdogs_causing_loss', []),
            ingredients_causing_loss=data.get('ingredients_causing_loss', []),
            total_sides_sold=data.get('total_sides_sold', 0)
        )