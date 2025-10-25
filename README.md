# IVAC Dashboard – French Middle School Performance Analysis

**Interactive data storytelling dashboard analyzing educational performance indicators (IVAC) across French middle schools**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Etalab%202.0-green)](https://www.etalab.gouv.fr/licence-ouverte-open-licence)

 **Live App:** [IVAC Streamlit Dashboard] https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app/?page=Introduction
---


## Structure du projet

STREAMLITAPP25_>20221191_AUBEL.MANON/
│
├── app.py                       # Application principale Streamlit
│
├── README.md                    # Documentation du projet
├── requirements.txt             # Dépendances Python
│
├── data/                        # Données utilisées pour les analyses
│   └── fr-en-indicateurs-valeur-ajoutee-colleges.csv
│
├── assets/                      # Ressources graphiques et géographiques
│   └── fr_departements.geojson
│
├── sections/                    # Pages du tableau de bord
│   ├── intro.py                 # Introduction et présentation du projet
│   ├── profiling.py             # Vérification de la qualité des données
│   ├── overview.py              # Analyse globale et indicateurs nationaux
│   ├── deep_dives.py            # Analyses détaillées (régions, établissements)
│   └── conclusions.py           # Conclusions et recommandations
│
├── utils/                       # Fonctions utilitaires (préparation, visualisation, etc.)
│   ├── io.py
│   ├── prep.py
│   ├── viz.py
│   └── geo.py
│
└── tests/                       # (Optionnel) Scripts de test ou de vérification

##  **Project Overview**

This Streamlit application provides an **interactive and bilingual analysis** of the French Ministry of Education's *Indicateurs de Valeur Ajoutée des Collèges (IVAC)* dataset.

It measures how much each school contributes to student success **beyond what is expected** given its socio-economic context.

##  **Objectives**

Transform open public data into an **educational and interactive dashboard** that helps to:

- Reveal **territorial disparities** in academic performance  
- Compare **public vs private** school outcomes  
- Highlight **best practices** among top-performing schools  
- Support **data-driven educational policy decisions**


##  **Narrative Flow**

**1️⃣ Introduction →** Understanding IVAC and its importance  
**2️⃣ Data Quality →** Checking completeness and reliability  
**3️⃣ Overview →** National analysis, trends, and key metrics  
**4️⃣ Deep Dives →** Regional and school-level exploration  
**5️⃣ Conclusions →** Insights, limitations, and recommendations  

---

## **Quick Start**

### 1️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

### 2️⃣ **Run the app**

```bash
streamlit run app.py
```

App will open at:
http://localhost:8501

### **Try it online**

🔗 https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app/?page=Introduction


##  **Key Features**

###  **Interactive Visualizations**
- Choropleth maps by department
- Boxplots comparing Public vs Private sectors
- Top & Bottom 10 regional rankings
- Correlation scatterplots
- Histograms with thresholds and annotations

###  **Bilingual Interface**
-  French /  English toggle
- Dynamic text, chart titles, and tooltips

### **Educational Insights**
- Structured "storytelling" navigation
- Policy implications highlighted with icons
- Contextual warnings (correlation ≠ causation)

### **Optimizations**
- Cached data loading with `@st.cache_data`
- Pre-aggregated tables for speed
- Lightweight structure for quick deployment

---

##  **Data Source**

- **Dataset:** Indicateurs de valeur ajoutée des collèges
- **Provider:** Ministère de l'Éducation nationale
- **License:** Licence Ouverte 2.0 (Etalab)
- **Years:** 2022 → 2024
- **Variables:**
  - Valeur Ajoutée (VA)
  - Taux de Réussite au DNB
  - Secteur (Public/Privé)
  - Nombre de candidats

---

##  **Learning Objectives**

✅ Master data storytelling through real-world data  
✅ Create interactive and bilingual dashboards  
✅ Apply statistical tools (correlation, regression, t-tests)  
✅ Visualize educational inequalities effectively  
✅ Communicate analytical insights clearly and ethically  


---

##  **Technical Highlights**

### **Cached Data Example**
```python
@st.cache_data(show_spinner=False)
def load_data():
    return pd.read_csv("data/fr-en-indicateurs-valeur-ajoutee-colleges.csv")
```

### **Linear Regression Example**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X, y)
st.metric("R²", f"{model.score(X, y):.3f}")
```

### **Language Adaptation**
```python
T = TEXTS["fr"] if lang == "fr" else TEXTS["en"]
st.metric(T["kpi_va"], f"{mean_va:+.2f}")
```

---

##  **Limitations**

- **VA ≠ Absolute Quality** → It's context-adjusted
- **Socio-economic proxies are imperfect**
- **Small schools show higher variability**
- **DNB captures only a part of educational outcomes**
- **Yearly variations may reflect temporary conditions**

---

##  **Academic Context**

This project was developed as part of the  
**EFREI Paris – M1 Data & Artificial Intelligence**  
**Module:** Data Visualization 

**Year:** 2025  
**Student:** Manon Aubel  
**Institution:** EFREI Paris  

---

##  **License**

- **Code:** MIT-style open license
- **Data:** Etalab Licence Ouverte 2.0

---

##  **Acknowledgments**

- **Data provider:** Ministère de l'Éducation nationale
- **Framework:** Streamlit
- **School:** EFREI Paris
- **Platform:** data.gouv.fr (Etalab initiative)

---

##  **Contact**

**Author:** Manon Aubel  
**Institution:** EFREI Paris  
**App:** https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app/?page=Introduction



**Built with ❤️ and Streamlit 🎈**
