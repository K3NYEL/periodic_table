import flet as ft

from ...domain.models.element import Element
from ..components.elements_title import ElementTile


class HomeView:
    def __init__(self, page: ft.Page, repository, state, services, navigate):
        self.page = page
        self.repository = repository
        self.state = state
        self.services = services
        self.navigate = navigate
        self.compare_feedback = ft.Text("", size=11, color="#7EA9D8")
        self.elements = repository.get_all()
        self.results = self.services["search"].search(state.query) if state.query.strip() else list(self.elements)
        self.detail = ft.Container(padding=18, border_radius=12, bgcolor="#1A222E", content=ft.Text("Select an element to inspect its properties.", color="#AAB6C5"))
        self.search = ft.TextField(value=self.state.query, hint_text="Search by name, symbol or atomic number", prefix_icon=ft.Icons.SEARCH, on_change=self._search, expand=True, border_color="#394657", focused_border_color="#6EA8FE")
        self.grid = ft.GridView(expand=True, runs_count=18, max_extent=76, child_aspect_ratio=0.92, spacing=5, run_spacing=5)
        self._render_grid()
        self.control = ft.Column(expand=True, spacing=14, controls=[
            ft.Container(padding=ft.padding.symmetric(horizontal=24, vertical=18), content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Column(spacing=2, controls=[ft.Text("PERIODIC TABLE", size=12, weight=ft.FontWeight.BOLD, color="#7EA9D8"), ft.Text("Explore the elements", size=25, weight=ft.FontWeight.BOLD, color="#F1F5F9")]),
                ft.Container(width=380, content=self.search),
                ft.TextButton("Compare", on_click=lambda event: self.navigate("/compare")),
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
        if self.state.query.strip():
            for element in self.results:
                self.grid.controls.append(ElementTile(element, on_click=lambda event, item=element: self._select(item)))
            return

        slots = [None] * (9 * 18)
        for element in self.results:
            if element.category.value == "lanthanide":
                row, column = 7, element.number - 57 + 3
            elif element.category.value == "actinide":
                row, column = 8, element.number - 89 + 3
            else:
                row, column = element.period - 1, (element.group or 1) - 1
            if 0 <= row < 9 and 0 <= column < 18:
                slots[row * 18 + column] = element

        for element in slots:
            if element is None:
                self.grid.controls.append(ft.Container(width=76, height=82))
            else:
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
        self.compare_feedback.value = ""
        self.detail.content = ft.Column(spacing=8, controls=[
            ft.Text(f"{element.number:03}", color="#8FA5BE", size=12),
            ft.Text(element.symbol, size=42, weight=ft.FontWeight.BOLD, color="#F4F7FB"),
            ft.Text(element.name, size=20, color="#F4F7FB"),
            ft.Divider(color="#394657"),
            *[self._property(label, value) for label, value in rows],
            ft.Divider(color="#394657"),
            ft.TextButton("Add / remove comparison", on_click=lambda event, item=element: self._toggle_compare(item)),
            self.compare_feedback,
        ])
        self.page.update()

    def _toggle_compare(self, element: Element):
        compare = self.services["compare"]
        was_selected = element.number in compare.numbers
        changed = compare.toggle(element.number)
        self.state.compare_numbers = list(compare.numbers)
        if not changed:
            self.compare_feedback.value = "Comparison is limited to four elements."
        else:
            self.compare_feedback.value = "Removed from comparison." if was_selected else "Added to comparison."
        self.page.update()

    @staticmethod
    def _property(label, value):
        return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text(label, size=11, color="#8290A2"), ft.Text("—" if value is None else str(value), size=11, color="#E1E8F0", selectable=True)])
