# PeriodicTable

Aplicación de escritorio/web de tabla periódica construida con Python y Flet. La interfaz sigue el documento **Periodic Table – Flet App Architecture**.

## Funcionalidades

- Tabla periódica de 118 elementos, organizada por período y grupo, con colores por categoría.
- Búsqueda por nombre, símbolo o número atómico.
- Panel de selección y detalle del elemento.
- Comparación de hasta cuatro elementos.
- Quiz de símbolos, nombres y categorías con puntuación, racha y mejor racha.
- Favoritos y notas por elemento.
- Ajustes de tema, idioma, unidad de temperatura, tamaño de casilla y colores por categoría.

## Requisitos y ejecución

Python 3.10 o superior.

```bash
uv sync
uv run flet run
```

Para navegador:

```bash
uv run flet run --web
```

## Pruebas

```bash
uv run pytest
```
