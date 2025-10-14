# verify_ivac.py
import pandas as pd
from utils.io import load_data
from utils.prep import clean_ivac, diff_columns_breakdown

# 1) Load raw
df_raw = load_data()
print("RAW shape:", df_raw.shape)

# 2) Clean
df_clean = clean_ivac(df_raw)
print("CLEAN shape:", df_clean.shape)

# 3) Columns diff
diff = diff_columns_breakdown(df_raw, df_clean)
print("Engineered columns:", diff["engineered"])
print("Renamed count:", len(diff["renamed"]))
print("Dropped columns:", diff["dropped"])

# 4) Sanity checks (prints + assertions)
print("\nHead (sorted by num_ligne):")
print(df_clean.head()[["num_ligne","session","uai","nom_de_l_etablissement"]])

# Numeric dtypes & missing ratios
num_checks = [
    "taux_de_reussite_g", "va_du_taux_de_reussite_g",
    "note_a_l_ecrit_g", "va_de_la_note_g",
    "nb_candidats_g", "nb_candidats_total"
]
for c in [x for x in num_checks if x in df_clean.columns]:
    print(f"{c:28s} dtype={df_clean[c].dtype}  missing={df_clean[c].isna().mean():.3f}")

# Sort & uniqueness
assert df_clean["num_ligne"].iloc[0] == 1, "num_ligne should start at 1 after cleaning/sort"
if {"uai","session"}.issubset(df_clean.columns):
    assert df_clean[["uai","session"]].drop_duplicates().shape[0] == len(df_clean), \
        "Duplicates on (uai, session) after cleaning"

print("\nOK ✅ Data load & cleaning look consistent.")