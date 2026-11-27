from pathlib import Path

from periodic_table.repository import JsonElementRepository
from periodic_table.services import ElementService, CompareService


def test_repository_loads_all_118_elements():
    repository = JsonElementRepository()
    elements = repository.all()
    assert len(elements) == 118
    assert elements[0].symbol == "H"
    assert elements[-1].symbol == "Og"


def test_search_by_name_symbol_and_atomic_number():
    service = ElementService(JsonElementRepository())
    assert service.search("hierro")[0].symbol == "Fe"
    assert service.search("Au")[0].name == "Oro"
    assert service.search("79")[0].symbol == "Au"


def test_repository_returns_none_for_unknown_number():
    assert JsonElementRepository().get(0) is None


def test_compare_is_limited_to_four_and_can_remove():
    compare = CompareService()
    assert all(compare.toggle(n) for n in (6, 26, 79, 8))
    assert compare.toggle(1) is False
    assert compare.toggle(26) is True
    assert 26 not in compare.numbers
    compare.clear()
    assert compare.numbers == []


def test_data_file_is_json_backed():
    path = Path(__file__).resolve().parents[1] / "src" / "data" / "elements.json"
    assert path.exists()
