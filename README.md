# C2_group2_Movie-Recommendation-System

# *Hybrid Movie Recommendation System*

This repository contains a hybrid movie recommendation system that integrates *TF–IDF–based content similarity, **mood filtering, **diversity control, **collaborative filtering, and **group recommendation*. The system is lightweight, modular, and suitable for deployment in real-world applications.

---

## 🚀 *Features*

### *1. Content-Based Recommendation (TF–IDF)*

* Uses multiple metadata fields:

  * Title
  * Overview
  * Tagline
  * Genres
  * Cast (Top 3 actors)
  * Director
  * Keywords
* Converts text into TF–IDF vectors (5000 features)
* Computes similarity using *cosine similarity*

### *2. Mood-Based Filtering*

* Built-in moods:
  *action, thriller, romantic, chill, funny, deep*
* Maps each mood to:

  * A set of genres
  * A list of descriptive keywords
* Assigns movies to moods using a scoring mechanism

### *3. Diversity Control*

* Parameter range: *0–100*
* 0 → Very similar movies
* 100 → Highly exploratory movies
* Adds controlled noise to similarity scores to increase novelty

### *4. Collaborative Filtering (Optional)*

* Uses user → movie rating dictionaries
* Computes similarities using Pearson correlation
* Predicts ratings for unseen movies
* Generates collaborative-based recommendations

### *5. Hybrid Recommendation*

Combines:

* Content score
* Collaborative score
* Weighted fusion:

  
  hybrid_score = w_content * content_score + w_collab * collab_score
  

### *6. Group Recommendation*

* Accepts multiple users’ favorite movies
* Merges preferences and generates group-friendly suggestions

---

## 📂 *Project Structure*


│── MovieRecommender.py      # Main class containing all modules
│── tmdb_5000_movies.csv     # Movie metadata dataset
│── tmdb_5000_credits.csv    # Cast & crew dataset
│── README.md


---

## 🧠 *How It Works*

### *1. Data Preprocessing*

* Loads and merges TMDB movies & credits datasets
* Safely parses JSON fields (genres, cast, crew, keywords)
* Extracts top actors and director
* Constructs combined text features

### *2. Vectorization*

* Applies *TF–IDF* with 5000 tokens
* Computes cosine similarity matrix between all movies

### *3. Recommendation Pipeline*


Input movies → Similarity Ranking → Mood Filter → Diversity Adjustment → Final Recommendations


### *4. Hybrid Pipeline*


Content-Based Score
        +               
Collaborative Score    
        ↓
Weighted Fusion → Ranked Output


---

## 🛠 *Usage*

python
from MovieRecommender import MovieRecommender

rec = MovieRecommender()

favorites = ["Avatar", "Inception"]
recommendations = rec.get_recommendations(favorites, top_n=10, mood="action", diversity=40)

for r in recommendations:
    print(r["title"], r["score"], r["moods"])


### *Group Recommendation*

python
group_favs = ["Avatar", "The Dark Knight", "La La Land"]
rec.get_group_recommendations(group_favs, top_n=10)


### *Hybrid Recommendation*

python
user_ratings = {"Inception": 5, "Interstellar": 4}
other_users = {
    "user1": {"Inception": 5, "Avatar": 3},
    "user2": {"Interstellar": 4, "Titanic": 5}
}

rec.get_hybrid_recommendations(
    favorite_movies=["Inception"],
    user_ratings=user_ratings,
    all_users_ratings=other_users,
    top_n=10,
    content_weight=0.6
)


---

## 📊 *Metrics Included*

* Genre diversity score
* User taste compatibility
* Mood classification score

---

## 📈 *Future Improvements*

* Integrating BERT/Sentence Transformers
* Neural collaborative filtering (NCF)
* Automatic mood detection via sentiment analysis
* Real-time adaptive personalization
* Fairness-aware group recommendation

---

## 📜 *License*

This project is open for academic and personal use.

---
