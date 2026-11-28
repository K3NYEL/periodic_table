import flet as ft

from ...domain.models.element import Category, Element
from ..theme import ELEMENT_COLORS


class ElementTile(ft.Container):
    def __init__(self, element: Element, on_click=None, selected: bool = False):
        color = ELEMENT_COLORS.get(element.category.value, "#303846")
        super().__init__(
            width=76,
            height=82,
            padding=5,
            border_radius=7,
            bgcolor=color,
            border=ft.Border.all(2, "#FFFFFF" if selected else "#00000022"),
            on_click=on_click,
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(str(element.number), size=10, color="#26313D"),
                    ft.Text(element.symbol, size=22, weight=ft.FontWeight.BOLD, color="#17212B"),
                    ft.Text(element.name, size=9, color="#26313D", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ],
            ),
        )
