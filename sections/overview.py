# sections/overview.py — CONDENSED & BILINGUAL (FR/EN)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from utils.io import load_data
from utils.prep import make_tables
from utils.viz import line_chart, bar_chart, histogram, scatter
from utils.geo import load_geojson, map_chart

# Bilingual texts
TEXTS = {
    "en": {
        "language": "Language", "en": "English", "fr": "Français",
        "header": "🎯 Overview & Analysis",
        "intro": "📊 This page provides a comprehensive view of IVAC results: trends, territorial disparities, sector comparison, and key insights.",
        
        # Filters
        "filters_title": "🔧 Filters",
        "filter_session": "📅 Session",
        "filter_regions": "🗺️ Regions",
        "filter_sector": "🏫 Sector",
        "sector_all": "All sectors",
        
        # KPIs
        "exec_title": "🎯 Key Performance Indicators",
        "kpi_rate": "🎓 Avg pass rate",
        "kpi_va": "📈 Avg value added",
        "kpi_sigma": "📊 Dispersion (σ)",
        "kpi_n": "Schools",
        "exec_success": "✅ **Excellent performance**: strong value added nationally.",
        "exec_alert": "🔴 **Alerts detected**: performance below expectations.",
        "exec_ok": "ℹ️ **Standard performance**: close to expectations.",
        
        # Trends
        "trend_title": "📈 Temporal Evolution",
        "trend_caption": "Rising line suggests national improvement; compare to latest session mean.",
        "multi_title": "Joint evolution: VA & Pass rate",
        "multi_note": "**Reading guide:** Both up → improvement | Pass rate up but VA flat → grade inflation | VA up but pass rate flat → qualitative improvement.",
        
        # Regional
        "regional_title": "🗺️ Territorial Disparities",
        "map_title": "Choropleth by department",
        "map_caption": "**Reading:** Warm colors = lower performance | Cool colors = higher performance | Hover for details.",
        "top_regions": "Top 10 regions (VA)",
        "bottom_regions": "Bottom 10 regions (VA)",
        
        # Distribution
        "dist_title": "📊 Performance Distribution",
        "dist_caption": "Centered near 0 = balanced; long tails = atypical schools.",
        "mean_label": "Mean",
        "expected_label": "Expected",
        "excellent_zone": "Excellent (>5)",
        "weak_zone": "Weak (<-5)",
        
        # Sector
        "sector_title": "🏫 Public vs Private Comparison",
        "sector_box": "VA distribution by sector",
        "sector_test": "🧮 Statistical test (t-test)",
        "stat_sig": "✅ Significant difference (p = {p:.4f})",
        "stat_nsig": "ℹ️ No significant difference (p = {p:.4f})",
        "sector_delta": "Δ(Private − Public) = {delta:+.2f} VA points",
        "sector_caption": "⚠️ Difference ≠ causality (selection effects, context...).",
        
        # Correlation
        "corrmatrix_title": "🔗 Correlation Matrix",
        "corrmatrix_caption": "Pearson coefficients between key variables. Values close to ±1 indicate strong relationships.",
        
        # Synthesis
        "synthesis_title": "🧾 National Synthesis",
        "synthesis_intro": "The analysis of session **{session}** presents a nuanced picture of the French educational system. With an average pass rate of **{rate:.1f}%**, the **average value added (VA = {va:+.2f})** indicates performance {va_interp}, while remaining globally stable (σ = {sigma:.2f}).",
        "synthesis_regional": "Regional disparities persist: **{best}** stands out as top performer, while **{worst}** shows more modest results.",
        "synthesis_sector": "The **private sector** shows a {direction} (**{gap:+.2f} VA points**) compared to public schools, though this may reflect **selection effects rather than structural inequality**.",
        "synthesis_conclusion": "🔍 **In conclusion:** session {session} depicts a system still solid, but with persistent disparities — calling for targeted support and replication of best practices from leading regions.",
        "va_below": "slightly below expectations",
        "va_within": "within expectations",
        "va_above": "above expectations",
        "advantage": "statistically significant advantage",
        "lag": "statistically significant lag",
        
        # Warnings
        "no_data": "No data available for this selection.",
        "insufficient_data": "Insufficient data to display this section.",
    },
    "fr": {
        "language": "Langue", "en": "English", "fr": "Français",
        "header": "🎯 Vue d'ensemble & Analyse",
        "intro": "📊 Cette page fournit une vue complète des résultats IVAC : tendances, disparités territoriales, comparaison sectorielle et synthèse des insights clés.",
        
        # Filters
        "filters_title": "🔧 Filtres",
        "filter_session": "📅 Session",
        "filter_regions": "🗺️ Régions",
        "filter_sector": "🏫 Secteur",
        "sector_all": "Tous secteurs",
        
        # KPIs
        "exec_title": "🎯 Indicateurs Clés de Performance",
        "kpi_rate": "🎓 Taux moyen",
        "kpi_va": "📈 VA moyenne",
        "kpi_sigma": "📊 Dispersion (σ)",
        "kpi_n": "Établissements",
        "exec_success": "✅ **Performance excellente** : forte valeur ajoutée nationale.",
        "exec_alert": "🔴 **Alertes détectées** : performance en-dessous des attentes.",
        "exec_ok": "ℹ️ **Performance standard** : proche des attentes.",
        
        # Trends
        "trend_title": "📈 Évolution Temporelle",
        "trend_caption": "Courbe ascendante suggère une amélioration nationale ; comparez à la moyenne de la dernière session.",
        "multi_title": "Évolution conjointe : VA & Taux de réussite",
        "multi_note": "**Lecture :** Les deux montent → amélioration | Taux ↑ mais VA plate → inflation des notes | VA ↑ mais taux stable → amélioration qualitative.",
        
        # Regional
        "regional_title": "🗺️ Disparités Territoriales",
        "map_title": "Carte choroplèthe par département",
        "map_caption": "**Lecture :** Couleurs chaudes = performance plus faible | Couleurs froides = performance plus élevée | Survolez pour détails.",
        "top_regions": "Top 10 régions (VA)",
        "bottom_regions": "Bottom 10 régions (VA)",
        
        # Distribution
        "dist_title": "📊 Distribution des Performances",
        "dist_caption": "Centrée proche de 0 = équilibrée ; longues queues = établissements atypiques.",
        "mean_label": "Moyenne",
        "expected_label": "Attendu",
        "excellent_zone": "Excellence (>5)",
        "weak_zone": "Fragile (<-5)",
        
        # Sector
        "sector_title": "🏫 Comparaison Public vs Privé",
        "sector_box": "Distribution VA par secteur",
        "sector_test": "🧮 Test statistique (t-test)",
        "stat_sig": "✅ Différence significative (p = {p:.4f})",
        "stat_nsig": "ℹ️ Pas de différence significative (p = {p:.4f})",
        "sector_delta": "Δ(Privé − Public) = {delta:+.2f} points de VA",
        "sector_caption": "⚠️ Différence ≠ causalité (effets de sélection, contexte...).",
        
        # Correlation
        "corrmatrix_title": "🔗 Matrice de Corrélation",
        "corrmatrix_caption": "Coefficients de Pearson entre variables clés. Valeurs proches de ±1 indiquent des relations fortes.",
        
        # Synthesis
        "synthesis_title": "🧾 Synthèse Nationale",
        "synthesis_intro": "L'analyse de la session **{session}** présente un tableau nuancé du système éducatif français. Avec un taux de réussite moyen de **{rate:.1f}%**, la **valeur ajoutée moyenne (VA = {va:+.2f})** indique des performances {va_interp}, restant globalement stables (σ = {sigma:.2f}).",
        "synthesis_regional": "Les écarts régionaux demeurent marqués : **{best}** se distingue comme région la plus performante, tandis que **{worst}** affiche des résultats plus modestes.",
        "synthesis_sector": "Le **secteur privé** présente un {direction} (**{gap:+.2f} points de VA**) par rapport au public, bien qu'il puisse s'agir d'un **effet de sélection plus que d'une différence structurelle**.",
        "synthesis_conclusion": "🔍 **En conclusion :** la session {session} illustre un système solide mais hétérogène — nécessitant un accompagnement ciblé et une diffusion des bonnes pratiques issues des régions leaders.",
        "va_below": "légèrement en deçà des attentes",
        "va_within": "conformes aux attentes",
        "va_above": "au-dessus des attentes",
        "advantage": "avantage statistiquement significatif",
        "lag": "retard statistiquement significatif",
        
        # Warnings
        "no_data": "Aucune donnée disponible pour cette sélection.",
        "insufficient_data": "Données insuffisantes pour afficher cette section.",
    }
}

