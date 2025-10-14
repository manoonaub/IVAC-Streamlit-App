import json
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px
import streamlit as st
import requests



def load_geojson(path="assets/fr_departements.geojson"):
    p = Path(path)
    if not p.exists():
        st.error(f"🌍 Fichier GeoJSON introuvable. Placez un fichier dans {path}.")
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(f"Erreur de lecture GeoJSON : {e}")
        return None
def load_geojson(path: str) -> Optional[dict]:
    geo_path = Path(path)
    if not geo_path.exists():
        return None
    try:
        with open(geo_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def fetch_geojson(url: str) -> Optional[dict]:
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def map_chart(
    by_departement: pd.DataFrame,
    geojson: Optional[dict],
    featureidkey: str = "properties.code",
    dep_code_col: str = "code_departement",
    value_col: str = "taux_reussite_g",
    title: str | None = None,
):
    if by_departement is None or by_departement.empty:
        st.info("Aucune donnée agrégée par département à cartographier.")
        return
    if geojson is None:
        st.info("Fichier GeoJSON introuvable. Placez un fichier dans assets/fr_departements.geojson.")
        return
    if dep_code_col not in by_departement.columns or value_col not in by_departement.columns:
        st.info("Colonnes nécessaires absentes pour la carte.")
        return

    df = by_departement.copy()
    df[dep_code_col] = df[dep_code_col].astype(str)

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations=dep_code_col,
        color=value_col,
        featureidkey=featureidkey,
        color_continuous_scale="Viridis",
        title=title,
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


