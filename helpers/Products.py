from dataclasses import dataclass,asdict
import uuid
from typing import Optional, List, Tuple

@dataclass
class ProductFilters:
    colours: Optional[List[str]] = None
    types: Optional[List[str]] = None
    price_range: Optional[Tuple[float, float]] = None
    ids: Optional[List[str]] = None

    @classmethod
    def from_json(cls, data):
        colours = data.get('colours', None)
        types = data.get('types', None)
        price_range = tuple(data.get('price_range', [None, None]))
        ids = data.get('ids', None)
        result = cls(colours=colours, types=types, price_range=price_range, ids=ids)
        return result


@dataclass
class Product:
    id: str
    name: str
    description: str
    colour: str
    type: str
    images_location: str
    price: float

    @classmethod
    def from_json(cls, data):
        required_fields = ['name', 'description', 'colour', 'type', 'images_location', 'price']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')

        product_id = str(uuid.uuid4())  # Generate a unique ID for the product
        return cls(
            id=product_id,
            name=data['name'],
            description=data['description'],
            colour=data['colour'],
            type=data['type'],
            images_location=data['images_location'],
            price=float(data['price'])  # Assuming price is stored as float
        )

    def to_dict(self):
        return asdict(self)
