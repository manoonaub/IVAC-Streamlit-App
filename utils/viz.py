import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.io as pio


PRIMARY_BLUE = "#2563eb"
NEGATIVE_RED = "#e11d48"

# Palette de couleurs vibrantes
VIBRANT_COLORS = [
    "#3b82f6",  # Bleu vif
    "#10b981",  # Vert émeraude
    "#f59e0b",  # Orange
    "#ef4444",  # Rouge
    "#8b5cf6",  # Violet
    "#ec4899",  # Rose
    "#06b6d4",  # Cyan
    "#84cc16",  # Lime
]


def _apply_common_layout(fig, xaxis_title=None, yaxis_title=None):
    """Apply common layout settings to charts for consistency and accessibility."""
    layout_params = {
        "margin": dict(l=10, r=10, t=50, b=10), 
        "font": dict(size=13), 
        "showlegend": True,
        "plot_bgcolor": "rgba(0,0,0,0)",  # Transparent background
        "paper_bgcolor": "rgba(0,0,0,0)"  # Transparent background
    }
    
    # Add axis titles if provided (for accessibility)
    if xaxis_title:
        layout_params["xaxis_title"] = xaxis_title
    if yaxis_title:
        layout_params["yaxis_title"] = yaxis_title
    
    fig.update_layout(**layout_params)


def line_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str | None = None, ref_y: float | None = None, ref_label: str | None = None, download_name: str | None = None, threshold_zones: list[dict] | None = None, annotations: list[dict] | None = None, xaxis_title: str | None = None, yaxis_title: str | None = None):
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        st.info("Aucune donnée à afficher pour le graphique de tendance.")
        return
    fig = px.line(df, x=x, y=y, color=color, markers=True, title=title, color_discrete_sequence=VIBRANT_COLORS)
    fig.update_traces(line=dict(width=4), marker=dict(size=10))
    _apply_common_layout(fig, xaxis_title=xaxis_title or x.replace('_', ' ').title(), yaxis_title=yaxis_title or y.replace('_', ' ').title())
    
    # Reference line
    if ref_y is not None:
        fig.add_hline(y=ref_y, line_dash="dash", line_color="red", annotation_text=ref_label or str(ref_y), annotation_position="top left")
    
    # Threshold zones (colored bands)
    if threshold_zones:
        for zone in threshold_zones:
            fig.add_hrect(
                y0=zone.get("y0", 0), y1=zone.get("y1", 0),
                fillcolor=zone.get("color", "lightgray"),
                opacity=zone.get("opacity", 0.2),
                line_width=0,
                annotation_text=zone.get("label", ""),
                annotation_position=zone.get("label_position", "top left")
            )
    
    # Custom annotations
    if annotations:
        for ann in annotations:
            fig.add_annotation(
                x=ann.get("x"), y=ann.get("y"),
                text=ann.get("text", ""),
                showarrow=ann.get("showarrow", True),
                arrowhead=ann.get("arrowhead", 2),
                arrowcolor=ann.get("arrowcolor", "red"),
                bgcolor=ann.get("bgcolor", "white"),
                bordercolor=ann.get("bordercolor", "red")
            )
    
    st.plotly_chart(fig, use_container_width=True)
    if download_name:
        try:
            png_bytes = pio.to_image(fig, format="png", scale=2)
            st.download_button("Télécharger PNG", data=png_bytes, file_name=download_name, mime="image/png")
        except Exception:
            st.caption("Astuce: installe kaleido pour activer l'export PNG.")


