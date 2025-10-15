# sections/conclusions.py — FULL BILINGUAL, DATA-DRIVEN
import streamlit as st
import pandas as pd
import numpy as np
from utils.io import load_data
from utils.prep import make_tables

TEXTS = {
    "en": {
        "language": "Language", "en": "English", "fr": "Français",
        "header": "💡 Conclusions & Insights",
        "intro": "This page synthesizes key findings from the IVAC dashboard and provides actionable recommendations for policy and practice.",

        "key_findings_title": "🔍 Key Findings (latest session)",
        "kf1_title": "1️⃣ Persistent Territorial Disparities",
        "kf2_title": "2️⃣ Public vs Private Sector Gap",
        "kf3_title": "3️⃣ Pass Rate vs Value Added: correlation",
        "kf4_title": "4️⃣ Stability over time (national VA)",

        "recommendations_title": "🎯 Policy Recommendations",
        "rec1": "**Territorial support:** Build peer-learning networks between top and Q4 regions; prioritize sustained low-VA areas.",
        "rec2": "**Contextualized evaluation:** Move beyond raw pass rates; emphasize **value added** adjusted for student background.",
        "rec3": "**Resource reallocation:** Channel funding and coaching to schools with persistently negative VA (esp. rural & high-need public).",
        "rec4": "**Best-practice sharing:** Document methods from top schools (public & private) and scale them via a national knowledge hub.",
        "rec5": "**Longitudinal monitoring:** Use multi-year panels to separate structural issues from one-off fluctuations.",
        "rec6": "**Transparency & comms:** Publish IVAC results with clear caveats (context matters; VA ≠ absolute quality).",

        "limitations_title": "⚠️ Limitations & Caveats",
        "lim1": "**Correlation ≠ causation.** High VA does not prove pedagogy; unobserved advantages may remain.",
        "lim2": "**Socio-economic proxies are imperfect.** Student background is complex.",
        "lim3": "**DNB is a snapshot.** It ignores creativity, critical thinking, long-term outcomes.",
        "lim4": "**Small-n volatility.** Small schools vary more; treat outliers with caution.",
        "lim5": "**Data quality varies.** Missingness, reporting errors, exam changes can affect comparability.",

        "next_steps_title": "🚀 Next Steps",
        "ns1": "**Deep-dives** on top performers to isolate transferable practices.",
        "ns2": "**Qualitative work** (interviews, observations) to complement VA.",
        "ns3": "**Student trajectories** beyond DNB (HS success, dropout).",
        "ns4": "**Field experiments** in low-VA regions with rigorous evaluation.",
        "ns5": "**International benchmarking** of value-added models.",

        "final_message": """
---
### 🎓 Final thought

Data can **reveal inequalities and guide action**, but numbers alone don’t transform schools — **people do**.
Treat this dashboard as a **starting point for dialogue**, not a final verdict.

**The goal is not to rank, but to support.**
""",

        "quick_stats": "📊 Quick Stats",
        "stat_avg_va": "Avg VA",
        "stat_sigma": "Dispersion (σ)",
        "stat_schools": "Schools",
        "stat_pos_va": "Positive VA (%)",
    },
    "fr": {
        "language": "Langue", "en": "English", "fr": "Français",
        "header": "💡 Conclusions & Enseignements",
        "intro": "Cette page synthétise les principaux enseignements du tableau de bord IVAC et propose des recommandations actionnables pour les politiques éducatives.",

        "key_findings_title": "🔍 Enseignements clés (dernier millésime)",
        "kf1_title": "1️⃣ Disparités territoriales persistantes",
        "kf2_title": "2️⃣ Écart Public vs Privé",
        "kf3_title": "3️⃣ Taux de réussite vs Valeur ajoutée : corrélation",
        "kf4_title": "4️⃣ Stabilité temporelle (VA nationale)",

        "recommendations_title": "🎯 Recommandations",
        "rec1": "**Soutien territorial :** Réseaux d'apprentissage entre régions leaders et Q4 ; prioriser les zones à VA durablement faible.",
        "rec2": "**Évaluation contextualisée :** Aller au-delà des taux bruts ; mettre l’accent sur la **valeur ajoutée** ajustée du contexte.",
        "rec3": "**Réallocation des ressources :** Financements & coaching vers les établissements à VA négative persistante (not. public & rural).",
        "rec4": "**Partage des pratiques :** Capitaliser les méthodes des meilleurs (publics & privés) via une base nationale.",
        "rec5": "**Suivi pluriannuel :** Panneaux multi-années pour distinguer structurel vs conjoncturel.",
        "rec6": "**Transparence & pédagogie :** Publier IVAC avec mises en garde (le contexte compte ; VA ≠ qualité absolue).",

        "limitations_title": "⚠️ Limites & précautions",
        "lim1": "**Corrélation ≠ causalité.** Une VA élevée ne prouve pas la pédagogie ; des avantages non observés peuvent subsister.",
        "lim2": "**Variables socio-éco imparfaites.** Le profil des élèves est complexe.",
        "lim3": "**Le DNB est un instantané.** Il ignore créativité, esprit critique, devenir à long terme.",
        "lim4": "**Volatilité petit effectif.** Petits établissements = variance plus forte ; prudence sur les outliers.",
        "lim5": "**Qualité de données variable.** Valeurs manquantes, erreurs, changements d’épreuve nuisent à la comparabilité.",

        "next_steps_title": "🚀 Prochaines étapes",
        "ns1": "**Études approfondies** des meilleurs pour isoler les pratiques transférables.",
        "ns2": "**Volet qualitatif** (entretiens, observations) pour compléter la VA.",
        "ns3": "**Trajectoires élèves** au-delà du DNB (réussite au lycée, décrochage).",
        "ns4": "**Expérimentations** en régions à VA faible avec évaluation rigoureuse.",
        "ns5": "**Benchmark international** des modèles de valeur ajoutée.",

        "final_message": """
---
### 🎓 Réflexion finale

Les données peuvent **éclairer les inégalités et guider l’action**, mais ce ne sont pas les chiffres qui transforment les écoles — **ce sont les personnes**.
Considérez ce tableau de bord comme un **point de départ du dialogue**, pas un jugement définitif.

**L’objectif n’est pas de classer, mais de soutenir.**
""",

        "quick_stats": "📊 Statistiques rapides",
        "stat_avg_va": "VA moyenne",
        "stat_sigma": "Dispersion (σ)",
        "stat_schools": "Établissements",
        "stat_pos_va": "VA positive (%)",
    },
}

