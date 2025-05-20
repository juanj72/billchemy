import pytest
from pathlib import Path
from src.usecases.invoices.list_template import ListTemplateUseCase
from src.domain.invoices.interfaces.template_repository import TemplateRepository


class DummyRepo(TemplateRepository):
    def __init__(self, names):

        self._paths = [Path(n) for n in names]

    def list(self):
        return self._paths

    def save(self, template_name: str, content: bytes):
        raise NotImplementedError

    def get_template(self, name: str):
        raise NotImplementedError


def test_execute_returns_names():
    repo = DummyRepo(names=["a.docx", "b.docx", "c.docx"])
    uc = ListTemplateUseCase(template_repository=repo)

    result = uc.execute()

    assert isinstance(result, list)
    assert result == ["a.docx", "b.docx", "c.docx"]


def test_execute_empty_list():
    repo = DummyRepo(names=[])
    uc = ListTemplateUseCase(template_repository=repo)

    result = uc.execute()
    assert result == []


def test_execute_repo_error_propagates():
    class BadRepo(TemplateRepository):
        def list(self):
            raise RuntimeError("list failed")

        def save(self, template_name: str, content: bytes): ...
        def get_template(self, name: str): ...

    uc = ListTemplateUseCase(template_repository=BadRepo())
    with pytest.raises(RuntimeError) as exc:
        uc.execute()
    assert "list failed" in str(exc.value)
