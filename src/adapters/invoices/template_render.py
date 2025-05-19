# src/adapters/invoices/pdf_generator.py
from pathlib import Path
from docxtpl import DocxTemplate
from datetime import datetime
from src.domain.invoices.interfaces.template_render import TemplateRender
from src.domain.invoices.entities.invoice import Invoice


class DocxRender(TemplateRender):
    def __init__(self, templates_dir: Path, rendered_dir: Path):
        self.templates_dir = templates_dir.resolve()
        self.rendered_dir = rendered_dir.resolve()
        self.rendered_dir.mkdir(parents=True, exist_ok=True)

    def render(self, invoice: Invoice, template_name: Path) -> Path:
        original = self.templates_dir / template_name

        # Render con docxtpl
        tpl = DocxTemplate(str(original))
        tpl.render(
            {
                "invoice": invoice,
                "items": invoice.items,
                "customer": invoice.customer,
                "today": datetime.now().date(),
            }
        )

        temp_name = f"rendered_{invoice.reference_code}.docx"
        temp_docx = self.rendered_dir / temp_name
        tpl.save(str(temp_docx))

        return Path(temp_docx)
