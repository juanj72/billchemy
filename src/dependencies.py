from pathlib import Path
from src.usecases.invoices.save_template import SaveTemplateUseCase
from src.usecases.invoices.list_template import ListTemplateUseCase
from src.adapters.invoices.template_repository import FileSystemTemplateRepository


def get_save_template_uc() -> SaveTemplateUseCase:
    repo = FileSystemTemplateRepository(base_dir=Path("src/raw/templates"))
    return SaveTemplateUseCase(repo)


def get_list_template_uc() -> ListTemplateUseCase:
    repo = FileSystemTemplateRepository(base_dir=Path("src/raw/templates"))
    return ListTemplateUseCase(repo)
