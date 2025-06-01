from flask import Flask, request, render_template
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from rapidfuzz import process

app = Flask(__name__)

# Load model BERT
bert_embeddings = joblib.load('Model/bert_embeddings.pkl')
df = joblib.load('Model/bert_df.pkl')
indices = joblib.load('Model/bert_indices.pkl')

# Load SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_recommendations_bert(title, top_n=10):
    best_match = process.extractOne(title.lower(), indices.index, score_cutoff=60)
    if not best_match:
        return None, None

    matched_title = best_match[0]
    idx = indices[matched_title]

    query_embedding = bert_embeddings[idx].reshape(1, -1)
    sim_scores = list(enumerate(cosine_similarity(query_embedding, bert_embeddings)[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

    results = []
    for i, score in sim_scores:
        poster_path = df.iloc[i].get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        movie = {
            'title': df.iloc[i].get('title', 'No title'),
            'score': round(score * 100, 2),
            'overview': df.iloc[i].get('overview', 'No overview available'),
            'poster_url': poster_url
        }
        results.append(movie)

    return results, matched_title

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title', '')
    if not title:
        return render_template('index.html', error="Masukkan judul film terlebih dahulu.")

    recommendations, matched = get_recommendations_bert(title)
    if not recommendations:
        return render_template('index.html', error=f'Film "{title}" tidak ditemukan.')

    return render_template('index.html', recommendations=recommendations, title_input=title, matched_title=matched)

if __name__ == '__main__':
    app.run(debug=True)
