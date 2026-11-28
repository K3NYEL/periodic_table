import flet as ft

from .core.router import AppRouter
from .core.state import AppState
from .data.json_repository import JsonElementRepository
from .services.compare_service import CompareService
from .services.search_service import SearchService


def create_app(page: ft.Page) -> None:
    repository = JsonElementRepository()
    state = AppState()
    services = {
        "search": SearchService(repository),
        "compare": CompareService(),
    }
    router = AppRouter(page, repository, state, services)
    page.title = "Periodic Table"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#10151D"
    page.padding = 0
    page.window.width = 1280
    page.window.height = 860
    router.go("/")
