import flet as ft
from typing import List, Optional
from ..domain.models.element import Element

class AppState:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_elements: List[Element] = []
        self.current_view = "home"
        self.search_query = ""
        
    def add_to_compare(self, element: Element):
        if len(self.selected_elements) < 4:
            if element not in self.selected_elements:
                self.selected_elements.append(element)
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Added {element.symbol}"))
                self.page.snack_bar.open = True
        
    def remove_from_compare(self, element: Element):
        self.selected_elements.remove(element)