import flet as ft

def view(page: ft.Page, elem_id: str):
    return ft.Column(
        controls=[
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/")),
            ft.Text(f"Elemento: {elem_id}", size=24),
        ],
        expand=True
    )