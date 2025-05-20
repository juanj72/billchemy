import pytest
from pathlib import Path
from src.usecases.invoices.save_template import SaveTemplateUseCase
from src.domain.invoices.interfaces.template_repository import TemplateRepository


class DummyRepo(TemplateRepository):
    def __init__(self):
        self.saved = {}

    def save(self, template_name: str, content: bytes) -> Path:

        p = Path("/tmp") / template_name
        self.saved[template_name] = content
        return p

    def list(self):
        raise NotImplementedError

    def get_template(self, name: str):
        raise NotImplementedError


def test_execute_success(tmp_path):

    repo = DummyRepo()
    uc = SaveTemplateUseCase(template_repository=repo)

    name = "invoice_template.docx"
    data = b"fake content"
    result = uc.execute(name, data)

    assert isinstance(result, Path)
    assert result.name == name

    assert repo.saved[name] == data


@pytest.mark.parametrize("bad_name", ["template.pdf", "doc.TXT", "noext"])
def test_execute_invalid_extension(bad_name):
    uc = SaveTemplateUseCase(template_repository=DummyRepo())
    with pytest.raises(ValueError) as exc:
        uc.execute(bad_name, b"")
    assert "Template name must end with .docx" in str(exc.value)


def test_execute_repo_error_propagates():
    class BadRepo(TemplateRepository):
        def save(self, template_name: str, content: bytes):
            raise RuntimeError("disk full")

        def list(self): ...
        def get_template(self, name: str): ...

    uc = SaveTemplateUseCase(template_repository=BadRepo())
    with pytest.raises(RuntimeError) as exc:
        uc.execute("t.docx", b"data")
    assert "disk full" in str(exc.value)
