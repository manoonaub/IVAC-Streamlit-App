# utils/io.py
from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

def _read_text_local(path: str | Path) -> str:
    """Read text from a local file handling potential UTF-8 BOM."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found at {path.resolve()}")
    # utf-8-sig removes BOM transparently if present
    return path.read_text(encoding="utf-8-sig")


def _read_text_url(url: str, timeout: int = 60) -> str:
    """Read text from a remote URL (CSV) with comprehensive error handling."""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.Timeout:
        raise ConnectionError(f"Timeout while fetching data from {url}")
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Could not connect to {url}")
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"HTTP error {e.response.status_code} when fetching {url}")


def _detect_header_index(raw_text: str) -> int:
    """
    Find the line index (0-based) where the real CSV header starts.
    We look for a line that contains both 'num_ligne' and 'session'
    (case-insensitive). If none is found, we assume header at 0.
    """
    lines = raw_text.splitlines()
    for i, line in enumerate(lines[:200]):  
        low = line.lower()
        if "num_ligne" in low and "session" in low:
            return i
    return 0


def _coerce_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply gentle typing and ensure a deterministic order:
    - num_ligne -> Int64 and sort ascending (if present)
    - Session/session -> Int64 (keeps friendly display with column_config)
    - UAI -> string trimmed
    """
    d = df.copy()

    if "num_ligne" in d.columns:
        d["num_ligne"] = pd.to_numeric(d["num_ligne"], errors="coerce").astype("Int64")
        d = d.sort_values("num_ligne").reset_index(drop=True)

    if "Session" in d.columns:
        d["Session"] = pd.to_numeric(d["Session"], errors="coerce").astype("Int64")
    if "session" in d.columns:
        d["session"] = pd.to_numeric(d["session"], errors="coerce").astype("Int64")

    if "UAI" in d.columns:
        d["UAI"] = d["UAI"].astype(str).str.strip()
    if "uai" in d.columns:
        d["uai"] = d["uai"].astype(str).str.strip()

    return d


@st.cache_data(show_spinner=False)
def load_data(
    path_or_url: str = "data/fr-en-indicateurs-valeur-ajoutee-colleges.csv",
    sep: str = ";",
) -> pd.DataFrame:
    """
    Robust CSV loader for the IVAC dataset.

    - Accepts a local path or an HTTP(S) URL
    - Handles UTF-8 BOM and stray lines before header
    - Uses `;` as the default separator (data.gouv.fr export)
    - Coerces useful dtypes and sorts by `num_ligne` (if present)
    - Cached with Streamlit for performance
    """
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        raw_text = _read_text_url(path_or_url)
    else:
        raw_text = _read_text_local(path_or_url)

    header_idx = _detect_header_index(raw_text)
    df = pd.read_csv(io.StringIO(raw_text), sep=sep, skiprows=header_idx, dtype=str)
    df = _coerce_and_sort(df)

    return df


@st.cache_data(show_spinner=False)
def fetch_csv(url: str, sep: str = ";", encoding: str = "utf-8") -> pd.DataFrame:
    """
    Simple network fetcher (no disk), cached by Streamlit.
    Use when you want *live* reads without storing the file.
    """
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return pd.read_csv(io.StringIO(resp.text), sep=sep, encoding=encoding)


def fetch_and_cache_to_disk(url: str, dest_path: str) -> str:
    """
    Download a file once and keep it on disk (idempotent).
    Returns the destination path as string.
    """
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return str(dest)
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    return str(dest)