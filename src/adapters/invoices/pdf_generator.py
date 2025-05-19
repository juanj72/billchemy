import subprocess
from pathlib import Path
from src.domain.invoices.interfaces.pdf_generator import PDFGenerator


class LibreOfficePDFGenerator(PDFGenerator):
    """
    Adaptador que convierte un .docx a PDF usando LibreOffice headless,
    guardando el PDF en un directorio de salida y devolviendo sus bytes.
    """

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _clear_output_dir(self):
        for old in self.output_dir.glob("*.pdf"):
            try:
                old.unlink()
            except OSError:
                pass

    def generate(self, rendered_path: Path) -> bytes:
        self._clear_output_dir()
        # Ejecutar la conversión indicando el directorio de salida
        cmd = [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(self.output_dir),
            str(rendered_path),
        ]
        r = subprocess.run(cmd, check=True)
        if r.returncode != 0:
            raise RuntimeError("PDF conversion failed")
        # Construir la ruta del PDF resultante
        pdf_path = self.output_dir / f"{rendered_path.stem}.pdf"
        if not pdf_path.exists():
            raise RuntimeError(
                "PDF conversion failed: please, check your template file,"
                + "check the template, it may be corrupted."
            )

        data = pdf_path.read_bytes()
        return data
