import pytest
from pathlib import Path
from src.usecases.invoices.generate_pdf import GeneratePDFUseCase
from src.domain.invoices.entities.invoice import Invoice, Item, Customer


class DummyRender:
    def __init__(self, out_path: Path):
        self.out_path = out_path

    def render(self, invoice: Invoice, template_name: Path) -> Path:
        # Simula que escribe un .docx en out_path
        self.out_path.write_bytes(b"rendered")
        return self.out_path


class DummyPDFGen:
    def __init__(self, data: bytes):
        self.data = data

    def generate(self, docx_path: Path) -> bytes:
        # Comprueba que recibe la ruta correcta
        assert docx_path.exists()
        return self.data


class DummyRepo:
    def __init__(self, templates):
        # templates: iterable de nombres de fichero
        self._templates = templates

    def list(self):
        # Devuelve Paths con esos nombres
        return [Path(name) for name in self._templates]


@pytest.fixture
def sample_invoice():
    items = [Item("X1", "A", 1, 100)]
    customer = Customer(1, "Co", "Name", "Addr", "a@b.c", "123")
    return Invoice(
        reference_code="R1",
        observation="obs",
        payment_method_code=1,
        items=items,
        customer=customer,
    )


def test_execute_success(tmp_path, sample_invoice):
    # Prepara un repo que contiene "tpl.docx"
    repo = DummyRepo(templates=["tpl.docx"])
    # El render creará un fichero en tmp_path/rendered.docx
    rendered = tmp_path / "rendered.docx"
    renderer = DummyRender(out_path=rendered)
    # El PDF generator devolverá estos bytes
    pdf_bytes = b"%PDF-SUCCESS%"
    pdfgen = DummyPDFGen(data=pdf_bytes)

    uc = GeneratePDFUseCase(renderer, repo, pdfgen)  # type: ignore
    result = uc.execute(sample_invoice, Path("tpl.docx"))

    assert result == pdf_bytes


def test_execute_template_not_found(sample_invoice):
    repo = DummyRepo(templates=[])  # no hay templates
    renderer = DummyRender(out_path=Path("unused.docx"))
    pdfgen = DummyPDFGen(data=b"")

    uc = GeneratePDFUseCase(renderer, repo, pdfgen)  # type: ignore
    with pytest.raises(ValueError) as exc:
        uc.execute(sample_invoice, Path("missing.docx"))
    assert "Template «missing.docx» not found" in str(exc.value)


def test_execute_render_raises(sample_invoice):
    # El renderer lanza cualquier excepción
    class BadRender:
        def render(self, invoice, tpl):
            raise RuntimeError("render failed")

    repo = DummyRepo(templates=["t.docx"])
    uc = GeneratePDFUseCase(BadRender(), repo, DummyPDFGen(data=b""))  # type: ignore
    with pytest.raises(RuntimeError) as exc:
        uc.execute(sample_invoice, Path("t.docx"))
    assert "render failed" in str(exc.value)


def test_execute_pdfgen_raises(tmp_path, sample_invoice):
    repo = DummyRepo(templates=["t.docx"])
    rendered = tmp_path / "rendered.docx"
    renderer = DummyRender(out_path=rendered)

    class BadPDFGen:
        def generate(self, p):
            raise RuntimeError("pdf failed")

    uc = GeneratePDFUseCase(renderer, repo, BadPDFGen())  # type:ignore
    with pytest.raises(RuntimeError) as exc:
        uc.execute(sample_invoice, Path("t.docx"))
    assert "pdf failed" in str(exc.value)
