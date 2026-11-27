import flet as ft
from ..ui.views.home import HomeView
from ..ui.views.compare import CompareView
from ..ui.views.quiz import QuizView

class AppRouter:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {
            "/": HomeView,
            "/compare": CompareView,
            "/quiz": QuizView,
        }
        self.current_view_instance = None

    def route(self, route_name: str):
        # Remove old view
        if self.current_view_instance:
            self.page.controls.remove(self.current_view_instance.control)
        
        # Create new view
        view_class = self.routes.get(route_name, HomeView)
        self.current_view_instance = view_class(self.page)
        
        # Add new view
        self.page.controls.append(self.current_view_instance.control)
        self.page.update()