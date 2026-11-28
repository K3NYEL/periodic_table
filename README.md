# Periodic Table

Aplicación de escritorio y web construida con Python y Flet. El proyecto está en proceso de reconstrucción por fases; esta rama prioriza estabilidad, un contrato de datos coherente y una primera experiencia funcional.

## Funcionalidades disponibles en esta rama

- Carga de los 118 elementos desde `assets/data/elements.json`.
- Modelo tipado con número atómico, símbolo, nombre, grupo, período, bloque, masa atómica, categoría, fase y propiedades físicas.
- Normalización de las categorías del conjunto de datos, incluidos los nombres localizados.
- Búsqueda por nombre, símbolo o número atómico.
- Tabla periódica posicionada por grupo y período, con lantánidos y actínidos en filas separadas.
- Panel de propiedades al seleccionar un elemento.
- Servicio de comparación con límite de cuatro elementos (la interfaz de comparación aún está pendiente).

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

## Pendiente

- Navegación completa y vistas independientes.
- Interfaz de comparación.
- Quiz, favoritos, notas y preferencias.
- Pruebas de integración de la interfaz y validación en escritorio/web.
