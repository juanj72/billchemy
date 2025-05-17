from abc import ABC, abstractmethod
from typing import Iterable
from pathlib import Path


class TemplateRepository(ABC):
    @abstractmethod
    def save(self, template_name: str, content: bytes) -> Path:
        # almacena/reemplaza el template en el sistema
        pass

    # @abstractmethod
    # def load(self, template_name: str) -> str:
    #     # devuelve el template
    #     pass

    @abstractmethod
    def list(self) -> Iterable[Path]:
        # devuelve la lista de templates
        pass

    @abstractmethod
    def get_template(self, template_name: str) -> bool:
        # devuelve el template
        pass
