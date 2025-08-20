import os
import sys
import pandas as pd
from rapidfuzz import fuzz
from deep_translator import GoogleTranslator

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# File setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "crops.xlsx")   # expects crops.xlsx in same folder

# Column names from your Excel
COL_EN = "cropName"           # English crop name
COL_VERN = "vernacular_name"  # Hindi / Hinglish name

# Load Excel
try:
    df = pd.read_excel(FILE_PATH, sheet_name=0)
    print(f"✅ Loaded Excel file: {FILE_PATH}")
except FileNotFoundError:
    print(f"❌ File not found at: {FILE_PATH}")
    exit(1)

# Check columns
if COL_EN not in df.columns or COL_VERN not in df.columns:
    print(f"❌ Required columns not found. Available: {list(df.columns)}")
    exit(1)

print("✅ Columns detected, starting comparison...")

# Translator setup with caching
translator = GoogleTranslator(source='auto', target='en')
translation_cache = {}

def translate_cached(text):
    """Translate with caching to avoid duplicate calls."""
    if text in translation_cache:
        return translation_cache[text]
    try:
        translated = translator.translate(text)
    except Exception:
        translated = text  # fallback if translation fails
    translation_cache[text] = translated
    return translated

# Compare English vs Translated Vernacular
results = []
for idx, row in df.iterrows():
    en_name = str(row[COL_EN]).strip() if pd.notna(row[COL_EN]) else ""
    vern_name = str(row[COL_VERN]).strip() if pd.notna(row[COL_VERN]) else ""

    if en_name and vern_name:
        vern_translated = translate_cached(vern_name)
        similarity = fuzz.WRatio(en_name, vern_translated)
        results.append({
            "Row": idx + 2,
            "English": en_name,
            "Vernacular": vern_name,
            "Translated": vern_translated,
            "Similarity": similarity
        })

# Convert to DataFrame
comparison_df = pd.DataFrame(results)

# Save mismatches (e.g. < 70% similarity)
mismatches = comparison_df[comparison_df["Similarity"] < 70]
output_file = os.path.join(BASE_DIR, "comparison_results.xlsx")
with pd.ExcelWriter(output_file) as writer:
    comparison_df.to_excel(writer, sheet_name="All_Comparisons", index=False)
    mismatches.to_excel(writer, sheet_name="Mismatches", index=False)

print(f"✅ Comparison complete. Results saved to: {output_file}")
print("ℹ️ Mismatches (Similarity < 70%) preview:")
print(mismatches.head())
