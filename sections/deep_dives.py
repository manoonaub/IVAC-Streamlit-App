import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import make_tables, profile_dataframe
from utils.viz import bar_chart, histogram, line_chart, scatter


TEXTS = {
    "en": {
        "language": "Language", "en": "English", "fr": "Français",
        "title": "🔬 Deep Dives – In-Depth Analysis",
        "filters": "Filters – Focus",
        "session": "Session",
        "academy": "Academy",
        "school": "School",
        "ranking_metric": "Ranking metric",
        "top_n": "Number of schools to show (Top/Bottom)",
        
        # Texte explicatif
        "intro_title": "🎯 Objective",
        "intro_text": """
The **Deep Dives** page goes beyond the national averages presented in the Analysis section.
It aims to identify **structural and contextual factors** that influence school performance.
The goal is to understand **why** some schools achieve better results than others — not just **how much**.
""",
        "methods_title": "🧩 Methods Used",
        "method_1": "**1. Analysis by School Size:**",
        "method_1_desc": "Compares average performance (VA) between small, medium, and large schools. This approach reveals the possible impact of size on success or added value.",
        "method_2": "**2. Sector × Size Interaction:**",
        "method_2_desc": "Studies whether size effects differ between public and private schools. This helps determine if sector modifies the relationship between size and performance.",
        "method_3": "**3. Outliers Analysis:**",
        "method_3_desc": "Identifies atypical schools — those with extremely high or low VA. These isolated cases often help spot innovative practices or unfavorable contexts.",
        "method_4": "**4. Detailed Regional Analysis:**",
        "method_4_desc": "Breaks down a region's performance by department to detect internal disparities.",
        
        "interpretation_title": "🧠 Overall Interpretation",
        "interpretation_text": """
The results of these analyses highlight:
- A **moderate correlation** between size and performance: medium-sized schools appear most balanced.
- A **visible sector effect**: private schools tend to perform better in small structures, while public schools remain more stable.
- The presence of **exceptional schools**, positive or negative, suggests that performance is not only linked to socio-economic context, but also to local management and pedagogical environment.
""",
        "conclusion_title": "💡 Conclusion",
        "conclusion_text": """
These in-depth analyses enrich the overall reading of IVAC results.
They reveal **hidden dynamics** behind averages and pave the way for reflection on factors of excellence and areas to strengthen in the French education system.
""",
        
        # Sections
        "school_evolution": "Evolution of a school (added value and pass rate)",
        "intra_academy": "Intra-academy comparison – schools (selected session)",
        "candidates_vs": "Candidates vs performance",
        "distribution": "Distribution (selected session)",
        "full_table": "Full filtered table",
        "export_csv": "Export CSV (filtered)",
    },
    "fr": {
        "language": "Langue", "en": "English", "fr": "Français",
        "title": "🔬 Deep Dives – Analyses approfondies",
        "filters": "Filtres – Focus",
        "session": "Session",
        "academy": "Académie",
        "school": "Établissement",
        "ranking_metric": "Métrique de classement",
        "top_n": "Nombre d'établissements à afficher (Top/Bottom)",
        
        # Texte explicatif
        "intro_title": "🎯 Objectif de la page",
        "intro_text": """
La page **Deep Dives** vise à aller au-delà de la moyenne nationale présentée dans la section Analysis.
Elle permet d'identifier les **facteurs structurels et contextuels** qui influencent la performance des établissements.
L'objectif est de comprendre **pourquoi** certaines écoles obtiennent de meilleurs résultats que d'autres — pas seulement **combien**.
""",
        "methods_title": "🧩 Méthodes utilisées",
        "method_1": "**1. Analyse par taille d'établissement :**",
        "method_1_desc": "Permet de comparer la performance moyenne (VA) entre petits, moyens et grands établissements. Cette approche révèle l'impact possible de la taille sur la réussite ou la valeur ajoutée.",
        "method_2": "**2. Croisement Secteur × Taille :**",
        "method_2_desc": "Étudie si les effets de taille diffèrent entre les établissements publics et privés. On peut ainsi déterminer si le secteur modifie la relation entre la taille et la performance.",
        "method_3": "**3. Analyse des Outliers :**",
        "method_3_desc": "Identifie les établissements atypiques — ceux qui obtiennent une VA extrêmement haute ou basse. Ces cas isolés permettent souvent de repérer des pratiques innovantes ou des contextes défavorables.",
        "method_4": "**4. Analyse régionale détaillée :**",
        "method_4_desc": "Décompose la performance d'une région par département afin de détecter des disparités internes.",
        
        "interpretation_title": "🧠 Interprétation globale",
        "interpretation_text": """
Les résultats de ces analyses mettent en évidence :
- Une **corrélation modérée** entre la taille et la performance : les établissements de taille moyenne semblent les plus équilibrés.
- Un **effet secteur visible** : le privé tend à mieux performer sur les petites structures, tandis que le public reste plus stable.
- La présence d'**établissements exceptionnels**, positifs ou négatifs, suggère que la performance n'est pas uniquement liée au contexte socio-économique, mais aussi à la gestion locale et à l'environnement pédagogique.
""",
        "conclusion_title": "💡 Conclusion",
        "conclusion_text": """
Ces analyses approfondies enrichissent la lecture globale des résultats IVAC.
Elles révèlent les **dynamiques cachées** derrière les moyennes et ouvrent la voie à une réflexion sur les facteurs d'excellence et les zones à renforcer dans le système éducatif français.
""",
        
        # Sections
        "school_evolution": "Évolution d'un établissement (valeur ajoutée et taux de réussite)",
        "intra_academy": "Comparaison intra-académique – établissements (session sélectionnée)",
        "candidates_vs": "Candidats vs performance",
        "distribution": "Distribution (session sélectionnée)",
        "full_table": "Table complète filtrée",
        "export_csv": "Exporter CSV (filtré)",
    }
}

