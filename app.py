from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import datetime
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load datasets
# Update path to be relative to the script location
current_dir = os.path.dirname(os.path.abspath(__file__))
movies = pd.read_csv(os.path.join(current_dir, 'data', 'movies.csv'))
ratings = pd.read_csv(os.path.join(current_dir, 'data', 'ratings_small.csv'))


# Preprocess movie titles
def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

def clean_genres(genres):
    return ", ".join(genres.split('|'))

movies["clean_title"] = movies["title"].apply(clean_title)
movies['genres'] = movies['genres'].apply(clean_genres)


# Initialize TF-IDF for search functionality
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf = vectorizer.fit_transform(movies['clean_title'])

@app.route('/search', methods=['GET'])
def search():
    """
    Endpoint for searching movies based on partial titles.
    """
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])  # Return an empty list if no query is provided

    query = clean_title(query)
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]  # Get top 10 results
    results = movies.iloc[indices][::-1].to_dict(orient="records")  # Convert to list of dictionaries

    return jsonify(results)

@app.route('/recommend', methods=['GET'])
def recommend():
    """
    Endpoint for recommending movies based on a selected movie ID.
    """
    movie_id = request.args.get('movie_id', type=int)
    if movie_id is None:
        return jsonify({'error': 'movie_id is required'}), 400

    # Find users who rated the movie highly
    similar_users = ratings[(ratings['movieId'] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    
    # Find movies highly rated by similar users
    similar_user_recs = ratings[(ratings['userId'].isin(similar_users)) & (ratings['rating'] > 4)]['movieId']
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > 0.1]
    
    # Find ratings by all users for the recommended movies
    # This is done to ensure the movies we are recommending aren't just popular movies, rather movies specifically only rated highly by people similar to us. This gives more accurate recommendations
    all_users = ratings[(ratings['movieId'].isin(similar_user_recs.index)) & (ratings['rating'] > 4)]
    all_users_recs = all_users['movieId'].value_counts() / len(all_users['userId'].unique())
    
    # Calculate recommendation scores
    rec_percentages = pd.concat([similar_user_recs, all_users_recs], axis=1)
    rec_percentages.columns = ['similar', 'all']
    rec_percentages['score'] = rec_percentages['similar'] / rec_percentages['all']
    rec_percentages = rec_percentages.sort_values('score', ascending=False)
    
    # Merge with movie data and return the top 10 recommendations
    recommendations = rec_percentages.iloc[1:11].merge(movies, left_index=True, right_on='movieId')[['score', 'title', 'genres']]
    
    return recommendations.to_json(orient="records")

@app.route('/ping')
def ping():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[SERVER PING] Server pinged at: {current_time}")
    return jsonify({"status": "alive", "time": current_time}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
