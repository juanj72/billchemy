import pytest
from pathlib import Path
from src.adapters.invoices.template_repository import FileSystemTemplateRepository


@pytest.fixture
def tmp_templates_dir(tmp_path):
    return tmp_path / "templates"


@pytest.fixture
def repo(tmp_templates_dir):

    return FileSystemTemplateRepository(base_dir=tmp_templates_dir)


def test_save_creates_file_and_returns_path(repo, tmp_templates_dir):
    name = "test.tpl"
    content = b"Hello, Template!"

    saved_path = repo.save(name, content)

    assert isinstance(saved_path, Path)
    assert saved_path == tmp_templates_dir / name

    assert saved_path.exists()
    assert saved_path.read_bytes() == content


def test_list_returns_all_files(repo, tmp_templates_dir):

    files = {
        "a.tpl": b"A",
        "b.tpl": b"B",
        "c.tpl": b"C",
    }
    for fname, data in files.items():
        (tmp_templates_dir / fname).write_bytes(data)

    # list() debe devolver un iterable de Paths
    listed = list(repo.list())
    # Nombres esperados
    listed_names = {p.name for p in listed}
    assert listed_names == set(files.keys())


def test_get_template_existing_and_nonexisting(repo, tmp_templates_dir):

    existing = "exists.tpl"
    (tmp_templates_dir / existing).write_bytes(b"X")
    assert repo.get_template(existing) is True

    assert repo.get_template("nope.tpl") is False
