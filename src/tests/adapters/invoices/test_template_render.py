import zipfile
import pytest
from src.adapters.invoices.template_render import DocxRender  # noqa
from src.domain.invoices.entities.invoice import Invoice, Item, Customer
from pathlib import Path


@pytest.fixture
def simple_docx():
    """
    Crea un .docx mínimo con un placeholder {{ reference_code }}
    en word/document.xml, para comprobar que DocxRender lo sustituye.
    """
    tpl = Path("src/raw/templates/template2.docx")
    return tpl


@pytest.fixture
def renderer(tmp_path, simple_docx):
    """
    Instancia el adaptador apuntando al directorio de plantilla y al de salida.
    """
    rendered_dir = tmp_path / "rendered"
    return DocxRender(templates_dir=simple_docx.parent, rendered_dir=rendered_dir)


@pytest.fixture
def sample_invoice():
    """Entidad de dominio con un único ítem y cliente dummy."""
    items = [Item(code_reference="X1", name="Test Item", quantity=2, price=1500)]
    customer = Customer(
        identification=123,
        company="ACME",
        names="John Doe",
        address="Calle Falsa 123",
        email="john@acme.com",
        phone="3001234567",
    )
    return Invoice(
        reference_code="INV-0001",
        observation="ninguna",
        payment_method_code=1,
        items=items,
        customer=customer,
    )


def test_render_creates_file_and_replaces_placeholder(
    renderer, sample_invoice, simple_docx
):
    # Llamamos a render con nuestro invoice y nombre de plantilla
    out_path = renderer.render(sample_invoice, simple_docx.name)

    # Verificamos que el archivo .docx resultante exista
    assert out_path.exists()
    assert out_path.suffix == ".docx"

    # Abrimos el .docx como ZIP y leemos el documento para comprobar la sustitución
    with zipfile.ZipFile(out_path) as z:
        content = z.read("word/document.xml").decode()
        # el placeholder {{ reference_code }} debería haber sido sustituido
        assert "INV-0001" in content
        # y ya no debe aparecer el template tag original
        assert "{{ reference_code }}" not in content
