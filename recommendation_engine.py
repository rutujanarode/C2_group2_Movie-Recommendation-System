import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import ast
import re
from datetime import datetime

class MovieRecommender:

    # Mood-based keyword mapping
    MOOD_KEYWORDS = {
        'chill': {
            'genres': ['Documentary', 'Music', 'Family'],
            'keywords': ['calm', 'peaceful', 'relaxing', 'gentle', 'soothing', 'nature', 'journey']
        },
        'thriller': {
            'genres': ['Thriller', 'Horror', 'Mystery', 'Crime'],
            'keywords': ['suspense', 'dark', 'twisted', 'murder', 'investigation', 'tension', 'fear']
        },
        'funny': {
            'genres': ['Comedy'],
            'keywords': ['funny', 'hilarious', 'humor', 'laugh', 'comedy', 'amusing', 'witty']
        },
        'deep': {
            'genres': ['Drama', 'History', 'War'],
            'keywords': ['emotional', 'profound', 'philosophical', 'meaningful', 'thought-provoking', 'complex']
        },
        'action': {
            'genres': ['Action', 'Adventure', 'Science Fiction'],
            'keywords': ['explosive', 'fast-paced', 'intense', 'battle', 'fight', 'chase', 'adrenaline']
        },
        'romantic': {
            'genres': ['Romance'],
            'keywords': ['love', 'relationship', 'romantic', 'heartwarming', 'passion', 'couple']
        }
    }

    # Context-based preferences
    CONTEXT_PREFERENCES = {
        'weather': {
            'Rainy': {'moods': ['chill', 'deep', 'romantic'], 'boost': 1.2},
            'Sunny': {'moods': ['action', 'funny', 'romantic'], 'boost': 1.15},
            'Cold': {'moods': ['chill', 'deep', 'thriller'], 'boost': 1.1},
            'Hot': {'moods': ['action', 'funny'], 'boost': 1.1},
            'Cloudy': {'moods': ['deep', 'thriller'], 'boost': 1.05}
        },
        'day': {
            'Monday': {'moods': ['funny', 'action'], 'boost': 1.1},
            'Tuesday': {'moods': ['deep', 'chill'], 'boost': 1.05},
            'Wednesday': {'moods': ['funny', 'action'], 'boost': 1.1},
            'Thursday': {'moods': ['romantic', 'chill'], 'boost': 1.05},
            'Friday': {'moods': ['action', 'funny', 'thriller'], 'boost': 1.15},
            'Saturday': {'moods': ['action', 'romantic', 'funny'], 'boost': 1.2},
            'Sunday': {'moods': ['chill', 'deep', 'romantic'], 'boost': 1.15}
        },
        'time_of_day': {
            'Morning': {'moods': ['chill', 'funny'], 'boost': 1.1},
            'Afternoon': {'moods': ['action', 'funny'], 'boost': 1.1},
            'Evening': {'moods': ['romantic', 'deep'], 'boost': 1.15},
            'Night': {'moods': ['thriller', 'deep', 'action'], 'boost': 1.2}
        }
    }

    def __init__(self, movies_csv="tmdb_5000_movies.csv", credits_csv="tmdb_5000_credits.csv"):
        # Load datasets
        movies = pd.read_csv(movies_csv, low_memory=False)
        credits = pd.read_csv(credits_csv, low_memory=False)

        # Merge both on title
        self.df = movies.merge(credits, left_on='title', right_on='title', how='left')

        # Safe parsing functions
        def safe_parse_names(x):
            if pd.isna(x):
                return []
            try:
                return [d['name'] for d in ast.literal_eval(str(x))]
            except Exception:
                return []

        def safe_parse_director(x):
            if pd.isna(x):
                return []
            try:
                data = ast.literal_eval(str(x))
                return [d['name'] for d in data if d.get('job') == 'Director']
            except Exception:
                return []

        # Apply safe parsing
        self.df['genres'] = self.df['genres'].apply(safe_parse_names)
        self.df['cast'] = self.df['cast'].apply(lambda x: safe_parse_names(x)[:3])
        self.df['crew'] = self.df['crew'].apply(safe_parse_director)
        self.df['keywords'] = self.df['keywords'].apply(safe_parse_names)
        self.df['production_companies'] = self.df['production_companies'].apply(safe_parse_names)

        # Combine important text features
        self.df['combined_features'] = (
            self.df['title'].fillna('') + " " +
            self.df['overview'].fillna('') + " " +
            self.df['tagline'].fillna('') + " " +
            self.df['genres'].apply(lambda x: " ".join(x)) + " " +
            self.df['cast'].apply(lambda x: " ".join(x)) + " " +
            self.df['crew'].apply(lambda x: " ".join(x)) + " " +
            self.df['keywords'].apply(lambda x: " ".join(x))
        )

        # TF-IDF vectorization
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['combined_features'])

        # Initialize KNN model (using cosine distance)
        print("🔧 Training KNN model...")
        self.knn = NearestNeighbors(
            n_neighbors=min(50, len(self.df)),  # Ensure we don't exceed dataset size
            metric='cosine',
            algorithm='brute'
        )
        self.knn.fit(self.tfidf_matrix)
        print("✅ KNN model ready!")

    # ---------------------------------------------------------------
    # Context Helper Functions
    # ---------------------------------------------------------------
    def get_time_of_day(self):
        """Auto-detect time of day"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"

    def get_current_day(self):
        """Get current day of week"""
        return datetime.now().strftime("%A").lower()

    # ---------------------------------------------------------------
    # Mood Classification
    # ---------------------------------------------------------------
    def classify_mood(self, movie_idx):
        """Classify a movie's mood based on genres and overview"""
        row = self.df.iloc[movie_idx]
        genres = row['genres']
        overview = str(row['overview']).lower()
        
        mood_scores = {}
        for mood, criteria in self.MOOD_KEYWORDS.items():
            score = 0
            # Genre matching (higher weight)
            for genre in genres:
                if genre in criteria['genres']:
                    score += 3
            
            # Keyword matching in overview
            for keyword in criteria['keywords']:
                if keyword in overview:
                    score += 1
            
            mood_scores[mood] = score
        
        return mood_scores

    def get_movie_moods(self, movie_idx):
        """Get top moods for a movie"""
        mood_scores = self.classify_mood(movie_idx)
        valid_moods = {k: v for k, v in mood_scores.items() if v > 0}
        return sorted(valid_moods.items(), key=lambda x: x[1], reverse=True)

    # ---------------------------------------------------------------
    # KNN-based Recommendations with Context
    # ---------------------------------------------------------------
    def get_recommendations(self, movie_titles, top_n=10, mood=None, diversity=50, 
                           weather=None, day=None, time_of_day=None, auto_context=False):
        """
        Get KNN-based recommendations with mood, diversity, and context filtering
        
        Args:
            movie_titles: List of favorite movie titles
            top_n: Number of recommendations
            mood: Filter by mood
            diversity: 0-100, exploration level
            weather: Weather condition for context
            day: Day of week for context
            time_of_day: Time of day for context
            auto_context: Auto-detect time and day
        """
        if not movie_titles:
            return []

        # Auto-detect context if enabled
        if auto_context:
            if time_of_day is None:
                time_of_day = self.get_time_of_day()
            if day is None:
                day = self.get_current_day()

        valid_indices = []
        for title in movie_titles:
            matches = self.df[self.df['title'].str.lower() == str(title).lower()]
            if not matches.empty:
                valid_indices.append(matches.index[0])

        if not valid_indices:
            return []

        # Get KNN neighbors for all input movies
        all_distances = []
        all_indices = []
        
        for idx in valid_indices:
            # Get more neighbors for diversity control
            n_neighbors = min(top_n * 5, len(self.df))
            distances, indices = self.knn.kneighbors(
                self.tfidf_matrix[idx], 
                n_neighbors=n_neighbors
            )
            all_distances.append(distances[0])
            all_indices.append(indices[0])

        # Combine and score results
        movie_scores = {}
        for distances, indices in zip(all_distances, all_indices):
            for dist, idx in zip(distances, indices):
                if idx not in valid_indices:
                    # Convert distance to similarity (1 - distance for cosine)
                    similarity = 1 - dist
                    
                    if idx in movie_scores:
                        movie_scores[idx] = max(movie_scores[idx], similarity)
                    else:
                        movie_scores[idx] = similarity

        # Apply diversity adjustment
        if diversity > 50:
            diversity_factor = (diversity - 50) / 50
            for idx in movie_scores:
                noise = np.random.random() * diversity_factor * 0.3
                movie_scores[idx] = movie_scores[idx] * (1 - diversity_factor * 0.5) + noise

        # Sort by score
        sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)

        # Apply context boosting
        context_boost = {}
        if weather or day or time_of_day:
            for idx, score in sorted_movies:
                boost = 1.0
                movie_moods = [m[0] for m in self.get_movie_moods(idx)]
                
                if weather and weather in self.CONTEXT_PREFERENCES['weather']:
                    prefs = self.CONTEXT_PREFERENCES['weather'][weather]
                    if any(m in prefs['moods'] for m in movie_moods):
                        boost *= prefs['boost']
                
                if day and day.title() in self.CONTEXT_PREFERENCES['day']:
                    prefs = self.CONTEXT_PREFERENCES['day'][day.title()]
                    if any(m in prefs['moods'] for m in movie_moods):
                        boost *= prefs['boost']
                
                if time_of_day and time_of_day.title() in self.CONTEXT_PREFERENCES['time_of_day']:
                    prefs = self.CONTEXT_PREFERENCES['time_of_day'][time_of_day.title()]
                    if any(m in prefs['moods'] for m in movie_moods):
                        boost *= prefs['boost']
                
                context_boost[idx] = boost

        # Build recommendations
        recommendations = []
        for idx, score in sorted_movies:
            if idx not in valid_indices:
                # Apply mood filter
                if mood:
                    movie_moods = self.get_movie_moods(idx)
                    mood_names = [m[0] for m in movie_moods]
                    if mood not in mood_names:
                        continue

                # Apply context boost
                final_score = score
                context_tag = ""
                if idx in context_boost and context_boost[idx] > 1.0:
                    final_score *= context_boost[idx]
                    context_tag = "🌟 Perfect for now!"

                movie_moods = self.get_movie_moods(idx)
                mood_str = ", ".join([f"{m[0]} ({m[1]})" for m in movie_moods[:2]]) if movie_moods else "N/A"
                
                recommendations.append({
                    'title': self.df.iloc[idx]['title'],
                    'genres': ", ".join(self.df.iloc[idx]['genres']),
                    'score': round(float(final_score) * 100, 1),
                    'moods': mood_str,
                    'overview': str(self.df.iloc[idx]['overview'])[:150] + "...",
                    'context_tags': context_tag
                })
            
            if len(recommendations) >= top_n:
                break
        
        return recommendations

    # ---------------------------------------------------------------
    # Taste Compatibility (KNN-based)
    # ---------------------------------------------------------------
    def calculate_taste_compatibility(self, user1_movies, user2_movies):
        """Calculate compatibility using KNN distances"""
        if not user1_movies or not user2_movies:
            return 0
        
        user1_indices = []
        user2_indices = []
        
        for title in user1_movies:
            matches = self.df[self.df['title'].str.lower() == str(title).lower()]
            if not matches.empty:
                user1_indices.append(matches.index[0])
        
        for title in user2_movies:
            matches = self.df[self.df['title'].str.lower() == str(title).lower()]
            if not matches.empty:
                user2_indices.append(matches.index[0])
        
        if not user1_indices or not user2_indices:
            return 0
        
        # Calculate average KNN distance between users' movies
        similarities = []
        for idx1 in user1_indices:
            distances, _ = self.knn.kneighbors(self.tfidf_matrix[idx1], n_neighbors=len(self.df))
            for idx2 in user2_indices:
                pos = np.where(_ == idx2)[1]
                if len(pos) > 0:
                    similarity = 1 - distances[0][pos[0]]
                    similarities.append(similarity)
        
        avg_similarity = np.mean(similarities) if similarities else 0
        return round(float(avg_similarity) * 100, 1)

    # ---------------------------------------------------------------
    # Genre Diversity Score
    # ---------------------------------------------------------------
    def calculate_genre_diversity(self, movie_titles):
        """Calculate how diverse a user's movie taste is (0-100)"""
        if not movie_titles:
            return 0
        
        all_genres = []
        for title in movie_titles:
            matches = self.df[self.df['title'].str.lower() == str(title).lower()]
            if not matches.empty:
                all_genres.extend(matches.iloc[0]['genres'])
        
        if not all_genres:
            return 0
        
        unique_genres = len(set(all_genres))
        total_possible_genres = 20
        
        diversity_score = min((unique_genres / total_possible_genres) * 100, 100)
        return round(diversity_score, 1)

    # ---------------------------------------------------------------
    # Search Methods
    # ---------------------------------------------------------------
    def search_movies(self, query="", actor="", company="", genre=""):
        """Advanced search with multiple filters"""
        result = self.df.copy()
        
        if query:
            query = query.lower().strip()
            result = result[result['title'].str.lower().str.contains(query, na=False)]
        
        if actor:
            actor = actor.lower().strip()
            result = result[result['cast'].apply(
                lambda cast_list: any(actor in c.lower() for c in cast_list)
            )]
        
        if company:
            company = company.lower().strip()
            if 'production_companies' in result.columns:
                def company_match(companies):
                    try:
                        return any(company in c.lower() for c in companies)
                    except:
                        return False
                result = result[result['production_companies'].apply(company_match)]
        
        if genre:
            genre = genre.lower().strip()
            result = result[result['genres'].apply(
                lambda genres: any(genre in g.lower() for g in genres)
            )]
        
        columns = ['title', 'genres']
        if 'cast' in result.columns:
            columns.append('cast')
        if 'production_companies' in result.columns:
            columns.append('production_companies')
        
        return result[columns].to_dict(orient='records')

    def search_by_actor(self, actor_name):
        """Return movies where the actor appears"""
        return self.search_movies(actor=actor_name)

    def search_by_production_company(self, company_name):
        """Return movies produced by the company"""
        return self.search_movies(company=company_name)

    def get_group_recommendations(self, all_favorite_movies, top_n=10, mood=None, diversity=50):
        """Get recommendations for group"""
        if not all_favorite_movies:
            return []
        unique_movies = list(set(all_favorite_movies))
        return self.get_recommendations(unique_movies, top_n, mood, diversity)

    def get_movie_by_title(self, title):
        """Get movie details by title"""
        match = self.df[self.df['title'].str.lower() == str(title).lower()]
        if not match.empty:
            row = match.iloc[0]
            return {
                'title': row['title'],
                'genres': ", ".join(row['genres'])
            }
        return None

    def get_collaborative_recommendations(self, user_ratings, all_users_ratings, top_n=10):
        """Collaborative filtering based on user ratings"""
        if not user_ratings or not all_users_ratings:
            return []

        user_rated_movies = set(user_ratings.keys())
        similar_users = []

        for other_user_id, other_ratings in all_users_ratings.items():
            common_movies = user_rated_movies.intersection(set(other_ratings.keys()))
            if len(common_movies) >= 2:
                user_scores = [user_ratings[m] for m in common_movies]
                other_scores = [other_ratings[m] for m in common_movies]
                
                correlation = np.corrcoef(user_scores, other_scores)[0, 1]
                if not np.isnan(correlation) and correlation > 0:
                    similar_users.append((other_user_id, correlation, other_ratings))

        if not similar_users:
            return []

        similar_users.sort(key=lambda x: x[1], reverse=True)

        movie_scores = {}
        movie_weights = {}
        
        for _, similarity, other_ratings in similar_users[:5]:
            for movie, rating in other_ratings.items():
                if movie not in user_rated_movies:
                    movie_scores[movie] = movie_scores.get(movie, 0) + rating * similarity
                    movie_weights[movie] = movie_weights.get(movie, 0) + similarity

        recommendations = []
        for movie in movie_scores:
            if movie_weights[movie] > 0:
                predicted_rating = movie_scores[movie] / movie_weights[movie]
                movie_info = self.get_movie_by_title(movie)
                if movie_info:
                    recommendations.append({
                        'title': movie,
                        'genres': movie_info['genres'],
                        'score': round(predicted_rating * 20, 1),
                        'predicted_rating': round(predicted_rating, 1)
                    })

        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]

    def get_hybrid_recommendations(self, favorite_movies, user_ratings, all_users_ratings, 
                                   top_n=10, content_weight=0.6, mood=None, diversity=50,
                                   weather=None, day=None, time_of_day=None):
        """Hybrid: KNN + Collaborative filtering"""
        content_recs = self.get_recommendations(favorite_movies, top_n * 2, mood, diversity,
                                               weather, day, time_of_day)
        collab_recs = self.get_collaborative_recommendations(user_ratings, all_users_ratings, top_n * 2)

        combined_scores = {}
        
        for rec in content_recs:
            combined_scores[rec['title']] = {
                'content_score': rec['score'],
                'collab_score': 0,
                'genres': rec['genres'],
                'moods': rec.get('moods', 'N/A')
            }

        for rec in collab_recs:
            if rec['title'] in combined_scores:
                combined_scores[rec['title']]['collab_score'] = rec['score']
            else:
                combined_scores[rec['title']] = {
                    'content_score': 0,
                    'collab_score': rec['score'],
                    'genres': rec['genres'],
                    'moods': 'N/A'
                }

        recommendations = []
        collab_weight = 1 - content_weight
        
        for title, scores in combined_scores.items():
            hybrid_score = (scores['content_score'] * content_weight + 
                          scores['collab_score'] * collab_weight)
            recommendations.append({
                'title': title,
                'genres': scores['genres'],
                'score': round(hybrid_score, 1),
                'content_score': round(scores['content_score'], 1),
                'collab_score': round(scores['collab_score'], 1),
                'moods': scores['moods']
            })

        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]

    def get_genre_distribution(self, movie_titles):
        """Get genre distribution from movies"""
        genre_counts = {}
        for title in movie_titles:
            movie_data = self.get_movie_by_title(title)
            if movie_data:
                genres = [g.strip() for g in str(movie_data['genres']).split(',')]
                for genre in genres:
                    if genre and genre != 'nan':
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1
        return genre_counts