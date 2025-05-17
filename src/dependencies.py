from pathlib import Path
from src.usecases.invoices.save_template import SaveTemplateUseCase
from src.usecases.invoices.list_template import ListTemplateUseCase
from src.adapters.invoices.template_repository import FileSystemTemplateRepository
from src.adapters.invoices.pdf_generator import DocxToPdfGenerator
from src.usecases.invoices.generate_pdf import GeneratePDFUseCase


TEMPLATES_DIR = Path("src/raw/templates")


def get_save_template_uc() -> SaveTemplateUseCase:
    repo = FileSystemTemplateRepository(base_dir=TEMPLATES_DIR)
    return SaveTemplateUseCase(repo)


def get_list_template_uc() -> ListTemplateUseCase:
    repo = FileSystemTemplateRepository(base_dir=TEMPLATES_DIR)
    return ListTemplateUseCase(repo)


def get_generate_pdf_uc() -> GeneratePDFUseCase:
    pdf_generator = DocxToPdfGenerator(templates_dir=TEMPLATES_DIR)
    repo = FileSystemTemplateRepository(base_dir=TEMPLATES_DIR)
    return GeneratePDFUseCase(pdf_generator, repo)
