# Periodic Table

Aplicación de escritorio y web construida con Python y Flet. La rama `local-charges` contiene una reconstrucción inicial de la aplicación, enfocada en estabilidad, datos coherentes y una primera experiencia de exploración.

## Funcionalidades implementadas

- Carga de los 118 elementos desde `assets/data/elements.json`.
- Modelo tipado con número atómico, símbolo, nombre, grupo, período, bloque, masa atómica, categoría, fase y propiedades físicas.
- Normalización de las categorías del conjunto de datos, incluidos los nombres localizados.
- Búsqueda por nombre, símbolo o número atómico.
- Tabla periódica posicionada por grupo y período, con lantánidos y actínidos en filas separadas.
- Panel de propiedades al seleccionar un elemento.
- Comparación de hasta cuatro elementos.

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

Las pruebas cubren la carga de los 118 elementos, el mapeo de categorías y fases, los valores opcionales, la búsqueda y el límite del servicio de comparación.

## Próximos pasos

- Pruebas de integración de la interfaz y validación en escritorio/web.
- Quiz, favoritos, notas y preferencias.
- Mejorar la navegación a medida que se incorporen nuevas funcionalidades.
