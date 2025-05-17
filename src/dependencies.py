from pathlib import Path
from src.usecases.invoices.save_template import SaveTemplateUseCase
from src.usecases.invoices.list_template import ListTemplateUseCase
from src.adapters.invoices.template_repository import FileSystemTemplateRepository
from src.adapters.invoices.template_render import DocxRender
from src.usecases.invoices.generate_pdf import GeneratePDFUseCase
from src.adapters.invoices.pdf_generator import LibreOfficePDFGenerator


TEMPLATES_DIR = Path("src/raw/templates")
OUTPUT_DIR = Path("src/raw/pdfs")


def get_save_template_uc() -> SaveTemplateUseCase:
    repo = FileSystemTemplateRepository(base_dir=TEMPLATES_DIR)
    return SaveTemplateUseCase(repo)


def get_list_template_uc() -> ListTemplateUseCase:
    repo = FileSystemTemplateRepository(base_dir=TEMPLATES_DIR)
    return ListTemplateUseCase(repo)


def get_generate_pdf_uc() -> GeneratePDFUseCase:
    template_render = DocxRender(templates_dir=TEMPLATES_DIR, output_dir=OUTPUT_DIR)
    repo = FileSystemTemplateRepository(base_dir=TEMPLATES_DIR)
    pdf_generator = LibreOfficePDFGenerator(output_dir=OUTPUT_DIR)

    return GeneratePDFUseCase(template_render, repo, pdf_generator)
