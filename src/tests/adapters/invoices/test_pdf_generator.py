# src/tests/adapters/invoices/test_pdf_generator.py
import subprocess
import pytest
from src.adapters.invoices.pdf_generator import LibreOfficePDFGenerator


@pytest.fixture
def dummy_docx(tmp_path):
    p = tmp_path / "dummy.docx"
    p.write_bytes(b"FAKE-DOCX")
    return p


@pytest.fixture
def output_dir(tmp_path):
    return tmp_path / "pdfs"


def test_generate_success(monkeypatch, dummy_docx, output_dir):
    """
    Cuando subprocess.run 'convierte' y crea dummy.pdf, generate() debe
    devolver sus bytes y no lanzar FileExistsError.
    """
    pdf_path = output_dir / "dummy.pdf"

    def fake_run(cmd, check):
        # NOTA: NO volvemos a mkdir(), porque el adaptador ya lo hizo en __init__
        output_dir.mkdir(exist_ok=True)  # opcional, con exist_ok=True
        pdf_path.write_bytes(b"%PDF-1.4")
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    gen = LibreOfficePDFGenerator(output_dir=output_dir)
    data = gen.generate(dummy_docx)

    assert data.startswith(b"%PDF-1.4")
    assert pdf_path.exists()


def test_generate_command_failure(monkeypatch, dummy_docx, output_dir):
    def fake_run(cmd, check):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)

    gen = LibreOfficePDFGenerator(output_dir=output_dir)
    with pytest.raises(subprocess.CalledProcessError):
        gen.generate(dummy_docx)


def test_generate_no_pdf(monkeypatch, dummy_docx, output_dir):
    def fake_run(cmd, check):
        # Simula éxito pero sin crear PDF
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    gen = LibreOfficePDFGenerator(output_dir=output_dir)
    with pytest.raises(RuntimeError) as exc:
        gen.generate(dummy_docx)

    assert "PDF conversion failed" in str(exc.value)
