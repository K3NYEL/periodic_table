import flet as ft


class Navbar(ft.Container):
    def __init__(self, active_route: str, on_navigate, compare_count: int = 0):
        self.active_route = active_route
        self.on_navigate = on_navigate

        super().__init__(
            height=72,
            padding=ft.Padding.symmetric(horizontal=24, vertical=10),
            bgcolor="#151D28",
            border=ft.Border.only(bottom=ft.BorderSide(1, "#293545")),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(
                                width=34,
                                height=34,
                                border_radius=9,
                                bgcolor="#243B59",
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(ft.Icons.SCIENCE_OUTLINED, color="#8DBBFF", size=20),
                            ),
                            ft.Column(
                                spacing=0,
                                controls=[
                                    ft.Text("PERIODIC", size=11, weight=ft.FontWeight.BOLD, color="#8DBBFF"),
                                    ft.Text("TABLE", size=17, weight=ft.FontWeight.BOLD, color="#F1F5F9"),
                                ],
                            ),
                        ],
                    ),
                    ft.Container(expand=True),
                    self._nav_item("Table", "/", ft.Icons.GRID_VIEW_OUTLINED),
                    self._nav_item("Compare", "/compare", ft.Icons.COMPARE_ARROWS_OUTLINED, compare_count),
                ],
            ),
        )

    def _nav_item(self, label: str, route: str, icon, count: int = 0):
        active = self.active_route == route
        controls = [
            ft.Icon(icon, size=17, color="#9CC4FF" if active else "#94A3B8"),
            ft.Text(
                label,
                size=13,
                weight=ft.FontWeight.W_600 if active else ft.FontWeight.NORMAL,
                color="#F1F5F9" if active else "#AAB6C5",
            ),
        ]
        if count:
            controls.append(
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=7, vertical=2),
                    border_radius=10,
                    bgcolor="#29466A",
                    content=ft.Text(str(count), size=10, color="#CFE2FF", weight=ft.FontWeight.BOLD),
                )
            )
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=8,
            bgcolor="#243449" if active else None,
            on_click=lambda event: self.on_navigate(route),
            content=ft.Row(spacing=8, controls=controls),
        )
