from pathlib import Path
from src.domain.invoices.interfaces.template_repository import TemplateRepository

class FileSystemTemplateRepository(TemplateRepository):
    def __init__(self, base_dir:Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, template_name: str, content: bytes) -> Path:
        template_path = self.base_dir / template_name
        template_path.write_bytes(content)
        return template_path