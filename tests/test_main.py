from periodic_table.data.json_repository import JsonElementRepository
from periodic_table.domain.models.element import Category, Phase
from periodic_table.services.compare_service import CompareService
from periodic_table.services.search_service import SearchService


def test_repository_loads_all_118_elements():
    repository = JsonElementRepository()
    elements = repository.get_all()
    assert len(elements) == 118
    assert [item.number for item in elements] == list(range(1, 119))
    assert elements[0].symbol == "H"
    assert elements[-1].symbol == "Og"


def test_repository_maps_categories_and_phases():
    repository = JsonElementRepository()
    assert repository.get_by_number(1).category is Category.NONMETAL
    assert repository.get_by_number(2).category is Category.NOBLE_GAS
    assert repository.get_by_number(3).category is Category.ALKALI_METAL
    assert repository.get_by_number(80).phase is Phase.LIQUID


def test_repository_preserves_optional_values():
    helium = JsonElementRepository().get_by_number(2)
    assert helium.electronegativity is None
    assert helium.atomic_mass == 4.0026022


def test_search_by_name_symbol_and_atomic_number():
    service = SearchService(JsonElementRepository())
    assert service.search("hierro")[0].symbol == "Fe"
    assert service.search("Au")[0].name == "Oro"
    assert service.search("79")[0].symbol == "Au"


def test_repository_returns_none_for_unknown_number():
    assert JsonElementRepository().get_by_number(0) is None


def test_compare_is_limited_to_four_and_can_remove():
    compare = CompareService()
    assert all(compare.toggle(number) for number in (6, 26, 79, 8))
    assert compare.toggle(1) is False
    assert compare.toggle(26) is True
    assert 26 not in compare.numbers
    compare.clear()
    assert compare.numbers == []