def bar_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str | None = None, ref_y: float | None = None, ref_label: str | None = None, download_name: str | None = None, sign_color: bool = False, threshold_zones: list[dict] | None = None, annotations: list[dict] | None = None, xaxis_title: str | None = None, yaxis_title: str | None = None):
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        st.info("Aucune donnée à afficher pour l'histogramme.")
        return
    plot_df = df.copy()
    color_arg = color
    color_map = None
    if sign_color:
        sign_col = f"__sign_{y}__"
        plot_df[sign_col] = plot_df[y].apply(lambda v: "≥ 0" if pd.notna(v) and v >= 0 else "< 0")
        color_arg = sign_col
        color_map = {"≥ 0": PRIMARY_BLUE, "< 0": NEGATIVE_RED}
    fig = px.bar(plot_df, x=x, y=y, color=color_arg, title=title, color_discrete_sequence=VIBRANT_COLORS, color_discrete_map=color_map)
    fig.update_traces(marker_line_color="#1f2937", marker_line_width=1.5)
    _apply_common_layout(fig, xaxis_title=xaxis_title or x.replace('_', ' ').title(), yaxis_title=yaxis_title or y.replace('_', ' ').title())
    
    # Reference line
    if ref_y is not None:
        fig.add_hline(y=ref_y, line_dash="dash", line_color="red", annotation_text=ref_label or str(ref_y), annotation_position="top left")
    
    # Threshold zones
    if threshold_zones:
        for zone in threshold_zones:
            fig.add_hrect(
                y0=zone.get("y0", 0), y1=zone.get("y1", 0),
                fillcolor=zone.get("color", "lightgray"),
                opacity=zone.get("opacity", 0.2),
                line_width=0,
                annotation_text=zone.get("label", ""),
                annotation_position=zone.get("label_position", "top left")
            )
    
    # Custom annotations
    if annotations:
        for ann in annotations:
            fig.add_annotation(
                x=ann.get("x"), y=ann.get("y"),
                text=ann.get("text", ""),
                showarrow=ann.get("showarrow", True),
                arrowhead=ann.get("arrowhead", 2),
                arrowcolor=ann.get("arrowcolor", "red"),
                bgcolor=ann.get("bgcolor", "white"),
                bordercolor=ann.get("bordercolor", "red")
            )
    
    st.plotly_chart(fig, use_container_width=True)
    if download_name:
        try:
            png_bytes = pio.to_image(fig, format="png", scale=2)
            st.download_button("Télécharger PNG", data=png_bytes, file_name=download_name, mime="image/png")
        except Exception:
            st.caption("Astuce: installe kaleido pour activer l'export PNG.")


def histogram(df: pd.DataFrame, x: str, nbins: int = 40, title: str | None = None, ref_x: float | None = None, ref_label: str | None = None, download_name: str | None = None, threshold_zones: list[dict] | None = None, annotations: list[dict] | None = None, xaxis_title: str | None = None, yaxis_title: str | None = None):
    if df is None or df.empty or x not in df.columns:
        st.info("Aucune donnée à afficher pour la distribution.")
        return
    fig = px.histogram(df, x=x, nbins=nbins, title=title, color_discrete_sequence=["#3b82f6"])
    fig.update_traces(marker_line_color="#1f2937", marker_line_width=1.5)
    _apply_common_layout(fig, xaxis_title=xaxis_title or x.replace('_', ' ').title(), yaxis_title=yaxis_title or "Frequency / Fréquence")
    
    # Reference line
    if ref_x is not None:
        fig.add_vline(x=ref_x, line_dash="dash", line_color="red", annotation_text=ref_label or str(ref_x), annotation_position="top left")
    
    # Threshold zones (vertical bands)
    if threshold_zones:
        for zone in threshold_zones:
            fig.add_vrect(
                x0=zone.get("x0", 0), x1=zone.get("x1", 0),
                fillcolor=zone.get("color", "lightgray"),
                opacity=zone.get("opacity", 0.2),
                line_width=0,
                annotation_text=zone.get("label", ""),
                annotation_position=zone.get("label_position", "top left")
            )
    
    # Custom annotations
    if annotations:
        for ann in annotations:
            fig.add_annotation(
                x=ann.get("x"), y=ann.get("y"),
                text=ann.get("text", ""),
                showarrow=ann.get("showarrow", True),
                arrowhead=ann.get("arrowhead", 2),
                arrowcolor=ann.get("arrowcolor", "red"),
                bgcolor=ann.get("bgcolor", "white"),
                bordercolor=ann.get("bordercolor", "red")
            )
    
    st.plotly_chart(fig, use_container_width=True)
    if download_name:
        try:
            png_bytes = pio.to_image(fig, format="png", scale=2)
            st.download_button("Télécharger PNG", data=png_bytes, file_name=download_name, mime="image/png")
        except Exception:
            st.caption("Astuce: installe kaleido pour activer l'export PNG.")


