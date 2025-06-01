import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib
import os

# =====================
# Load metadata
# =====================
df = pd.read_csv("data/tmdb_bulk_movies.csv")  # jangan yang full atau popular


# =====================
# Preprocessing
# =====================
df.fillna('', inplace=True)

# Gabungkan informasi penting
def safe_concat(*cols):
    return ' '.join([str(c) for c in cols if c != '' and pd.notna(c)])

# Jika kolom tidak ada (karena kesalahan fetch), isi default
for col in ['title', 'overview', 'tagline', 'director', 'keywords', 'genre_names', 'production_companies']:
    if col not in df.columns:
        df[col] = ''

# Gabungkan menjadi satu kolom teks yang akan diproses TF-IDF
df['combined'] = df.apply(lambda x: safe_concat(
    x['title'],
    x['overview'],
    x['tagline'],
    x['director'],
    x['keywords'],
    x['genre_names'],
    x['production_companies']
), axis=1)

# =====================
# TF-IDF Vectorization
# =====================
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined'])

# =====================
# Cosine Similarity
# =====================
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# =====================
# Index berdasarkan judul (gunakan original_title jika ada)
# =====================
title_column = 'title'
if 'original_title' in df.columns:
    title_column = 'original_title'

indices = pd.Series(df.index, index=df[title_column].str.lower()).drop_duplicates()

# =====================
# Save model
# =====================
os.makedirs("Model", exist_ok=True)

joblib.dump(tfidf, 'Model/tfidf_metadata_vectorizer.pkl')
joblib.dump(tfidf_matrix, 'Model/tfidf_metadata_matrix.pkl')
joblib.dump(df, 'Model/metadata_df.pkl')
joblib.dump(indices, 'Model/metadata_indices.pkl')

print("\n✅ Model metadata berbasis konten berhasil dibuat dan disimpan!")