def _get_lang():
    return st.session_state.get("lang_deepdives", "fr")

def _set_lang(lang: str):
    st.session_state["lang_deepdives"] = lang

def show_explanatory_text(T: dict):
    """Affiche le texte explicatif pédagogique"""
    st.markdown("---")
    
    # Objectif
    st.markdown(f"## {T['intro_title']}")
    st.markdown(T["intro_text"])
    
    st.markdown("---")
    
    # Méthodes
    st.markdown(f"## {T['methods_title']}")
    st.markdown(f"{T['method_1']}")
    st.markdown(T["method_1_desc"])
    st.markdown("")
    st.markdown(f"{T['method_2']}")
    st.markdown(T["method_2_desc"])
    st.markdown("")
    st.markdown(f"{T['method_3']}")
    st.markdown(T["method_3_desc"])
    st.markdown("")
    st.markdown(f"{T['method_4']}")
    st.markdown(T["method_4_desc"])
    
    st.markdown("---")
    
    # Interprétation
    st.markdown(f"## {T['interpretation_title']}")
    st.markdown(T["interpretation_text"])
    
    st.markdown("---")
    
    # Conclusion
    st.markdown(f"## {T['conclusion_title']}")
    st.markdown(T["conclusion_text"])
    
    st.markdown("---")

