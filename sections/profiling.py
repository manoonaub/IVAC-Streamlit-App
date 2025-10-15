# sections/profiling.py
import streamlit as st
import pandas as pd
import numpy as np

from utils.io import load_data
from utils.prep import (
    clean_ivac, info_table, validity_checks,
    impute_numeric, impute_categorical,
    drop_exact_duplicates, drop_key_duplicates
)

TEXTS = {
    "en": {
        "language": "Language", "en": "English", "fr": "Français",
        "title": "📊 Data Quality & Profiling",
        "intro": "This section validates the dataset before analysis: schema, missingness, validity, outliers, and quick distributions.",

        # KPIs
        "kpi_rows": "Rows",
        "kpi_cols": "Columns (raw → cleaned)",
        "kpi_dups": "Duplicate rows (raw)",
        "kpi_uai": "Unique schools (UAI)",
        "badge_label": "↑ {added} added / {dropped} dropped (net {net:+d})",

        # Donut
        "donut_title": "Column structure (before/after cleaning)",
        "donut_kept": "Kept/Renamed",
        "donut_added": "Added (engineered)",
        "donut_dropped": "Dropped",
        "eng_cols_caption": "Engineered columns added:",
        "renamed_expander": "Show renamed columns (raw → cleaned)",
        "no_renamed": "No renamed columns detected.",
        "dropped_caption": "Dropped columns:",

        # Schema
        "schema_only_title": "🧬 Schema (standardized)",
        "schema_legend": "_Legend_: **Dtype** = inferred type; **Null_Pct** = missing share per column.",

        # Missingness
        "missing_title": "🕳️ Missing values (by column)",
        "missing_top": "Most incomplete columns",
        "missing_legend": "Columns with **_p** suffix belong to the vocational track — higher missingness is expected.",
        "missing_none": "No missing values detected in the standardized frame.",

        # Validity
        "valid_title": "⚠️ Validity checks",
        "valid_ok": "✅ No data validity issues detected.",
        "valid_warn": "⚠️ {n} potential issue(s) detected.",
        "valid_expander": "Show samples of invalid records",

        # Advanced validity
        "adv_valid_title": "🧪 Advanced business checks",
        "adv_valid_note": "Additional sanity checks (bounds, logic, identifiers).",

        # Cross-validation
        "cross_title": "🔁 Cross-column consistency",
        "cross_note": "Checks relationships across columns (sums, formats).",

        # Outliers
        "outliers_title": "🚨 Outlier detection",
        "outliers_note": "Flag extreme observations (IQR) for key metrics.",
        "box_title": "Distribution of value added by sector (box plot)",

        # Quality score & alerts
        "quality_title": "🏆 Data Quality Score",
        "alerts_title": "🔔 Quality alerts",
        "alerts_none": "No alerts — the dataset looks healthy.",
        "alert_missing": "⚠️ {col}: {pct:.1f}% missing",
        "alert_dups": "🔴 {pct:.1f}% of duplicate rows detected",

        # Preview
        "preview_title": "🧾 Cleaned data preview (filterable)",
        "filter_session": "Session",
        "filter_region": "Academic region",
        "filter_sector": "Sector",
        "filter_rows": "Rows to display",
        "filtered_rows": "Rows after filtering: **{n}**",
        "preview_note": "This preview reflects the standardized frame (before sandbox operations).",
        "download_btn": "Download filtered CSV",

        # Sandbox
        "sandbox_title": "🧼 Interactive cleaning (apply & preview)",
        "sandbox_note": "Experiment safely with imputations & deduplication. Source data remains unchanged.",
        "imp_num": "Impute numeric columns with:",
        "imp_none": "Do not impute",
        "imp_cat": "Impute categorical columns with the mode",
        "group_by": "Group-wise imputation by:",
        "group_none": "No grouping",
        "drop_exact": "Drop exact duplicate rows",
        "drop_key": "Drop duplicates by key (UAI, Session)",
        "apply_btn": "Apply cleaning steps",
        "applied_ok": "Actions applied. NA cells handled: {fixed}. Rows: {before} → {after} (change {after_minus_before:+d}).",
        "save_btn": "Save preview (session)",
        "reset_btn": "Reset preview",
        "save_ok": "Saved to session (key: ivac_cleaned_preview).",
        "reset_ok": "Preview reset.",
        "sandbox_legend": "Operations are ephemeral (kept only in the current app session).",

        # Distributions
        "quick_title": "Quick distributions (post-cleaning preview)",
        "dist_va": "Value Added (success rate)",
        "dist_total": "Total candidates",
        "dist_insufficient": "Not enough numeric data in **{label}** to draw a histogram.",
        "dist_legend": "Histograms computed on the current preview (filters & sandbox applied).",

        # Report
        "report_btn": "📄 Download quality report (CSV)",

        # Green card
        "edu_goal": (
            "🎯 <b>Goal:</b> visualize the distribution of school performance (value added) "
            "and typical school size (total candidates)."
        ),
    },
    "fr": {
        "language": "Langue", "en": "English", "fr": "Français",
        "title": "📊 Qualité & Profilage des données",
        "intro": "Cette section valide le jeu de données avant l’analyse : schéma, valeurs manquantes, validité, outliers et distributions rapides.",

        # KPIs
        "kpi_rows": "Lignes",
        "kpi_cols": "Colonnes (brut → nettoyé)",
        "kpi_dups": "Doublons (brut)",
        "kpi_uai": "Collèges uniques (UAI)",
        "badge_label": "↑ {added} ajoutées / {dropped} supprimées (net {net:+d})",

        # Donut
        "donut_title": "Structure des colonnes (avant/après nettoyage)",
        "donut_kept": "Conservées/Renom.",
        "donut_added": "Ajoutées (engineered)",
        "donut_dropped": "Supprimées",
        "eng_cols_caption": "Colonnes dérivées ajoutées :",
        "renamed_expander": "Afficher les colonnes renommées (brut → nettoyé)",
        "no_renamed": "Aucune colonne renommée détectée.",
        "dropped_caption": "Colonnes supprimées :",

        # Schema
        "schema_only_title": "🧬 Schéma (standardisé)",
        "schema_legend": "_Légende_ : **Dtype** = type inféré ; **Null_Pct** = part de manquants par colonne.",

        # Missingness
        "missing_title": "🕳️ Valeurs manquantes (par colonne)",
        "missing_top": "Colonnes les plus incomplètes",
        "missing_legend": "Les colonnes en **_p** appartiennent à la voie pro — un taux élevé de manquants est attendu.",
        "missing_none": "Aucune valeur manquante détectée dans le tableau standardisé.",

        # Validity
        "valid_title": "⚠️ Contrôles de validité",
        "valid_ok": "✅ Aucun problème de validité détecté.",
        "valid_warn": "⚠️ {n} anomalie(s) potentielle(s) détectée(s).",
        "valid_expander": "Afficher des exemples de lignes invalides",

        # Advanced validity
        "adv_valid_title": "🧪 Contrôles métier avancés",
        "adv_valid_note": "Vérifications supplémentaires (bornes, logique, identifiants).",

        # Cross-validation
        "cross_title": "🔁 Cohérence inter-colonnes",
        "cross_note": "Vérifie les relations entre colonnes (sommes, formats).",

        # Outliers
        "outliers_title": "🚨 Détection d'outliers",
        "outliers_note": "Repère les observations extrêmes (IQR) sur les métriques clés.",
        "box_title": "Distribution de la valeur ajoutée par secteur (box plot)",

        # Quality score & alerts
        "quality_title": "🏆 Score global de qualité",
        "alerts_title": "🔔 Alertes qualité",
        "alerts_none": "Aucune alerte — le jeu semble sain.",
        "alert_missing": "⚠️ {col} : {pct:.1f}% manquant",
        "alert_dups": "🔴 {pct:.1f}% de doublons détectés",

        # Preview
        "preview_title": "🧾 Aperçu des données nettoyées (filtrable)",
        "filter_session": "Session",
        "filter_region": "Région académique",
        "filter_sector": "Secteur",
        "filter_rows": "Lignes à afficher",
        "filtered_rows": "Lignes après filtres : **{n}**",
        "preview_note": "Cet aperçu reflète le cadre standardisé (avant la sandbox).",
        "download_btn": "Télécharger le CSV filtré",

        # Sandbox
        "sandbox_title": "🧼 Nettoyage interactif (appliquer & prévisualiser)",
        "sandbox_note": "Testez en sécurité les imputations & la déduplication. La source n’est pas modifiée.",
        "imp_num": "Imputer les numériques avec :",
        "imp_none": "Ne pas imputer",
        "imp_cat": "Imputer les catégorielles avec la modalité la plus fréquente",
        "group_by": "Imputation par groupe :",
        "group_none": "Sans regroupement",
        "drop_exact": "Supprimer les doublons exacts",
        "drop_key": "Supprimer les doublons par clé (UAI, Session)",
        "apply_btn": "Appliquer le nettoyage",
        "applied_ok": "Actions appliquées. Cellules manquantes traitées : {fixed}. Lignes : {before} → {after} (variation {after_minus_before:+d}).",
        "save_btn": "Sauvegarder l’aperçu (session)",
        "reset_btn": "Réinitialiser l’aperçu",
        "save_ok": "Sauvegardé en session (clé : ivac_cleaned_preview).",
        "reset_ok": "Aperçu réinitialisé.",
        "sandbox_legend": "Opérations éphémères (valables dans la session de l’app).",

        # Distributions
        "quick_title": "Distributions rapides (aperçu post-nettoyage)",
        "dist_va": "Valeur ajoutée (taux de réussite)",
        "dist_total": "Total candidats",
        "dist_insufficient": "Données insuffisantes dans **{label}** pour tracer un histogramme.",
        "dist_legend": "Histogrammes calculés sur l’aperçu courant (filtres & sandbox appliqués).",

        # Report
        "report_btn": "📄 Télécharger le rapport qualité (CSV)",

        # Green card
        "edu_goal": (
            "🎯 <b>Objectif :</b> visualiser la répartition des performances (valeur ajoutée) "
            "et la taille typique des collèges (total candidats)."
        ),
    },
}

