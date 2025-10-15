# 🎓 IVAC Dashboard – French Middle School Performance Analysis

> **Interactive data storytelling dashboard analyzing educational performance indicators (IVAC) across French middle schools**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Etalab%202.0-green)](https://www.etalab.gouv.fr/licence-ouverte-open-licence)

🖥️ **Live App:** [👉 IVAC Streamlit Dashboard](https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app)

---

## 📖 **Project Overview**

This Streamlit application provides an **interactive and bilingual analysis** of the French Ministry of Education's *Indicateurs de Valeur Ajoutée des Collèges (IVAC)* dataset.

It measures how much each school contributes to student success **beyond what is expected** given its socio-economic context.

---

## 🎯 **Objectives**

Transform open public data into an **educational and interactive dashboard** that helps to:

- Reveal **territorial disparities** in academic performance  
- Compare **public vs private** school outcomes  
- Highlight **best practices** among top-performing schools  
- Support **data-driven educational policy decisions**

---

## 🧭 **Narrative Flow**

**1️⃣ Introduction →** Understanding IVAC and its importance  
**2️⃣ Data Quality →** Checking completeness and reliability  
**3️⃣ Overview →** National analysis, trends, and key metrics  
**4️⃣ Deep Dives →** Regional and school-level exploration  
**5️⃣ Conclusions →** Insights, limitations, and recommendations  

---

## 🚀 **Quick Start**

### 1️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

### 2️⃣ **Run the app**

```bash
streamlit run app.py
```

App will open at:
👉 http://localhost:8501

### 3️⃣ **Try it online**

🔗 https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app

---

## 📂 **Project Structure**

```
IVAC-Streamlit-App/
│
├── app.py                        
├── README.md                     
│
├── data/
│   └── fr-en-indicateurs-valeur-ajoutee-colleges.csv
│
├── assets/
│   └── fr_departements.geojson   
│
├── sections/
│   ├── intro.py                  #
│   ├── profiling.py              
│   ├── overview.py               
│   └── conclusions.py            
│
└── utils/
    ├── io.py, prep.py, viz.py, geo.py  # Helper scripts
```

---

## 🎨 **Key Features**

### 📈 **Interactive Visualizations**
- Choropleth maps by department
- Boxplots comparing Public vs Private sectors
- Top & Bottom 10 regional rankings
- Correlation scatterplots
- Histograms with thresholds and annotations

### 🌍 **Bilingual Interface**
- 🇫🇷 French / 🇬🇧 English toggle
- Dynamic text, chart titles, and tooltips

### 🧠 **Educational Insights**
- Structured "storytelling" navigation
- Policy implications highlighted with icons
- Contextual warnings (correlation ≠ causation)

### ⚡ **Optimizations**
- Cached data loading with `@st.cache_data`
- Pre-aggregated tables for speed
- Lightweight structure for quick deployment

---

## 📚 **Data Source**

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

## 🎓 **Learning Objectives**

✅ Master data storytelling through real-world data  
✅ Create interactive and bilingual dashboards  
✅ Apply statistical tools (correlation, regression, t-tests)  
✅ Visualize educational inequalities effectively  
✅ Communicate analytical insights clearly and ethically  

---

## 🧩 **Technical Highlights**

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

## ⚠️ **Limitations**

- **VA ≠ Absolute Quality** → It's context-adjusted
- **Socio-economic proxies are imperfect**
- **Small schools show higher variability**
- **DNB captures only a part of educational outcomes**
- **Yearly variations may reflect temporary conditions**

---

## 🏫 **Academic Context**

This project was developed as part of the  
🎓 **EFREI Paris – M1 Data & Artificial Intelligence**  
**Module:** Data Visualization & Storytelling

📅 **Year:** 2025  
👩‍💻 **Student:** Manon Aubel  
🏫 **Institution:** EFREI Paris  

---

## 📜 **License**

- **Code:** MIT-style open license
- **Data:** Etalab Licence Ouverte 2.0

---

## 🙏 **Acknowledgments**

- **Data provider:** Ministère de l'Éducation nationale
- **Framework:** Streamlit
- **School:** EFREI Paris
- **Platform:** data.gouv.fr (Etalab initiative)

---

## 📧 **Contact**

**Author:** Manon Aubel  
**Institution:** EFREI Paris  
**App:** https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app

---

**Built with ❤️ and Streamlit 🎈**

---

# 🇫🇷 **Tableau de Bord IVAC – Analyse des Collèges Français**

> **Application interactive d'analyse des indicateurs de valeur ajoutée (IVAC) dans les collèges français**

🖥️ **Application en ligne :** [👉 Tableau de bord IVAC](https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app)

---

## 📖 **Présentation du Projet**

Cette application Streamlit permet une analyse interactive et bilingue des Indicateurs de Valeur Ajoutée des Collèges (IVAC) publiés par le Ministère de l'Éducation nationale.

Elle évalue dans quelle mesure les établissements contribuent à la réussite de leurs élèves au-delà de ce qui est attendu compte tenu du contexte socio-économique.

---

## 🎯 **Objectifs**

Transformer des données publiques ouvertes en un tableau de bord interactif permettant de :
- Mettre en évidence les inégalités territoriales
- Comparer les performances du secteur public et privé
- Identifier les bonnes pratiques des établissements performants
- Aider à la prise de décision éducative fondée sur les données

---

## 🧭 **Structure Narrative**

**1️⃣ Introduction →** Comprendre le concept d'IVAC  
**2️⃣ Qualité des Données →** Vérifications et nettoyage  
**3️⃣ Vue d'Ensemble →** Tendances et performances nationales  
**4️⃣ Analyses Approfondies →** Par région, secteur et établissement  
**5️⃣ Conclusions →** Enseignements et recommandations  

---

## 🚀 **Démarrage Rapide**

### 1️⃣ **Installer les dépendances**

```bash
pip install -r requirements.txt
```

### 2️⃣ **Lancer l'application**

```bash
streamlit run app.py
```

Ouvrir dans le navigateur :
👉 http://localhost:8501

### 3️⃣ **Tester en ligne**

🔗 https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app

---

## 📂 **Structure du Projet**

```
IVAC-Streamlit-App/
│
├── app.py                        # Script principal
├── requirements.txt              # Dépendances Python
├── README.md                     # Documentation
│
├── data/
│   └── fr-en-indicateurs-valeur-ajoutee-colleges.csv
│
├── assets/
│   └── fr_departements.geojson   # Carte des départements
│
├── sections/
│   ├── intro.py                  # Introduction & contexte
│   ├── profiling.py              # Qualité des données
│   ├── overview.py               # Tendances et cartes
│   ├── deep_dives.py             # Analyses locales
│   └── conclusions.py            # Recommandations
│
└── utils/
    ├── io.py, prep.py, viz.py, geo.py  # Fonctions d'aide
```

---

## 🎨 **Fonctionnalités Principales**

- **Cartes interactives** par département
- **Classement des régions** (Top/Bottom 10)
- **Comparaison Public vs Privé** (boxplots)
- **Corrélations** entre indicateurs
- **Histogrammes et nuages de points**
- **Interface bilingue** FR/EN

---

## 🧠 **Enseignements et Objectifs Pédagogiques**

✅ Démontrer une approche de data storytelling  
✅ Appliquer des méthodes statistiques de base  
✅ Concevoir un tableau de bord clair et pédagogique  
✅ Visualiser les inégalités territoriales  
✅ Communiquer les résultats de manière éthique et compréhensible  

---

## ⚠️ **Limites**

- **La VA n'est pas un indicateur absolu de qualité**
- **Les variables socio-économiques ne capturent pas toute la réalité**
- **Les petits établissements présentent plus de variance**
- **Le DNB ne mesure qu'une partie des compétences**

---

## 🏫 **Contexte Académique**

Projet réalisé dans le cadre du  
🎓 **Master 1 Data & Intelligence Artificielle – EFREI Paris**  
**Module :** Data Visualization & Storytelling

📅 **Année :** 2025  
👩‍💻 **Étudiante :** Manon Aubel  
🏫 **Établissement :** EFREI Paris  

---

## 📜 **Licence**

- **Code :** Open Source (MIT)
- **Données :** Licence Ouverte Etalab 2.0

---

## 🙏 **Remerciements**

- **Ministère de l'Éducation nationale** – Fournisseur des données
- **Streamlit** – Framework de visualisation
- **EFREI Paris** – Encadrement académique
- **data.gouv.fr** – Plateforme open data

---

## 📧 **Contact**

**Auteur :** Manon Aubel  
**Établissement :** EFREI Paris  
**Application :** https://manoonaub-ivac-streamlit-app-app-x6gn6z.streamlit.app

---

**Développé avec ❤️ et Streamlit 🎈**
