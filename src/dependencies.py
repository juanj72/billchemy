from pathlib import Path
from src.usecases.invoices.save_template import SaveTemplate
from src.adapters.invoices.template_repository import FileSystemTemplateRepository


def get_save_template_uc() -> SaveTemplate:
    repo = FileSystemTemplateRepository(base_dir=Path("src/raw/templates"))
    return SaveTemplate(repo)
