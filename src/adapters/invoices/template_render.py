# src/adapters/invoices/pdf_generator.py
from pathlib import Path
from docxtpl import DocxTemplate
from src.domain.invoices.interfaces.template_render import TemplateRender
from src.domain.invoices.entities.invoice import Invoice
from src.utils.mappers import invoice_to_template_context


class DocxRender(TemplateRender):
    def __init__(self, templates_dir: Path, rendered_dir: Path):
        self.templates_dir = templates_dir.resolve()
        self.rendered_dir = rendered_dir.resolve()
        self.rendered_dir.mkdir(parents=True, exist_ok=True)

    def render(self, invoice: Invoice, template_name: Path) -> Path:
        original = self.templates_dir / template_name

        # Render con docxtpl
        tpl = DocxTemplate(str(original))
        invoice_ = invoice_to_template_context(invoice)
        tpl.render(invoice_)

        temp_name = f"rendered_{invoice.reference_code}.docx"
        temp_docx = self.rendered_dir / temp_name
        tpl.save(str(temp_docx))

        return Path(temp_docx)
