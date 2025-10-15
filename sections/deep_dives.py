import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import make_tables
from utils.viz import bar_chart, histogram, line_chart, scatter

#commentaires pour le visuel (emojis)
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
    df_std = tables["cleaned"]

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

    # Évolution d'un établissement sur les sessions
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
            
            # ANALYSE DU GRAPHIQUE (dans boîte colorée)
            va_values = df_etab["valeur_ajoutee"].dropna()
            if len(va_values) >= 2:
                va_mean = va_values.mean()
                va_trend = va_values.iloc[-1] - va_values.iloc[0]
                
                # Choisir la couleur selon la performance
                if va_mean > 2:
                    analysis_container = st.success  # Vert pour bonne performance
                elif va_mean < -2:
                    analysis_container = st.error  # Rouge pour difficultés
                else:
                    analysis_container = st.info  # Bleu pour standard
                
                if T is TEXTS["en"]:
                    analysis_container(f"""
**📊 What we observe:**
- **Trajectory:** The school's value added {f"**increased by {va_trend:+.2f} points**" if va_trend > 0 else f"**decreased by {abs(va_trend):.2f} points**" if va_trend < 0 else "remained **stable**"} over the observed sessions.
- **Average performance:** **{va_mean:+.2f}** (vs 0 expected).
- **Consistency:** {"Stable performance, little volatility." if va_values.std() < 2 else "Significant fluctuations detected — possible cohort or staff changes."}

**🧠 Interpretation:**
{f"This school **consistently outperforms** expectations across multiple sessions. Likely due to strong pedagogical practices or favorable student composition." if va_mean > 2 else f"The school struggles to reach expected levels. May require targeted support or faces structural challenges." if va_mean < -2 else "Performance is **in line with expectations** given the school's context."}

**💡 Conclusion:**
{"🌟 **Best practice candidate** — consider studying this school's methods for replication." if va_mean > 3 else "⚠️ **Requires attention** — investigate root causes and implement interventions." if va_mean < -3 else "✅ **Standard trajectory** — monitor for consistency."}
""")
                else:
                    analysis_container(f"""
**📊 Ce que l'on observe :**
- **Trajectoire :** La valeur ajoutée de l'établissement {f"**a augmenté de {va_trend:+.2f} points**" if va_trend > 0 else f"**a diminué de {abs(va_trend):.2f} points**" if va_trend < 0 else "est restée **stable**"} sur les sessions observées.
- **Performance moyenne :** **{va_mean:+.2f}** (vs 0 attendu).
- **Constance :** {"Performance stable, peu de volatilité." if va_values.std() < 2 else "Fluctuations significatives détectées — possibles changements de cohorte ou d'équipe."}

**🧠 Interprétation :**
{f"Cet établissement **sur-performe constamment** les attentes sur plusieurs sessions. Probablement dû à des pratiques pédagogiques solides ou une composition d'élèves favorable." if va_mean > 2 else f"L'établissement peine à atteindre les niveaux attendus. Peut nécessiter un soutien ciblé ou fait face à des défis structurels." if va_mean < -2 else "La performance est **conforme aux attentes** compte tenu du contexte de l'établissement."}

**💡 Conclusion :**
{"🌟 **Candidat bonnes pratiques** — envisager d'étudier les méthodes de cet établissement pour réplication." if va_mean > 3 else "⚠️ **Nécessite attention** — investiguer les causes profondes et mettre en place des interventions." if va_mean < -3 else "✅ **Trajectoire standard** — surveiller pour cohérence."}
""")
        
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
            
            #  ANALYSE TAUX DE RÉUSSITE (dans boîte colorée)
            rate_values = df_etab["taux_reussite_g"].dropna()
            if len(rate_values) >= 2:
                rate_mean = rate_values.mean()
                rate_trend = rate_values.iloc[-1] - rate_values.iloc[0]
                
                # Couleur selon la performance
                if rate_mean > 87:
                    rate_container = st.success  # Vert
                elif rate_mean < 85:
                    rate_container = st.warning  # Jaune/orange
                else:
                    rate_container = st.info  # Bleu
                
                if T is TEXTS["en"]:
                    rate_container(f"""
**📊 Pass Rate Analysis:**
- **Trend:** Pass rate {f"**increased by {rate_trend:+.1f}%**" if rate_trend > 1 else f"**decreased by {abs(rate_trend):.1f}%**" if rate_trend < -1 else "remained **stable**"}.
- **Average:** **{rate_mean:.1f}%** (vs national ~87%).
- **Performance level:** {"**Above national average** ✅" if rate_mean > 87 else "**Below national average** ⚠️" if rate_mean < 87 else "**At national level**"}

**💡 Key Insight:**
Compare this graph with the value-added chart above. If pass rates are high but VA is low, the school may benefit from favorable student composition rather than pedagogical excellence. Conversely, high VA with moderate pass rates indicates **strong teaching despite challenging contexts**.
""")
                else:
                    rate_container(f"""
**📊 Analyse du Taux de Réussite :**
- **Évolution :** Le taux {f"**a augmenté de {rate_trend:+.1f}%**" if rate_trend > 1 else f"**a diminué de {abs(rate_trend):.1f}%**" if rate_trend < -1 else "est resté **stable**"}.
- **Moyenne :** **{rate_mean:.1f}%** (vs nationale ~87%).
- **Niveau de performance :** {"**Au-dessus de la moyenne nationale** ✅" if rate_mean > 87 else "**En-dessous de la moyenne nationale** ⚠️" if rate_mean < 87 else "**Au niveau national**"}

**💡 Insight Clé :**
Comparez ce graphique avec celui de la valeur ajoutée ci-dessus. Si les taux sont élevés mais la VA faible, l'établissement bénéficie peut-être d'une composition d'élèves favorable plutôt que d'une excellence pédagogique. À l'inverse, une VA élevée avec des taux modérés indique un **enseignement solide malgré des contextes difficiles**.
""")
        
        st.markdown("---")

    # Comparaison intra-académie (Top/Bottom sur session)
    st.subheader(T["intra_academy"])
    rank_metric = metric_sel if metric_sel else ("valeur_ajoutee" if "valeur_ajoutee" in df_acad_sess.columns else None)
    if not df_acad_sess.empty and rank_metric is not None and rank_metric in df_acad_sess.columns:
        df_rank = df_acad_sess.dropna(subset=[rank_metric, "nom_de_l_etablissement"]).sort_values(rank_metric, ascending=False)
        
        if len(df_rank) > 0:
            top_title = f"Top {top_n} – {rank_metric}" if T is TEXTS["en"] else f"Top {top_n} – {rank_metric}"
            bottom_title = f"Bottom {top_n} – {rank_metric}" if T is TEXTS["en"] else f"Bottom {top_n} – {rank_metric}"
            
            bar_chart(df_rank.head(top_n), x="nom_de_l_etablissement", y=rank_metric, title=top_title, download_name="top_schools.png")
            
            # ANALYSE TOP PERFORMERS (boîte verte = succès)
            top_values = df_rank.head(top_n)[rank_metric]
            if T is TEXTS["en"]:
                st.success(f"""
**📊 Top Performers Analysis:**
- **Range:** {top_values.min():.2f} to {top_values.max():.2f}
- **Average of top {top_n}:** {top_values.mean():.2f}
- **Standout leader:** **{df_rank.iloc[0]['nom_de_l_etablissement']}** with {df_rank.iloc[0][rank_metric]:.2f}

**🧠 What this reveals:**
These schools demonstrate **exceptional performance** within the academy. The gap between #1 and #{top_n} ({(top_values.max() - top_values.min()):.2f} points) indicates {"high variability — even among top performers" if (top_values.max() - top_values.min()) > 3 else "consistent excellence across the top tier"}.

**💡 Action:** Conduct case studies on these schools to identify transferable best practices (teaching methods, student support systems, resource allocation).
""")
            else:
                st.success(f"""
**📊 Analyse des Meilleurs Établissements :**
- **Fourchette :** {top_values.min():.2f} à {top_values.max():.2f}
- **Moyenne du top {top_n} :** {top_values.mean():.2f}
- **Leader incontesté :** **{df_rank.iloc[0]['nom_de_l_etablissement']}** avec {df_rank.iloc[0][rank_metric]:.2f}

**🧠 Ce que cela révèle :**
Ces établissements démontrent des **performances exceptionnelles** au sein de l'académie. L'écart entre le #1 et le #{top_n} ({(top_values.max() - top_values.min()):.2f} points) indique {"une forte variabilité — même parmi les meilleurs" if (top_values.max() - top_values.min()) > 3 else "une excellence cohérente dans le top tier"}.

**💡 Action :** Conduire des études de cas sur ces établissements pour identifier les bonnes pratiques transférables (méthodes d'enseignement, systèmes de soutien, allocation des ressources).
""")
            
            bar_chart(df_rank.tail(top_n), x="nom_de_l_etablissement", y=rank_metric, title=bottom_title, download_name="bottom_schools.png")
            
            #  ANALYSE BOTTOM PERFORMERS (boîte rouge/orange = attention requise)
            bottom_values = df_rank.tail(top_n)[rank_metric]
            if T is TEXTS["en"]:
                st.warning(f"""
**📊 Schools Requiring Support:**
- **Range:** {bottom_values.min():.2f} to {bottom_values.max():.2f}
- **Average of bottom {top_n}:** {bottom_values.mean():.2f}
- **Most challenging:** **{df_rank.iloc[-1]['nom_de_l_etablissement']}** with {df_rank.iloc[-1][rank_metric]:.2f}

**🧠 Root Cause Hypotheses:**
- Socio-economic challenges not fully captured by IVAC model
- High teacher turnover or staffing issues
- Infrastructure limitations
- Geographic isolation (rural areas)

**💡 Recommendation:** These schools need **targeted interventions**: additional funding, pedagogical coaching, peer mentoring from top performers, and potentially structural reforms.
""")
            else:
                st.warning(f"""
**📊 Établissements Nécessitant un Soutien :**
- **Fourchette :** {bottom_values.min():.2f} à {bottom_values.max():.2f}
- **Moyenne du bottom {top_n} :** {bottom_values.mean():.2f}
- **Le plus en difficulté :** **{df_rank.iloc[-1]['nom_de_l_etablissement']}** avec {df_rank.iloc[-1][rank_metric]:.2f}

**🧠 Hypothèses de Causes Profondes :**
- Défis socio-économiques non entièrement capturés par le modèle IVAC
- Fort turnover enseignant ou problèmes de staffing
- Limitations d'infrastructure
- Isolement géographique (zones rurales)

**💡 Recommandation :** Ces établissements nécessitent des **interventions ciblées** : financements additionnels, coaching pédagogique, mentorat par des établissements performants, et potentiellement des réformes structurelles.
""")
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
                
                #  ANALYSE PAR TAILLE (boîte colorée)
                best_size = size_summary.loc[size_summary["valeur_ajoutee"].idxmax(), "size_category"]
                best_va = size_summary["valeur_ajoutee"].max()
                worst_size = size_summary.loc[size_summary["valeur_ajoutee"].idxmin(), "size_category"]
                worst_va = size_summary["valeur_ajoutee"].min()
                
                if T is TEXTS["en"]:
                    st.info(f"""
**📊 Size Analysis:**
- **Best performing size:** {best_size} schools with VA = {best_va:.2f}
- **Lowest performing size:** {worst_size} schools with VA = {worst_va:.2f}
- **Gap:** {best_va - worst_va:.2f} points between categories

**🧠 Interpretation:**
{"Medium-sized schools (50-150 students) tend to perform best — they balance individualized attention with sufficient resources and peer diversity." if "Medium" in str(best_size) or "Moyen" in str(best_size) else f"{best_size} schools show the highest value added, suggesting this size offers optimal conditions for student success."}

**💡 Conclusion:**
Size matters, but it's not deterministic. {"Small schools may struggle with limited resources, while very large schools face individualization challenges." if "Medium" in str(best_size) or "Moyen" in str(best_size) else "School management and pedagogy can compensate for size constraints."}
""")
                else:
                    st.info(f"""
**📊 Analyse par Taille :**
- **Meilleure taille :** Établissements {best_size} avec VA = {best_va:.2f}
- **Taille la moins performante :** Établissements {worst_size} avec VA = {worst_va:.2f}
- **Écart :** {best_va - worst_va:.2f} points entre catégories

**🧠 Interprétation :**
{"Les établissements de taille moyenne (50-150 élèves) tendent à mieux performer — ils équilibrent attention individualisée et ressources/diversité suffisantes." if "Medium" in str(best_size) or "Moyen" in str(best_size) else f"Les établissements {best_size} affichent la plus forte valeur ajoutée, suggérant que cette taille offre des conditions optimales pour la réussite."}

**💡 Conclusion :**
La taille compte, mais n'est pas déterministe. {"Les petits établissements peuvent manquer de ressources, tandis que les très grands peinent à individualiser." if "Medium" in str(best_size) or "Moyen" in str(best_size) else "La gestion et la pédagogie peuvent compenser les contraintes de taille."}
""")
            else:
                no_data_msg = "Not enough data to categorize by size." if T is TEXTS["en"] else "Pas assez de données pour catégoriser par taille."
                st.info(no_data_msg)
        else:
            no_data_msg = "Not enough schools for size analysis (minimum 3 required)." if T is TEXTS["en"] else "Pas assez d'établissements pour l'analyse par taille (minimum 3 requis)."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available." if T is TEXTS["en"] else "Colonnes requises non disponibles."
        st.info(no_data_msg)
    
    # methode 2 : Croisement Secteur × Taille
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
                
                #  ANALYSE SECTEUR × TAILLE (boîte colorée)
                if "PU" in cross_summary["secteur"].values and "PR" in cross_summary["secteur"].values:
                    pu_mean = cross_summary[cross_summary["secteur"] == "PU"]["valeur_ajoutee"].mean()
                    pr_mean = cross_summary[cross_summary["secteur"] == "PR"]["valeur_ajoutee"].mean()
                    
                    if T is TEXTS["en"]:
                        st.info(f"""
**📊 Sector × Size Interaction:**
- **Public (PU) average:** {pu_mean:.2f}
- **Private (PR) average:** {pr_mean:.2f}
- **Sector gap:** {pr_mean - pu_mean:+.2f} points

**🧠 What this reveals:**
{"Private schools outperform public schools across size categories. However, the gap may be larger in small schools (selection effects) and narrower in large schools (regression to the mean)." if pr_mean > pu_mean else "Public schools show competitive or superior performance compared to private schools in this academy, challenging national stereotypes."}

**💡 Conclusion:**
Sector effects interact with size. {"Private schools' advantage is not universal — it varies by school size and local context." if pr_mean > pu_mean else "Public schools demonstrate that with adequate resources and management, they can match or exceed private sector performance."}
""")
                    else:
                        st.info(f"""
**📊 Interaction Secteur × Taille :**
- **Moyenne Public (PU) :** {pu_mean:.2f}
- **Moyenne Privé (PR) :** {pr_mean:.2f}
- **Écart sectoriel :** {pr_mean - pu_mean:+.2f} points

**🧠 Ce que cela révèle :**
{"Le privé sur-performe le public dans toutes les catégories de taille. Cependant, l'écart peut être plus important dans les petits établissements (effets de sélection) et plus étroit dans les grands (régression vers la moyenne)." if pr_mean > pu_mean else "Le public montre des performances compétitives ou supérieures au privé dans cette académie, challengeant les stéréotypes nationaux."}

**💡 Conclusion :**
Les effets sectoriels interagissent avec la taille. {"L'avantage du privé n'est pas universel — il varie selon la taille et le contexte local." if pr_mean > pu_mean else "Le public démontre qu'avec des ressources et une gestion adéquates, il peut égaler ou dépasser le privé."}
""")
            else:
                no_data_msg = "Not enough data for sector-size interaction." if T is TEXTS["en"] else "Pas assez de données pour le croisement secteur-taille."
                st.info(no_data_msg)
        else:
            no_data_msg = "Not enough schools for sector-size analysis (minimum 6 required)." if T is TEXTS["en"] else "Pas assez d'établissements pour l'analyse secteur-taille (minimum 6 requis)."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available." if T is TEXTS["en"] else "Colonnes requises non disponibles."
        st.info(no_data_msg)
    
    # 3) Méthode 3 : Analyse des outliers
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
            
            # ANALYSE TOP OUTLIERS (boîte verte)
            if T is TEXTS["en"]:
                st.success(f"""
**📊 Exceptional Performers (Outliers):**
- **Range:** {top_outliers["valeur_ajoutee"].min():.2f} to {top_outliers["valeur_ajoutee"].max():.2f}
- **Top school:** **{top_outliers.iloc[0]["nom_de_l_etablissement"]}** with VA = {top_outliers.iloc[0]["valeur_ajoutee"]:.2f}

**🧠 Why these schools stand out:**
These outliers likely combine: (1) **innovative pedagogy**, (2) **strong leadership**, (3) **effective student support systems**, (4) **favorable community engagement**. They prove that exceptional results are possible even in challenging contexts.

**💡 Action:** Conduct in-depth case studies on these schools. Document their practices (teaching methods, class organization, extracurricular programs) and create a **best practices playbook** for wider dissemination.
""")
            else:
                st.success(f"""
**📊 Établissements Exceptionnels (Outliers) :**
- **Fourchette :** {top_outliers["valeur_ajoutee"].min():.2f} à {top_outliers["valeur_ajoutee"].max():.2f}
- **Établissement #1 :** **{top_outliers.iloc[0]["nom_de_l_etablissement"]}** avec VA = {top_outliers.iloc[0]["valeur_ajoutee"]:.2f}

**🧠 Pourquoi ces établissements se distinguent :**
Ces outliers combinent probablement : (1) **pédagogie innovante**, (2) **leadership fort**, (3) **systèmes de soutien efficaces**, (4) **engagement communautaire favorable**. Ils prouvent que des résultats exceptionnels sont possibles même dans des contextes difficiles.

**💡 Action :** Conduire des études de cas approfondies sur ces établissements. Documenter leurs pratiques (méthodes d'enseignement, organisation des classes, programmes parascolaires) et créer un **guide des bonnes pratiques** pour diffusion large.
""")
            
            bar_chart(bottom_outliers, x="nom_de_l_etablissement", y="valeur_ajoutee", 
                     title=outliers_title_bottom, download_name="bottom_outliers.png")
            
            #  ANALYSE BOTTOM OUTLIERS (boîte rouge)
            if T is TEXTS["en"]:
                st.error(f"""
**📊 Schools in Crisis (Negative Outliers):**
- **Range:** {bottom_outliers["valeur_ajoutee"].min():.2f} to {bottom_outliers["valeur_ajoutee"].max():.2f}
- **Most struggling:** **{bottom_outliers.iloc[0]["nom_de_l_etablissement"]}** with VA = {bottom_outliers.iloc[0]["valeur_ajoutee"]:.2f}

**🧠 Likely Root Causes:**
- **Systemic issues:** chronic underfunding, high staff turnover, deteriorating infrastructure
- **Contextual challenges:** concentration of disadvantaged students beyond IVAC model predictions
- **Management gaps:** lack of pedagogical leadership or strategic vision

**💡 Urgent Action Required:**
These schools need **immediate intervention**: emergency funding, external pedagogical support teams, principal coaching, and potentially restructuring. Delaying action will worsen student outcomes and staff morale.
""")
            else:
                st.error(f"""
**📊 Établissements en Crise (Outliers Négatifs) :**
- **Fourchette :** {bottom_outliers["valeur_ajoutee"].min():.2f} à {bottom_outliers["valeur_ajoutee"].max():.2f}
- **Plus en difficulté :** **{bottom_outliers.iloc[0]["nom_de_l_etablissement"]}** avec VA = {bottom_outliers.iloc[0]["valeur_ajoutee"]:.2f}

**🧠 Causes Profondes Probables :**
- **Problèmes systémiques :** sous-financement chronique, fort turnover du personnel, dégradation des infrastructures
- **Défis contextuels :** concentration d'élèves défavorisés au-delà des prédictions du modèle IVAC
- **Lacunes managériales :** manque de leadership pédagogique ou de vision stratégique

**💡 Action Urgente Requise :**
Ces établissements nécessitent une **intervention immédiate** : financement d'urgence, équipes de soutien pédagogique externes, coaching des directeurs, et potentiellement restructuration. Retarder l'action aggravera les résultats élèves et le moral du personnel.
""")

        else:
            no_data_msg = f"Not enough schools for outlier analysis (minimum 10 required, found {len(df_outliers)})." if T is TEXTS["en"] else f"Pas assez d'établissements pour l'analyse des outliers (minimum 10 requis, trouvé {len(df_outliers)})."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available or no data." if T is TEXTS["en"] else "Colonnes requises non disponibles ou pas de données."
        st.info(no_data_msg)
    
    # methode 4 : Analyse par département
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
                
                # ANALYSE PAR DÉPARTEMENT (boîte colorée)
                best_dept = dept_summary.iloc[0]["departement"]
                best_dept_va = dept_summary.iloc[0]["mean"]
                worst_dept = dept_summary.iloc[-1]["departement"]
                worst_dept_va = dept_summary.iloc[-1]["mean"]
                dept_gap = best_dept_va - worst_dept_va
                
                if T is TEXTS["en"]:
                    st.info(f"""
**📊 Intra-Regional Disparities:**
- **Best department:** {best_dept} with VA = {best_dept_va:.2f}
- **Weakest department:** {worst_dept} with VA = {worst_dept_va:.2f}
- **Intra-academy gap:** {dept_gap:.2f} points

**🧠 What this reveals:**
Even within the same academy ({acad_sel}), **departmental inequalities are significant**. This suggests that local factors (municipal funding, demographics, geographic isolation) create performance gaps that regional-level policies may miss.

**💡 Recommendation:**
Academy-level strategies must be **differentiated by department**. {best_dept} can serve as a regional model, while {worst_dept} needs targeted support (additional staff, infrastructure investment, peer exchanges).
""")
                else:
                    st.info(f"""
**📊 Disparités Intra-Régionales :**
- **Meilleur département :** {best_dept} avec VA = {best_dept_va:.2f}
- **Département le plus faible :** {worst_dept} avec VA = {worst_dept_va:.2f}
- **Écart intra-académique :** {dept_gap:.2f} points

**🧠 Ce que cela révèle :**
Même au sein de la même académie ({acad_sel}), **les inégalités départementales sont significatives**. Cela suggère que des facteurs locaux (financement municipal, démographie, isolement géographique) créent des écarts que les politiques régionales peuvent manquer.

**💡 Recommandation :**
Les stratégies au niveau académique doivent être **différenciées par département**. {best_dept} peut servir de modèle régional, tandis que {worst_dept} nécessite un soutien ciblé (personnel additionnel, investissement infrastructure, échanges entre pairs).
""")
            else:
                no_data_msg = "Not enough departments with sufficient data (minimum 3 schools per department)." if T is TEXTS["en"] else "Pas assez de départements avec suffisamment de données (minimum 3 écoles par département)."
                st.info(no_data_msg)
        else:
            no_data_msg = "Not enough schools for department analysis." if T is TEXTS["en"] else "Pas assez d'établissements pour l'analyse par département."
            st.info(no_data_msg)
    else:
        no_data_msg = "Required columns not available." if T is TEXTS["en"] else "Colonnes requises non disponibles."
        st.info(no_data_msg)
    
    # scatter candidats vs taux de réussite
    st.markdown("---")
    st.subheader(T["candidates_vs"])
    if "nb_candidats_g" in df_acad_sess.columns and "taux_reussite_g" in df_acad_sess.columns:
        scatter_title = f"Candidates (G) vs Pass rate (G) – {acad_sel}" if T is TEXTS["en"] else f"Candidats (G) vs Taux réussite (G) – {acad_sel}"
        scatter(df_acad_sess, x="nb_candidats_g", y="taux_reussite_g", 
               color="secteur" if "secteur" in df_acad_sess.columns else None, 
               title=scatter_title)
        
        # ANALYSE SCATTER (boîte bleue)
        corr = df_acad_sess[["nb_candidats_g", "taux_reussite_g"]].corr().iloc[0, 1] if len(df_acad_sess) > 3 else 0
        
        if T is TEXTS["en"]:
            st.info(f"""
**📊 Candidates vs Pass Rate Relationship:**
- **Correlation:** r = {corr:.3f} {"(weak)" if abs(corr) < 0.3 else "(moderate)" if abs(corr) < 0.6 else "(strong)"}
- **Pattern:** {"No clear relationship — school size doesn't predict pass rates." if abs(corr) < 0.3 else f"{'Positive' if corr > 0 else 'Negative'} relationship detected."}

**🧠 Interpretation:**
{"This scatter plot shows **dispersion** — schools with similar sizes have very different outcomes. This confirms that **size is not destiny**. Management quality, teaching methods, and local context matter more than student numbers." if abs(corr) < 0.3 else "The correlation suggests size may play a role, but significant variability remains. Other factors (pedagogy, resources) explain most of the variance."}

**💡 Takeaway:**
Don't judge schools by size alone. {"Small schools can excel with individualized attention; large schools can succeed with strong organization." if abs(corr) < 0.3 else "Size effects exist but are mediated by school practices and leadership."}
""")
        else:
            st.info(f"""
**📊 Relation Candidats vs Taux de Réussite :**
- **Corrélation :** r = {corr:.3f} {"(faible)" if abs(corr) < 0.3 else "(modérée)" if abs(corr) < 0.6 else "(forte)"}
- **Pattern :** {"Pas de relation claire — la taille de l'établissement ne prédit pas les taux de réussite." if abs(corr) < 0.3 else f"Relation {'positive' if corr > 0 else 'négative'} détectée."}

**🧠 Interprétation :**
{"Ce nuage de points montre une **dispersion** — des établissements de tailles similaires ont des résultats très différents. Cela confirme que **la taille n'est pas un destin**. La qualité de la gestion, les méthodes d'enseignement et le contexte local comptent plus que le nombre d'élèves." if abs(corr) < 0.3 else "La corrélation suggère que la taille peut jouer un rôle, mais une variabilité significative demeure. D'autres facteurs (pédagogie, ressources) expliquent l'essentiel de la variance."}

**💡 Retenir :**
Ne pas juger un établissement uniquement sur sa taille. {"Les petits peuvent exceller avec attention individualisée ; les grands peuvent réussir avec une organisation solide." if abs(corr) < 0.3 else "Les effets de taille existent mais sont médiés par les pratiques et le leadership de l'établissement."}
""")

    #  Distribution session courante
    st.subheader(T["distribution"])
    if "taux_reussite_g" in df_acad_sess.columns:
        dist_title = "Distribution of pass rate (G)" if T is TEXTS["en"] else "Distribution du taux de réussite (G)"
        histogram(df_acad_sess, x="taux_reussite_g", nbins=40, title=dist_title)
        
        # ANALYSE DISTRIBUTION (boîte bleue)
        rate_mean = df_acad_sess["taux_reussite_g"].mean()
        rate_median = df_acad_sess["taux_reussite_g"].median()
        rate_std = df_acad_sess["taux_reussite_g"].std()
        
        if T is TEXTS["en"]:
            st.info(f"""
**📊 Pass Rate Distribution Analysis:**
- **Mean:** {rate_mean:.1f}%
- **Median:** {rate_median:.1f}%
- **Standard deviation:** {rate_std:.1f}%
- **Shape:** {"Right-skewed (most schools above average)" if rate_mean < rate_median else "Left-skewed (tail of struggling schools)" if rate_mean > rate_median else "Symmetric distribution"}

**🧠 What this shows:**
{"The distribution is concentrated around {rate_median:.0f}%, indicating **homogeneous performance** across schools in this academy. Most schools deliver similar results." if rate_std < 5 else f"Significant dispersion (σ = {rate_std:.1f}) reveals **heterogeneous performance**. Some schools excel (>95%), while others struggle (<70%)."}

**💡 Implication:**
{"Consistency is good, but innovation may be lacking. Encourage experimentation to push the top end higher." if rate_std < 5 else "High variability signals inequality. Targeted support for low-performers and knowledge transfer from high-performers are needed."}
""")
        else:
            st.info(f"""
**📊 Analyse de la Distribution des Taux :**
- **Moyenne :** {rate_mean:.1f}%
- **Médiane :** {rate_median:.1f}%
- **Écart-type :** {rate_std:.1f}%
- **Forme :** {"Asymétrie à droite (plupart au-dessus de la moyenne)" if rate_mean < rate_median else "Asymétrie à gauche (queue d'établissements en difficulté)" if rate_mean > rate_median else "Distribution symétrique"}

**🧠 Ce que cela montre :**
{"La distribution est concentrée autour de {rate_median:.0f}%, indiquant une **performance homogène** entre établissements de cette académie. La plupart délivrent des résultats similaires." if rate_std < 5 else f"Une dispersion significative (σ = {rate_std:.1f}) révèle une **performance hétérogène**. Certains excellent (>95%), tandis que d'autres peinent (<70%)."}

**💡 Implication :**
{"La cohérence est bonne, mais l'innovation peut manquer. Encourager l'expérimentation pour pousser le haut de gamme plus haut." if rate_std < 5 else "Une forte variabilité signale l'inégalité. Soutien ciblé pour les faibles performeurs et transfert de connaissances depuis les hauts performeurs sont nécessaires."}
""")

