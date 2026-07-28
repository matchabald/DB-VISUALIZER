from pathlib import Path

import pandas as pd
import streamlit as st

# Ruta absoluta
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Data_base_Export.xlsx"

st.set_page_config(
    page_title="Base de Exportación",
    page_icon="🚢",
    layout="wide",
)


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        # Ayuda de diagnóstico: mostrAINDO qué hay realmente en el repo
        contenido_base = sorted(p.name for p in BASE_DIR.iterdir())
        data_dir = BASE_DIR / "data"
        contenido_data = (
            sorted(p.name for p in data_dir.iterdir()) if data_dir.exists() else "la carpeta 'data' no existe"
        )
        st.error(
            f"No se encontró el archivo en: {DATA_PATH}\n\n"
            f"Contenido de la carpeta raíz del repo: {contenido_base}\n\n"
            f"Contenido de la carpeta 'data': {contenido_data}\n\n"
            "Verificá que el Excel se haya subido a GitHub dentro de una carpeta "
            "llamada exactamente 'data' y con el nombre exacto 'Data_base_Export.xlsx'."
        )
        st.stop()

    exportadores = pd.read_excel(DATA_PATH, sheet_name="Exportadores ")
    navieras = pd.read_excel(DATA_PATH, sheet_name="Navieras")
    exportadores.columns = [c.strip() for c in exportadores.columns]
    navieras.columns = [c.strip() for c in navieras.columns]
    return exportadores, navieras


def cross_filter(df: pd.DataFrame, columns: list[str], key_prefix: str) -> pd.DataFrame:
    """
    Muestra un multiselect por cada columna. Cada vez que el usuario elige un
    valor en cualquiera de ellos, las opciones disponibles en TODOS los demás
    se recalculan (filtro cruzado), no solo en una dirección fija.
    """
    selections: dict[str, list] = {}

    # Leemos primero lo que ya está seleccionado en el estado de la sesión
    for col in columns:
        selections[col] = st.session_state.get(f"{key_prefix}_{col}", [])

    cols_widgets = st.columns(len(columns))

    for i, col in enumerate(columns):
        # Filtramos el df usando las selecciones de TODAS las demás columnas -- revisar q max 4
        temp = df.copy()
        for other_col, values in selections.items():
            if other_col != col and values:
                temp = temp[temp[other_col].isin(values)]

        options = sorted(temp[col].dropna().astype(str).unique().tolist())

        # Limpiamos defaults que ya no sean válidos tras el filtrado
        current_default = [v for v in selections[col] if v in options]

        with cols_widgets[i]:
            selected = st.multiselect(
                col,
                options=options,
                default=current_default,
                key=f"{key_prefix}_{col}",
            )
        selections[col] = selected

    # Filtro final combinando todas las selecciones
    result = df.copy()
    for col, values in selections.items():
        if values:
            result = result[result[col].isin(values)]

    return result


def reset_filters(columns: list[str], key_prefix: str):
    for col in columns:
        st.session_state.pop(f"{key_prefix}_{col}", None)


def render_section(df: pd.DataFrame, columns: list[str], key_prefix: str, title: str):
    st.subheader(title)
    st.caption(
        "Se puede seleccionar uno o varias opciones en cualquier columna: las opciones del resto "
        "se filtrán automáticamente"
    )

    col_btn, _ = st.columns([1, 6])
    with col_btn:
        if st.button("🧹 Limpiar filtros", key=f"reset_{key_prefix}"):
            reset_filters(columns, key_prefix)
            st.rerun()

    filtered = cross_filter(df, columns, key_prefix)

    st.markdown(f"**{len(filtered)}** registro(s) encontrados de {len(df)} totales.")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    csv = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Descargar resultados (CSV)",
        data=csv,
        file_name=f"{key_prefix}_filtrado.csv",
        mime="text/csv",
    )

#esto es basicament la cara o la fn main de la app 
def main():
    st.title("🚢 DB Export")
    st.markdown(
        "by AGVM"
    )

    exportadores, navieras = load_data()

    tab1, tab2 = st.tabs(["🛻 Exportadores", "🚢 Navieras"])

    with tab1:
        columns_exp = ["SHIPPER", "POD", "COMMODITY", "HS CODE", "CONSIGNATARIO", "EORI"]
        render_section(exportadores, columns_exp, "exp", "Exportadores")

    with tab2:
        columns_nav = [
            "CONTRACT HOLDER",
            "NAVIERA",
            "CONTRATO",
            "DESTINO",
            "COMMODITY",
            "EXPORTADORES",
            "VALIDEZ",
        ]
        render_section(navieras, columns_nav, "nav", "Navieras")

    st.divider()
    st.caption("Datos cargados desde data/Data_base_Export.xlsx")


if __name__ == "__main__":
    main()
