# src/tests/schemas/test_invoice_schema.py

import pytest
from pydantic import ValidationError
from src.schemas.invoice_schema import (
    ItemSchema,
    CustomerSchema,
    InvoiceDataSchema,
    InvoiceRequest,
    InvoiceResponse,
)
from src.domain.invoices.entities.invoice import (
    Item as ItemDomain,
    Customer as CustomerDomain,
    Invoice as InvoiceDomain,
)

# ------- ItemSchema --------


def test_item_schema_to_domain_success():
    schema = ItemSchema(
        code_reference="ABC123", name="Test Item", quantity=2, price=1500
    )
    domain = schema.to_domain()
    assert isinstance(domain, ItemDomain)
    assert domain.code_reference == "ABC123"
    assert domain.name == "Test Item"
    assert domain.quantity == 2
    assert domain.price == 1500
    assert domain.total == 3000


@pytest.mark.parametrize(
    "field, value, msg",
    [
        ("quantity", 0, "Quantity must be greater than 0"),
        ("quantity", -5, "Quantity must be greater than 0"),
        ("price", 0, "Price must be greater than 0"),
        ("price", -10, "Price must be greater than 0"),
    ],
)
def test_item_schema_invalid_numbers(field, value, msg):
    kwargs = {
        "code_reference": "X",
        "name": "Y",
        "quantity": 1,
        "price": 100,
    }

    kwargs[field] = value

    schema = ItemSchema(**kwargs)  # type: ignore

    with pytest.raises(ValueError) as exc:
        schema.to_domain()

    assert msg in str(exc.value)


# ------- CustomerSchema --------


def test_customer_schema_to_domain_success():
    schema = CustomerSchema(
        identification=123,
        company="My Co",
        names="John Doe",
        address="123 Main St",
        email="john@example.com",
        phone="555-0101",
    )
    domain = schema.to_domain()
    assert isinstance(domain, CustomerDomain)
    assert domain.identification == 123
    assert domain.company == "My Co"
    assert domain.names == "John Doe"
    assert domain.email == "john@example.com"


@pytest.mark.parametrize("email", ["not-an-email", ""])
def test_customer_schema_invalid_email(email):
    kwargs = {
        "identification": 1,
        "company": "Co",
        "names": "Name",
        "address": "Addr",
        "email": email,
        "phone": "123",
    }
    with pytest.raises(ValidationError) as exc:
        CustomerSchema(**kwargs)
    assert "value is not a valid email address" in str(exc.value)


# ------- InvoiceDataSchema --------


@pytest.fixture
def valid_invoice_data():
    return {
        "reference_code": "INV-100",
        "observation": "Obs",
        "payment_method_code": 2,
        "customer": {
            "identification": 10,
            "company": "Co",
            "names": "Jane",
            "address": "Addr",
            "email": "jane@doe.com",
            "phone": "000",
        },
        "items": [
            {"code_reference": "I1", "name": "Item1", "quantity": 1, "price": 500},
            {"code_reference": "I2", "name": "Item2", "quantity": 3, "price": 200},
        ],
    }


def test_invoice_data_schema_to_domain(valid_invoice_data):
    schema = InvoiceDataSchema(**valid_invoice_data)
    domain = schema.to_domain()
    assert isinstance(domain, InvoiceDomain)
    assert domain.reference_code == "INV-100"
    # total = 1*500 + 3*200 = 1100
    assert domain.total == 1100
    # customer nested
    assert isinstance(domain.customer, CustomerDomain)
    # items nested
    assert all(isinstance(it, ItemDomain) for it in domain.items)


@pytest.mark.parametrize("field", ["reference_code", "payment_method_code"])
def test_invoice_data_schema_missing_required(field, valid_invoice_data):
    data = valid_invoice_data.copy()
    data.pop(field)
    with pytest.raises(ValidationError) as exc:
        InvoiceDataSchema(**data)
    assert field in str(exc.value)


# ------- InvoiceRequest --------


def test_invoice_request_to_domain(valid_invoice_data):
    req = InvoiceRequest(template_name="tpl.docx", invoice=valid_invoice_data)
    inv_domain, tpl_name = req.to_domain()
    assert isinstance(inv_domain, InvoiceDomain)
    assert tpl_name == "tpl.docx"


# ------- InvoiceResponse --------


def test_invoice_response_from_domain(valid_invoice_data):
    schema = InvoiceDataSchema(**valid_invoice_data)
    inv = schema.to_domain()
    resp = InvoiceResponse.from_domain(inv)
    assert resp.reference_code == inv.reference_code
    # total computed correctly
    assert resp.total == inv.total
