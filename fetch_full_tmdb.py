import requests
import pandas as pd
import os
import time
from tqdm import tqdm

API_KEY = "6558e76ee51c35514757da011de20d5a"
BASE_URL = "https://api.themoviedb.org/3"

endpoints = [
    "movie/popular",
    "movie/top_rated",
    "movie/now_playing",
    "movie/upcoming",
    "trending/movie/day"
]

os.makedirs("data", exist_ok=True)

def fetch_movies(endpoint):
    all_movies = []
    for page in range(1, 6):
        url = f"{BASE_URL}/{endpoint}?api_key={API_KEY}&language=en-US&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json().get("results", [])
        for item in data:
            all_movies.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "overview": item.get("overview"),
                "popularity": item.get("popularity"),
                "vote_average": item.get("vote_average"),
                "release_date": item.get("release_date"),
            })
        time.sleep(0.2)
    return all_movies

def get_genres():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    r = requests.get(url)
    genres = {}
    if r.status_code == 200:
        for g in r.json().get("genres", []):
            genres[g["id"]] = g["name"]
    return genres

def add_genres(movies, genre_map):
    results = []
    for m in tqdm(movies, desc="🛠️ Adding genres"):
        url = f"{BASE_URL}/movie/{m['id']}?api_key={API_KEY}&language=en-US"
        r = requests.get(url)
        if r.status_code == 200:
            genres = [g["name"] for g in r.json().get("genres", [])]
            m["genres"] = ", ".join(genres)
            results.append(m)
        time.sleep(0.25)
    return results

# Ambil semua data dari semua endpoint
all_movies = []
for ep in endpoints:
    print(f"🔄 Fetching from {ep}...")
    all_movies.extend(fetch_movies(ep))

# Hilangkan duplikat
df = pd.DataFrame(all_movies).drop_duplicates(subset="id")
genre_map = get_genres()
enhanced_movies = add_genres(df.to_dict(orient="records"), genre_map)

final_df = pd.DataFrame(enhanced_movies)
final_df.to_csv("data/tmdb_full_movies.csv", index=False)
print("✅ Data lengkap berhasil disimpan ke data/tmdb_full_movies.csv")
