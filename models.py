#Contiene las classes para: Ingredient, HotDog, y SalesDay.

from typing import List, Optional, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Ingredient:
    id: str
    name: str
    category: str
    type: str
    length: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'type': self.type,
            'length': self.length
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Ingredient':
        return Ingredient(
            id=data.get('id', ''),
            name=data.get('name', ''),
            category=data.get('category', ''),
            type=data.get('type', ''),
            length=data.get('length')
        )
    
    def __str__(self) -> str:
        length_info = f" (Length: {self.length})" if self.length else ""
        return f"{self.name} [{self.type}]{length_info}"


@dataclass
class HotDog:
    id: str
    name: str
    pan_id: str
    salchicha_id: str
    topping_ids: List[str] = field(default_factory=list)
    salsa_ids: List[str] = field(default_factory=list)
    acompañante_id: Optional[str] = None
    
    def to_dict(self) -> dict:
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
        ids = [self.pan_id, self.salchicha_id]
        ids.extend(self.topping_ids)
        ids.extend(self.salsa_ids)
        if self.acompañante_id:
            ids.append(self.acompañante_id)
        return ids


@dataclass
class SalesDay:
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