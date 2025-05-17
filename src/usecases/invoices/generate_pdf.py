# src/usecases/invoices/generate_pdf.py
from pathlib import Path
from src.domain.invoices.entities.invoice import Invoice
from src.domain.invoices.interfaces.pdf_generator import PDFGenerator
from src.domain.invoices.interfaces.template_repository import TemplateRepository


class GeneratePDFUseCase:
    def __init__(
        self, pdf_generator: PDFGenerator, template_repository: TemplateRepository
    ):
        self.pdf_generator = pdf_generator
        self.template_repository = template_repository

    def execute(self, invoice: Invoice, template_name: Path) -> bytes:

        available = [p.name for p in self.template_repository.list()]
        if str(template_name) not in available:
            raise ValueError(f"Template «{template_name}» not found")

        return self.pdf_generator.generate(invoice, template_name)
