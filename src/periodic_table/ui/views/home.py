import flet as ft
from ..components.periodic_grid import PeriodicGrid
from ..components.search_bar import SearchBar

class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.control = ft.Column(
            expand=True,
            spacing=10,
            controls=[
                SearchBar(),
                ft.Container(
                    expand=True,
                    content=PeriodicGrid(),
                    border_radius=10,
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                )
            ]
        )