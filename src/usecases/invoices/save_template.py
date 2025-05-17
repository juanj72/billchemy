from src.domain.invoices.interfaces.template_repository import TemplateRepository
from pathlib import Path


class SaveTemplateUseCase:
    def __init__(self, template_repository: TemplateRepository):
        self.template_repository = template_repository

    def execute(self, template_name: str, content: bytes) -> Path:
        if not template_name.lower().endswith(".docx"):
            raise ValueError("Template name must end with .docx")

        saver_path = self.template_repository.save(template_name, content)
        return saver_path
