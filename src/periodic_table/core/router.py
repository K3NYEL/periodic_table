import flet as ft

from ..navbar import Navbar
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
            view = HomeView(
                self.page,
                self.repository,
                self.state,
                self.services,
                self.go,
                self.refresh_navbar,
            )
        elif route == "/compare":
            view = CompareView(self.page, self.repository, self.state, self.services, self.go)
        else:
            view = ft.Text("View not found", color=ft.Colors.WHITE)

        shell = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                self._build_navbar(),
                ft.Container(expand=True, padding=20, content=view.control if hasattr(view, "control") else view),
            ],
        )
        self.page.add(shell)
        self.page.update()

    def _build_navbar(self):
        return Navbar(
            active_route=self.state.current_view,
            on_navigate=self.go,
            compare_count=len(self.services["compare"].numbers),
        )

    def refresh_navbar(self):
        if self.page.controls:
            shell = self.page.controls[0]
            if isinstance(shell, ft.Column) and shell.controls:
                shell.controls[0] = self._build_navbar()
                self.page.update()