def _get_lang():
    try:
        return st.query_params.get("lang", "en") if st.query_params.get("lang", "en") in ("en", "fr") else "en"
    except Exception:
        return "en"

def _set_lang(v: str):
    try:
        st.query_params["lang"] = v
    except Exception:
        pass

def _green_badge(text: str):
    st.markdown(
        f"""<span style="
            display:inline-block;
            background:#173d2b;
            color:#a5e7c1;
            border:1px solid #1f6f45;
            padding:.25rem .6rem;
            border-radius:.9rem;
            font-size:.9rem;
            ">
            {text}
        </span>""",
        unsafe_allow_html=True,
    )


def advanced_validity_checks(df: pd.DataFrame) -> dict:
    """Contrôles métier supplémentaires (bornes, logique, formats)."""
    issues = {}
    d = df.copy()

    if "taux_reussite_g" in d.columns:
        bad = d["taux_reussite_g"].apply(pd.to_numeric, errors="coerce")
        mask = (bad < 0) | (bad > 100)
        issues["invalid_success_rate_g"] = d.loc[mask]

    if "valeur_ajoutee" in d.columns:
        va = d["valeur_ajoutee"].apply(pd.to_numeric, errors="coerce").abs() > 50
        issues["extreme_value_added_(>|50|)"] = d.loc[va]

    if {"nb_candidats_total", "taux_reussite_g"}.issubset(d.columns):
        tot = pd.to_numeric(d["nb_candidats_total"], errors="coerce").fillna(0)
        mask = (tot == 0) & d["taux_reussite_g"].notna()
        issues["logic_zero_candidates_but_rate"] = d.loc[mask]

    if "uai" in d.columns:
        mask = ~d["uai"].astype(str).str.match(r"^[0-9]{7}[A-Z]$", na=False)
        issues["invalid_uai_format"] = d.loc[mask]

    return {k: v for k, v in issues.items() if len(v) > 0}

