# 🎓 IVAC Dashboard – French Middle School Performance Analysis

> **Interactive data storytelling application exploring educational performance indicators (IVAC) for French middle schools**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Etalab%202.0-green)](https://www.etalab.gouv.fr/licence-ouverte-open-licence)

---

## 📖 Project Overview

This Streamlit application presents a comprehensive analysis of **IVAC (Indicateurs de Valeur Ajoutée des Collèges)** – value-added indicators that measure how much middle schools contribute to student success **beyond what's predicted** by their socio-economic background.

### 🎯 Objective

Transform raw open data into an **actionable narrative** that:
- Reveals **territorial disparities** in educational performance
- Compares **public vs private** sector outcomes
- Identifies **best practices** from high-performing schools
- Guides **evidence-based policy decisions**

### 📊 The Story We Tell

**Hook:** Not all schools start equal. Some elevate students beyond expectations; others fall short despite favorable conditions.

**Journey:**
1. **Introduction** → Understanding IVAC and why context matters
2. **Data Quality** → Assessing reliability and limitations
3. **Overview & Analysis** → National trends, regional gaps, and correlations
4. **Deep Dives** → School-level insights, outliers, and success factors
5. **Conclusions** → Key findings, recommendations, and next steps

**Insight:** Value-added is a better metric than raw pass rates. Geographic and sectoral inequalities persist, but targeted interventions can work.

**Implication:** Policymakers should prioritize support for low-VA regions and share practices from leaders.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### 3. Explore the Data

- Use **sidebar filters** to select sessions, regions, and sectors
- Switch between **🇫🇷 French** and **🇬🇧 English** with the language toggle
- Hover over charts for **detailed tooltips**
- Follow the **navigation guide** in the intro section

## 🚀 Deployment

### Deploy to Streamlit Community Cloud

1. **Fork this repository** on GitHub
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your forked repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live** at: `https://your-username-streamlit-app-xxx.streamlit.app`

### Alternative: Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/StreamlitApp25_IVAC.git
cd StreamlitApp25_IVAC

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

---

## 📂 Project Structure

```
StreamlitApp25_IVAC/
│
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/
│   └── fr-en-indicateurs-valeur-ajoutee-colleges.csv  # IVAC dataset
│
├── assets/
│   └── fr_departements.geojson     # GeoJSON for choropleth maps
│
├── sections/                       # Page modules
│   ├── intro.py                    # Context & methodology
│   ├── profiling.py                # Data quality checks
│   ├── overview.py                 # KPIs, trends, maps, synthesis
│   ├── deep_dives.py               # School-level analysis
│   └── conclusions.py              # Insights & recommendations
│
└── utils/                          # Reusable utilities
    ├── io.py                       # Data loading & caching
    ├── prep.py                     # Cleaning & aggregation
    ├── viz.py                      # Chart templates (Plotly)
    └── geo.py                      # Geographic mapping
```

---

## 🎨 Key Features

### 📈 Interactive Visualizations
- **Line charts** with performance zones (excellence, weak)
- **Bar charts** for regional rankings (top/bottom)
- **Choropleth maps** showing departmental disparities
- **Histograms** with reference lines (mean, expected value)
- **Box plots** for sector comparison (Public vs Private)
- **Heatmaps** for correlation matrices
- **Scatter plots** for school-level deep dives

### 🌍 Bilingual Support (FR/EN)
- Complete interface translation
- Dynamic chart labels and annotations
- Context-aware explanations

### ♿ Accessibility (WCAG Compliant)
- High-contrast color schemes
- Meaningful axis labels and titles
- Descriptive tooltips and captions
- Screen-reader friendly structure

### ⚡ Performance Optimizations
- `@st.cache_data` for data loading
- Pre-aggregated tables (timeseries, regions, departments)
- Efficient Plotly charts with vectorized operations

### 🎓 Storytelling Elements
- **TL;DR summaries** with key metrics
- **Narrative transitions** between sections ("Step 1 → Trends")
- **Policy implications** highlighted with custom badges
- **Contextual warnings** (e.g., "correlation ≠ causation")

---

## 📊 Data Source

- **Dataset:** [Indicateurs de valeur ajoutée des collèges](https://www.data.gouv.fr/fr/datasets/indicateurs-de-valeur-ajoutee-des-colleges/)
- **Provider:** Ministère de l'Éducation nationale (French Ministry of Education)
- **License:** [Licence Ouverte / Open License 2.0 (Etalab)](https://www.etalab.gouv.fr/licence-ouverte-open-licence)
- **Coverage:** French middle schools (collèges), multiple academic sessions
- **Metrics:** Value-added (VA), pass rates, candidate counts, sectoral data

### 🔍 What is IVAC?

**Value-Added (Valeur Ajoutée)** measures the difference between:
- **Observed performance** (actual pass rates)
- **Expected performance** (predicted based on student backgrounds, school context)

**Interpretation:**
- **VA > 0:** School performs **better than expected** (adds value)
- **VA ≈ 0:** School performs **as expected** (neutral)
- **VA < 0:** School performs **below expectations** (needs support)

---

## 🎯 Learning Objectives Achieved

✅ **Data Storytelling:** Clear narrative arc (problem → analysis → insights → recommendations)  
✅ **Data Quality:** Profiling, validation, transparency about limitations  
✅ **Interactive Dashboard:** Filters, multi-page navigation, responsive design  
✅ **EDA & Analytics:** Aggregations, correlations, t-tests, clustering (optional)  
✅ **Visualization Best Practices:** Appropriate chart types, annotations, color choices  
✅ **Reproducibility:** Pinned dependencies, modular code, clear documentation  

---

## 📐 Technical Highlights

### Caching Strategy
```python
@st.cache_data(show_spinner=False)
def load_data():
    return pd.read_csv("data/fr-en-indicateurs-valeur-ajoutee-colleges.csv")
```

### Reusable Chart Functions
```python
from utils.viz import line_chart, bar_chart, histogram

line_chart(df, x="session_str", y="valeur_ajoutee", 
           title="VA Trend", 
           ref_y=0, ref_label="Expected",
           threshold_zones=[
               {"y0": 5, "y1": 15, "color": "green", "opacity": 0.15, "label": "Excellence"}
           ])
```

### Bilingual Support
```python
T = TEXTS["fr"] if lang == "fr" else TEXTS["en"]
st.metric(T["kpi_va"], f"{mean_va:+.2f}")
```

---

## 🧪 Data Quality & Limitations

### Strengths
- Large sample size (thousands of schools)
- Multiple sessions for longitudinal analysis
- Contextualized metrics (value-added adjusts for background)

### Limitations
- **IVAC ≠ absolute quality** — VA measures relative performance vs predictions, not pedagogical excellence
- **Socio-economic proxies are imperfect** — Cannot fully capture student diversity
- **DNB is one test** — Doesn't measure creativity, critical thinking, long-term success
- **Small schools have high variance** — Outliers may reflect sample size, not quality
- **Missing data** — Some schools/sessions incomplete

⚠️ **Critical reminder:** Use IVAC as a **conversation starter**, not a final judgment.



## 🚀 Deployment

### Streamlit Community Cloud (Recommended)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy! 🎉

**Note:** Ensure `requirements.txt` and `data/` folder are committed.

### Alternative: Local Network

```bash
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

Access from other devices on your network via `http://<your-ip>:8080`.

---

## 📚 Educational Context

This project was developed as part of the **EFREI Paris Data Visualization & Storytelling** course (2025). It demonstrates:

- **Open data reuse** (data.gouv.fr)
- **Statistical literacy** (value-added models, hypothesis testing)
- **Ethical data communication** (transparency, caveats, avoiding causal claims)
- **Policy relevance** (actionable recommendations)

**Course hashtags:** `#EFREIDataStories2025` `#DataVisualization` `#Streamlit`

---

## 🤝 Contributing

This is a student project, but feedback is welcome!

**Suggestions:**
- Report bugs via GitHub Issues
- Propose features or improvements
- Share educational use cases

---

## 📜 License

- **Code:** Open source (MIT-style, adjust as needed)
- **Data:** [Licence Ouverte 2.0 (Etalab)](https://www.etalab.gouv.fr/licence-ouverte-open-licence)

**Citation:**
> Ministère de l'Éducation nationale, *Indicateurs de valeur ajoutée des collèges*, [data.gouv.fr](https://www.data.gouv.fr), retrieved 2025.

---

## 🙏 Acknowledgments

- **Data provider:** Ministère de l'Éducation nationale
- **Open data platform:** data.gouv.fr (Etalab)
- **Framework:** Streamlit team
- **Inspiration:** [FT Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary), Data Viz Society

---

## 📧 Contact

**Student:** Manon Aubel  
**Institution:** EFREI Paris  
**Course:** Data Visualization & Storytelling 2025

---

**Built with ❤️ and Streamlit 🎈**
