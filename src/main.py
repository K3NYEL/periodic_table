import flet as ft
from pages import home, element, search

def main(page: ft.Page):
    page.title = "Tabla Periódica"
    page.theme_mode = ft.ThemeMode.DARK

    def route_change(e):
        page.views.clear()
        
        if e.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [home.view(page)]
                )
            )
        elif e.route.startswith("/element/"):
            elem_id = e.route.split("/")[-1]
            page.views.append(
                ft.View(
                    e.route,
                    [element.view(page, elem_id)]
                )
            )
        elif e.route == "/search":
            page.views.append(
                ft.View(
                    "/search",
                    [search.view(page)]
                )
            )
        
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)