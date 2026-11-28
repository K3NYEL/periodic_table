import flet as ft

from ..ui.views.compare import CompareView
from ..ui.views.home import HomeView


class AppRouter:
    def __init__(self, page: ft.Page, repository, state, services):
        self.page = page
        self.repository = repository
        self.state = state
        self.services = services

    def go(self, route: str) -> None:
        self.state.current_view = route
        self.page.controls.clear()
        if route == "/":
            view = HomeView(self.page, self.repository, self.state, self.services, self.go)
        elif route == "/compare":
            view = CompareView(self.page, self.repository, self.state, self.services, self.go)
        else:
            self.page.add(ft.Text("View not found", color=ft.Colors.WHITE))
            self.page.update()
            return
        self.page.add(ft.Container(expand=True, padding=20, content=view.control))
        self.page.update()
