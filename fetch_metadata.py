import requests
import pandas as pd
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

# Load API key dari .env
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise Exception("❌ API key tidak ditemukan. Pastikan sudah diatur di file .env dengan TMDB_API_KEY=your_key")

# Load movie IDs dari file sebelumnya
df = pd.read_csv("data/tmdb_full_movies.csv")
movie_ids = df["id"].dropna().astype(int).unique()

metadata = []

print("🔄 Ambil metadata tambahan (sutradara, tagline, dll)...")
for movie_id in tqdm(movie_ids):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=credits"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            director = ""
            if "credits" in data:
                crew = data["credits"].get("crew", [])
                directors = [person["name"] for person in crew if person["job"] == "Director"]
                director = directors[0] if directors else ""

            metadata.append({
                "id": movie_id,
                "title": data.get("title", ""),
                "overview": data.get("overview", ""),
                "genres": ", ".join([genre["name"] for genre in data.get("genres", [])]),
                "tagline": data.get("tagline", ""),
                "release_date": data.get("release_date", ""),
                "director": director
            })
        else:
            time.sleep(0.2)  # delay biar aman
    except Exception as e:
        print(f"⚠️ Gagal ambil ID {movie_id}: {e}")
        continue

# Simpan hasilnya
if metadata:
    df_meta = pd.DataFrame(metadata)
    os.makedirs("data", exist_ok=True)
    df_meta.to_csv("data/movie_metadata.csv", index=False)
    print("✅ Metadata berhasil disimpan ke data/movie_metadata.csv")
else:
    print("❌ Tidak ada metadata yang berhasil diambil.")
