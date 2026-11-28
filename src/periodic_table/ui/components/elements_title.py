import flet as ft

class ElementTile(ft.Container):
    def __init__(self, element, on_click=None):
        # Color based on category
        color_map = {
            "Metal": ft.Colors.BLUE_200,
            "Nonmetal": ft.Colors.GREEN_200,
            # ...
        }
        bg = color_map.get(element.category.value, ft.Colors.GREY_200)
        
        super().__init__(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(str(element.number), size=10),
                    ft.Text(element.symbol, size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(element.name, size=8),
                ],
                spacing=0,
            ),
            bgcolor=bg,
            border_radius=5,
            width=50,
            height=50,
            on_click=on_click,
        )