# sections/conclusions.py — BILINGUAL (FR/EN)
import streamlit as st
import pandas as pd
from utils.io import load_data
from utils.prep import make_tables

TEXTS = {
    "en": {
        "language": "Language", "en": "English", "fr": "Français",
        "header": "💡 Conclusions & Insights",
        "intro": "This page synthesizes the key findings from the IVAC dashboard and provides actionable recommendations for educational policy.",
        
        "key_findings_title": "🔍 Key Findings",
        "kf1_title": "1️⃣ Persistent Territorial Disparities",
        "kf1_text": """
The analysis reveals **significant regional inequalities** in school performance:
- Academic regions show VA gaps **up to 10-15 points**
- Best-performing regions systematically outperform expectations
- Struggling regions remain below national average across multiple sessions

**Implication:** Geographic location remains a strong predictor of educational outcomes, highlighting the need for **targeted territorial policies**.
""",
        
        "kf2_title": "2️⃣ Public vs Private Sector Gap",
        "kf2_text": """
Statistical tests consistently show a **significant difference** between public and private sectors:
- Private schools show **higher value added** on average (+2 to +3 points)
- However, this gap likely reflects **selection effects** (student backgrounds, parental involvement) rather than pedagogical superiority
- Public schools serve more diverse populations and face greater contextual challenges

**Implication:** Difference ≠ causality. The gap calls for **equitable resource distribution** and **sharing best practices** across sectors, not simplistic conclusions.
""",
        
        "kf3_title": "3️⃣ Weak Correlation Between Pass Rates and Value Added",
        "kf3_text": """
The correlation between pass rates and value added is **moderate to weak** (r ≈ 0.3-0.5):
- High pass rates don't always mean high value added
- Some schools achieve strong results despite difficult contexts (high VA, moderate pass rate)
- Others have high pass rates but low VA (potential **grade inflation** or favorable student composition)

**Implication:** **Value added is a better indicator** of school effectiveness than raw pass rates. Policy should focus on VA improvement, not just pass rate targets.
""",
        
        "kf4_title": "4️⃣ Stability Over Time with Pockets of Volatility",
        "kf4_text": """
Temporal trends show:
- **National VA remains stable** around 0 (as expected by design)
- Some regions show **consistent improvement** or decline
- Individual schools can experience **high volatility** (staff changes, local policies, cohort effects)

**Implication:** Multi-year tracking is essential. Single-session judgments can be misleading.
""",
        
        "recommendations_title": "🎯 Policy Recommendations",
        "rec1": "**Territorial Support Programs:** Create peer-learning networks between high-performing and struggling regions. Focus on Q4 regions with sustained low VA.",
        "rec2": "**Contextualized Evaluation:** Move beyond raw pass rates. Evaluate schools primarily on **value added** to account for student background.",
        "rec3": "**Resource Reallocation:** Target additional funding and pedagogical support to schools with consistently negative VA, especially in public sector and rural areas.",
        "rec4": "**Best Practice Sharing:** Document and disseminate methods from top-performing schools (both public and private) through a national knowledge base.",
        "rec5": "**Longitudinal Monitoring:** Implement multi-year dashboards to distinguish structural issues from temporary fluctuations.",
        "rec6": "**Transparency & Communication:** Make IVAC data accessible to parents and local communities while explaining limitations (context matters, VA ≠ quality in absolute terms).",
        
        "limitations_title": "⚠️ Limitations & Caveats",
        "lim1": "**IVAC reflects correlation, not causation.** High VA doesn't prove pedagogical excellence; it may reflect favorable contexts not captured in models.",
        "lim2": "**Socio-economic variables are approximations.** Student background is complex and cannot be fully controlled for.",
        "lim3": "**DNB is one snapshot.** It doesn't capture creativity, critical thinking, or long-term success.",
        "lim4": "**Sample size matters.** Small schools have high variance. Interpret outliers cautiously.",
        "lim5": "**Data quality varies.** Missing values, reporting errors, and changes in exam structure over time can affect comparisons.",
        
        "next_steps_title": "🚀 Next Steps",
        "ns1": "**Deep-dive studies** on top-performing schools to identify transferable practices.",
        "ns2": "**Qualitative research** to complement quantitative VA (teacher interviews, classroom observations).",
        "ns3": "**Student trajectory tracking** beyond DNB (high school success, dropout rates).",
        "ns4": "**Experimental interventions** in low-VA regions with rigorous evaluation.",
        "ns5": "**International benchmarking** to compare French IVAC system with value-added models abroad.",
        
        "final_message": """
---
### 🎓 Final Thought

The IVAC dashboard demonstrates that **data can illuminate inequalities and guide action**. However, numbers alone don't change schools — **people do**. 

This analysis should serve as a **starting point for conversation**, not a final judgment. Educational success is multidimensional, and every school faces unique challenges.

**The goal is not to rank, but to support.**

🔗 For more information: [Ministère de l'Éducation nationale](https://www.education.gouv.fr) | [data.gouv.fr](https://www.data.gouv.fr)
"""
    },
    
    "fr": {
        "language": "Langue", "en": "English", "fr": "Français",
        "header": "💡 Conclusions & Enseignements",
        "intro": "Cette page synthétise les principaux enseignements du tableau de bord IVAC et propose des recommandations concrètes pour les politiques éducatives.",
        
        "key_findings_title": "🔍 Enseignements Clés",
        "kf1_title": "1️⃣ Disparités Territoriales Persistantes",
        "kf1_text": """
L'analyse révèle des **inégalités régionales significatives** dans les performances scolaires :
- Les régions académiques affichent des écarts de VA **jusqu'à 10-15 points**
- Les régions les plus performantes sur-performent systématiquement les attentes
- Les régions en difficulté restent en-dessous de la moyenne nationale sur plusieurs sessions

**Implication :** La localisation géographique demeure un fort prédicteur des résultats éducatifs, soulignant le besoin de **politiques territoriales ciblées**.
""",
        
        "kf2_title": "2️⃣ Écart Public vs Privé",
        "kf2_text": """
Les tests statistiques montrent systématiquement une **différence significative** entre secteurs public et privé :
- Les établissements privés affichent une **valeur ajoutée plus élevée** en moyenne (+2 à +3 points)
- Cependant, cet écart reflète probablement des **effets de sélection** (profil des élèves, implication parentale) plutôt qu'une supériorité pédagogique
- Le public accueille des populations plus diverses et fait face à des défis contextuels plus importants

**Implication :** Différence ≠ causalité. L'écart appelle à une **distribution équitable des ressources** et au **partage des bonnes pratiques** entre secteurs, pas à des conclusions simplistes.
""",
        
        "kf3_title": "3️⃣ Faible Corrélation entre Taux de Réussite et Valeur Ajoutée",
        "kf3_text": """
La corrélation entre taux de réussite et valeur ajoutée est **modérée à faible** (r ≈ 0.3-0.5) :
- Des taux de réussite élevés ne signifient pas toujours une forte valeur ajoutée
- Certains établissements obtiennent de bons résultats malgré des contextes difficiles (VA élevée, taux modéré)
- D'autres ont des taux élevés mais une faible VA (possible **inflation des notes** ou composition favorable des élèves)

**Implication :** **La valeur ajoutée est un meilleur indicateur** de l'efficacité scolaire que les taux bruts. Les politiques doivent se concentrer sur l'amélioration de la VA, pas seulement sur les objectifs de taux de réussite.
""",
        
        "kf4_title": "4️⃣ Stabilité Temporelle avec Poches de Volatilité",
        "kf4_text": """
Les tendances temporelles montrent :
- La **VA nationale reste stable** autour de 0 (comme prévu par construction)
- Certaines régions montrent une **amélioration ou déclin constants**
- Les établissements individuels peuvent connaître une **forte volatilité** (changements d'équipe, politiques locales, effets de cohorte)

**Implication :** Un suivi pluriannuel est essentiel. Les jugements sur une seule session peuvent être trompeurs.
""",
        
        "recommendations_title": "🎯 Recommandations Politiques",
        "rec1": "**Programmes de Soutien Territorial :** Créer des réseaux d'apprentissage entre pairs entre régions performantes et en difficulté. Focus sur les régions Q4 avec VA durablement faible.",
        "rec2": "**Évaluation Contextualisée :** Aller au-delà des taux bruts. Évaluer les établissements principalement sur la **valeur ajoutée** pour tenir compte du profil des élèves.",
        "rec3": "**Réallocation des Ressources :** Cibler financements et soutiens pédagogiques additionnels vers les établissements avec VA négative persistante, notamment dans le public et les zones rurales.",
        "rec4": "**Partage des Bonnes Pratiques :** Documenter et diffuser les méthodes des établissements les plus performants (publics et privés) via une base de connaissances nationale.",
        "rec5": "**Suivi Longitudinal :** Mettre en place des tableaux de bord pluriannuels pour distinguer problèmes structurels et fluctuations temporaires.",
        "rec6": "**Transparence & Communication :** Rendre les données IVAC accessibles aux parents et communautés locales tout en expliquant les limites (le contexte compte, VA ≠ qualité absolue).",
        
        "limitations_title": "⚠️ Limites & Précautions",
        "lim1": "**IVAC reflète une corrélation, pas une causalité.** Une VA élevée ne prouve pas l'excellence pédagogique ; elle peut refléter des contextes favorables non capturés par les modèles.",
        "lim2": "**Les variables socio-économiques sont des approximations.** Le profil des élèves est complexe et ne peut être entièrement contrôlé.",
        "lim3": "**Le DNB est un instantané.** Il ne capture pas la créativité, l'esprit critique ou la réussite à long terme.",
        "lim4": "**La taille d'échantillon compte.** Les petits établissements ont une forte variance. Interpréter les outliers avec prudence.",
        "lim5": "**La qualité des données varie.** Valeurs manquantes, erreurs de saisie et changements dans la structure de l'examen affectent les comparaisons.",
        
        "next_steps_title": "🚀 Prochaines Étapes",
        "ns1": "**Études approfondies** sur les établissements les plus performants pour identifier les pratiques transférables.",
        "ns2": "**Recherche qualitative** pour compléter la VA quantitative (entretiens enseignants, observations en classe).",
        "ns3": "**Suivi des trajectoires élèves** au-delà du DNB (réussite au lycée, taux de décrochage).",
        "ns4": "**Interventions expérimentales** dans les régions à faible VA avec évaluation rigoureuse.",
        "ns5": "**Benchmarking international** pour comparer le système IVAC français avec les modèles de valeur ajoutée à l'étranger.",
        
        "final_message": """
---
### 🎓 Réflexion Finale

Le tableau de bord IVAC démontre que **les données peuvent éclairer les inégalités et guider l'action**. Cependant, les chiffres seuls ne changent pas les écoles — **les personnes le font**.

Cette analyse doit servir de **point de départ pour la conversation**, pas de jugement final. La réussite éducative est multidimensionnelle, et chaque établissement fait face à des défis uniques.

**L'objectif n'est pas de classer, mais de soutenir.**

🔗 Plus d'informations : [Ministère de l'Éducation nationale](https://www.education.gouv.fr) | [data.gouv.fr](https://www.data.gouv.fr)
"""
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

def show():
    # Language switcher
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

    # Header
    st.header(T["header"])
    st.info(T["intro"])
    
    st.markdown("---")
    
    # ==================== KEY FINDINGS ====================
    st.markdown(f"## {T['key_findings_title']}")
    
    st.markdown(f"### {T['kf1_title']}")
    st.markdown(T["kf1_text"])
    
    st.markdown(f"### {T['kf2_title']}")
    st.markdown(T["kf2_text"])
    
    st.markdown(f"### {T['kf3_title']}")
    st.markdown(T["kf3_text"])
    
    st.markdown(f"### {T['kf4_title']}")
    st.markdown(T["kf4_text"])
    
    st.markdown("---")
    
    # ==================== RECOMMENDATIONS ====================
    st.markdown(f"## {T['recommendations_title']}")
    
    st.markdown(f"1. {T['rec1']}")
    st.markdown(f"2. {T['rec2']}")
    st.markdown(f"3. {T['rec3']}")
    st.markdown(f"4. {T['rec4']}")
    st.markdown(f"5. {T['rec5']}")
    st.markdown(f"6. {T['rec6']}")
    
    st.markdown("---")
    
    # ==================== LIMITATIONS ====================
    st.markdown(f"## {T['limitations_title']}")
    
    st.warning(f"""
**⚠️ Rappel important / Important reminder:**

- {T['lim1']}
- {T['lim2']}
- {T['lim3']}
- {T['lim4']}
- {T['lim5']}
""")
    
    st.markdown("---")
    
    # ==================== NEXT STEPS ====================
    st.markdown(f"## {T['next_steps_title']}")
    
    st.markdown(f"- {T['ns1']}")
    st.markdown(f"- {T['ns2']}")
    st.markdown(f"- {T['ns3']}")
    st.markdown(f"- {T['ns4']}")
    st.markdown(f"- {T['ns5']}")
    
    # ==================== FINAL MESSAGE ====================
    st.markdown(T["final_message"])
    
    # ==================== QUICK STATS (BONUS) ====================
    try:
        df_raw = load_data()
        tables = make_tables(df_raw)
        df_over = tables.get("overview", pd.DataFrame())
        
        if not df_over.empty and "valeur_ajoutee" in df_over.columns:
            st.markdown("---")
            if T is TEXTS["fr"]:
                st.markdown("### 📊 Statistiques Rapides")
            else:
                st.markdown("### 📊 Quick Stats")
            
            col1, col2, col3, col4 = st.columns(4)
            
            mean_va = df_over["valeur_ajoutee"].mean()
            std_va = df_over["valeur_ajoutee"].std()
            n_schools = len(df_over)
            n_positive_va = (df_over["valeur_ajoutee"] > 0).sum()
            
            col1.metric("VA moyenne" if T is TEXTS["fr"] else "Avg VA", f"{mean_va:+.2f}")
            col2.metric("Dispersion (σ)", f"{std_va:.2f}")
            col3.metric("Établissements" if T is TEXTS["fr"] else "Schools", f"{n_schools:,}")
            col4.metric("VA positive (%)" if T is TEXTS["fr"] else "Positive VA (%)", 
                       f"{100*n_positive_va/n_schools:.1f}%")
    except Exception:
        pass  # Si erreur de chargement, on ne montre pas les stats
