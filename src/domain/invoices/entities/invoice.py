from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    code_reference: str
    name: str
    quantity: int
    price: int

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be greater than 0")
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if self.name == "" or self.name is None:
            raise ValueError("Name is required")


@dataclass
class Customer:
    identification: int
    company: str
    names: str
    address: str
    email: str
    phone: str

    def __post_init__(self):

        if self.identification == "" or self.identification is None:
            raise ValueError("Identification is required")

        if self.names == "" or self.names is None:
            raise ValueError("Names is required")

        if self.address == "" or self.address is None:
            raise ValueError("Address is required")

        if self.email == "" or self.email is None:
            raise ValueError("Email is required")

        if self.phone == "" or self.phone is None:
            raise ValueError("Phone is required")


@dataclass
class Invoice:
    # numbering_range_id: int
    reference_code: str
    observation: str
    payment_method_code: int
    items: List[Item]
    customer: Customer

    def __post_init__(self):
        if self.reference_code == "" or self.reference_code is None:
            raise ValueError("Reference code is required")

        if self.payment_method_code == "" or self.payment_method_code is None:
            raise ValueError("Payment method code is required")

        if self.items == "" or self.items is None:
            raise ValueError("Items is required")
