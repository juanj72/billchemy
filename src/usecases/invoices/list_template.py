from src.domain.invoices.interfaces.template_repository import TemplateRepository
from typing import Iterable


class ListTemplateUseCase:
    def __init__(self, template_repository: TemplateRepository):
        self.template_repository = template_repository

    def execute(self) -> Iterable[str]:
        name_list = [p.name for p in self.template_repository.list()]

        return name_list