def cross_validation_checks(df: pd.DataFrame) -> dict:
    """Cohérence inter-colonnes (somme candidats, format session...)."""
    issues = {}
    d = df.copy()

    if {"nb_candidats_g", "nb_candidats_p", "nb_candidats_total"}.issubset(d.columns):
        g = pd.to_numeric(d["nb_candidats_g"], errors="coerce").fillna(0)
        p = pd.to_numeric(d["nb_candidats_p"], errors="coerce").fillna(0)
        t = pd.to_numeric(d["nb_candidats_total"], errors="coerce").fillna(0)
        mask = (g + p) != t
        issues["total_candidates_mismatch"] = d.loc[mask]

    if "session" in d.columns:
        mask = ~d["session"].astype(str).str.match(r"^20\d{2}$", na=False)
        issues["invalid_session_format"] = d.loc[mask]

    return {k: v for k, v in issues.items() if len(v) > 0}

def detect_outliers_mask(series: pd.Series, method: str = "iqr") -> pd.Series:
    """Renvoie un masque booléen (aligné à l'index) d'outliers via IQR ou Z-score."""
    s = pd.to_numeric(series, errors="coerce")
    mask = pd.Series(False, index=s.index)
    s_valid = s.dropna()
    if s_valid.empty:
        return mask
    if method == "iqr":
        q1, q3 = s_valid.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask.loc[s.notna()] = (s_valid < lower) | (s_valid > upper)
    elif method == "zscore":
        from scipy import stats  
        z = np.abs(stats.zscore(s_valid))
        mask.loc[s.notna()] = z > 3
    return mask

