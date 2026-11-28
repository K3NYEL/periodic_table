import flet as ft


class Sidebar(ft.Container):
    def __init__(self, active_route: str, on_navigate, compare_count: int = 0):
        self.active_route = active_route
        self.on_navigate = on_navigate

        super().__init__(
            width=248,
            bgcolor="#151D28",
            padding=ft.Padding.symmetric(horizontal=16, vertical=22),
            border=ft.Border.only(right=ft.BorderSide(1, "#293545")),
            content=ft.Column(
                expand=True,
                spacing=8,
                controls=[
                    ft.Container(
                        padding=ft.Padding.only(left=8, right=8, bottom=24),
                        content=ft.Row(
                            spacing=11,
                            controls=[
                                ft.Container(
                                    width=38,
                                    height=38,
                                    border_radius=10,
                                    bgcolor="#243B59",
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.Icon(ft.Icons.SCIENCE, color="#8DBBFF", size=22),
                                ),
                                ft.Column(
                                    spacing=1,
                                    controls=[
                                        ft.Text("PERIODIC", size=11, weight=ft.FontWeight.BOLD, color="#8DBBFF"),
                                        ft.Text("TABLE", size=18, weight=ft.FontWeight.BOLD, color="#F1F5F9"),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.Padding.only(left=10, top=8, bottom=8),
                        content=ft.Text("WORKSPACE", size=10, weight=ft.FontWeight.BOLD, color="#718096"),
                    ),
                    self._nav_item("Periodic table", "/", ft.Icons.GRID_VIEW),
                    self._nav_item("Compare elements", "/compare", ft.Icons.COMPARE_ARROWS, compare_count),
                    ft.Container(expand=True),
                    ft.Divider(color="#293545"),
                    ft.Container(
                        padding=ft.Padding.only(left=10, top=8),
                        content=ft.Column(
                            spacing=3,
                            controls=[
                                ft.Text("CHEMISTRY REFERENCE", size=10, weight=ft.FontWeight.BOLD, color="#8FA5BE"),
                                ft.Text("118 known elements", size=11, color="#718096"),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _nav_item(self, label: str, route: str, icon, count: int = 0):
        active = self.active_route == route
        controls = [
            ft.Icon(icon, size=18, color="#9CC4FF" if active else "#94A3B8"),
            ft.Text(
                label,
                size=13,
                weight=ft.FontWeight.W_600 if active else ft.FontWeight.NORMAL,
                color="#F1F5F9" if active else "#AAB6C5",
                expand=True,
            ),
        ]
        if count:
            controls.append(
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=7, vertical=3),
                    border_radius=10,
                    bgcolor="#29466A",
                    content=ft.Text(str(count), size=10, color="#CFE2FF", weight=ft.FontWeight.BOLD),
                )
            )
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=12),
            border_radius=8,
            bgcolor="#243449" if active else None,
            on_click=lambda event: self.on_navigate(route),
            content=ft.Row(spacing=11, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=controls),
        )
