import streamlit as st
from urllib.parse import quote, unquote

# Pages
from sections import intro, overview, deep_dives, conclusions, profiling

# ---------- Page config ----------
st.set_page_config(
    page_title="IVAC – Value Added Indicators (French Middle Schools)",
    page_icon="🎓",
    layout="wide",
    menu_items={
        "Get Help": "https://www.data.gouv.fr/en/datasets/indicateurs-de-valeur-ajoutee-des-colleges/",
        "Report a bug": None,
        "About": "IVAC dashboard – educational data storytelling (Etalab 2.0).",
    },
)

# ---------- Page registry (dict label -> module) ----------
PAGES = {
    "Introduction": intro,
    "Data Quality & Profiling": profiling,
    "Overview & Analysis": overview,
    "Deep Dives": deep_dives,
    "Conclusions": conclusions,
}
LABELS = list(PAGES.keys())

# ---------- URL state helpers ----------
def set_query_page(name: str) -> None:
    """Update ?page= in the URL (no experimental API)."""
    try:
        st.query_params["page"] = quote(name)
    except Exception:
        pass

def get_query_page() -> str | None:
    """Read current ?page= value from URL."""
    try:
        val = st.query_params.get("page", None)
        return unquote(val) if val else None
    except Exception:
        return None

# ---------- Sidebar navigation ----------
st.sidebar.title("📚 Menu")

# 1) Determine default page BEFORE creating the radio
page_from_url = get_query_page()
if page_from_url in LABELS:
    default_label = page_from_url
elif st.session_state.get("nav_page") in LABELS:
    default_label = st.session_state["nav_page"]
else:
    default_label = "Introduction"

# 2) Create radio with a dedicated key (avoid conflicts)
selected = st.sidebar.radio(
    "Go to:",
    LABELS,
    index=LABELS.index(default_label),
    key="nav_page",  # <- clé du widget
)

# 3) Keep everything in sync (session & URL)
set_query_page(selected)
st.session_state["page"] = selected  # clé interne libre (utile pour tes boutons)
# NB: ne pas réécrire st.session_state["nav_page"] ici (c'est le widget)

# ---------- Render selected page ----------
try:
    PAGES[selected].show()
except Exception:
    st.error(f"⚠️ An error occurred while rendering **{selected}**.")
    with st.expander("Show technical details"):
        import traceback
        st.code("".join(traceback.format_exc()), language="python")

# ---------- Footer ----------
st.markdown(
    """
    <hr style="margin-top:3rem;margin-bottom:0.5rem;">
    <div style="font-size:0.9rem;opacity:0.75;text-align:center;">
        Source: Ministère de l'Éducation nationale —
        <a href="https://www.data.gouv.fr" target="_blank" style="text-decoration:none;">data.gouv.fr</a> ·
        License: Etalab 2.0 ·
        Built with <b style="color:#FF4B4B;">Streamlit</b> 🎈
    </div>
    """,
    unsafe_allow_html=True,
)