from abc import ABC, abstractmethod
from src.domain.invoices.entities.invoice import Invoice
from pathlib import Path


class TemplateRender(ABC):
    @abstractmethod
    def render(self, invoice: Invoice, template_path: Path) -> Path:
        # devuelve el pdf con los valores llenados del template
        pass
