# src/schemas/invoice_schema.py

from pydantic import BaseModel, EmailStr
from typing import List


# Importa tus dataclasses de dominio con alias para evitar colisiones de nombres
from src.domain.invoices.entities.invoice import (
    Item as ItemDomain,
    Customer as CustomerDomain,
    Invoice as InvoiceDomain,
)


class ItemSchema(BaseModel):
    code_reference: str
    name: str
    quantity: int
    price: int

    def to_domain(self) -> ItemDomain:
        return ItemDomain(
            code_reference=self.code_reference,
            name=self.name,
            quantity=self.quantity,
            price=self.price,
        )


class CustomerSchema(BaseModel):
    identification: int
    company: str
    names: str
    address: str
    email: EmailStr
    phone: str

    def to_domain(self) -> CustomerDomain:
        return CustomerDomain(
            identification=self.identification,
            company=self.company,
            names=self.names,
            address=self.address,
            email=self.email,
            phone=self.phone,
        )


class InvoiceDataSchema(BaseModel):
    reference_code: str
    observation: str
    payment_method_code: int
    customer: CustomerSchema
    items: List[ItemSchema]

    def to_domain(self) -> InvoiceDomain:
        return InvoiceDomain(
            reference_code=self.reference_code,
            observation=self.observation,
            payment_method_code=self.payment_method_code,
            items=[item.to_domain() for item in self.items],
            customer=self.customer.to_domain(),
        )


class InvoiceRequest(BaseModel):
    """
    Request DTO para generar un PDF de factura.
    Contiene la ruta de la plantilla y los datos de la factura.
    """

    template_name: str
    invoice: InvoiceDataSchema

    def to_domain(self):
        """
        Devuelve una tupla (InvoiceDomain, template_name) lista para el use case.
        """
        return self.invoice.to_domain(), self.template_name


class InvoiceResponse(BaseModel):
    reference_code: str
    total: int

    @classmethod
    def from_domain(cls, invoice: InvoiceDomain) -> "InvoiceResponse":
        total = sum(item.quantity * item.price for item in invoice.items)
        return cls(
            reference_code=invoice.reference_code,
            total=total,
        )
