# Base de Exportación — App Streamlit

App para explorar la base de **Exportadores** y **Navieras** con filtros cruzados:
seleccionás un valor en cualquier columna (por ejemplo el `SHIPPER`) y las opciones
de las demás columnas (`POD`, `COMMODITY`, `HS CODE`, etc.) se acotan automáticamente,
y viceversa.

## Estructura del repo

```
export-navieras-app/
├── app.py                     # App principal de Streamlit
├── requirements.txt
├── data/
│   └── Data_base_Export.xlsx  # Base de datos (hojas: "Exportadores ", "Navieras")
├── .streamlit/
│   └── config.toml            # Tema visual
└── README.md
```

## Cómo correr localmente

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Se abre en `http://localhost:8501`.

## Cómo actualizar los datos

Simplemente reemplazá el archivo `data/Data_base_Export.xlsx` manteniendo los
mismos nombres de hoja (`Exportadores `, con el espacio final, y `Navieras`) y
las mismas columnas. La app se actualiza sola al recargar.

## Deploy gratis en Streamlit Community Cloud

1. Subí este repo a GitHub (público o privado).
2. Entrá a https://share.streamlit.io con tu cuenta de GitHub.
3. "New app" → elegí el repo, la rama y `app.py` como archivo principal.
4. Deploy. Listo, queda con una URL pública.

## Notas

- Los filtros usan `st.multiselect`, así que podés elegir más de un valor a la vez
  en cada columna (por ejemplo, dos `SHIPPER` al mismo tiempo).
- Hay botón de "Limpiar filtros" y botón para descargar el resultado filtrado en CSV.
- Si el Excel crece mucho, se puede migrar a una base real (SQLite/Postgres) sin
  cambiar la lógica de filtrado, solo la función `load_data()`.