def _get_lang() -> str:
    try:
        lang = st.query_params.get("lang", "fr")
        return lang if lang in ("en", "fr") else "fr"
    except Exception:
        return "fr"

def _set_lang(lang: str):
    try:
        st.query_params["lang"] = lang
    except Exception:
        pass

def _ensure_session_str(df: pd.DataFrame | None) -> pd.DataFrame | None:
    if df is None or len(getattr(df, "columns", [])) == 0:
        return df
    if "session" in df.columns and "session_str" not in df.columns:
        df = df.copy()
        df["session"] = df["session"].astype("Int64")
        df["session_str"] = df["session"].astype(str)
    return df

def show():
    # Language switcher
    current = _get_lang()
    st.sidebar.subheader(TEXTS[current]["language"])
    choice = st.sidebar.radio(
        label=" ",
        options=["en", "fr"],
        format_func=lambda x: TEXTS[x][x],
        key="lang_selector_overview",
        horizontal=True,
        label_visibility="collapsed",
    )
    if choice != current:
        _set_lang(choice)
        st.rerun()
    T = TEXTS[choice]

    # Header
    st.header(T["header"])
    st.info(T["intro"])

    # Load data
    df_raw = load_data()
    tables = make_tables(df_raw)

    ts = _ensure_session_str(tables.get("timeseries"))
    by_region = _ensure_session_str(tables.get("by_region"))
    by_dep = tables.get("by_departement", pd.DataFrame()).copy()
    df_over = tables.get("overview", pd.DataFrame()).copy()

    # Sidebar filters
    with st.sidebar:
        st.subheader(T["filters_title"])
        
        # Session
        sessions = sorted(ts["session_str"].unique().tolist()) if (ts is not None and not ts.empty and "session_str" in ts.columns) else []
        selected_session = st.selectbox(T["filter_session"], sessions, index=len(sessions) - 1 if sessions else 0) if sessions else None
        
        # Regions
        regions = (
            sorted(by_region["region_academique"].dropna().unique().tolist())
            if (by_region is not None and not by_region.empty and "region_academique" in by_region.columns) else []
        )
        selected_regions = st.multiselect(T["filter_regions"], regions, default=regions[:5] if regions else [])
        
        # Sector
        sector_sel = st.selectbox(
            T["filter_sector"], 
            [T["sector_all"], "PU", "PR"],
            index=0
        ) if "secteur" in df_over.columns else T["sector_all"]

    # Apply filters
    df_view = df_over.copy()
    if selected_session and "session_str" in df_view.columns:
        df_view = df_view[df_view["session_str"] == selected_session]
    if selected_regions and "region_academique" in df_view.columns:
        df_view = df_view[df_view["region_academique"].isin(selected_regions)]
    if sector_sel != T["sector_all"] and "secteur" in df_view.columns:
        df_view = df_view[df_view["secteur"] == sector_sel]

    # Regional view
    reg_view = by_region.copy() if (by_region is not None) else pd.DataFrame()
    if selected_session and not reg_view.empty and "session_str" in reg_view.columns:
        reg_view = reg_view[reg_view["session_str"] == selected_session]
    if selected_regions and not reg_view.empty and "region_academique" in reg_view.columns:
        reg_view = reg_view[reg_view["region_academique"].isin(selected_regions)]

    # ==================== SECTION 1: KPIs ====================
    st.markdown(f"### {T['exec_title']}")
    if not df_view.empty:
        mean_va = df_view["valeur_ajoutee"].mean() if "valeur_ajoutee" in df_view.columns else 0.0
        mean_rate = df_view["taux_reussite_g"].mean() if "taux_reussite_g" in df_view.columns else 0.0
        std_va = df_view["valeur_ajoutee"].std() if "valeur_ajoutee" in df_view.columns else 0.0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(T["kpi_rate"], f"{mean_rate:.1f}%")
        c2.metric(T["kpi_va"], f"{mean_va:+.2f}")
        c3.metric(T["kpi_sigma"], f"{std_va:.2f}")
        c4.metric(T["kpi_n"], f"{len(df_view):,}")

        st.markdown("---")
        if mean_va > 2:
            st.success(T["exec_success"])
        elif mean_va < -2:
            st.error(T["exec_alert"])
        else:
            st.info(T["exec_ok"])
    else:
        st.warning(T["no_data"])

    st.divider()

    # ==================== SECTION 2: TRENDS ====================
    st.subheader(T["trend_title"])
    if ts is not None and not ts.empty and "valeur_ajoutee" in ts.columns and "session_str" in ts.columns:
        ts_valid = ts["valeur_ajoutee"].dropna()
        if len(ts_valid) >= 2:
            # Joint evolution chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ts["session_str"], y=ts["valeur_ajoutee"],
                name=T["kpi_va"], mode="lines+markers",
                line=dict(color="#2E86AB", width=3), marker=dict(size=8)
            ))
            if "taux_reussite_g" in ts.columns:
                fig.add_trace(go.Scatter(
                    x=ts["session_str"], y=ts["taux_reussite_g"],
                    name=T["kpi_rate"], mode="lines+markers",
                    line=dict(color="#A23B72", width=3, dash="dash"),
                    marker=dict(size=8), yaxis="y2"
                ))
            
            fig.update_layout(
                title=T["multi_title"],
                yaxis=dict(title=T["kpi_va"], side="left", color="#2E86AB"),
                yaxis2=dict(title=T["kpi_rate"], side="right", overlaying="y", color="#A23B72"),
                hovermode="x unified", height=450
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption(T["multi_note"])
        else:
            st.info(T["insufficient_data"])
    else:
        st.warning(T["no_data"])

    st.divider()

    # ==================== SECTION 3: REGIONAL DISPARITIES ====================
    st.subheader(T["regional_title"])
    
    # Top/Bottom regions bar charts
    if not reg_view.empty and "valeur_ajoutee" in reg_view.columns and "region_academique" in reg_view.columns:
        reg_sorted = reg_view.sort_values("valeur_ajoutee", ascending=False)
        
        col1, col2 = st.columns(2)
        with col1:
            top_10 = reg_sorted.head(10)
            if not top_10.empty:
                bar_chart(top_10, x="region_academique", y="valeur_ajoutee", 
                         title=T["top_regions"], sign_color=True)
        
        with col2:
            bottom_10 = reg_sorted.tail(10).sort_values("valeur_ajoutee")
            if not bottom_10.empty:
                bar_chart(bottom_10, x="region_academique", y="valeur_ajoutee", 
                         title=T["bottom_regions"], sign_color=True)
    
    # Map
    st.markdown(f"#### {T['map_title']}")
    if not by_dep.empty and "code_departement" in by_dep.columns:
        # Normalize codes
        by_dep["code_departement"] = (
            by_dep["code_departement"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.zfill(2)
            .replace({"201": "2A", "202": "2B"})
        )
        
        value_col = "taux_reussite_g" if "taux_reussite_g" in by_dep.columns else "valeur_ajoutee"
        if value_col in by_dep.columns:
            geojson = load_geojson("/Users/manonaubel/Library/CloudStorage/OneDrive-Efrei/StreamlitApp25_>20221191_AUBEL.MANON/assets/assets/fr_departements.geojson")
            if geojson:
                map_chart(
                    by_departement=by_dep,
                    geojson=geojson,
                    featureidkey="properties.code",
                    dep_code_col="code_departement",
                    value_col=value_col,
                    title=T["map_title"],
                )
                st.caption(T["map_caption"])
    else:
        st.info(T["no_data"])

    st.divider()

    # ==================== SECTION 4: DISTRIBUTION ====================
    st.subheader(T["dist_title"])
    if "valeur_ajoutee" in df_view.columns and not df_view.empty:
        va_valid = df_view["valeur_ajoutee"].dropna()
        if len(va_valid) >= 5:
            va_mean = float(va_valid.mean())
            va_max = float(va_valid.max())
            va_min = float(va_valid.min())
            
            # Performance zones
            zones = []
            if va_max > 5:
                zones.append({"x0": 5, "x1": va_max, "color": "green", "opacity": 0.15, "label": T["excellent_zone"]})
            if va_min < -5:
                zones.append({"x0": va_min, "x1": -5, "color": "red", "opacity": 0.15, "label": T["weak_zone"]})
            
            histogram(df_view, x="valeur_ajoutee", nbins=40, title=T["dist_title"],
                     ref_x=va_mean, ref_label=T["mean_label"],
                     threshold_zones=zones if zones else None)
            st.caption(T["dist_caption"])
        else:
            st.info(T["insufficient_data"])
    else:
        st.warning(T["no_data"])

    st.divider()

    # ==================== SECTION 5: SECTOR COMPARISON ====================
    st.subheader(T["sector_title"])
    if "secteur" in df_view.columns and "valeur_ajoutee" in df_view.columns and not df_view.empty:
        df_sector = df_view[df_view["secteur"].isin(["PU", "PR"])].copy()
        if not df_sector.empty:
            # Box plots
            fig = px.box(
                df_sector, x="secteur", y="valeur_ajoutee",
                title=T["sector_box"], color="secteur",
                color_discrete_map={"PU": "#3498db", "PR": "#e74c3c"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistical test
            from scipy import stats
            pu = df_sector[df_sector["secteur"] == "PU"]["valeur_ajoutee"].dropna()
            pr = df_sector[df_sector["secteur"] == "PR"]["valeur_ajoutee"].dropna()
            
            if len(pu) > 3 and len(pr) > 3:
                t_stat, p_value = stats.ttest_ind(pu, pr)
                st.markdown(f"#### {T['sector_test']}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("t-stat", f"{t_stat:.3f}")
                col2.metric("p-value", f"{p_value:.4f}")
                
                if p_value < 0.05:
                    col3.success(T["stat_sig"].format(p=p_value))
                else:
                    col3.info(T["stat_nsig"].format(p=p_value))
                
                delta = pr.mean() - pu.mean()
                st.markdown(T["sector_delta"].format(delta=delta))
                st.caption(T["sector_caption"])
        else:
            st.info(T["no_data"])
    else:
        st.warning(T["no_data"])

    st.divider()

    # ==================== SECTION 6: CORRELATION MATRIX ====================
    st.subheader(T["corrmatrix_title"])
    numeric_cols = ["valeur_ajoutee", "taux_reussite_g", "nb_candidats_total", 
                    "taux_brut_reussite_g", "effectif_presents_g", "effectif_admis_g"]
    available_cols = [col for col in numeric_cols if col in df_view.columns]
    
    if len(available_cols) >= 2:
        corr_data = df_view[available_cols].dropna()
        if not corr_data.empty and len(corr_data) >= 3:
            corr_matrix = corr_data.corr()
            
            # Labels
            if T is TEXTS["fr"]:
                label_map = {
                    "valeur_ajoutee": "Valeur ajoutée",
                    "taux_reussite_g": "Taux réussite",
                    "nb_candidats_total": "Nb candidats",
                    "taux_brut_reussite_g": "Taux brut",
                    "effectif_presents_g": "Effectif présents",
                    "effectif_admis_g": "Effectif admis"
                }
            else:
                label_map = {
                    "valeur_ajoutee": "Added value",
                    "taux_reussite_g": "Pass rate",
                    "nb_candidats_total": "Candidates",
                    "taux_brut_reussite_g": "Raw pass rate",
                    "effectif_presents_g": "Present",
                    "effectif_admis_g": "Admitted"
                }
            
            display_labels = [label_map.get(col, col) for col in corr_matrix.columns]
            
            # Heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=display_labels,
                y=display_labels,
                colorscale='RdBu_r',
                zmid=0, zmin=-1, zmax=1,
                text=np.round(corr_matrix.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Corrélation" if T is TEXTS["fr"] else "Correlation"),
                hovertemplate='%{x} vs %{y}<br>r = %{z:.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=T["corrmatrix_title"],
                height=500, width=700,
                font=dict(size=11),
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.caption(T["corrmatrix_caption"])
        else:
            st.info(T["insufficient_data"])
    else:
        st.warning(T["no_data"])

    st.divider()

    # ==================== SECTION 7: NATIONAL SYNTHESIS ====================
    st.markdown(f"### {T['synthesis_title']}")
    if not df_view.empty and "valeur_ajoutee" in df_view.columns:
        mean_va = df_view["valeur_ajoutee"].mean()
        std_va = df_view["valeur_ajoutee"].std()
        mean_rate = df_view["taux_reussite_g"].mean() if "taux_reussite_g" in df_view.columns else None
        
        # VA interpretation
        if mean_va < -0.5:
            va_interp = T["va_below"]
        elif mean_va < 0.5:
            va_interp = T["va_within"]
        else:
            va_interp = T["va_above"]
        
        # Best/worst regions
        best_region = worst_region = "—"
        if "region_academique" in df_view.columns:
            reg_mean = df_view.groupby("region_academique")["valeur_ajoutee"].mean().dropna()
            if not reg_mean.empty:
                best_region = reg_mean.idxmax()
                worst_region = reg_mean.idxmin()
        
        # Sector gap
        sector_gap = None
        sector_direction = ""
        if "secteur" in df_view.columns:
            pu = df_view.loc[df_view["secteur"] == "PU", "valeur_ajoutee"].dropna()
            pr = df_view.loc[df_view["secteur"] == "PR", "valeur_ajoutee"].dropna()
            if len(pu) > 0 and len(pr) > 0:
                sector_gap = pr.mean() - pu.mean()
                sector_direction = T["advantage"] if sector_gap > 0 else T["lag"]
        
        # Build synthesis
        st.markdown(T["synthesis_intro"].format(
            session=selected_session or "2024",
            rate=mean_rate if mean_rate else 0,
            va=mean_va,
            va_interp=va_interp,
            sigma=std_va
        ))
        
        st.markdown(T["synthesis_regional"].format(
            best=best_region,
            worst=worst_region
        ))
        
        if sector_gap is not None:
            st.markdown(T["synthesis_sector"].format(
                direction=sector_direction,
                gap=sector_gap
            ))
        
        st.info(T["synthesis_conclusion"].format(session=selected_session or "2024"))
    else:
        st.warning(T["no_data"])