def show():
    # Language switch
    current = _get_lang()
    st.sidebar.subheader(TEXTS[current]["language"])
    choice = st.sidebar.radio(
        label=" ",
        options=["en", "fr"],
        format_func=lambda x: TEXTS[x][x],
        horizontal=True,
        key="lang_selector_deepdives",
        label_visibility="collapsed",
    )
    if choice != current:
        _set_lang(choice)
        st.rerun()
    
    T = TEXTS[current]
    
    # Titre principal
    st.header(T["title"])
    
    # Afficher le texte explicatif
    show_explanatory_text(T)
    
    # Charger les données
    df_raw = load_data()
    tables = make_tables(df_raw)
    prof = profile_dataframe(df_raw)
    df_std = prof["standardized"]

    # Filtres
    with st.sidebar:
        st.subheader(T["filters"])
        sessions = sorted(df_std["session_str"].dropna().unique().tolist()) if "session_str" in df_std.columns else []
        session_sel = st.selectbox(T["session"], sessions, index=len(sessions) - 1 if sessions else 0)
        academies = sorted(df_std["academie"].dropna().unique().tolist()) if "academie" in df_std.columns else []
        acad_sel = st.selectbox(T["academy"], academies, index=0 if academies else None)
        # Liste des établissements de l'académie sélectionnée
        etabs = []
        if acad_sel and "academie" in df_std.columns and "nom_de_l_etablissement" in df_std.columns:
            etabs = sorted(df_std.loc[df_std["academie"] == acad_sel, "nom_de_l_etablissement"].dropna().unique().tolist())
        etab_sel = st.selectbox(T["school"], etabs, index=0 if etabs else None)
        # Contrôles d'affichage
        metric_choices = [m for m in ["valeur_ajoutee", "taux_reussite_g", "nb_candidats_g"] if m in df_std.columns]
        metric_sel = st.selectbox(T["ranking_metric"], metric_choices) if metric_choices else None
        top_n = st.slider(T["top_n"], min_value=5, max_value=100, value=15, step=5)

    # Sous-ensembles
    df_acad = df_std.copy()
    if acad_sel and "academie" in df_acad.columns:
        df_acad = df_acad[df_acad["academie"] == acad_sel]
    if session_sel and "session_str" in df_acad.columns:
        df_acad_sess = df_acad[df_acad["session_str"] == session_sel]
    else:
        df_acad_sess = df_acad

    # 1) Évolution d'un établissement sur les sessions
    if etab_sel and "nom_de_l_etablissement" in df_std.columns and "session_str" in df_std.columns:
        st.subheader(T["school_evolution"])
        df_etab = df_std[df_std["nom_de_l_etablissement"] == etab_sel]
        
        # Labels bilingues pour les zones
        excellent_label = "Excellent" if T is TEXTS["en"] else "Excellent"
        good_label = "Good" if T is TEXTS["en"] else "Bon"
        watch_label = "Watch" if T is TEXTS["en"] else "Vigilance"
        weak_label = "Weak" if T is TEXTS["en"] else "Fragile"
        expected_label = "Expected (0)" if T is TEXTS["en"] else "Attendu (0)"
        nat_avg_label = "National avg (~87%)" if T is TEXTS["en"] else "Moy. nationale (~87%)"
        
        # Performance zones for school evolution
        zones_school = [
            {"y0": 5, "y1": 15, "color": "green", "opacity": 0.1, "label": excellent_label},
            {"y0": 2, "y1": 5, "color": "lightgreen", "opacity": 0.1, "label": good_label},
            {"y0": -5, "y1": -2, "color": "lightyellow", "opacity": 0.1, "label": watch_label},
            {"y0": -15, "y1": -5, "color": "lightcoral", "opacity": 0.1, "label": weak_label}
        ]
        
        if "valeur_ajoutee" in df_etab.columns and not df_etab.empty:
            title_va = f"Added value – {etab_sel}" if T is TEXTS["en"] else f"Valeur ajoutée – {etab_sel}"
            line_chart(df_etab.sort_values("session_str"), x="session_str", y="valeur_ajoutee", 
                      title=title_va,
                      ref_y=0, ref_label=expected_label,
                      threshold_zones=zones_school)
        if "taux_reussite_g" in df_etab.columns and not df_etab.empty:
            # Pass rate thresholds
            excellent_rate = "Excellent (>90%)" if T is TEXTS["en"] else "Excellent (>90%)"
            good_rate = "Good (>85%)" if T is TEXTS["en"] else "Bon (>85%)"
            zones_rate = [
                {"y0": 90, "y1": 100, "color": "green", "opacity": 0.1, "label": excellent_rate},
                {"y0": 85, "y1": 90, "color": "lightgreen", "opacity": 0.1, "label": good_rate}
            ]
            title_rate = f"Pass rate (G) – {etab_sel}" if T is TEXTS["en"] else f"Taux de réussite (G) – {etab_sel}"
            line_chart(df_etab.sort_values("session_str"), x="session_str", y="taux_reussite_g", 
                      title=title_rate,
                      ref_y=87, ref_label=nat_avg_label,
                      threshold_zones=zones_rate)

    # 2) Comparaison intra-académie (Top/Bottom sur session)
    st.subheader(T["intra_academy"])
    rank_metric = metric_sel if metric_sel else ("valeur_ajoutee" if "valeur_ajoutee" in df_acad_sess.columns else None)
    if not df_acad_sess.empty and rank_metric is not None and rank_metric in df_acad_sess.columns:
        df_rank = df_acad_sess.dropna(subset=[rank_metric, "nom_de_l_etablissement"]).sort_values(rank_metric, ascending=False)
        
        if len(df_rank) > 0:
            top_title = f"Top {top_n} – {rank_metric}" if T is TEXTS["en"] else f"Top {top_n} – {rank_metric}"
            bottom_title = f"Bottom {top_n} – {rank_metric}" if T is TEXTS["en"] else f"Bottom {top_n} – {rank_metric}"
            
            bar_chart(df_rank.head(top_n), x="nom_de_l_etablissement", y=rank_metric, title=top_title, download_name="top_schools.png")
            bar_chart(df_rank.tail(top_n), x="nom_de_l_etablissement", y=rank_metric, title=bottom_title, download_name="bottom_schools.png")
        else:
            no_data_msg = "No data available for this filter combination." if T is TEXTS["en"] else "Aucune donnée disponible pour cette combinaison de filtres."
            st.info(no_data_msg)
    else:
        no_data_msg = "No data available for this filter combination." if T is TEXTS["en"] else "Aucune donnée disponible pour cette combinaison de filtres."
        st.info(no_data_msg)

    # 3) Méthode 1 : Analyse par taille d'établissement
    st.markdown("---")
    method1_title = "**Method 1:** Analysis by School Size" if T is TEXTS["en"] else "**Méthode 1 :** Analyse par taille d'établissement"
    st.markdown(f"### {method1_title}")
    
    if "nb_candidats_g" in df_acad_sess.columns and "valeur_ajoutee" in df_acad_sess.columns:
        # Catégoriser par taille
        df_size = df_acad_sess.dropna(subset=["nb_candidats_g", "valeur_ajoutee"])
        
        if len(df_size) >= 3:
            df_size["size_category"] = pd.cut(
                df_size["nb_candidats_g"], 
                bins=[0, 50, 150, 1000], 
                labels=["Small (<50)" if T is TEXTS["en"] else "Petit (<50)", 
                       "Medium (50-150)" if T is TEXTS["en"] else "Moyen (50-150)", 
                       "Large (>150)" if T is TEXTS["en"] else "Grand (>150)"]
            )
            
            # Moyenne par catégorie de taille
            size_summary = df_size.groupby("size_category", observed=True)["valeur_ajoutee"].mean().reset_index()
            
            if not size_summary.empty:
                size_title = "Average added value by school size" if T is TEXTS["en"] else "Valeur ajoutée moyenne par taille d'établissement"
                bar_chart(size_summary, x="size_category", y="valeur_ajoutee", 
                         title=size_title, ref_y=0, ref_label="Expected (0)" if T is TEXTS["en"] else "Attendu (0)")
            else:
                no_data_msg = "Not enough data to categorize by size." if T is TEXTS["en"] else "Pas assez de données pour catégoriser par taille."
                st.info(no_data_msg)
        else:
            no_data_msg = "Not enough schools for size analysis (minimum 3 required)." if T is TEXTS["en"] else "Pas assez d'établissements pour l'analyse par taille (minimum 3 requis)."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available." if T is TEXTS["en"] else "Colonnes requises non disponibles."
        st.info(no_data_msg)
    
    # 4) Méthode 2 : Croisement Secteur × Taille
    st.markdown("---")
    method2_title = "**Method 2:** Sector × Size Interaction" if T is TEXTS["en"] else "**Méthode 2 :** Croisement Secteur × Taille"
    st.markdown(f"### {method2_title}")
    
    if "nb_candidats_g" in df_acad_sess.columns and "valeur_ajoutee" in df_acad_sess.columns and "secteur" in df_acad_sess.columns:
        df_cross = df_acad_sess.dropna(subset=["nb_candidats_g", "valeur_ajoutee", "secteur"])
        
        if len(df_cross) >= 6:  # Au moins 6 écoles pour avoir des données dans plusieurs catégories
            df_cross["size_category"] = pd.cut(
                df_cross["nb_candidats_g"], 
                bins=[0, 50, 150, 1000], 
                labels=["Small" if T is TEXTS["en"] else "Petit", 
                       "Medium" if T is TEXTS["en"] else "Moyen", 
                       "Large" if T is TEXTS["en"] else "Grand"]
            )
            
            # Moyenne par secteur et taille
            cross_summary = df_cross.groupby(["secteur", "size_category"], observed=True)["valeur_ajoutee"].mean().reset_index()
            
            if not cross_summary.empty:
                cross_title = "Added value: Sector × Size" if T is TEXTS["en"] else "Valeur ajoutée : Secteur × Taille"
                bar_chart(cross_summary, x="size_category", y="valeur_ajoutee", color="secteur",
                         title=cross_title, ref_y=0)
            else:
                no_data_msg = "Not enough data for sector-size interaction." if T is TEXTS["en"] else "Pas assez de données pour le croisement secteur-taille."
                st.info(no_data_msg)
        else:
            no_data_msg = "Not enough schools for sector-size analysis (minimum 6 required)." if T is TEXTS["en"] else "Pas assez d'établissements pour l'analyse secteur-taille (minimum 6 requis)."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available." if T is TEXTS["en"] else "Colonnes requises non disponibles."
        st.info(no_data_msg)
    
    # 5) Méthode 3 : Analyse des Outliers
    st.markdown("---")
    method3_title = "**Method 3:** Outliers Analysis" if T is TEXTS["en"] else "**Méthode 3 :** Analyse des Outliers"
    st.markdown(f"### {method3_title}")
    
    if "valeur_ajoutee" in df_acad_sess.columns and "nom_de_l_etablissement" in df_acad_sess.columns and not df_acad_sess.empty:
        df_outliers = df_acad_sess.dropna(subset=["valeur_ajoutee", "nom_de_l_etablissement"])
        if len(df_outliers) >= 10:
            # Identifier les outliers (top 5 et bottom 5)
            top_outliers = df_outliers.nlargest(5, "valeur_ajoutee")
            bottom_outliers = df_outliers.nsmallest(5, "valeur_ajoutee")
            
            outliers_title_top = "Top 5 exceptional schools (highest VA)" if T is TEXTS["en"] else "Top 5 établissements exceptionnels (VA la plus haute)"
            outliers_title_bottom = "Bottom 5 schools needing attention (lowest VA)" if T is TEXTS["en"] else "Bottom 5 établissements nécessitant attention (VA la plus basse)"
            
            bar_chart(top_outliers, x="nom_de_l_etablissement", y="valeur_ajoutee", 
                     title=outliers_title_top, download_name="top_outliers.png")
            bar_chart(bottom_outliers, x="nom_de_l_etablissement", y="valeur_ajoutee", 
                     title=outliers_title_bottom, download_name="bottom_outliers.png")
        else:
            no_data_msg = f"Not enough schools for outlier analysis (minimum 10 required, found {len(df_outliers)})." if T is TEXTS["en"] else f"Pas assez d'établissements pour l'analyse des outliers (minimum 10 requis, trouvé {len(df_outliers)})."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available or no data." if T is TEXTS["en"] else "Colonnes requises non disponibles ou pas de données."
        st.info(no_data_msg)
    
    # 6) Méthode 4 : Analyse régionale détaillée (par département)
    st.markdown("---")
    method4_title = "**Method 4:** Detailed Regional Analysis" if T is TEXTS["en"] else "**Méthode 4 :** Analyse régionale détaillée"
    st.markdown(f"### {method4_title}")
    
    if "departement" in df_acad_sess.columns and "valeur_ajoutee" in df_acad_sess.columns:
        df_dept = df_acad_sess.dropna(subset=["departement", "valeur_ajoutee"])
        
        if len(df_dept) >= 3:
            dept_summary = df_dept.groupby("departement")["valeur_ajoutee"].agg(['mean', 'count']).reset_index()
            dept_summary = dept_summary[dept_summary['count'] >= 3]  # Au moins 3 établissements par département
            dept_summary = dept_summary.sort_values('mean', ascending=False)
            
            if not dept_summary.empty and len(dept_summary) > 0:
                dept_title = f"Average added value by department – {acad_sel}" if T is TEXTS["en"] else f"Valeur ajoutée moyenne par département – {acad_sel}"
                bar_chart(dept_summary, x="departement", y="mean", 
                         title=dept_title, ref_y=0, ref_label="Expected (0)" if T is TEXTS["en"] else "Attendu (0)")
            else:
                no_data_msg = "Not enough departments with sufficient data (minimum 3 schools per department)." if T is TEXTS["en"] else "Pas assez de départements avec suffisamment de données (minimum 3 écoles par département)."
                st.info(no_data_msg)
        else:
            no_data_msg = "Not enough schools for department analysis." if T is TEXTS["en"] else "Pas assez d'établissements pour l'analyse par département."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available." if T is TEXTS["en"] else "Colonnes requises non disponibles."
        st.info(no_data_msg)
    
    # 7) Scatter: Candidats vs Performance (visualisation supplémentaire)
    st.markdown("---")
    st.subheader(T["candidates_vs"])
    if "nb_candidats_g" in df_acad_sess.columns and "taux_reussite_g" in df_acad_sess.columns:
        scatter_title = f"Candidates (G) vs Pass rate (G) – {acad_sel}" if T is TEXTS["en"] else f"Candidats (G) vs Taux réussite (G) – {acad_sel}"
        scatter(df_acad_sess, x="nb_candidats_g", y="taux_reussite_g", 
               color="secteur" if "secteur" in df_acad_sess.columns else None, 
               title=scatter_title)

    # 4) Distribution session courante
    st.subheader(T["distribution"])
    if "taux_reussite_g" in df_acad_sess.columns:
        dist_title = "Distribution of pass rate (G)" if T is TEXTS["en"] else "Distribution du taux de réussite (G)"
        histogram(df_acad_sess, x="taux_reussite_g", nbins=40, title=dist_title)

    # 5) Table complète filtrée + export CSV
    st.subheader(T["full_table"])
    show_cols = [c for c in [
        "session_str", "academie", "departement", "commune", "nom_de_l_etablissement", "secteur",
        "taux_reussite_g", "valeur_ajoutee", "nb_candidats_g"
    ] if c in df_acad_sess.columns]
    table_df = df_acad_sess[show_cols].sort_values(by=[rank_metric] if rank_metric in df_acad_sess.columns else show_cols[0], ascending=False)
    st.dataframe(table_df, use_container_width=True)

    csv = table_df.to_csv(index=False).encode("utf-8")
    st.download_button(T["export_csv"], data=csv, file_name="etablissements_filtres.csv", mime="text/csv")
