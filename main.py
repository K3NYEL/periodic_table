from pathlib import Path
import sys
import flet as ft

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from periodic_table.app import create_app


def main(page: ft.Page) -> None:
    create_app(page)


if __name__ == "__main__":
    ft.run(main)
