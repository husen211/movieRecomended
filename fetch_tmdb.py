import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Load API Key dari .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def fetch_popular_movies(pages=5):
    movie_list = []

    for page in range(1, pages + 1):
        res = requests.get(
            f"{BASE_URL}/movie/popular",
            params={"language": "en-US", "page": page},
            headers=HEADERS
        )

        if res.status_code != 200:
            print("Gagal ambil data halaman", page)
            continue

        for movie in res.json()["results"]:
            movie_list.append({
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie.get("overview", ""),
                "rating": movie.get("vote_average", 0),
                "release_date": movie.get("release_date", ""),
                "popularity": movie.get("popularity", 0)
            })

        time.sleep(0.2)

    return pd.DataFrame(movie_list)

if __name__ == "__main__":
    df = fetch_popular_movies(10)
    df.to_csv("data/popular_movies.csv", index=False)
    print("✅ Selesai ambil data, simpan ke data/popular_movies.csv")
