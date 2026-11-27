import flet as ft
from src.periodic_table.app import create_app

def main(page: ft.Page):
    page.title = "PeriodicTable"
    page.window.width = 1200
    page.window.height = 800
    
    # Create app components
    app_components = create_app(page)
    
    # Add Navbar (from your previous code)
    # navbar = Navbar(page)
    # page.add(navbar)
    
    # Add the view container
    page.add(
        app_components["router"].current_view_instance.control
    )

if __name__ == "__main__":
    ft.app(target=main)