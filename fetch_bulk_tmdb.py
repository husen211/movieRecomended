import os
import requests
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# Load API key dari .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Config
BASE_URL = "https://api.themoviedb.org/3"
CSV_PATH = "data/tmdb_bulk_movies.csv"

# Endpoint yang akan diambil
endpoints = [
    "movie/popular",
    "movie/top_rated",
    "movie/now_playing",
    "movie/upcoming",
    "trending/movie/day"
]

# Ambil data dari semua endpoint
all_movies = []
print("🎬 Mengambil data film dari TMDb...")
for endpoint in endpoints:
    print(f"🔄 Fetching from {endpoint}...")
    for page in tqdm(range(1, 20)):  # Bisa dinaikkan hingga 500
        url = f"{BASE_URL}/{endpoint}"
        params = {
            "api_key": API_KEY,
            "page": page
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            results = res.json().get("results", [])
            all_movies.extend(results)
        else:
            print(f"⚠️ Gagal fetch page {page} dari {endpoint}: {res.status_code}")
            break

# Buang duplikat
df = pd.DataFrame(all_movies)
df.drop_duplicates(subset="id", inplace=True)

# Simpan ke CSV
os.makedirs("data", exist_ok=True)
df.to_csv(CSV_PATH, index=False)
print(f"\n✅ Berhasil menyimpan {len(df)} film ke {CSV_PATH}")
