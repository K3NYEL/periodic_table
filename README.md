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

> El conjunto contiene los 118 elementos con masa atómica, configuración electrónica, electronegatividad, estado, puntos de fusión/ebullición y densidad cuando la fuente dispone de esos valores. Los campos ausentes permanecen como `null` y se muestran como **No disponible**.

## Arquitectura

```text
src/
├── main.py
├── data/
│   └── elements.json
└── periodic_table/
    ├── app.py          # UI Flet y coordinación de pantallas
    ├── domain.py       # Modelo Element, sin dependencias de Flet
    ├── repository.py   # Protocolo y adaptador JSON
    └── services.py     # Búsqueda, filtros y comparación
```

Flujo: **ui → services → domain ← data**. Los modelos y servicios no dependen de Flet.

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

## Datos

El archivo `src/data/elements.json` contiene los 118 elementos. Los datos base se adaptaron de [Periodic-Table-JSON](https://github.com/Bowserinator/Periodic-Table-JSON); cada registro conserva su URL de procedencia en `source_url`. Temperaturas en kelvin y densidad normalizada a g/cm³. Los valores ausentes permanecen como `null`.

## Estado de implementación

La navegación y los flujos principales están implementados en `local-charges`. Las propiedades científicas opcionales requieren completar/verificar la fuente de datos antes de mostrarse como valores definitivos.