def calculate_quality_score(df: pd.DataFrame) -> float:
    """Score global (0-100) combinant complétude, unicité, validité, cohérence."""
    if len(df) == 0:
        return 0.0

    # Completeness
    completeness = (1 - df.isna().sum().sum() / df.size) * 100

    # Uniqueness (%) sur uai si dispo, sinon 100%
    uniqueness = (df["uai"].nunique() / len(df) * 100) if "uai" in df.columns else 100.0

    # Validity
    invalid_idx = set()
    base_val = validity_checks(df)
    for fr in base_val["frames"].values():
        invalid_idx.update(fr.index.tolist())
    adv = advanced_validity_checks(df)
    for fr in adv.values():
        invalid_idx.update(fr.index.tolist())
    cross = cross_validation_checks(df)
    for fr in cross.values():
        invalid_idx.update(fr.index.tolist())
    validity = 100 * (1 - (len(invalid_idx) / len(df)))

    # Consistency
    if {"uai", "session"}.issubset(df.columns):
        dup_pct = (df.duplicated(subset=["uai", "session"]).sum() / len(df)) * 100
        consistency = max(0.0, 100 - dup_pct)
    else:
        consistency = 100.0

    weights = {"completeness": 0.30, "uniqueness": 0.20, "validity": 0.30, "consistency": 0.20}
    score = (
        completeness * weights["completeness"] +
        uniqueness   * weights["uniqueness"]   +
        validity     * weights["validity"]     +
        consistency  * weights["consistency"]
    )
    return round(float(score), 1)

def quality_alerts(df: pd.DataFrame, T: dict) -> list[str]:
    """Alerte sur manquants importants et doublons élevés."""
    alerts = []
    for col in ["valeur_ajoutee", "taux_reussite_g"]:
        if col in df.columns:
            pct = (df[col].isna().sum() / len(df)) * 100
            if pct > 30:
                alerts.append(T["alert_missing"].format(col=col, pct=pct))
    dup_pct = (df.duplicated().sum() / len(df)) * 100
    if dup_pct > 5:
        alerts.append(T["alert_dups"].format(pct=dup_pct))
    return alerts


try:
    from sklearn.impute import KNNImputer
    HAS_SK = True
except Exception:
    HAS_SK = False

def impute_by_group(df: pd.DataFrame, col: str, group_by: str) -> pd.DataFrame:
    """Impute col avec la médiane par groupe (ex: par académie)."""
    d = df.copy()
    if group_by in d.columns and col in d.columns:
        d[col] = d.groupby(group_by)[col].transform(lambda x: x.fillna(x.median()))
    return d

