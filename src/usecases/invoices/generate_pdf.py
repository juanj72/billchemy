# src/usecases/invoices/generate_pdf.py
from pathlib import Path
from src.domain.invoices.entities.invoice import Invoice
from src.domain.invoices.interfaces.template_render import TemplateRender
from src.domain.invoices.interfaces.template_repository import TemplateRepository
from src.domain.invoices.interfaces.pdf_generator import PDFGenerator


class GeneratePDFUseCase:
    def __init__(
        self,
        template_render: TemplateRender,
        template_repository: TemplateRepository,
        pdf_generator: PDFGenerator,
    ):
        self.template_render = template_render
        self.template_repository = template_repository
        self.pdf_generator = pdf_generator

    def execute(self, invoice: Invoice, template_name: Path) -> bytes:

        available = [p.name for p in self.template_repository.list()]
        if str(template_name) not in available:
            raise ValueError(f"Template «{template_name}» not found")

        return self.pdf_generator.generate(
            self.template_render.render(invoice, template_name)
        )
