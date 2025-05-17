from abc import ABC, abstractmethod
from src.domain.invoices.entities.invoice import Invoice
from pathlib import Path


class PDFGenerator(ABC):
    @abstractmethod
    def generate(self, invoice: Invoice, template_path: Path) -> bytes:
        # devuelve el pdf con los valores llenados del template
        pass
