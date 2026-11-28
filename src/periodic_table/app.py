import flet as ft
from .core.router import AppRouter
from .core.state import AppState
from .data.json_repository import JsonElementRepository
from .services.search_service import SearchService

def create_app(page: ft.Page):
    # 1. Initialize Repository (Data Layer)
    repo = JsonElementRepository("assets/data/elements.json")
    
    # 2. Initialize Services (Service Layer)
    search_service = SearchService(repo)
    
    # 3. Initialize State (Core Layer)
    state = AppState(page)
    
    # 4. Initialize Router (Core Layer)
    router = AppRouter(page)
    
    # 5. Set initial route
    router.route("/")
    
    # 6. Setup Theme
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50
    
    return {
        "router": router,
        "state": state,
        "repo": repo,
        "services": {"search": search_service}
    }