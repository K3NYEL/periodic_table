import flet as ft

from ..sidebar import Sidebar
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
                self.refresh_sidebar,
            )
        elif route == "/compare":
            view = CompareView(self.page, self.repository, self.state, self.services, self.go)
        else:
            view = ft.Text("View not found", color=ft.Colors.WHITE)

        content = ft.Container(
            expand=True,
            padding=20,
            content=view.control if hasattr(view, "control") else view,
        )
        shell = ft.Row(
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self._build_sidebar(),
                content,
            ],
        )
        self.page.add(shell)
        self.page.update()

    def _build_sidebar(self):
        return Sidebar(
            active_route=self.state.current_view,
            on_navigate=self.go,
            compare_count=len(self.services["compare"].numbers),
        )

    def refresh_sidebar(self):
        if self.page.controls:
            shell = self.page.controls[0]
            if isinstance(shell, ft.Row) and shell.controls:
                shell.controls[0] = self._build_sidebar()
                self.page.update()
