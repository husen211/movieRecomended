import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib
import os

# Load metadata
df = pd.read_csv("data/movie_metadata.csv")

# Isi NaN dengan string kosong
df.fillna('', inplace=True)

# Gabungkan informasi penting untuk fitur
def combine_metadata(row):
    return ' '.join([
        str(row.get('original_title', '')),
        str(row.get('overview', '')),
        str(row.get('genres', '')),
        str(row.get('tagline', '')),
        str(row.get('director', '')),
        str(row.get('cast', '')),
        str(row.get('keywords', ''))
    ])

df['combined'] = df.apply(combine_metadata, axis=1)

# Vectorize pakai TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined'])

# Simpan model dan data
os.makedirs("Model", exist_ok=True)
joblib.dump(tfidf, "Model/tfidf_metadata_vectorizer.pkl")
joblib.dump(tfidf_matrix, "Model/tfidf_metadata_matrix.pkl")
joblib.dump(df, "Model/movies_metadata_df.pkl")
joblib.dump(pd.Series(df.index, index=df['original_title']).drop_duplicates(), "Model/metadata_indices.pkl")

print("✅ Model metadata berhasil dibuat dari movie_metadata.csv!")
