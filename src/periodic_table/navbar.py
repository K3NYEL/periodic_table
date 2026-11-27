import flet as ft


class Navbar(ft.Container):
    def __init__(self):
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Text("My App", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SEARCH),
                    ft.IconButton(icon=ft.Icons.PERSON),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            border_radius=10,
            expand=False,
        )