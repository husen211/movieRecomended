import pandas as pd
import joblib
import os
from sentence_transformers import SentenceTransformer

# Load data dari CSV
df = pd.read_csv("data/tmdb_bulk_movies.csv")

# Pastikan kolom-kolom penting tetap ada
needed_cols = ['id', 'title', 'overview', 'genres', 'tagline', 'release_date', 'poster_path']
for col in needed_cols:
    if col not in df.columns:
        df[col] = ''

# Isi NaN
df.fillna('', inplace=True)

# Kolom tambahan jika ada metadata lanjutan
for meta_col in ['director', 'keywords', 'genre_names', 'production_companies']:
    if meta_col not in df.columns:
        df[meta_col] = ''

# Gabungkan konten
def safe_concat(*cols):
    return ' '.join([str(c) for c in cols if c != '' and pd.notna(c)])

df['combined'] = df.apply(lambda x: safe_concat(
    x['title'], x['overview'], x['tagline'],
    x['director'], x['keywords'], x['genre_names'], x['production_companies']
), axis=1)

# Load dan encode dengan BERT
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['combined'], show_progress_bar=True)

# Save model dan data
os.makedirs("Model", exist_ok=True)
joblib.dump(embeddings, 'Model/bert_embeddings.pkl')
joblib.dump(df, 'Model/bert_df.pkl')  # <- Sekarang df ini udah ada 'poster_path'
joblib.dump(pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates(), 'Model/bert_indices.pkl')

print("✅ Model berbasis BERT berhasil dibuat dan disimpan dengan poster_path!")
