from dataclasses import dataclass, asdict
import uuid

@dataclass
class Address:
    id: str
    user_id: str
    street: str
    state: str
    zip: str
    country: str
    type : str

    @classmethod
    def from_json(cls, data):
        required_fields = ['user_id', 'street', 'state', 'zip', 'country','type']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')

        address_id = str(uuid.uuid4())
        return cls(
            id=address_id,
            user_id=data['user_id'],
            street=data['street'],
            state=data['state'],
            zip=data['zip'],
            country=data['country'],
            type=data['type']
        )

    def to_dict(self):
        return asdict(self)
