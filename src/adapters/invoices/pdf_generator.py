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

    def generate(self, template_path: Path) -> bytes:

        # Ejecutar la conversión indicando el directorio de salida
        cmd = [
            (
                "soffice"
                if subprocess.call(["which", "soffice"], stdout=subprocess.DEVNULL) == 0
                else "libreoffice"
            ),
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(self.output_dir),
            str(template_path),
        ]
        subprocess.run(cmd, check=True)

        # Construir la ruta del PDF resultante
        pdf_path = self.output_dir / f"{template_path.stem}.pdf"
        if not pdf_path.exists():
            raise RuntimeError(f"PDF conversion failed, file not found: {pdf_path}")

        # Leer y devolver el contenido en bytes
        data = pdf_path.read_bytes()
        return data
