# sections/intro.py
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.io import load_data
from utils.prep import clean_ivac, diff_columns_breakdown

LANG_TEXT = {
    # EN
"metric_delta_fmt": "{eng} added / {drop} dropped (net {net:+d})",

# FR
"metric_delta_fmt": "{eng} ajoutées / {drop} supprimées (net {net:+d})",
    "en": {
        "title": "🎓 IVAC – Measuring the True Impact of French Middle Schools",
        "hook1": (
            "Every year, more than **800,000 students** take the Diplôme National du Brevet (DNB). "
            "But beyond pass rates, **how can we know which schools truly help students progress?**"
        ),
        "hook2": (
            "The **Added Value Indicators of Middle Schools (IVAC)** published by the French Ministry of National Education "
            "aim to answer this question. They estimate how much a school *contributes* to student success after accounting "
            "for **prior level, age, and socio-economic background**."
        ),
        "def_va": (
            "> A high *added value* means a school helps its students perform **better than expected** compared to similar schools. "
            "A negative value may indicate challenges that limit student progress."
        ),
        "context_title": "🎯 Project Context & Research Question",
        "rq": "Which middle schools in France demonstrate the strongest **added value**, and what patterns explain these differences?",
        "goals": (
            "- Analyze **trends and inequalities** across regions and sessions (2022–2024)\n"
            "- Compare **public vs. private** institutions in terms of added value\n"
            "- Identify **top/bottom schools** to understand what drives success"
        ),
        "source": "Source: French Ministry of National Education - data.gouv.fr - Etalab 2.0 license",
        "prep_title": "🧹 Data Preparation Summary",
        "applied_steps": (
            "**Applied steps**:\n"
            "- Harmonization of column names and types\n"
            "- Standardization of numeric and categorical fields\n"
            "- Creation of derived indicators such as `valeur_ajoutee` (added value)\n"
            "- Aggregations by **academic region** and **exam session**\n\n"
            "These transformations ensure the data is clean, comparable, and ready for interactive analysis."
        ),
        "preview_title": "📋 Preview of the first 5 rows (standardized)",
        "checklist_title": "✅ Dataset Selection & Relevance Checklist",
        "checklist_table": (
            "| Criterion | Justification |\n"
            "|:--|:--|\n"
            "| **Relevance** | Education & school performance; linked to public policy. |\n"
            "| **Granularity** | By session (time) and academy/department (geography). |\n"
            "| **Quality & Metadata** | Official open dataset with documentation; Etalab 2.0 license. |\n"
            "| **Audience** | Educators, policymakers, researchers, parents. |\n"
            "| **Size & Usability** | ~20,000 rows; manageable locally for interactive analysis. |"
        ),
        "narrative_title": "🧭 Narrative Design",
        "narrative": (
            "We follow a **Comparative & Ranking** pattern:\n"
            "1. **Data Quality & Profiling** -> assess reliability and completeness\n"
            "2. **Visualization & Analysis** -> compare regions/sectors and highlight inequalities\n"
            "3. **Deep Dives** -> detect outliers and top/bottom schools\n"
            "4. **Conclusions** -> insights, implications, recommendations"
        ),
        "next": "🧩 **Next step:** go to **Data Quality & Profiling** to validate key indicators before analysis.",
        "metric_rows": "Rows",
        "metric_cols": "Columns",
        "metric_dups": "Duplicate rows",
        "metric_academies": "Unique academies",
        "metric_schools": "Unique schools",
        "language": "Language",
        "en": "English",
        "fr": "Français",
        "std_note": "🧩 *Standardized* means the raw IVAC data has been cleaned and harmonized (column names, types, missing values) so it is comparable across schools and regions.",
        # donut / details
        "donut_title": "Column structure (before/after cleaning)",
        "donut_kept": "Kept/Renamed",
        "donut_added": "Added (engineered)",
        "donut_dropped": "Dropped",
        "eng_cols_caption": "🧩 **Engineered columns added:**",
        "renamed_expander": "🔄 Show renamed columns (raw -> cleaned)",
        "no_renamed": "No renamed columns detected.",
        "dropped_caption": "🗑️ Dropped columns:",
    },
    "fr": {
        "title": "🎓 IVAC – Mesurer l’impact réel des collèges en France",
        "hook1": (
            "Chaque année, plus de **800 000 élèves** passent le Diplôme National du Brevet (DNB). "
            "Mais au-delà du taux de réussite, **comment savoir quels collèges font réellement progresser leurs élèves ?**"
        ),
        "hook2": (
            "Les **Indicateurs de Valeur Ajoutée des Collèges (IVAC)**, publiés par le Ministère de l’Éducation nationale, "
            "cherchent à répondre à cette question. Ils estiment la part de réussite *attribuable au collège* en neutralisant "
            "le **niveau antérieur, l’âge et le contexte socio-économique** des élèves."
        ),
        "def_va": (
            "> Une *valeur ajoutée* élevée signifie qu’un collège fait réussir ses élèves **mieux qu’attendu** "
            "par rapport à des établissements comparables. Une valeur négative peut révéler des difficultés structurelles."
        ),
        "context_title": "🎯 Contexte & Question de recherche",
        "rq": "Quels collèges en France présentent la plus forte **valeur ajoutée**, et quels schémas expliquent ces écarts ?",
        "goals": (
            "- Analyser les **tendances et inégalités** entre académies et sessions (2022–2024)\n"
            "- Comparer **secteur public vs privé** en termes de valeur ajoutée\n"
            "- Identifier les **meilleurs/moins bons collèges** pour comprendre les facteurs de succès"
        ),
        "source": "Source : Ministère de l’Éducation nationale - data.gouv.fr - Licence Etalab 2.0",
        "prep_title": "🧹 Synthèse de la préparation des données",
        "applied_steps": (
            "**Étapes appliquées** :\n"
            "- Harmonisation des noms de colonnes et des types\n"
            "- Standardisation des variables numériques et catégorielles\n"
            "- Création d’indicateurs dérivés comme `valeur_ajoutee`\n"
            "- Agrégations par **région académique** et **session**\n\n"
            "Ces transformations garantissent des comparaisons fiables et reproductibles."
        ),
        "preview_title": "📋 Aperçu des 5 premières lignes (standardisées)",
        "checklist_title": "✅ Checklist - Choix du jeu de données",
        "checklist_table": (
            "| Critère | Justification |\n"
            "|:--|:--|\n"
            "| **Pertinence** | Éducation & performance scolaire ; utile pour l’action publique. |\n"
            "| **Granularité** | Par session (temps) et académie/département (géo). |\n"
            "| **Qualité & Métadonnées** | Open data officielle documentée ; licence Etalab 2.0. |\n"
            "| **Public** | Équipe éducative, décideurs, chercheurs, parents. |\n"
            "| **Taille & usage** | ~20 000 lignes ; exploitable localement en mode interactif. |"
        ),
        "narrative_title": "🧭 Trame narrative",
        "narrative": (
            "Nous suivons un schéma **Comparaisons & Classements** :\n"
            "1. **Data Quality & Profiling** -> fiabilité et complétude\n"
            "2. **Visualization & Analysis** -> comparaisons régions/secteurs et inégalités\n"
            "3. **Deep Dives** -> détection d’outliers et top/bottom\n"
            "4. **Conclusions** -> enseignements, implications, recommandations"
        ),
        "next": "🧩 **Étape suivante :** ouvrir **Data Quality & Profiling** pour valider les indicateurs clés avant l’analyse.",
        "metric_rows": "Lignes",
        "metric_cols": "Colonnes",
        "metric_dups": "Doublons",
        "metric_academies": "Académies uniques",
        "metric_schools": "Collèges uniques",
        "language": "Langue",
        "en": "English",
        "fr": "Français",
        "std_note": "🧩 *Standardisé* signifie que les données IVAC brutes ont été nettoyées et harmonisées (noms de colonnes, types, valeurs manquantes) pour être comparables entre collèges et régions.",
        # donut / détails
        "donut_title": "Structure des colonnes (avant/après nettoyage)",
        "donut_kept": "Conservées/Renommées",
        "donut_added": "Ajoutées (engineered)",
        "donut_dropped": "Supprimées",
        "eng_cols_caption": "🧩 **Colonnes dérivées ajoutées :**",
        "renamed_expander": "🔄 Voir les colonnes renommées (raw -> cleaned)",
        "no_renamed": "Aucune colonne renommée détectée.",
        "dropped_caption": "🗑️ Colonnes supprimées :",
    },
}

