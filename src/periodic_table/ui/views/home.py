import flet as ft

from ...domain.models.element import Element
from ..components.elements_title import ElementTile


class HomeView:
    def __init__(self, page: ft.Page, repository, state, services):
        self.page = page
        self.repository = repository
        self.state = state
        self.services = services
        self.elements = repository.get_all()
        self.results = list(self.elements)
        self.detail = ft.Container(padding=18, border_radius=12, bgcolor="#1A222E", content=ft.Text("Select an element to inspect its properties.", color="#AAB6C5"))
        self.search = ft.TextField(hint_text="Search by name, symbol or atomic number", prefix_icon=ft.Icons.SEARCH, on_change=self._search, expand=True, border_color="#394657", focused_border_color="#6EA8FE")
        self.grid = ft.GridView(expand=True, runs_count=18, max_extent=82, child_aspect_ratio=0.92, spacing=6, run_spacing=6)
        self._render_grid()
        self.control = ft.Column(expand=True, spacing=14, controls=[
            ft.Container(padding=ft.padding.symmetric(horizontal=24, vertical=18), content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Column(spacing=2, controls=[ft.Text("PERIODIC TABLE", size=12, weight=ft.FontWeight.BOLD, color="#7EA9D8"), ft.Text("Explore the elements", size=25, weight=ft.FontWeight.BOLD, color="#F1F5F9")]),
                ft.Container(width=420, content=self.search),
            ])),
            ft.Container(expand=True, padding=ft.padding.symmetric(horizontal=20), content=ft.Row(expand=True, vertical_alignment=ft.CrossAxisAlignment.START, spacing=16, controls=[
                ft.Container(expand=4, content=self.grid), ft.Container(width=280, content=self.detail),
            ])),
            ft.Container(padding=ft.padding.only(left=24, right=24, bottom=14), content=ft.Text(f"{len(self.elements)} elements · Search and select an element for details", color="#8290A2", size=12)),
        ])

    def _search(self, event):
        self.state.set_query(event.control.value or "")
        self.results = self.services["search"].search(self.state.query)
        self._render_grid()
        self.page.update()

    def _render_grid(self):
        self.grid.controls.clear()
        for element in self.results:
            self.grid.controls.append(ElementTile(element, on_click=lambda event, item=element: self._select(item)))

    def _select(self, element: Element):
        self.state.select(element)
        rows = [
            ("Category", element.category.value.replace("_", " ").title()),
            ("Atomic mass", element.atomic_mass),
            ("Group / period", f"{element.group or '—'} / {element.period}"),
            ("Phase", element.phase.value.title()),
            ("Electronegativity", element.electronegativity),
            ("Melting point", element.melting_point),
            ("Boiling point", element.boiling_point),
            ("Density", f"{element.density} {element.density_unit or ''}" if element.density is not None else None),
            ("Electron configuration", element.electron_configuration),
        ]
        self.detail.content = ft.Column(spacing=8, controls=[ft.Text(f"{element.number:03}", color="#8FA5BE", size=12), ft.Text(element.symbol, size=42, weight=ft.FontWeight.BOLD, color="#F4F7FB"), ft.Text(element.name, size=20, color="#F4F7FB"), ft.Divider(color="#394657")] + [self._property(label, value) for label, value in rows])
        self.page.update()

    @staticmethod
    def _property(label, value):
        return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text(label, size=11, color="#8290A2"), ft.Text("—" if value is None else str(value), size=11, color="#E1E8F0", selectable=True)])
