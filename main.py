import flet as ft

from src.periodic_table.ui.theme import COLORS, ELEMENT_COLORS

def main(page: ft.Page):
    page.title = "Gab Periodic Table"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        ft.SafeArea(
            content=ft.Container(
                width=480,
                padding=10,
                border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
                border_radius=10,
                content=ft.Row(
                    controls=[

                    ]
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)