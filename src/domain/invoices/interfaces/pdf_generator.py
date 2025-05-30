from abc import ABC, abstractmethod
from pathlib import Path


class PDFGenerator(ABC):
    @abstractmethod
    def generate(self, template_path: Path) -> bytes:
        # devuelve el pdf con los valores llenados del template
        pass