def _get_lang() -> str:
    lang = st.query_params.get("lang", "en")
    return lang if lang in ("en", "fr") else "en"

def _set_lang(lang: str):
    st.query_params["lang"] = lang
def show():
    current_lang = _get_lang()
    st.sidebar.subheader(LANG_TEXT[current_lang].get("language", "Language"))
    choice = st.sidebar.radio(
        label=" ",
        options=["en", "fr"],
        format_func=lambda x: LANG_TEXT[x].get(x, x.title()),
        horizontal=True,
        key="lang_selector_intro",
        label_visibility="collapsed",
    )
    if choice and choice != current_lang:
        _set_lang(choice)
        st.rerun()
    T = LANG_TEXT.get(choice or current_lang, LANG_TEXT["en"])

    st.title(T.get("title", "IVAC – Added Value Indicators"))
    st.markdown(f"{T.get('hook1','')}\n\n{T.get('hook2','')}")
    if T.get("def_va"):
        st.info(T["def_va"])
    
    # Storyboard simple
    st.markdown("### 🗺️ Navigation Guide")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**1️⃣ Intro**<br>Context & Data", unsafe_allow_html=True)
    with col2:
        st.markdown("**2️⃣ Data Quality**<br>Validation & Cleaning", unsafe_allow_html=True)
    with col3:
        st.markdown("**3️⃣ Overview**<br>KPIs & Trends", unsafe_allow_html=True)
    with col4:
        st.markdown("**4️⃣ Deep Dives**<br>School Analysis", unsafe_allow_html=True)
    with col5:
        st.markdown("**5️⃣ Conclusions**<br>Insights & Actions", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call-to-action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Explore the Data Now ->", use_container_width=True, type="primary"):
            st.query_params["page"] = "Overview & Analysis"
            st.rerun()

    # question contexte
    with st.expander("📖 Learn More About the Project Context", expanded=False):
        if T.get("context_title"):
            st.subheader(T["context_title"])
        rq = T.get("rq", "")
        goals = T.get("goals", "")
        if rq or goals:
            st.markdown(f"> **{rq}**\n\n{goals}")
        if T.get("source"):
            st.caption(T["source"])

    # 
    if T.get("prep_title"):
        st.subheader(T["prep_title"])

    # Load / clean / diff with error handling
    try:
        df_raw = load_data()
        df_clean = clean_ivac(df_raw)
        diff = diff_columns_breakdown(df_raw, df_clean)
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        st.stop()

    #  KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(T.get("metric_rows", "Rows"), f"{df_raw.shape[0]:,}".replace(",", " "))

    engineered_count = len(diff.get("engineered", []))
    dropped_count    = len(diff.get("dropped", []))
    net_delta        = engineered_count - dropped_count

    delta_fmt = T.get(
        "metric_delta_fmt",
        "{eng} added / {drop} dropped (net {net:+d})"
    )
    c2.metric(
        f"{T.get('metric_cols','Columns')} (raw -> cleaned)",
        f"{df_raw.shape[1]} -> {df_clean.shape[1]}",
        delta=delta_fmt.format(eng=engineered_count, drop=dropped_count, net=net_delta),
    )

    c3.metric(T.get("metric_dups", "Duplicates"), str(df_raw.duplicated().sum()))

    n_academies = df_clean["region_academique"].nunique() if "region_academique" in df_clean.columns else "N/A"
    n_schools   = df_clean["uai"].nunique() if "uai" in df_clean.columns else "N/A"
    c4.metric(T.get("metric_academies", "Academic regions"), n_academies)
    c5.metric(T.get("metric_schools", "Unique schools (UAI)"), n_schools)
    st.caption("Counts computed on the cleaned dataset (all sessions combined).")
    raw_cols_count = df_raw.shape[1]
    kept_or_renamed_count = max(raw_cols_count - dropped_count, 0)

    donut_df = pd.DataFrame({
        "Category": [
            T.get("donut_kept", "Kept/Renamed"),
            T.get("donut_added", "Added (engineered)"),
            T.get("donut_dropped", "Dropped"),
        ],
        "Count": [kept_or_renamed_count, engineered_count, dropped_count],
    })
    fig = px.pie(
        donut_df, values="Count", names="Category",
        title=T.get("donut_title", "Column structure after cleaning"),
        hole=0.4
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "> **Legend** - *Kept/Renamed*: original columns kept or renamed · "
        "*Added (engineered)*: columns created during cleaning (e.g., `valeur_ajoutee`, `row_id`) · "
        "*Dropped*: columns removed (duplicates, replaced, or irrelevant)."
    )
    

    if df_clean.shape[0] != df_raw.shape[0]:
        st.warning(f"⚠️ Row count changed during cleaning: {df_raw.shape[0]} -> {df_clean.shape[0]}")
    
    missing_cols = [col for col in ["valeur_ajoutee", "nb_candidats_total", "row_id"] if col not in df_clean.columns]
    if missing_cols:
        st.warning(f"⚠️ Expected columns missing after cleaning: {', '.join(missing_cols)}")
    
    # ---- Details on changes
    if diff.get("engineered"):
        st.caption(f"{T.get('eng_cols_caption','Engineered columns added:')} {', '.join(diff['engineered'])}")

    with st.expander(T.get("renamed_expander", "Show renamed columns (raw -> cleaned)")):
        renamed_data = diff.get("renamed", [])
        if renamed_data:
            st.dataframe(
                pd.DataFrame(renamed_data, columns=["Raw Name", "Clean Name"]),
                use_container_width=True,
            )
        else:
            st.write(T.get("no_renamed", "No renamed columns detected."))

    if diff.get("dropped"):
        st.caption(f"{T.get('dropped_caption','Dropped columns:')} {', '.join(diff['dropped'])}")

    
    if T.get("applied_steps"):
        st.markdown(T["applied_steps"])

    # ---- Preview
    if T.get("preview_title"):
        st.subheader(T["preview_title"])
    st.dataframe(df_clean.head(), use_container_width=True)
    if T.get("std_note"):
        st.caption(T["std_note"])

    # ---- Checklist & narrative
    if T.get("checklist_title"):
        st.subheader(T["checklist_title"])
    if T.get("checklist_table"):
        st.markdown(T["checklist_table"])

    if T.get("narrative_title"):
        st.subheader(T["narrative_title"])
    if T.get("narrative"):
        st.markdown(T["narrative"])

    # ---- Next
    if T.get("next"):
        st.info(T["next"])