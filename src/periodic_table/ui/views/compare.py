import flet as ft


class CompareView:
    def __init__(self, page, repository, state, services, navigate):
        self.page = page
        self.repository = repository
        self.state = state
        self.services = services
        self.navigate = navigate
        self.control = self._build()

    def _build(self):
        numbers = self.services["compare"].numbers
        elements = [self.repository.get_by_number(number) for number in numbers]
        elements = [element for element in elements if element is not None]
        cards = []
        for element in elements:
            cards.append(ft.Container(
                expand=True,
                padding=16,
                border_radius=10,
                bgcolor="#1A222E",
                content=ft.Column(spacing=8, controls=[
                    ft.Text(f"{element.number:03}", color="#8FA5BE", size=12),
                    ft.Text(element.symbol, color="#F4F7FB", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text(element.name, color="#F4F7FB", size=16),
                    ft.Divider(color="#394657"),
                    ft.Text(f"Category: {element.category.value.replace('_', ' ').title()}", color="#AAB6C5"),
                    ft.Text(f"Atomic mass: {element.atomic_mass or '—'}", color="#AAB6C5"),
                    ft.Text(f"Phase: {element.phase.value.title()}", color="#AAB6C5"),
                    ft.Text(f"Electronegativity: {element.electronegativity if element.electronegativity is not None else '—'}", color="#AAB6C5"),
                    ft.Text(f"Density: {element.density if element.density is not None else '—'} {element.density_unit or ''}", color="#AAB6C5"),
                    ft.TextButton("Remove", on_click=lambda event, number=element.number: self._remove(number)),
                ]),
            ))
        if not cards:
            cards = [ft.Text("No elements selected. Return to the table and add up to four elements.", color="#AAB6C5")]
        return ft.Column(expand=True, spacing=18, controls=[
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Column(spacing=2, controls=[ft.Text("COMPARISON", color="#7EA9D8", size=12, weight=ft.FontWeight.BOLD), ft.Text("Compare elements", color="#F1F5F9", size=25, weight=ft.FontWeight.BOLD)]),
                ft.TextButton("Back to table", on_click=lambda event: self.navigate("/")),
            ]),
            ft.Text(f"{len(elements)} of 4 slots used", color="#8290A2"),
            ft.Row(expand=True, vertical_alignment=ft.CrossAxisAlignment.START, controls=cards, spacing=12),
        ])

    def _remove(self, number):
        self.services["compare"].toggle(number)
        self.state.compare_numbers = list(self.services["compare"].numbers)
        self.navigate("/compare")