# =========================
def _get_lang(default="fr") -> str:
    try:
        lang = st.query_params.get("lang", default)
        return lang if lang in ("en", "fr") else default
    except Exception:
        return default
 
def _set_lang(lang: str):
    try:
        st.query_params["lang"] = lang
    except Exception:
        pass


def _fmt(x, fmt="{:.2f}", na="—"):
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return na
        return fmt.format(x)
    except Exception:
        return na

def _safe_corr(df, a, b):
    try:
        c = df[[a, b]].corr(numeric_only=True).iloc[0, 1]
        return None if np.isnan(c) else float(c)
    except Exception:
        return None


# =========================
def show():
    current = _get_lang()
    st.sidebar.subheader(TEXTS[current]["language"])
    choice = st.sidebar.radio(
        label=" ",
        options=["en", "fr"],
        format_func=lambda x: TEXTS[x][x],
        key="lang_selector_conclusions",
        horizontal=True,
        label_visibility="collapsed",
    )
    if choice != current:
        _set_lang(choice)
        st.rerun()
    T = TEXTS[choice]

    #  Header & intro 
    st.header(T["header"])
    st.info(T["intro"])

    # Load data (robust) 
    try:
        df_raw = load_data()
        tables = make_tables(df_raw)
    except Exception as e:
        st.error(f"Data loading error: {e}")
        return

    df_over = tables.get("overview", pd.DataFrame())
    by_region = tables.get("by_region", pd.DataFrame())
    ts = tables.get("timeseries", pd.DataFrame())

    # Identify latest session if available
    session_col = "session" if "session" in df_over.columns else None
    latest_session = int(df_over[session_col].max()) if (session_col and not df_over.empty) else None
    df_latest = df_over[df_over[session_col] == latest_session] if (latest_session is not None) else df_over

    # Precompute metrics 
    mean_va = float(df_latest["valeur_ajoutee"].mean()) if "valeur_ajoutee" in df_latest.columns and not df_latest.empty else None
    mean_rate = float(df_latest["taux_reussite_g"].mean()) if "taux_reussite_g" in df_latest.columns and not df_latest.empty else None
    sigma_va = float(df_latest["valeur_ajoutee"].std()) if "valeur_ajoutee" in df_latest.columns and not df_latest.empty else None
    n_schools = int(len(df_latest)) if not df_latest.empty else 0
    pos_va_pct = float((df_latest["valeur_ajoutee"] > 0).mean() * 100) if "valeur_ajoutee" in df_latest.columns and len(df_latest) else None

    # Regions (latest)
    top_region = bottom_region = None
    top_va = bottom_va = None
    gap_va = None
    if isinstance(by_region, pd.DataFrame) and not by_region.empty and {"region_academique", "valeur_ajoutee"}.issubset(by_region.columns):
        if session_col and "session" in by_region.columns and latest_session is not None:
            reg_latest = by_region[by_region["session"] == latest_session].copy()
        else:
            reg_latest = by_region.copy()
        reg_latest = reg_latest.dropna(subset=["valeur_ajoutee"])
        if not reg_latest.empty:
            grp = reg_latest.groupby("region_academique", dropna=True)["valeur_ajoutee"].mean().sort_values(ascending=False)
            if len(grp) > 0:
                top_region, top_va = grp.index[0], float(grp.iloc[0])
                bottom_region, bottom_va = grp.index[-1], float(grp.iloc[-1])
                gap_va = top_va - bottom_va

    # Sector gap (latest)
    sector_delta = None
    p_value = None
    if "secteur" in df_latest.columns and "valeur_ajoutee" in df_latest.columns:
        pu = df_latest.loc[df_latest["secteur"] == "PU", "valeur_ajoutee"].dropna()
        pr = df_latest.loc[df_latest["secteur"] == "PR", "valeur_ajoutee"].dropna()
        if len(pu) > 3 and len(pr) > 3:
            sector_delta = float(pr.mean() - pu.mean())
            try:
                from scipy import stats
                _, p_value = stats.ttest_ind(pr, pu, equal_var=False)
                p_value = float(p_value)
            except Exception:
                p_value = None

    # Correlation (latest)
    corr_rate_va = _safe_corr(df_latest, "taux_reussite_g", "valeur_ajoutee")

    # Time trend (national VA)
    delta_va = None
    if isinstance(ts, pd.DataFrame) and not ts.empty and {"valeur_ajoutee", "session"}.issubset(ts.columns):
        ts_sorted = ts.dropna(subset=["session", "valeur_ajoutee"]).sort_values("session")
        if len(ts_sorted) >= 2:
            delta_va = float(ts_sorted["valeur_ajoutee"].iloc[-1] - ts_sorted["valeur_ajoutee"].iloc[0])
    # =========================
    st.markdown(f"## {T['key_findings_title']}")

    # Territorial disparities
    if choice == "fr":
        st.markdown(f"### {T['kf1_title']}")
        st.markdown(
            f"- **Leader** : **{top_region or '—'}** ({_fmt(top_va, '{:+.2f}')}) &nbsp;•&nbsp; "
            f"**À surveiller** : **{bottom_region or '—'}** ({_fmt(bottom_va, '{:+.2f}')})  \n"
            f"- **Écart Top–Bottom (VA)** : **{_fmt(gap_va, '{:.2f}')} pts**  \n"
            f"- **VA moyenne nationale** : **{_fmt(mean_va, '{:+.2f}')}**  "
        )
        st.caption("Lecture : un écart important entre régions confirme des disparités territoriales persistantes.")
    else:
        st.markdown(f"### {T['kf1_title']}")
        st.markdown(
            f"- **Leader**: **{top_region or '—'}** ({_fmt(top_va, '{:+.2f}')}) &nbsp;•&nbsp; "
            f"**Watch**: **{bottom_region or '—'}** ({_fmt(bottom_va, '{:+.2f}')})  \n"
            f"- **Top–Bottom gap (VA)**: **{_fmt(gap_va, '{:.2f}')} pts**  \n"
            f"- **National average VA**: **{_fmt(mean_va, '{:+.2f}')}**  "
        )
        st.caption("Interpretation: a large spread across regions signals persistent territorial disparities.")

    # Sector gap
    if choice == "fr":
        st.markdown(f"### {T['kf2_title']}")
        st.markdown(
            f"- **Δ(PR − PU)** : **{_fmt(sector_delta, '{:+.2f}')} pts VA**  \n"
            f"- **Significativité (p-value)** : **{_fmt(p_value, '{:.4f}')}** "
            + ("→ **différence significative**" if (p_value is not None and p_value < 0.05) else "→ différence non significative")
        )
        st.caption("Rappel : écart statistique ≠ causalité (sélection, contexte).")
    else:
        st.markdown(f"### {T['kf2_title']}")
        st.markdown(
            f"- **Δ(PR − PU)**: **{_fmt(sector_delta, '{:+.2f}')} VA pts**  \n"
            f"- **Significance (p-value)**: **{_fmt(p_value, '{:.4f}')}** "
            + ("→ **significant difference**" if (p_value is not None and p_value < 0.05) else "→ not significant")
        )
        st.caption("Reminder: statistical gap ≠ causality (selection, context).")

    # Correlation pass rate vs VA
    if choice == "fr":
        st.markdown(f"### {T['kf3_title']}")
        if corr_rate_va is None:
            st.markdown("Corrélation non calculable sur le dernier millésime.")
        else:
            st.markdown(f"- **Corrélation de Pearson (taux vs VA)** : **{corr_rate_va:.2f}**")
            st.caption(
                "Si |r| > 0,5 → relation forte ; ~0,3 → modérée ; < 0,2 → faible. "
                "Association ≠ causalité."
            )
    else:
        st.markdown(f"### {T['kf3_title']}")
        if corr_rate_va is None:
            st.markdown("Correlation not computable on latest vintage.")
        else:
            st.markdown(f"- **Pearson correlation (rate vs VA)**: **{corr_rate_va:.2f}**")
            st.caption(
                "If |r| > 0.5 → strong; ~0.3 → moderate; < 0.2 → weak. "
                "Association ≠ causation."
            )

    # Stability over time
    if choice == "fr":
        st.markdown(f"### {T['kf4_title']}")
        st.markdown(
            f"- **Δ VA nationale (début → fin)** : **{_fmt(delta_va, '{:+.2f}')} pts**  \n"
            f"- **VA moyenne (dernier millésime)** : **{_fmt(mean_va, '{:+.2f}')}**"
        )
        st.caption("Par construction, la VA nationale oscille autour de 0 ; suivre l’évolution multi-annuelle reste essentiel.")
    else:
        st.markdown(f"### {T['kf4_title']}")
        st.markdown(
            f"- **Δ National VA (first → last)**: **{_fmt(delta_va, '{:+.2f}')} pts**  \n"
            f"- **Avg VA (latest)**: **{_fmt(mean_va, '{:+.2f}')}**"
        )
        st.caption("By design, national VA hovers around 0; multi-year tracking is still essential.")

    # Recommendations, limitations, next steps 
    st.markdown("---")
    st.markdown(f"## {T['recommendations_title']}")
    st.markdown(f"1. {T['rec1']}")
    st.markdown(f"2. {T['rec2']}")
    st.markdown(f"3. {T['rec3']}")
    st.markdown(f"4. {T['rec4']}")
    st.markdown(f"5. {T['rec5']}")
    st.markdown(f"6. {T['rec6']}")

    st.markdown("---")
    st.markdown(f"## {T['limitations_title']}")
    st.warning(
        "- " + T["lim1"] + "\n\n"
        "- " + T["lim2"] + "\n\n"
        "- " + T["lim3"] + "\n\n"
        "- " + T["lim4"] + "\n\n"
        "- " + T["lim5"]
    )

    st.markdown("---")
    st.markdown(f"## {T['next_steps_title']}")
    st.markdown(f"- {T['ns1']}")
    st.markdown(f"- {T['ns2']}")
    st.markdown(f"- {T['ns3']}")
    st.markdown(f"- {T['ns4']}")
    st.markdown(f"- {T['ns5']}")

    st.markdown(T["final_message"])

    # Quick stats (optional footer)
    if not df_latest.empty and "valeur_ajoutee" in df_latest.columns:
        st.markdown("---")
        st.markdown(f"### {T['quick_stats']}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(T["stat_avg_va"], _fmt(mean_va, "{:+.2f}"))
        col2.metric(T["stat_sigma"], _fmt(sigma_va, "{:.2f}"))
        col3.metric(T["stat_schools"], f"{n_schools:,}")
        col4.metric(T["stat_pos_va"], _fmt(pos_va_pct, "{:.1f}%"))