def apply_imputation(df: pd.DataFrame, num_cols: list[str], strategy: str, group_by: str | None):
    """Applique diverses stratégies d'imputation sur num_cols."""
    d = df.copy()
    if not num_cols:
        return d

    if group_by and group_by in d.columns and strategy in {"median", "mean"}:
        # Imputation par groupe 
        for c in num_cols:
            d = impute_by_group(d, c, group_by)
        return d

    if strategy in {"median", "mean"}:
        return impute_numeric(d, num_cols, strategy=strategy)

    if strategy == "mode":
        # Appliquer le mode numérique via impute_categorical 
        for c in num_cols:
            mode_val = pd.to_numeric(d[c], errors="coerce").mode()
            if not mode_val.empty:
                d[c] = pd.to_numeric(d[c], errors="coerce").fillna(mode_val.iloc[0])
        return d

    if strategy == "ffill":
        return d.sort_index().fillna(method="ffill")

    if strategy == "bfill":
        return d.sort_index().fillna(method="bfill")

    if strategy == "knn" and HAS_SK:
        # Imputation KNN sur les colonnes numériques sélectionnées
        work = d[num_cols].apply(pd.to_numeric, errors="coerce")
        imputer = KNNImputer(n_neighbors=5, weights="distance")
        imputed = imputer.fit_transform(work)
        d[num_cols] = imputed
        return d

    # Si stratégie non reconnue / indisponible (ex: knn sans sklearn)
    return d


