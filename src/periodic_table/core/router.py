import flet as ft

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
            view = HomeView(self.page, self.repository, self.state, self.services)
            self.page.add(view.control)
        else:
            self.page.add(ft.Text("View not found", color=ft.Colors.WHITE))
        self.page.update()
