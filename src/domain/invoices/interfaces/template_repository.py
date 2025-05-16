from abc import ABC, abstractmethod
from typing import Iterable


class TemplateRepository(ABC):
    @abstractmethod
    def save(self, template_name: str, content: bytes) -> None:
        # almacena/reemplaza el template en el sistema
        pass

    # @abstractmethod
    # def load(self, template_name: str) -> str:
    #     # devuelve el template
    #     pass

    @abstractmethod
    def list(self) -> Iterable[str]:
        # devuelve la lista de templates
        pass