def show():
    current = _get_lang()
    st.sidebar.subheader(TEXTS[current]["language"])
    choice = st.sidebar.radio(
        label=" ",
        options=["en", "fr"],
        format_func=lambda x: TEXTS[x][x],
        key="lang_selector_prof",
        horizontal=True,
        label_visibility="collapsed",
    )
    if choice != current:
        _set_lang(choice)
        st.rerun()
    T = TEXTS[choice]

    st.header(T["title"])
    st.markdown(T["intro"])

    #  Load + clean baseline
    df_raw = load_data()
    df_base = clean_ivac(df_raw)
    rows_raw, cols_raw = df_raw.shape
    rows_clean, cols_clean = df_base.shape


    def _to_snake(s: str) -> str:
        import re as _re
        s = str(s).strip().lower()
        s = (s.replace("é", "e").replace("è", "e").replace("ê","e")
               .replace("à","a").replace("ç","c"))
        s = _re.sub(r"[^a-z0-9]+", "_", s)
        s = _re.sub(r"_+", "_", s).strip("_")
        return s

    raw_norm = {_to_snake(c): c for c in df_raw.columns}
    added = [c for c in df_base.columns if c not in raw_norm]
    dropped = [c for c in df_raw.columns if _to_snake(c) not in set(df_base.columns)]
    renamed = [(raw_norm[c], c) for c in df_base.columns if c in raw_norm and raw_norm[c] != c]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(T["kpi_rows"], f"{rows_raw:,}".replace(",", " "))
    with c2:
        st.metric(T["kpi_cols"], f"{cols_raw} → {cols_clean}")
        _green_badge(T["badge_label"].format(added=len(added), dropped=len(dropped), net=cols_clean - cols_raw))
    c3.metric(T["kpi_dups"], f"{int(df_raw.duplicated().sum())}")
    c4.metric(T["kpi_uai"], str(df_base["uai"].nunique()) if "uai" in df_base.columns else "N/A")
   
    # Donut colonne
    import plotly.express as px
    kept_count = max(cols_clean - len(added), 0)
    donut_df = pd.DataFrame({
        "Category": [T["donut_kept"], T["donut_added"], T["donut_dropped"]],
        "Count": [kept_count, len(added), len(dropped)],
    })
    fig = px.pie(donut_df, values="Count", names="Category",
                 title=T["donut_title"], hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

    if added:
        st.caption(f"{T['eng_cols_caption']} {', '.join(added)}")
    with st.expander(T["renamed_expander"]):
        if renamed:
            st.dataframe(pd.DataFrame(renamed, columns=["Raw Name", "Clean Name"]), use_container_width=True)
        else:
            st.write(T["no_renamed"])
    if dropped:
        st.caption(f"{T['dropped_caption']} {', '.join(dropped)}")

    st.divider()

    #  Schema (types & non-null)
    st.subheader(T["schema_only_title"])
    schema = info_table(df_base)[["Non-Null Count", "Null Count", "Dtype", "Null_Pct"]]
    st.dataframe(schema, use_container_width=True)
    st.caption(T["schema_legend"])

    st.divider()

    #  Missingness
    st.subheader(T["missing_title"])
    missing_pct = schema["Null_Pct"].sort_values(ascending=False)
    worst = missing_pct[missing_pct > 0].head(5)
    if not worst.empty:
        bullets = ", ".join([f"`{col}` : {val:.1f}%" for col, val in worst.items()])
        st.markdown("**" + T["missing_top"] + ":** " + bullets)
    st.bar_chart(missing_pct.rename("% missing"))
    st.caption(T["missing_legend"])

    st.divider()

    # Validity (
    st.subheader(T["valid_title"])
    base_checks = validity_checks(df_raw)
    total_issues = sum(base_checks["summary"].values())
    if total_issues == 0:
        st.success(T["valid_ok"])
    else:
        st.warning(T["valid_warn"].format(n=total_issues))
        with st.expander(T["valid_expander"]):
            for name, frame in base_checks["frames"].items():
                if len(frame) > 0:
                    st.markdown(f"**{name}** — {len(frame)}")
                    st.dataframe(frame.head(10), use_container_width=True)

    st.subheader(T["adv_valid_title"])
    st.caption(T["adv_valid_note"])
    adv = advanced_validity_checks(df_base)
    if len(adv) == 0:
        st.success(T["valid_ok"])
    else:
        st.warning(T["valid_warn"].format(n=sum(len(v) for v in adv.values())))
        with st.expander(T["valid_expander"]):
            for name, frame in adv.items():
                st.markdown(f"**{name}** — {len(frame)}")
                st.dataframe(frame.head(10), use_container_width=True)

    st.subheader(T["cross_title"])
    st.caption(T["cross_note"])
    cross = cross_validation_checks(df_base)
    if len(cross) == 0:
        st.success(T["valid_ok"])
    else:
        st.warning(T["valid_warn"].format(n=sum(len(v) for v in cross.values())))
        with st.expander(T["valid_expander"]):
            for name, frame in cross.items():
                st.markdown(f"**{name}** — {len(frame)}")
                st.dataframe(frame.head(10), use_container_width=True)

    st.divider()

    
    st.subheader(T["quality_title"])
    score = calculate_quality_score(df_base)
    st.metric(T["quality_title"], f"{score}/100")
    alerts = quality_alerts(df_base, T)
    if alerts:
        st.subheader(T["alerts_title"])
        for a in alerts:
            st.warning(a)
    else:
        st.subheader(T["alerts_title"])
        st.info(T["alerts_none"])

    st.divider()

    
    st.subheader(T["preview_title"])
    colf1, colf2, colf3, colf4 = st.columns(4)
    sessions = sorted(df_base["session"].dropna().unique().tolist()) if "session" in df_base.columns else []
    regions  = sorted(df_base["region_academique"].dropna().unique().tolist()) if "region_academique" in df_base.columns else []
    sectors  = sorted(df_base["secteur"].dropna().unique().tolist()) if "secteur" in df_base.columns else []

    sel_session = colf1.multiselect(T["filter_session"], sessions, default=sessions[:1] if sessions else [])
    sel_region  = colf2.multiselect(T["filter_region"], regions)
    sel_sector  = colf3.multiselect(T["filter_sector"], sectors)
    sample_n    = colf4.slider(T["filter_rows"], min_value=50, max_value=500, value=200, step=50)

    df_view = df_base.copy()
    if sel_session: df_view = df_view[df_view["session"].isin(sel_session)]
    if sel_region:  df_view = df_view[df_view["region_academique"].isin(sel_region)]
    if sel_sector:  df_view = df_view[df_view["secteur"].isin(sel_sector)]

    st.caption(T["filtered_rows"].format(n=f"{len(df_view):,}".replace(",", " ")))
    st.dataframe(df_view.head(sample_n), use_container_width=True)
    st.caption(T["preview_note"])

    csv_bytes = df_view.to_csv(index=False).encode("utf-8")
    st.download_button(T["download_btn"], data=csv_bytes, file_name="ivac_filtered.csv", mime="text/csv")

    st.divider()

    
    st.subheader(T["outliers_title"])
    st.caption(T["outliers_note"])
    cols_to_flag = [c for c in ["valeur_ajoutee", "nb_candidats_total", "taux_reussite_g"] if c in df_view.columns]
    if cols_to_flag:
        cA, cB, cC = st.columns(3)
        slots = [cA, cB, cC]
        for i, col in enumerate(cols_to_flag):
            mask = detect_outliers_mask(df_view[col], method="iqr")
            pct = (mask.sum() / len(df_view) * 100) if len(df_view) else 0
            slots[i].metric(f"{col}", f"{int(mask.sum())} ({pct:.1f}%)")

    st.divider()

    
    st.subheader(T["quick_title"])
    st.markdown(
        f"""
        <div style="
            background-color:#10351c;
            border:1px solid #1f6f45;
            color:#a5e7c1;
            padding:0.8rem 1rem;
            border-radius:0.6rem;
            margin-bottom:1rem;">
            {TEXTS[choice]["edu_goal"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    def plot_hist(series: pd.Series, label: str, bins: int = 30):
        import plotly.express as px
        s = pd.to_numeric(series, errors="coerce").dropna()
        if len(s) < 5 or s.nunique() < 2:
            st.info(T["dist_insufficient"].format(label=label))
            return
        fig = px.histogram(s, nbins=bins, title=label)
        fig.update_layout(height=330, bargap=0.03)
        st.plotly_chart(fig, use_container_width=True)

    cols = st.columns(2)
    with cols[0]:
        if "valeur_ajoutee" in df_view.columns:
            plot_hist(df_view["valeur_ajoutee"], T["dist_va"])
    with cols[1]:
        if "nb_candidats_total" in df_view.columns:
            plot_hist(df_view["nb_candidats_total"], T["dist_total"])

    st.caption(T["dist_legend"])

    
    if choice == "fr":
        st.markdown("""
        **📈 Valeur ajoutée (taux de réussite)**  
        - Mesure la performance réelle du collège (contexte neutralisé).  
        - **≈ 0** = conforme aux attentes ; **> 0** = surperformance ; **< 0** = sous-performance.

        **🧮 Total candidats**  
        - Nombre d'élèves présentés par collège.  
        - La majorité entre **80–150** → collèges de taille moyenne ; quelques grands > 300.
        """)
    else:
        st.markdown("""
        **📈 Value Added (success rate)**  
        - School’s contribution adjusted for background.  
        - **≈ 0** = as expected; **> 0** = above expected; **< 0** = below expected.

        **🧮 Total candidates**  
        - Students sitting the exam per school.  
        - Most between **80–150** (medium size); a few > 300.
        """)

    st.markdown("---")

    
    def generate_quality_report(df: pd.DataFrame) -> pd.DataFrame:
        miss_pct = (df.isna().sum().sum() / df.size * 100) if df.size else 0
        return pd.DataFrame({
            "Metric": ["Rows", "Columns", "Duplicates", "Missing %", "Quality Score"],
            "Value": [
                len(df),
                len(df.columns),
                int(df.duplicated().sum()),
                f"{miss_pct:.1f}%",
                calculate_quality_score(df),
            ]
        })

    report_df = generate_quality_report(df_base)
    st.download_button(T["report_btn"], report_df.to_csv(index=False).encode("utf-8"), "quality_report.csv", mime="text/csv")
    st.markdown("""
---
### 👉 Next step: explore national trends
Now that we've validated data quality, go to **Overview** to see the big picture.
""")