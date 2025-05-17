# src/adapters/invoices/pdf_generator.py
from pathlib import Path
from io import BytesIO
from docxtpl import DocxTemplate
import mammoth
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from src.domain.invoices.interfaces.pdf_generator import PDFGenerator
from src.domain.invoices.entities.invoice import Invoice


class DocxToPdfGenerator(PDFGenerator):
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.font_config = FontConfiguration()

    def generate(self, invoice: Invoice, template_name: Path) -> bytes:
        template_path = self.templates_dir / template_name
        tpl = DocxTemplate(str(template_path))
        tpl.render(
            {
                "invoice": invoice,
                "items": invoice.items,
            }
        )

        docx_io = BytesIO()  # TODO: cambiar la forma en que se convierte a pdf
        tpl.save(docx_io)
        docx_io.seek(0)

        html = mammoth.convert_to_html(docx_io).value

        pdf_bytes = (
            HTML(string=html, base_url=str(self.templates_dir))
            .render(font_config=self.font_config)
            .write_pdf()
        )
        return pdf_bytes
