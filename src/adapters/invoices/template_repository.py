from pathlib import Path
from src.domain.invoices.interfaces.template_repository import TemplateRepository
from typing import Iterable


class FileSystemTemplateRepository(TemplateRepository):
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self, template_name: str, content: bytes
    ) -> Path:  # TODO: change this method of save
        template_path = self.base_dir / template_name
        template_path.write_bytes(content)
        return template_path

    def list(self) -> Iterable[Path]:
        return self.base_dir.iterdir()

    def get_template(self, template_name: str) -> bool:
        template_path = self.base_dir / template_name
        return template_path.exists()
