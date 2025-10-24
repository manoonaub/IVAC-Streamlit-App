# utils/prep.py
import re
from typing import Dict, Tuple
import pandas as pd
import streamlit as st



def _ensure_session_str(df: pd.DataFrame | None) -> pd.DataFrame | None:
    """
    Add a string version of session column if missing (returns copy or None).
    Used for filtering and display across the app.
    """
    if df is None or df.empty:
        return df
    if "session" in df.columns and "session_str" not in df.columns:
        df = df.copy()
        df["session"] = df["session"].astype("Int64")
        df["session_str"] = df["session"].astype(str)
    return df


def _to_snake(s: str) -> str:
    """Converts a string to snake_case with enhanced French character handling."""
    if not s or not isinstance(s, str):
        return ""
    
    s = str(s).strip().lower()
    # Enhanced French character normalization
    replacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a", "ä": "a",
        "ç": "c",
        "ù": "u", "û": "u", "ü": "u",
        "ô": "o", "ö": "o",
        "î": "i", "ï": "i"
    }
    
    for old, new in replacements.items():
        s = s.replace(old, new)
    
    # Remove special characters and convert to snake_case
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s

@st.cache_data(show_spinner=False)
def clean_ivac(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and standardizes the raw IVAC dataframe."""
    if df is None or df.empty:
        return df
    
    d = df.copy()
    d.columns = [_to_snake(c) for c in d.columns]

    # Define numeric columns with better organization
    numeric_columns = {
        "performance": ["taux_reussite_g", "taux_reussite_p", "va_du_taux_de_reussite_g", "va_de_la_note_g"],
        "grades": ["note_a_l_ecrit_g", "note_a_l_ecrit_p"],
        "candidates": ["nb_candidats_g", "nb_candidats_p"],
        "access": ["taux_d_acces_6eme_3eme"],
        "attendance": ["part_presents_3eme_ordinaire_total", "part_presents_3eme_ordinaire_g", "part_presents_3eme_ordinaire_p", "part_presents_3eme_segpa_total"],
        "mentions": ["nb_mentions_ab_g", "nb_mentions_b_g", "nb_mentions_tb_g", "nb_mentions_global_g"]
    }
    
    # Flatten the dictionary to get all numeric columns
    all_numeric_cols = [col for cols in numeric_columns.values() for col in cols]
    
    # Convert to numeric with better error handling
    for col in all_numeric_cols:
        if col in d.columns:
            d[col] = pd.to_numeric(d[col], errors="coerce")

    if "valeur_ajoutee" not in d.columns:
        if "va_du_taux_de_reussite_g" in d.columns:
            d["valeur_ajoutee"] = d["va_du_taux_de_reussite_g"]
        elif "va_de_la_note_g" in d.columns:
            d["valeur_ajoutee"] = d["va_de_la_note_g"]
    # Après avoir passé _to_snake et avant les agrégations :
    if "taux_reussite_g" not in d.columns and "taux_de_reussite_g" in d.columns:
        d["taux_reussite_g"] = pd.to_numeric(d["taux_de_reussite_g"], errors="coerce") 
    if "nb_candidats_total" not in d.columns:
        d["nb_candidats_total"] = d.get("nb_candidats_g", 0).fillna(0) + d.get("nb_candidats_p", 0).fillna(0)

    for c in ["academie", "region_academique", "departement", "commune", "secteur"]:
        if c in d.columns:
            d[c] = d[c].astype(str).str.strip().str.upper()

    if "session" in d.columns:
        d["session"] = pd.to_numeric(d["session"], errors="coerce").astype("Int64")
        d["session_str"] = d["session"].astype(str)
    
    if "row_id" not in d.columns and "num_ligne" in d.columns:
        d.rename(columns={"num_ligne": "row_id"}, inplace=True)

    return d


# data aggregation functions
def make_tables(df_raw: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Builds pre-aggregated tables used by the dashboard."""
    df = clean_ivac(df_raw.copy())

    # Return full cleaned data, not just latest session
    df_latest = df.copy()

    timeseries_cols = [c for c in ["taux_reussite_g", "valeur_ajoutee"] if c in df.columns]
    ts = pd.DataFrame()
    if timeseries_cols and "session_str" in df.columns:
        ts = (
            df.groupby("session_str")[timeseries_cols]
            .mean(numeric_only=True)
            .reset_index()
            .sort_values("session_str")
        )

    by_region = pd.DataFrame()
    if "region_academique" in df.columns and "session_str" in df.columns and timeseries_cols:
        by_region = (
            df.groupby(["region_academique", "session_str"])[timeseries_cols]
            .mean(numeric_only=True)
            .reset_index()
        )

    by_dep = pd.DataFrame()
    if "code_departement" in df_latest.columns:
        dep_metrics = [c for c in ["taux_reussite_g", "valeur_ajoutee", "nb_candidats_total"] if c in df_latest.columns]
        if dep_metrics:
            by_dep = df_latest.groupby(["code_departement", "departement"])[dep_metrics].mean(numeric_only=True).reset_index()

    return {
        "overview": df_latest,
        "timeseries": ts,
        "by_region": by_region,
        "by_departement": by_dep,
        "cleaned": df
    }


def compute_kpis(df_latest: pd.DataFrame) -> Tuple[str, str, str]:
    """Computes three simple KPIs from the latest session dataframe."""
    kpi1 = "N/A"
    if "taux_reussite_g" in df_latest.columns and not df_latest["taux_reussite_g"].empty:
        kpi1 = f"{df_latest['taux_reussite_g'].mean():.1f}%"

    kpi2 = "N/A"
    if "valeur_ajoutee" in df_latest.columns and not df_latest["valeur_ajoutee"].empty:
        kpi2 = f"{df_latest['valeur_ajoutee'].mean():+.1f}"

    kpi3 = "N/A"
    if "nb_candidats_total" in df_latest.columns and not df_latest["nb_candidats_total"].empty:
        kpi3 = f"{int(df_latest['nb_candidats_total'].sum()):,}".replace(",", " ")

    return kpi1, kpi2, kpi3

# profiling functions
def info_table(df: pd.DataFrame) -> pd.DataFrame:
    """Generates a summary table similar to df.info()."""
    return (pd.DataFrame({
        "Non-Null Count": df.notna().sum(),
        "Null Count": df.isna().sum(),
        "Dtype": df.dtypes.astype(str)
    })
    .assign(Null_Pct=lambda d: (d["Null Count"] / len(df) * 100).round(2))
    .sort_values(["Null_Pct", "Dtype"], ascending=[False, True]))

def validity_checks(df: pd.DataFrame) -> dict:
    """Performs data validity checks specific to the IVAC dataset."""
    issues = {}
    clean_df = clean_ivac(df.copy()) 

    if "taux_reussite_g" in clean_df.columns:
        bad = ~clean_df["taux_reussite_g"].between(0, 100) & clean_df["taux_reussite_g"].notna()
        if bad.any():
            issues["Invalid Success Rate (G)"] = clean_df.loc[bad]

    if "valeur_ajoutee" in clean_df.columns:
        bad = ~clean_df["valeur_ajoutee"].between(-50, 50) & clean_df["valeur_ajoutee"].notna()
        if bad.any():
            issues["Suspicious Value Added (out of [-50, 50] range)"] = clean_df.loc[bad]
    
    if "uai" in clean_df.columns:
        bad = (~clean_df["uai"].astype(str).str.match(r"^[0-9]{7}[A-Z]$", na=False)) & (clean_df["uai"].notna())
        if bad.any():
            issues["Invalid UAI Format"] = clean_df.loc[bad]

    if {"uai", "session"}.issubset(clean_df.columns):
        dup_mask = clean_df.duplicated(subset=["uai", "session"], keep=False)
        if dup_mask.any():
            issues["Duplicate entries (by UAI and Session)"] = clean_df.loc[dup_mask].sort_values(["uai", "session"])

    summary = {k: len(v) for k, v in issues.items()}
    return {"summary": summary, "frames": issues}

def profile_dataframe(df_raw: pd.DataFrame) -> dict:
    """Generates a basic profile of the raw dataframe."""
    df_clean = clean_ivac(df_raw.copy())
    return {
        "shape_rows": int(df_raw.shape[0]),
        "shape_cols": int(df_raw.shape[1]),
        "duplicates_raw": int(df_raw.duplicated().sum()),
        "standardized": df_clean,
        "info": info_table(df_clean),
        "validity": validity_checks(df_raw)
    }
    
# transformation diff functions
def diff_columns_breakdown(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> dict:
    """
    Returns a clean breakdown of column changes:
    - engineered: New columns in df_clean.
    - renamed: Mapping of old_raw_name -> new_clean_name.
    - dropped: Columns from raw that are not in clean.
    - unchanged: Columns with identical names.
    """
    raw_cols = list(df_raw.columns)
    clean_cols = list(df_clean.columns)

    norm_raw_to_original = { _to_snake(c): c for c in raw_cols }
    norm_raw_names = set(norm_raw_to_original.keys())
    clean_set = set(clean_cols)
    
    engineered = sorted(list(clean_set - norm_raw_names))
    dropped = sorted([c for c in raw_cols if _to_snake(c) not in clean_set])
    
    renamed = []
    for clean_name in clean_set:
        if clean_name in norm_raw_names:
            original_name = norm_raw_to_original[clean_name]
            if original_name != clean_name:
                renamed.append((original_name, clean_name))

    return {
        "engineered": engineered,
        "renamed": sorted(renamed),
        "dropped": dropped,
    }

#in
def impute_numeric(df: pd.DataFrame, cols: list[str], strategy: str = "median") -> pd.DataFrame:
    """Imputes missing numeric values."""
    d = df.copy()
    for c in cols:
        if c in d.columns:
            if strategy == "median":
                d[c] = d[c].fillna(d[c].median())
            elif strategy == "mean":
                d[c] = d[c].fillna(d[c].mean())
    return d

def impute_categorical(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Imputes missing categorical values with the mode."""
    d = df.copy()
    for c in cols:
        if c in d.columns:
            mode_val = d[c].mode()
            if not mode_val.empty:
                d[c] = d[c].fillna(mode_val.iloc[0])
    return d

def drop_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drops exact duplicate rows."""
    return df.drop_duplicates()

def drop_key_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drops duplicates based on the (UAI, Session) key."""
    if {"uai", "session"}.issubset(df.columns):
        return df.drop_duplicates(subset=["uai", "session"])
    return df