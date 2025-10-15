# utils/geo.py — Geographic utilities for choropleth maps
import json
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px
import streamlit as st
import requests


@st.cache_data(show_spinner=False)
def load_geojson(path: str) -> Optional[dict]:
    """Load GeoJSON file from local path with error handling."""
    geo_path = Path(path)
    if not geo_path.exists():
        st.warning(f"🌍 GeoJSON file not found at: {path}")
        return None
    try:
        with open(geo_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Error reading GeoJSON: {e}")
        return None


@st.cache_data(show_spinner=False)
def fetch_geojson(url: str) -> Optional[dict]:
    """Fetch GeoJSON from remote URL (cached)."""
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"⚠️ Could not fetch GeoJSON from {url}: {e}")
        return None


def map_chart(
    by_departement: pd.DataFrame,
    geojson: Optional[dict],
    featureidkey: str = "properties.code",
    dep_code_col: str = "code_departement",
    value_col: str = "taux_reussite_g",
    title: str | None = None,
    alt_text: str | None = None,
):
    """
    Render choropleth map with Plotly.
    
    Parameters:
        by_departement: DataFrame with departmental aggregates
        geojson: GeoJSON dict with department geometries
        featureidkey: Path to department code in GeoJSON features
        dep_code_col: Column name for department codes in DataFrame
        value_col: Column name for values to visualize
        title: Chart title
        alt_text: Alternative text for accessibility (screen readers)
    """
    # Validation
    if by_departement is None or by_departement.empty:
        st.info("ℹ️ No departmental data available for mapping.")
        return
    if geojson is None:
        st.info("ℹ️ GeoJSON file required. Place file at: assets/fr_departements.geojson")
        return
    if dep_code_col not in by_departement.columns or value_col not in by_departement.columns:
        st.warning(f"⚠️ Required columns missing: {dep_code_col}, {value_col}")
        return

    # Prepare data
    df = by_departement.copy()
    df[dep_code_col] = df[dep_code_col].astype(str)

    # Create choropleth
    fig = px.choropleth(
        df,
        geojson=geojson,
        locations=dep_code_col,
        color=value_col,
        featureidkey=featureidkey,
        color_continuous_scale="RdYlGn",  # Red-Yellow-Green for performance
        title=title,
        hover_data={dep_code_col: True, value_col: True},
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        height=600,
    )
    
    # Accessibility: add alt text as hidden annotation
    if alt_text:
        fig.add_annotation(
            text=alt_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.15,
            font=dict(size=0),  # Invisible but accessible to screen readers
        )
    
    st.plotly_chart(fig, use_container_width=True)
