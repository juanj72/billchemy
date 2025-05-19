import pytest
from src.domain.invoices.entities.invoice import Item, Customer, Invoice


# ---------- Item ----------


def test_item_valid_and_total():
    item = Item(code_reference="X1", name="Widget", quantity=3, price=100)
    assert item.price == 100
    assert item.quantity == 3
    assert item.total == 300  # 3 * 100


@pytest.mark.parametrize("price", [0, -10])
def test_item_invalid_price(price):
    with pytest.raises(ValueError) as exc:
        Item(code_reference="X1", name="Widget", quantity=1, price=price)
    assert "Price must be greater than 0" in str(exc.value)


@pytest.mark.parametrize("quantity", [0, -5])
def test_item_invalid_quantity(quantity):
    with pytest.raises(ValueError) as exc:
        Item(code_reference="X1", name="Widget", quantity=quantity, price=100)
    assert "Quantity must be greater than 0" in str(exc.value)


@pytest.mark.parametrize("name", ["", None])
def test_item_invalid_name(name):
    with pytest.raises(ValueError) as exc:
        Item(code_reference="X1", name=name, quantity=1, price=100)
    assert "Name is required" in str(exc.value)


# ---------- Customer ----------


def test_customer_valid():
    cust = Customer(
        identification=123,
        company="Acme",
        names="Jane Doe",
        address="123 Main St",
        email="jane@acme.com",
        phone="555-1234",
    )
    assert cust.identification == 123
    assert cust.company == "Acme"
    assert cust.names == "Jane Doe"


@pytest.mark.parametrize(
    "field, bad",
    [
        ("identification", None),
        ("identification", ""),
        ("names", None),
        ("names", ""),
        ("address", None),
        ("address", ""),
        ("email", None),
        ("email", ""),
        ("phone", None),
        ("phone", ""),
    ],
)
def test_customer_invalid(field, bad):
    kwargs = {
        "identification": 1,
        "company": "Acme",
        "names": "Jane Doe",
        "address": "123 Main St",
        "email": "jane@acme.com",
        "phone": "555-1234",
    }
    kwargs[field] = bad
    with pytest.raises(ValueError) as exc:
        Customer(**kwargs)  # type: ignore
    msg = str(exc.value)
    # chequea que mencione el campo
    assert field.capitalize() in msg or "required" in msg


# ---------- Invoice ----------


@pytest.fixture
def sample_item():
    return Item(code_reference="X1", name="Widget", quantity=2, price=500)


@pytest.fixture
def sample_customer():
    return Customer(
        identification=123,
        company="Acme",
        names="Jane Doe",
        address="123 Main St",
        email="jane@acme.com",
        phone="555-1234",
    )


def test_invoice_valid_and_total(sample_item, sample_customer):
    inv = Invoice(
        reference_code="INV-001",
        observation="Test",
        payment_method_code=1,
        items=[sample_item],
        customer=sample_customer,
    )
    assert inv.reference_code == "INV-001"
    assert inv.total == 1000  # 2 * 500


@pytest.mark.parametrize("ref", ["", None])
def test_invoice_invalid_reference(ref, sample_item, sample_customer):
    with pytest.raises(ValueError) as exc:
        Invoice(
            reference_code=ref,
            observation="",
            payment_method_code=1,
            items=[sample_item],
            customer=sample_customer,
        )
    assert "Reference code is required" in str(exc.value)


@pytest.mark.parametrize("pm", ["", None])
def test_invoice_invalid_payment_method(pm, sample_item, sample_customer):
    with pytest.raises(ValueError) as exc:
        Invoice(
            reference_code="INV-001",
            observation="",
            payment_method_code=pm,
            items=[sample_item],
            customer=sample_customer,
        )
    assert "Payment method code is required" in str(exc.value)


def test_invoice_invalid_items(sample_customer):
    with pytest.raises(ValueError) as exc:
        Invoice(
            reference_code="INV-001",
            observation="",
            payment_method_code=1,
            items=None,  # type: ignore
            customer=sample_customer,
        )
    assert "Items is required" in str(exc.value)