def boxplot(df: pd.DataFrame, x: str | None, y: str, color: str | None = None, title: str | None = None, download_name: str | None = None, xaxis_title: str | None = None, yaxis_title: str | None = None):
    if df is None or df.empty or y not in df.columns:
        st.info("Aucune donnée pour le boxplot.")
        return
    fig = px.box(df, x=x, y=y, color=color, points="outliers", title=title, color_discrete_sequence=VIBRANT_COLORS)
    _apply_common_layout(fig, 
                        xaxis_title=xaxis_title or (x.replace('_', ' ').title() if x else ""),
                        yaxis_title=yaxis_title or y.replace('_', ' ').title())
    st.plotly_chart(fig, use_container_width=True)
    if download_name:
        try:
            png_bytes = pio.to_image(fig, format="png", scale=2)
            st.download_button("Télécharger PNG", data=png_bytes, file_name=download_name, mime="image/png")
        except Exception:
            st.caption("Astuce: installe kaleido pour activer l'export PNG.")


def scatter(df: pd.DataFrame, x: str, y: str, color: str | None = None, size: str | None = None, trendline: str | None = "ols", title: str | None = None, download_name: str | None = None, xaxis_title: str | None = None, yaxis_title: str | None = None):
    if df is None or df.empty or x not in df.columns or y not in df.columns:
        st.info("Aucune donnée pour le nuage de points.")
        return
    fig = px.scatter(df, x=x, y=y, color=color, size=size, trendline=trendline, title=title, color_discrete_sequence=VIBRANT_COLORS, opacity=0.7)
    fig.update_traces(marker=dict(size=12, line=dict(width=2, color='#1f2937')))
    _apply_common_layout(fig, 
                        xaxis_title=xaxis_title or x.replace('_', ' ').title(),
                        yaxis_title=yaxis_title or y.replace('_', ' ').title())
    st.plotly_chart(fig, use_container_width=True)
    if download_name:
        try:
            png_bytes = pio.to_image(fig, format="png", scale=2)
            st.download_button("Télécharger PNG", data=png_bytes, file_name=download_name, mime="image/png")
        except Exception:
            st.caption("Astuce: installe kaleido pour activer l'export PNG.")


def correlation_heatmap(df: pd.DataFrame, cols: list[str], title: str | None = None, download_name: str | None = None):
    if df is None or df.empty:
        st.info("Aucune donnée pour la matrice de corrélation.")
        return
    subset = df[cols].select_dtypes(include=["number"]).dropna()
    if subset.empty:
        st.info("Colonnes numériques insuffisantes pour la corrélation.")
        return
    corr = subset.corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=True, aspect="auto", title=title, color_continuous_scale="RdBu_r", origin="lower")
    _apply_common_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
    if download_name:
        try:
            png_bytes = pio.to_image(fig, format="png", scale=2)
            st.download_button("Télécharger PNG", data=png_bytes, file_name=download_name, mime="image/png")
        except Exception:
            st.caption("Astuce: installe kaleido pour activer l'export PNG.")
# --- Palette utils -----------------------------------------------------------
def make_color_map(categories):
    """Retourne un dict {categorie: couleur} avec une grande palette qualitative."""
    import plotly.express as px
    # On concatène plusieurs palettes pour avoir > 30 couleurs distinctes
    banks = [
        px.colors.qualitative.Set3,
        px.colors.qualitative.D3,
        px.colors.qualitative.Bold,
        px.colors.qualitative.Safe,
        px.colors.qualitative.Pastel,
    ]
    flat = [c for bank in banks for c in bank]
    return {cat: flat[i % len(flat)] for i, cat in enumerate(categories)}

def scatter(
    df, x, y, color=None, title="",
    color_map=None, opacity=0.55, trendline=None, height=520
):
    import plotly.express as px
    # Catégories ordonnées pour des couleurs stables
    cat_orders = {color: list(color_map.keys())} if (color and color_map) else None

    fig = px.scatter(
        df, x=x, y=y, color=color, title=title,
        trendline=trendline,  # None = pas de régression par région
        color_discrete_map=color_map or {},
        category_orders=cat_orders,
    )
    fig.update_traces(marker=dict(size=6, opacity=opacity))
    fig.update_layout(
        height=height,
        legend=dict(
            y=1, x=1.02, yanchor="top", xanchor="left", bgcolor="rgba(0,0,0,0)"
        )
    )
    import streamlit as st
    st.plotly_chart(fig, use_container_width=True)

