# import streamlit as st
# import pyrebase
# import json
# from datetime import datetime
# import firebase_admin
# from firebase_admin import credentials, firestore
# import numpy as np
# import pandas as pd
# import random
# import string
# import plotly.express as px
# import plotly.graph_objects as go
# from recommendation_engine import MovieRecommender
# import os
# from google.cloud import firestore
# from firebase_admin import credentials, firestore  
# from heuristic_selector import HeuristicMovieSelector, extract_user_preferences
# st.set_page_config(
#     page_title="🎬 College Movie Recommender",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("""
# <style>
#     .compatibility-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 12px;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#         border-left: 5px solid #667eea;
#     }
    
#     .mood-badge {
#         display: inline-block;
#         padding: 0.25rem 0.75rem;
#         border-radius: 15px;
#         font-size: 0.85rem;
#         font-weight: 500;
#         margin: 0.25rem;
#     }
    
#     .mood-chill { background: #E3F2FD; color: #1976D2; }
#     .mood-thriller { background: #FCE4EC; color: #C2185B; }
#     .mood-funny { background: #FFF9C4; color: #F57F17; }
#     .mood-deep { background: #F3E5F5; color: #7B1FA2; }
#     .mood-action { background: #FFEBEE; color: #D32F2F; }
#     .mood-romantic { background: #FFE0E9; color: #E91E63; }


#     .main .block-container {
#         padding: 1rem 2rem;
#         max-width: 1200px;
#         margin: 0 auto;
#     }
    
#     @media (max-width: 768px) {
#         .main .block-container {
#             padding: 0.5rem 1rem;
#         }
        
#         .stButton button {
#             width: 100%;
#             margin: 0.25rem 0;
#         }
        
#         .stTextInput input {
#             font-size: 16px !important;
#         }
#     }
    
#     .movie-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem;
#         border-radius: 15px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin-bottom: 1rem;
#         color: white;
#     }
    
#     .info-card {
#         background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 1rem 0;
#         color: white;
#         text-align: center;
#     }
    
#     .group-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 12px;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         margin: 1rem 0;
#         border-left: 4px solid #667eea;
#     }
    
#     .main-header {
#         text-align: center;
#         padding: 2rem 0;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         border-radius: 15px;
#         margin-bottom: 2rem;
#         color: white;
#     }
    
#     .user-id-badge {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 0.75rem 1.5rem;
#         border-radius: 25px;
#         display: inline-block;
#         font-weight: bold;
#         font-size: 1.1rem;
#         margin: 1rem 0;
#         box-shadow: 0 4px 8px rgba(0,0,0,0.15);
#     }
    
#     .movie-item {
#         background: #f8f9fa;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 0.5rem 0;
#         transition: all 0.2s ease;
#     }
    
#     .movie-item:hover {
#         background: #e9ecef;
#         transform: translateX(5px);
#     }
    
#     .recommendation-card {
#         background: white;
#         padding: 1rem;
#         border-radius: 10px;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.1);
#         margin: 0.5rem 0;
#         border-left: 4px solid #667eea;
#     }
    
#     .filter-box {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 1rem 0;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#     }
    
#     @media (max-width: 768px) {
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         header {visibility: hidden;}
#     }
# </style>
# """, unsafe_allow_html=True)

# if not os.path.exists("firebase_config.json"):
#     st.error("⚠️ Firebase configuration missing! Please create `firebase_config.json` file.")
#     st.stop()

# if not os.path.exists("serviceAccountKey.json"):
#     st.error("⚠️ Service account key missing! Please download `serviceAccountKey.json` from Firebase Console.")
#     st.stop()

# with open("firebase_config.json") as f:
#     firebaseConfig = json.load(f)

# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()

# cred = credentials.Certificate("serviceAccountKey.json")
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred)
# db = firestore.client()

# @st.cache_resource
# def load_recommender():
#     return MovieRecommender("tmdb_5000_movies.csv", "tmdb_5000_credits.csv")

# recommender = load_recommender()
# movies_df = pd.read_csv("tmdb_5000_movies.csv", low_memory=False)

# def generate_user_id():
#     while True:
#         user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#         existing = db.collection("user_ids").document(user_id).get()
#         if not existing.exists:
#             return user_id

# def get_username_by_id(user_id):
#     try:
#         user_id_doc = db.collection("user_ids").document(user_id).get()
#         if user_id_doc.exists:
#             firebase_uid = user_id_doc.to_dict().get("firebase_uid")
#             user_doc = db.collection("users").document(firebase_uid).get()
#             if user_doc.exists:
#                 return user_doc.to_dict().get("email")
#         return None
#     except:
#         return None

# def check_group_name_exists(group_name):
#     groups = db.collection("groups").where("name", "==", group_name).limit(1).stream()
#     return len(list(groups)) > 0
# # app.py: Add this helper function near the top (e.g., after get_pending_requests_count)

# def safe_parse_genres(x):
#     if pd.isna(x) or not x:
#         return []
#     try:
#         # Use ast.literal_eval to safely parse the genre JSON string
#         return [d['name'] for d in ast.literal_eval(str(x)) if isinstance(d, dict) and 'name' in d]
#     except Exception:
#         return []
    

# def get_pending_requests_count(user_id):
#     """Count pending join requests for groups created by this user"""
#     count = 0
#     groups = db.collection("groups").where("created_by", "==", user_id).stream()
#     for group in groups:
#         pending = group.to_dict().get("pending_requests", [])
#         count += len(pending)
#     return count

# if "user" not in st.session_state:
#     st.session_state["user"] = None
# if "user_id" not in st.session_state:
#     st.session_state["user_id"] = None
# if "custom_user_id" not in st.session_state:
#     st.session_state["custom_user_id"] = None

# st.markdown("""
# <div class="main-header">
#     <h1>🎬 College Movie Recommender</h1>
#     <p style="font-size: 1.1rem; opacity: 0.95;">Discover movies with friends & get personalized ML-powered recommendations</p>
# </div>
# """, unsafe_allow_html=True)

# if st.session_state["user"] is None:
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         tab1, tab2 = st.tabs(["🔐 Login", "🆕 Sign Up"])

#         with tab1:
#             st.markdown("### Welcome Back!")
#             email = st.text_input("Email Address", key="login_email", placeholder="your.email@example.com")
#             password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

#             if st.button("🚀 Login", type="primary", use_container_width=True):
#                 try:
#                     user = auth.sign_in_with_email_and_password(email, password)
#                     st.session_state["user"] = email
#                     st.session_state["user_id"] = user["localId"]

#                     user_doc = db.collection("users").document(user["localId"]).get()
#                     if user_doc.exists:
#                         st.session_state["custom_user_id"] = user_doc.to_dict().get("custom_user_id")

#                     st.success("✅ Logged in successfully!")
#                     st.balloons()
#                     st.rerun()

#                 except Exception as e:
#                     st.error("❌ Login failed. Please check your credentials.")

#         with tab2:
#             st.markdown("### Create Your Account")
#             email = st.text_input("Email Address", key="signup_email", placeholder="your.email@example.com")
#             password = st.text_input("Password (min 6 characters)", type="password", key="signup_password", placeholder="Create a strong password")

#             if st.button("✨ Create Account", type="primary", use_container_width=True):
#                 if len(password) < 6:
#                     st.error("Password must be at least 6 characters long.")
#                 else:
#                     try:
#                         user = auth.create_user_with_email_and_password(email, password)
                        
#                         custom_user_id = generate_user_id()
                        
#                         db.collection("users").document(user["localId"]).set({
#                             "email": email,
#                             "custom_user_id": custom_user_id,
#                             "created_at": datetime.now(),
#                             "favorite_movies": [],
#                             "groups_joined": []
#                         })
                        
#                         db.collection("user_ids").document(custom_user_id).set({
#                             "firebase_uid": user["localId"],
#                             "email": email
#                         })
                        
#                         st.success("✅ Account created successfully!")
#                         st.markdown(f"""
#                         <div class="info-card">
#                             <h3>🆔 Your User ID</h3>
#                             <div style="font-size: 2rem; font-weight: bold; margin: 1rem 0;">{custom_user_id}</div>
#                             <p>⚠️ Save this ID! You'll need it to join groups and for friends to add you.</p>
#                         </div>
#                         """, unsafe_allow_html=True)
#                         st.balloons()
                        
#                     except Exception as e:
#                         st.error(f"⚠️ Error creating account: {str(e)}")

# else:
#     user_doc = db.collection("users").document(st.session_state["user_id"]).get()
#     user_data = user_doc.to_dict()
#     custom_id = user_data.get("custom_user_id", "Unknown")
    
#     # Check for pending requests
#     pending_count = get_pending_requests_count(st.session_state["user_id"])
    
#     col1, col2, col3 = st.columns([2, 2, 1])
#     with col1:
#         st.markdown(f"**👤 {st.session_state['user']}**")
#     with col2:
#         notification_text = f'<div class="user-id-badge">🆔 {custom_id}'
#         if pending_count > 0:
#             notification_text += f' <span style="background:#ff4444;color:white;border-radius:50%;padding:0.2rem 0.5rem;font-size:0.8rem;margin-left:0.5rem;">{pending_count}</span>'
#         notification_text += '</div>'
#         st.markdown(notification_text, unsafe_allow_html=True)
#     with col3:
#         if st.button("🚪 Logout", use_container_width=True):
#             st.session_state["user"] = None
#             st.session_state["user_id"] = None
#             st.session_state["custom_user_id"] = None
#             st.rerun()

#     st.markdown("---")

#     tab1, tab2, tab3, tab4, tab5, tab6,tab7= st.tabs([
#         "🎬 My Favorites", 
#         "👥 Movie Groups", 
#         "💡 Recommendations", 
#         "🎯 Group Board", 
#         "💬 Group Chat",
#         "📊 Analytics",
#         "🤝 Compatibility" 
#     ])

    
#     with tab1:
#         st.markdown("### 🌟 Your Favorite Movies")

#         # --- SEARCH BAR ---
#         search_query = st.text_input("🔍 Search movies by title, actor, genre, or company...", 
#                                     placeholder="Type something like 'Inception' or 'Warner Bros.'")

#         results = []
#         if search_query.strip():
#             with st.spinner("Searching across all filters..."):
#                 # Use your recommender methods (assuming they exist)
#                 title_results = recommender.search_movies(query=search_query)
#                 actor_results = recommender.search_by_actor(search_query)
#                 company_results = recommender.search_by_production_company(search_query)

#                 # Combine results uniquely by title
#                 seen = set()
#                 for group in [title_results, actor_results, company_results]:
#                     if group:
#                         for movie in group:
#                             title = movie.get('title', '')
#                             if title and title not in seen:
#                                 seen.add(title)
#                                 results.append(movie)

#             if results:
#                 st.success(f"✅ Found {len(results)} matching movies!")
#                 for idx, movie in enumerate(results[:15]):
#                     with st.container():
#                         col1, col2 = st.columns([4, 1])
#                         with col1:
#                             title = movie.get('title', 'Unknown')
#                             genres = movie.get('genres', [])
#                             if isinstance(genres, list):
#                                 genres_str = ", ".join(genres)
#                             else:
#                                 genres_str = str(genres)
                            
#                             cast_info = ""
#                             if 'cast' in movie and isinstance(movie['cast'], list):
#                                 cast_info = f"<br><small>🎭 Cast: {', '.join(movie['cast'][:3])}</small>"

#                             company_info = ""
#                             if 'production_companies' in movie and isinstance(movie['production_companies'], list):
#                                 company_info = f"<br><small>🏭 Companies: {', '.join(movie['production_companies'][:2])}</small>"

#                             st.markdown(f"""
#                             <div class="movie-item">
#                                 <strong>🎬 {title}</strong><br>
#                                 <small>📁 Genres: {genres_str}</small>
#                                 {cast_info}
#                                 {company_info}
#                             </div>
#                             """, unsafe_allow_html=True)
#                         with col2:
#                             if st.button("➕ Add", key=f"add_{idx}_{title[:20]}", use_container_width=True):
#                                 try:
#                                     db.collection("users").document(st.session_state["user_id"]).update({
#                                         "favorite_movies": firestore.ArrayUnion([title])
#                                     })
#                                     st.success(f"✅ Added '{title}'!")
#                                     st.rerun()
#                                 except Exception as e:
#                                     st.error(f"Error adding movie: {str(e)}")
#             else:
#                 st.warning("❌ No matching movies found.")
        
#         st.markdown("---")
#         # --- FAVORITES LIST ---
#         fav_movies = user_data.get("favorite_movies", [])
#         if fav_movies:
#             st.markdown(f"**📊 Your Collection: {len(fav_movies)} movies**")
#             for m in fav_movies:
#                 col1, col2 = st.columns([5, 1])
#                 with col1:
#                     st.markdown(f"""
#                     <div class="movie-item">
#                         <span>🎬 {m}</span>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 with col2:
#                     if st.button("🗑️", key=f"del_{m}", use_container_width=True):
#                         db.collection("users").document(st.session_state["user_id"]).update({
#                             "favorite_movies": firestore.ArrayRemove([m])
#                         })
#                         st.rerun()
#         else:
#             st.info("🎥 No favorite movies yet. Start adding some!")


  

#     with tab2:
#         st.markdown("### 🎭 Movie Groups")
        
#         # Show pending requests notification
#         if pending_count > 0:
#             st.warning(f"🔔 You have {pending_count} pending join request(s)!")
        
#         create_tab, join_tab, my_groups_tab, requests_tab = st.tabs([
#             "➕ Create Group", 
#             "🔗 Join Group", 
#             "📋 My Groups",
#             f"📥 Requests ({pending_count})"
#         ])
        
#         with create_tab:
#             st.markdown("#### Create a New Movie Club")
#             group_name = st.text_input("Group Name", placeholder="e.g., Marvel Fans Club")
            
#             if st.button("🎬 Create Group", type="primary", use_container_width=True):
#                 if not group_name.strip():
#                     st.error("Please enter a group name.")
#                 elif check_group_name_exists(group_name.strip()):
#                     st.error("❌ Group name already exists.")
#                 else:
#                     group_ref = db.collection("groups").document()
#                     group_ref.set({
#                         "name": group_name.strip(),
#                         "members": [st.session_state["user_id"]],
#                         "pending_requests": [],
#                         "group_movies": {},
#                         "polls": [],
#                         "chat_messages": [],
#                         "created_by": st.session_state["user_id"],
#                         "created_at": datetime.now()
#                     })
                    
#                     db.collection("users").document(st.session_state["user_id"]).update({
#                         "groups_joined": firestore.ArrayUnion([group_ref.id])
#                     })
                    
#                     st.success(f"✅ Group '{group_name}' created!")
#                     st.balloons()
#                     st.rerun()
        
#         with join_tab:
#             st.markdown("#### Join an Existing Group")
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 join_group_name = st.text_input("Group Name", placeholder="Enter exact group name", label_visibility="collapsed")
#             with col2:
#                 join_btn = st.button("📤 Request", type="primary", use_container_width=True)
            
#             if join_btn and join_group_name.strip():
#                 groups_query = db.collection("groups").where("name", "==", join_group_name.strip()).limit(1).stream()
#                 groups_list = list(groups_query)
                
#                 if groups_list:
#                     group_doc = groups_list[0]
#                     group_id = group_doc.id
#                     group_data = group_doc.to_dict()
                    
#                     if st.session_state["user_id"] in group_data.get("members", []):
#                         st.warning("You're already in this group!")
#                     elif st.session_state["user_id"] in group_data.get("pending_requests", []):
#                         st.info("Your request is pending approval.")
#                     else:
#                         db.collection("groups").document(group_id).update({
#                             "pending_requests": firestore.ArrayUnion([st.session_state["user_id"]])
#                         })
#                         st.success(f"✅ Join request sent for '{join_group_name}'!")
#                         st.rerun()
#                 else:
#                     st.error("❌ Group not found.")
        
#         with requests_tab:
#             st.markdown("#### Pending Join Requests")
#             groups = db.collection("groups").where("created_by", "==", st.session_state["user_id"]).stream()
            
#             has_requests = False
#             for group in groups:
#                 group_data = group.to_dict()
#                 pending = group_data.get("pending_requests", [])
                
#                 if pending:
#                     has_requests = True
#                     st.markdown(f"**Group: {group_data.get('name')}**")
#                     for req_uid in pending:
#                         req_doc = db.collection("users").document(req_uid).get()
#                         if req_doc.exists:
#                             req_data = req_doc.to_dict()
#                             col1, col2, col3 = st.columns([3, 1, 1])
#                             with col1:
#                                 st.write(f"👤 {req_data.get('email')} ({req_data.get('custom_user_id')})")
#                             with col2:
#                                 if st.button("✅ Accept", key=f"accept_{group.id}_{req_uid}"):
#                                     db.collection("groups").document(group.id).update({
#                                         "members": firestore.ArrayUnion([req_uid]),
#                                         "pending_requests": firestore.ArrayRemove([req_uid])
#                                     })
#                                     db.collection("users").document(req_uid).update({
#                                         "groups_joined": firestore.ArrayUnion([group.id])
#                                     })
#                                     st.success("Request approved!")
#                                     st.rerun()
#                             with col3:
#                                 if st.button("❌ Reject", key=f"reject_{group.id}_{req_uid}"):
#                                     db.collection("groups").document(group.id).update({
#                                         "pending_requests": firestore.ArrayRemove([req_uid])
#                                     })
#                                     st.success("Request rejected!")
#                                     st.rerun()
#                     st.markdown("---")
            
#             if not has_requests:
#                 st.info("No pending requests.")
        
#         with my_groups_tab:
#             groups = user_data.get("groups_joined", [])
#             if groups:
#                 st.markdown(f"**You're in {len(groups)} group(s)**")
#                 for group_id in groups:
#                     try:
#                         group_doc = db.collection("groups").document(group_id).get()
#                         if group_doc.exists:
#                             group_data = group_doc.to_dict()
#                             with st.expander(f"🎬 {group_data.get('name')} ({len(group_data.get('members', []))} members)"):
#                                 st.markdown("**👥 Members:**")
#                                 for member_uid in group_data.get('members', []):
#                                     m_doc = db.collection("users").document(member_uid).get()
#                                     if m_doc.exists:
#                                         m_data = m_doc.to_dict()
#                                         is_creator = member_uid == group_data.get('created_by')
#                                         creator_badge = " 👑" if is_creator else ""
#                                         st.write(f"• {m_data.get('email')}{creator_badge} (ID: {m_data.get('custom_user_id')})")
#                     except:
#                         pass
#             else:
#                 st.info("🎭 You haven't joined any groups yet.")
# #         =====================================================================
# # TAB 3: 🎬 Personalized Recommendations
# # =====================================================================

#     with tab3:
#         st.markdown("### 💡 Your Personal Recommendations")
        
#         fav_movies = user_data.get("favorite_movies", [])
#         user_groups = user_data.get("groups_joined", [])
        
#         # Collect user ratings and group data
#         user_ratings = {}
#         all_users_ratings = {}
#         group_favorites = []
        
#         for group_id in user_groups:
#             try:
#                 group_doc = db.collection("groups").document(group_id).get()
#                 if group_doc.exists:
#                     group_data = group_doc.to_dict()
#                     group_movies = group_data.get("group_movies", {})
                    
#                     # FIXED: Safe handling of group_movies
#                     if isinstance(group_movies, dict):
#                         for movie_title, movie_data in group_movies.items():
#                             if isinstance(movie_data, dict):
#                                 ratings = movie_data.get("ratings", {})
#                                 if isinstance(ratings, dict):
#                                     if st.session_state["user_id"] in ratings:
#                                         user_ratings[movie_title] = ratings[st.session_state["user_id"]]
                                    
#                                     for uid, rating in ratings.items():
#                                         if uid not in all_users_ratings:
#                                             all_users_ratings[uid] = {}
#                                         all_users_ratings[uid][movie_title] = rating
                    
#                     # Collect group members' favorites
#                     for member_uid in group_data.get("members", []):
#                         try:
#                             m_doc = db.collection("users").document(member_uid).get()
#                             if m_doc.exists:
#                                 group_favorites.extend(m_doc.to_dict().get("favorite_movies", []))
#                         except:
#                             pass
#             except Exception as e:
#                 st.error(f"Error loading group data: {str(e)}")
#                 continue
        
#         if fav_movies or group_favorites:
#             # Mood and Diversity Controls
#             st.markdown("---")
#             st.markdown("#### 🎭 Customize Your Recommendations")
            
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 rec_mode = st.selectbox(
#                     "📊 Data Source:",
#                     ["🎨 My Favorites Only", "👥 Group Influence", "🔬 Hybrid (Combined)"],
#                     help="Choose what data to base recommendations on"
#                 )
            
#             with col2:
#                 mood_filter = st.selectbox(
#                     "🎭 Mood Filter:",
#                     ["All Moods", "Chill", "Thriller", "Funny", "Deep", "Action", "Romantic"],
#                     help="Filter movies by mood"
#                 )
            
#             with col3:
#                 diversity_level = st.slider(
#                     "🎲 Exploration Level:",
#                     min_value=0,
#                     max_value=100,
#                     value=50,
#                     help="0=Similar to favorites, 100=Explore new genres"
#                 )
            
#             # Visual indicator for diversity
#             if diversity_level < 30:
#                 diversity_desc = "🎯 Playing it safe - Very similar to your favorites"
#             elif diversity_level < 70:
#                 diversity_desc = "⚖️ Balanced - Mix of familiar and new"
#             else:
#                 diversity_desc = "🚀 Adventure mode - Exploring new territory!"
            
#             st.markdown(f"<p style='text-align:center;color:#667eea;'><em>{diversity_desc}</em></p>", 
#                         unsafe_allow_html=True)
            
#             st.markdown("---")
            
#             if st.button("✨ Get Recommendations", type="primary", use_container_width=True):
#                 with st.spinner("🤖 Analyzing your taste..."):
#                     recommendations = []
#                     mood_param = None if mood_filter == "All Moods" else mood_filter.lower()
                    
#                     try:
#                         if rec_mode == "🎨 My Favorites Only":
#                             recommendations = recommender.get_recommendations(
#                                 fav_movies, 
#                                 top_n=10, 
#                                 mood=mood_param, 
#                                 diversity=diversity_level
#                             )
#                             rec_description = f"Based on your {len(fav_movies)} favorites"
                        
#                         elif rec_mode == "👥 Group Influence":
#                             combined_movies = list(set(fav_movies + group_favorites))
#                             recommendations = recommender.get_recommendations(
#                                 combined_movies, 
#                                 top_n=10, 
#                                 mood=mood_param, 
#                                 diversity=diversity_level
#                             )
#                             rec_description = f"Based on {len(combined_movies)} movies from you and your groups"
                        
#                         else:  # Hybrid
#                             if user_ratings and len(all_users_ratings) > 1:
#                                 combined_movies = list(set(fav_movies + group_favorites))
#                                 recommendations = recommender.get_hybrid_recommendations(
#                                     combined_movies, 
#                                     user_ratings, 
#                                     all_users_ratings, 
#                                     top_n=10,
#                                     mood=mood_param,
#                                     diversity=diversity_level
#                                 )
#                                 rec_description = "Hybrid: Content + Collaborative filtering"
#                             else:
#                                 combined_movies = list(set(fav_movies + group_favorites))
#                                 recommendations = recommender.get_recommendations(
#                                     combined_movies, 
#                                     top_n=10, 
#                                     mood=mood_param, 
#                                     diversity=diversity_level
#                                 )
#                                 rec_description = "Content-based (need more ratings for hybrid)"
                        
#                         if recommendations:
#                             st.markdown(f"### 🎯 Recommended For You")
#                             st.markdown(f"*{rec_description}*")
                            
#                             for i, rec in enumerate(recommendations, 1):
#                                 with st.expander(f"**#{i} 🎬 {rec['title']}** - {rec['score']}% match"):
#                                     col1, col2 = st.columns([3, 1])
                                    
#                                     with col1:
#                                         st.markdown(f"**Genres:** {rec['genres']}")
#                                         if 'moods' in rec:
#                                             st.markdown(f"**Moods:** {rec['moods']}")
#                                         if 'overview' in rec:
#                                             st.markdown(f"**Plot:** {rec['overview']}")
                                    
#                                     with col2:
#                                         if st.button("➕ Add", key=f"add_rec_{rec['title']}", use_container_width=True):
#                                             db.collection("users").document(st.session_state["user_id"]).update({
#                                                 "favorite_movies": firestore.ArrayUnion([rec['title']])
#                                             })
#                                             st.success("Added!")
#                                             st.rerun()
#                         else:
#                             st.warning("No recommendations found with these filters. Try adjusting your settings!")
                    
#                     except Exception as e:
#                         st.error(f"Error generating recommendations: {str(e)}")
#                         st.info("Try different settings or check your data.")
#         else:
#             st.info("👆 Add some favorite movies or join a group to get recommendations!")
        
#     with tab4:
#         st.markdown("### 🎯 Group Movie Board & Ratings")
        
#         groups = user_data.get("groups_joined", [])
        
#         if groups:
#             group_options = {}
#             for g_id in groups:
#                 g_doc = db.collection("groups").document(g_id).get()
#                 if g_doc.exists:
#                     group_options[g_doc.to_dict().get("name")] = g_id
            
#             if group_options:
#                 selected_group_name = st.selectbox("📊 Select a Group", list(group_options.keys()))
#                 selected_group_id = group_options[selected_group_name]
                
#                 group_doc = db.collection("groups").document(selected_group_id).get()
#                 group_data = group_doc.to_dict()
                
#                 st.markdown("---")
                
#                 board_tab, rec_tab = st.tabs(["🎬 Movie Board & Ratings", "💡 Group Recommendations"])
                
#                 with board_tab:
#                     col1, col2 = st.columns([3, 1])
#                     with col1:
#                         movie_title = st.text_input("Add Movie to Board", placeholder="Enter movie name")
#                     with col2:
#                        if st.button("➕ Add", type="primary"):

#                         if movie_title.strip():
#                             group_movies = group_data.get("group_movies", {})

#                             # 🩵 FIX: Ensure group_movies is always a dictionary
#                             if isinstance(group_movies, list):
#                                 # convert list into a dict with placeholder values
#                                 group_movies = {str(i): {"added_by": None, "ratings": {}, "added_at": ""} for i in group_movies}
#                             elif not isinstance(group_movies, dict):
#                                 group_movies = {}

#                             if movie_title.strip() not in group_movies:
#                                 group_movies[movie_title.strip()] = {
#                                     "added_by": st.session_state["user_id"],
#                                     "ratings": {},
#                                     "added_at": datetime.now().isoformat()
#                                 }
#                                 db.collection("groups").document(selected_group_id).update({
#                                     "group_movies": group_movies
#                                 })
#                                 st.success(f"✅ Added '{movie_title}'!")
#                                 st.rerun()

                    
#                     st.markdown("---")
#                     st.markdown("**📽️ Movies on Board:**")
                    
#                     group_movies = group_data.get("group_movies", {})
#                     if group_movies:
#                         for movie_title, movie_data in group_movies.items():
#                             with st.expander(f"🎬 {movie_title}"):
#                                 ratings = movie_data.get("ratings", {})
#                                 if ratings:
#                                     avg_rating = sum(ratings.values()) / len(ratings)
#                                     st.write(f"**Average Rating:** ⭐ {avg_rating:.1f}/5 ({len(ratings)} ratings)")
                                
#                                 user_rating = ratings.get(st.session_state["user_id"], 0)
#                                 rating = st.slider(
#                                     "Your Rating",
#                                     min_value=1,
#                                     max_value=5,
#                                     value=int(user_rating) if user_rating else 3,
#                                     key=f"rating_{selected_group_id}_{movie_title}"
#                                 )
                                
#                                 if st.button("💾 Save Rating", key=f"save_{selected_group_id}_{movie_title}"):
#                                     group_movies[movie_title]["ratings"][st.session_state["user_id"]] = rating
#                                     db.collection("groups").document(selected_group_id).update({
#                                         "group_movies": group_movies
#                                     })
#                                     st.success(f"✅ Rated '{movie_title}' with {rating} stars!")
#                                     st.rerun()
#                     else:
#                         st.info("No movies on board yet.")
                
#                 # ---------------- UPDATED rec_tab SECTION ----------------
#                 with rec_tab:
#                     st.markdown("#### 💡 Group Recommendations")
#                     st.markdown("Get recommendations based on your entire group's preferences!")
                    
#                     # Collect all favorites from group members
#                     all_group_favorites = []
#                     members_list = group_data.get("members", [])
#                     for member_uid in members_list:
#                         try:
#                             m_doc = db.collection("users").document(member_uid).get()
#                             if m_doc.exists:
#                                 member_favs = m_doc.to_dict().get("favorite_movies", [])
#                                 all_group_favorites.extend(member_favs)
#                         except:
#                             continue
                    
#                     # FIXED: Handle group_movies safely
#                     group_movies_data = group_data.get("group_movies", {})
#                     group_movies_list = []
                    
#                     if isinstance(group_movies_data, dict):
#                         group_movies_list = list(group_movies_data.keys())
#                     elif isinstance(group_movies_data, list):
#                         # If it's accidentally stored as a list, convert
#                         group_movies_list = group_movies_data
                    
#                     combined_group_movies = list(set(all_group_favorites + group_movies_list))
                    
#                     if combined_group_movies:
#                         st.write(f"📊 Analyzing {len(combined_group_movies)} movies from {len(members_list)} members")
                        
#                         col1, col2 = st.columns(2)
#                         with col1:
#                             rec_method = st.radio(
#                                 "Recommendation Method:",
#                                 ["🎨 Content-Based", "⭐ Rating-Based"],
#                                 horizontal=True
#                             )
#                         with col2:
#                             group_diversity = st.slider(
#                                 "🎲 Exploration Level:",
#                                 min_value=0,
#                                 max_value=100,
#                                 value=50,
#                                 key="group_diversity"
#                             )
                        
#                         if st.button("✨ Get Group Recommendations", type="primary"):
#                             with st.spinner("🤖 Analyzing group preferences..."):
#                                 if rec_method == "🎨 Content-Based":
#                                     recommendations = recommender.get_recommendations(
#                                         combined_group_movies, 
#                                         top_n=10,
#                                         diversity=group_diversity
#                                     )
#                                     rec_description = f"Based on content similarity from {len(combined_group_movies)} group movies"
#                                 else:
#                                     # FIXED: Collect all ratings safely
#                                     all_ratings = {}
                                    
#                                     if isinstance(group_movies_data, dict):
#                                         for movie, data in group_movies_data.items():
#                                             if isinstance(data, dict):
#                                                 ratings = data.get("ratings", {})
#                                                 if isinstance(ratings, dict):
#                                                     for uid, rating in ratings.items():
#                                                         if uid not in all_ratings:
#                                                             all_ratings[uid] = {}
#                                                         all_ratings[uid][movie] = rating
                                    
#                                     if len(all_ratings) > 1:
#                                         # Use average user's ratings
#                                         avg_ratings = {}
#                                         for uid, ratings in all_ratings.items():
#                                             if ratings:
#                                                 avg_ratings[uid] = sum(ratings.values()) / len(ratings)
                                        
#                                         if avg_ratings:
#                                             best_user = max(avg_ratings, key=avg_ratings.get)
#                                             recommendations = recommender.get_collaborative_recommendations(
#                                                 all_ratings[best_user],
#                                                 all_ratings,
#                                                 top_n=10
#                                             )
#                                             rec_description = "Based on collaborative filtering from group ratings"
#                                         else:
#                                             recommendations = recommender.get_recommendations(
#                                                 combined_group_movies, 
#                                                 top_n=10,
#                                                 diversity=group_diversity
#                                             )
#                                             rec_description = "Content-based (no ratings available)"
#                                     else:
#                                         recommendations = recommender.get_recommendations(
#                                             combined_group_movies, 
#                                             top_n=10,
#                                             diversity=group_diversity
#                                         )
#                                         rec_description = "Content-based (need more ratings)"
                                
#                                 if recommendations:
#                                     st.markdown("### 🏆 Recommended for Your Group")
#                                     st.markdown(f"*{rec_description}*")
                                    
#                                     for i, rec in enumerate(recommendations, 1):
#                                         with st.expander(f"**#{i} 🎬 {rec['title']}** - {rec['score']}% match"):
#                                             st.markdown(f"**Genres:** {rec['genres']}")
#                                             if 'moods' in rec:
#                                                 st.markdown(f"**Moods:** {rec['moods']}")
#                                             if 'overview' in rec:
#                                                 st.markdown(f"**Plot:** {rec['overview']}")
                                            
#                                             if st.button("➕ Add to Group Board", key=f"add_group_{rec['title']}"):
#                                                 # Initialize group_movies if needed
#                                                 if not isinstance(group_movies_data, dict):
#                                                     group_movies_data = {}
                                                
#                                                 if rec['title'] not in group_movies_data:
#                                                     group_movies_data[rec['title']] = {
#                                                         "added_by": st.session_state["user_id"],
#                                                         "ratings": {},
#                                                         "added_at": datetime.now().isoformat()
#                                                     }
#                                                     db.collection("groups").document(selected_group_id).update({
#                                                         "group_movies": group_movies_data
#                                                     })
#                                                     st.success(f"Added '{rec['title']}' to group board!")
#                                                     st.rerun()
#                                 else:
#                                     st.warning("No recommendations found!")
#                     else:
#                         st.info("Add movies to favorites or the group board first!")
#         else:
#             st.info("👥 Join or create a group first!")

#     with tab5:
#         st.markdown("### 💬 Group Chat & 🎮 Fun Zone")

#         groups = user_data.get("groups_joined", [])

#         if groups:
#             group_options = {}
#             for g_id in groups:
#                 g_doc = db.collection("groups").document(g_id).get()
#                 if g_doc.exists:
#                     group_options[g_doc.to_dict().get("name")] = g_id

#             if group_options:
#                 selected_group_name = st.selectbox("💬 Select Group", list(group_options.keys()), key="chat_group_select")
#                 selected_group_id = group_options[selected_group_name]

#                 group_ref = db.collection("groups").document(selected_group_id)

#                 # ==============================
#                 # 📊 Real-time data listeners
#                 # ==============================
#                 if "chat_messages" not in st.session_state:
#                     st.session_state.chat_messages = []
#                 if "online_members" not in st.session_state:
#                     st.session_state.online_members = []
#                 if "current_game" not in st.session_state:
#                     st.session_state.current_game = None

#                 # Firestore real-time updates (mocked with polling for Streamlit)
#                 group_doc = group_ref.get()
#                 if group_doc.exists:
#                     data = group_doc.to_dict()
#                     st.session_state.chat_messages = data.get("chat_messages", [])
#                     st.session_state.online_members = data.get("online_members", [])
#                     st.session_state.current_game = data.get("current_game", None)

#                 # ==============================
#                 # 🟢 Online members section
#                 # ==============================
#                 with st.expander("🟢 Online Members", expanded=True):
#                     current_user = st.session_state["user_id"]
#                     if current_user not in st.session_state.online_members:
#                         st.session_state.online_members.append(current_user)
#                         group_ref.update({"online_members": st.session_state.online_members})
#                     st.markdown(", ".join([f"✅ **{m}**" for m in st.session_state.online_members]))

#                 st.markdown("---")

#                 # ==============================
#                 # 💬 Chat Display
#                 # ==============================
#                 chat_container = st.container()
#                 with chat_container:
#                     messages = st.session_state.chat_messages[-50:]
#                     for msg in messages:
#                         sender = msg.get("sender_id", "Unknown")
#                         message = msg.get("message", "")
#                         timestamp = msg.get("timestamp", "")
#                         time_str = datetime.fromisoformat(timestamp).strftime("%I:%M %p") if timestamp else ""
#                         st.markdown(f"""
#                         <div style="background:#f8f9fa;padding:0.75rem;border-radius:8px;margin:0.5rem 0;border-left:3px solid #667eea;">
#                             <strong>{sender}</strong> <span style="color:#888;font-size:0.85rem;">{time_str}</span>
#                             <p style="margin:0.25rem 0 0 0;">{message}</p>
#                         </div>
#                         """, unsafe_allow_html=True)

#                 # ==============================
#                 # 📤 Send message box
#                 # ==============================
#                 st.markdown("---")
#                 col1, col2 = st.columns([5, 1])
#                 with col1:
#                     msg = st.text_input("Type a message", key=f"chat_input_{selected_group_id}", placeholder="Share your thoughts...")
#                 with col2:
#                     if st.button("📤 Send", key=f"send_{selected_group_id}"):
#                         if msg and msg.strip():
#                             new_msg = {
#                                 "sender_id": st.session_state["user_id"],
#                                 "message": msg.strip(),
#                                 "timestamp": datetime.now().isoformat()
#                             }
#                             current_messages = st.session_state.chat_messages.copy()
#                             current_messages.append(new_msg)
#                             group_ref.update({"chat_messages": current_messages})
#                             st.rerun()

#                 # ==============================
#                 # 🎮 Guess the Movie Mini-Game
#                 # ==============================
#                 st.markdown("---")
#                 st.subheader("🎮 Group Game: Guess the Movie")

#                 if st.session_state.current_game:
#                     game = st.session_state.current_game
#                     st.info(f"🎭 Hint: {game['hint']}")
#                     guess = st.text_input("Your guess:", key=f"guess_{selected_group_id}")
#                     if st.button("✅ Submit Guess", key=f"submit_{selected_group_id}"):
#                         if guess and guess.lower().strip() == game["answer"].lower():
#                             st.success("🎉 Correct! You guessed the movie!")
#                             group_ref.update({"current_game": firestore.DELETE_FIELD})
#                             st.session_state.current_game = None
#                             st.rerun()
#                         else:
#                             st.warning("❌ Nope, try again!")
#                 else:
#                     st.info("No game active. Start one below!")
#                     with st.expander("🎬 Start a New Game"):
#                         hint = st.text_input("Enter emoji or hint for movie:", key=f"hint_{selected_group_id}")
#                         answer = st.text_input("Enter correct movie name (hidden)", type="password", key=f"answer_{selected_group_id}")
#                         if st.button("🎯 Start Game", key=f"start_game_{selected_group_id}"):
#                             if hint and answer:
#                                 new_game = {"hint": hint, "answer": answer.lower()}
#                                 group_ref.update({"current_game": new_game})
#                                 st.session_state.current_game = new_game
#                                 st.success("Game started! Others can guess now.")
#                                 st.rerun()
#             else:
#                 st.info("You haven't joined any groups yet!")
#         else:
#             st.info("👥 Join a group to start chatting and gaming!")



#     # 📊 TAB 6: Analytics Dashboard

#     with tab6:
#         st.markdown("### 📊 Analytics Dashboard")

#         # Personal stats summary card
#         fav_movies = user_data.get("favorite_movies", [])
#         groups = user_data.get("groups_joined", [])

#         if fav_movies:
#             # Calculate personal metrics
#             genre_diversity = recommender.calculate_genre_diversity(fav_movies)

#             st.markdown(f"""
#             <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                         padding:2rem;border-radius:15px;color:white;margin:1rem 0;">
#                 <h3 style="margin:0;">🎭 Your Movie Profile</h3>
#                 <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
#                             gap:1rem;margin-top:1rem;">
#                     <div style="background:rgba(255,255,255,0.2);padding:1rem;
#                                 border-radius:10px;text-align:center;">
#                         <div style="font-size:2rem;font-weight:bold;">{len(fav_movies)}</div>
#                         <div>Total Movies</div>
#                     </div>
#                     <div style="background:rgba(255,255,255,0.2);padding:1rem;
#                                 border-radius:10px;text-align:center;">
#                         <div style="font-size:2rem;font-weight:bold;">{genre_diversity:.0f}%</div>
#                         <div>Genre Diversity</div>
#                     </div>
#                     <div style="background:rgba(255,255,255,0.2);padding:1rem;
#                                 border-radius:10px;text-align:center;">
#                         <div style="font-size:2rem;font-weight:bold;">{len(groups)}</div>
#                         <div>Groups Joined</div>
#                     </div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#         # Continue with detailed analytics options
#         analysis_type = st.radio("Select Analysis Type:", ["👤 Personal Analytics", "👥 Group Analytics"])
        
#         # ---------------- PERSONAL ANALYTICS ----------------
#         if analysis_type == "👤 Personal Analytics":
#             if fav_movies:
#                 genre_dist = recommender.get_genre_distribution(fav_movies)
                
#                 if genre_dist:
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.markdown("#### 🎭 Your Favorite Genres")
#                         fig = px.pie(
#                             values=list(genre_dist.values()),
#                             names=list(genre_dist.keys()),
#                             title="Genre Distribution",
#                             color_discrete_sequence=px.colors.sequential.RdBu
#                         )
#                         st.plotly_chart(fig, use_container_width=True)
                    
#                     with col2:
#                         st.markdown("#### 📈 Genre Breakdown")
#                         fig = px.bar(
#                             x=list(genre_dist.keys()),
#                             y=list(genre_dist.values()),
#                             title="Movies per Genre",
#                             labels={'x': 'Genre', 'y': 'Count'},
#                             color=list(genre_dist.values()),
#                             color_continuous_scale='Viridis'
#                         )
#                         st.plotly_chart(fig, use_container_width=True)
                    
#                     st.markdown("#### 📊 Your Stats")
#                     col1, col2, col3 = st.columns(3)
#                     with col1:
#                         st.metric("Total Movies", len(fav_movies))
#                     with col2:
#                         st.metric("Unique Genres", len(genre_dist))
#                     with col3:
#                         top_genre = max(genre_dist, key=genre_dist.get)
#                         st.metric("Top Genre", top_genre)
#             else:
#                 st.info("🎬 Add favorite movies to see your analytics!")
        
#         # ---------------- GROUP ANALYTICS ----------------
#         else:
#             if groups:
#                 group_options = {}
#                 for g_id in groups:
#                     g_doc = db.collection("groups").document(g_id).get()
#                     if g_doc.exists:
#                         group_options[g_doc.to_dict().get("name")] = g_id
                
#                 if group_options:
#                     selected_group = st.selectbox("Select Group", list(group_options.keys()))
#                     selected_group_id = group_options[selected_group]
                    
#                     group_doc = db.collection("groups").document(selected_group_id).get()
#                     group_data = group_doc.to_dict()
#                     group_movies = group_data.get("group_movies", {})
#                     members = group_data.get("members", [])
                    
#                     all_favorites = []
#                     for member_uid in members:
#                         m_doc = db.collection("users").document(member_uid).get()
#                         if m_doc.exists:
#                             all_favorites.extend(m_doc.to_dict().get("favorite_movies", []))
                    
#                     if all_favorites or group_movies:
#                         col1, col2 = st.columns(2)
                        
#                         with col1:
#                             if all_favorites:
#                                 st.markdown("#### 🎭 Group Genre Preferences")
#                                 genre_dist = recommender.get_genre_distribution(all_favorites)
#                                 fig = px.pie(
#                                     values=list(genre_dist.values()),
#                                     names=list(genre_dist.keys()),
#                                     title="Combined Genre Distribution",
#                                     color_discrete_sequence=px.colors.sequential.Plasma
#                                 )
#                                 st.plotly_chart(fig, use_container_width=True)
                        
#                         with col2:
#                             if group_movies:
#                                 st.markdown("#### ⭐ Top Rated Movies")
                                
#                                 movie_ratings = []
#                                 for title, data in group_movies.items():
#                                     ratings = data.get("ratings", {})
#                                     if ratings:
#                                         avg = sum(ratings.values()) / len(ratings)
#                                         movie_ratings.append({
#                                             "Movie": title,
#                                             "Avg Rating": avg,
#                                             "Votes": len(ratings)
#                                         })
                                
#                                 if movie_ratings:
#                                     df = pd.DataFrame(movie_ratings).sort_values("Avg Rating", ascending=False).head(10)
#                                     fig = px.bar(
#                                         df,
#                                         x="Movie",
#                                         y="Avg Rating",
#                                         title="Top Rated Movies",
#                                         color="Avg Rating",
#                                         color_continuous_scale="Tealgrn"
#                                     )
#                                     fig.update_layout(xaxis_tickangle=-45)
#                                     st.plotly_chart(fig, use_container_width=True)
                        
#                         st.markdown("#### 📊 Group Stats")
#                         col1, col2, col3, col4 = st.columns(4)
#                         with col1:
#                             st.metric("Members", len(members))
#                         with col2:
#                             st.metric("Movies on Board", len(group_movies))
#                         with col3:
#                             total_ratings = sum(len(m.get("ratings", {})) for m in group_movies.values())
#                             st.metric("Total Ratings", total_ratings)
#                         with col4:
#                             st.metric("Combined Favorites", len(all_favorites))
#                     else:
#                         st.info("No data available yet for this group.")
#             else:
#                 st.info("Join a group to see group analytics!")

# # =====================================================================
# # TAB 7: 🤝 Movie Taste Compatibility
# # =====================================================================

#     with tab7:
#         st.markdown("### 🤝 Movie Taste Compatibility")

#         groups = user_data.get("groups_joined", [])
#         fav_movies = user_data.get("favorite_movies", [])

#         if groups and fav_movies:
#             st.markdown("See how your movie taste compares with your friends!")

#             # Collect group names from Firestore
#             group_options = {}
#             for g_id in groups:
#                 g_doc = db.collection("groups").document(g_id).get()
#                 if g_doc.exists:
#                     group_data = g_doc.to_dict()
#                     group_options[group_data.get("name", f"Group {g_id[:6]}")] = g_id

#             if group_options:
#                 selected_group = st.selectbox("Select a Group", list(group_options.keys()))
#                 selected_group_id = group_options[selected_group]

#                 group_doc = db.collection("groups").document(selected_group_id).get()
#                 group_data = group_doc.to_dict()
#                 members = group_data.get("members", [])

#                 st.markdown("---")
#                 st.markdown("#### 💫 Your Compatibility Scores")

#                 # Calculate compatibility for each member
#                 compatibility_scores = []

#                 for member_uid in members:
#                     if member_uid != st.session_state["user_id"]:
#                         m_doc = db.collection("users").document(member_uid).get()
#                         if m_doc.exists:
#                             m_data = m_doc.to_dict()
#                             member_favs = m_data.get("favorite_movies", [])

#                             if member_favs:
#                                 score = recommender.calculate_taste_compatibility(
#                                     fav_movies, member_favs
#                                 )
#                                 compatibility_scores.append({
#                                     'name': m_data.get('email', 'Unknown User'),
#                                     'user_id': m_data.get('custom_user_id', member_uid[:6]),
#                                     'score': score,
#                                     'movies': len(member_favs)
#                                 })

#                 # Sort results by score (highest first)
#                 compatibility_scores.sort(key=lambda x: x['score'], reverse=True)

#                 # Display results
#                 if compatibility_scores:
#                     for comp in compatibility_scores:
#                         score = comp['score']

#                         # Color and label based on score
#                         if score >= 70:
#                             color = "#4CAF50"
#                             emoji = "🎯"
#                             desc = "Perfect Match!"
#                         elif score >= 50:
#                             color = "#FFC107"
#                             emoji = "👍"
#                             desc = "Good Match"
#                         elif score >= 30:
#                             color = "#FF9800"
#                             emoji = "🤔"
#                             desc = "Some Overlap"
#                         else:
#                             color = "#F44336"
#                             emoji = "🎲"
#                             desc = "Very Different"

#                         st.markdown(f"""
#                         <div style="background:white;padding:1rem;border-radius:10px;margin:0.5rem 0;
#                                     border-left:5px solid {color};box-shadow:0 2px 4px rgba(0,0,0,0.1);">
#                             <div style="display:flex;justify-content:space-between;align-items:center;">
#                                 <div>
#                                     <strong>{emoji} {comp['name']}</strong> ({comp['user_id']})
#                                     <br><small>{comp['movies']} movies in their collection</small>
#                                 </div>
#                                 <div style="text-align:right;">
#                                     <div style="font-size:2rem;font-weight:bold;color:{color};">{score}%</div>
#                                     <div style="color:#666;font-size:0.9rem;">{desc}</div>
#                                 </div>
#                             </div>
#                         </div>
#                         """, unsafe_allow_html=True)

#                     # Summary stats
#                     st.markdown("---")
#                     st.markdown("#### 📊 Group Summary")

#                     col1, col2, col3 = st.columns(3)

#                     with col1:
#                         avg_compat = sum(c['score'] for c in compatibility_scores) / len(compatibility_scores)
#                         st.metric("Average Compatibility", f"{avg_compat:.1f}%")

#                     with col2:
#                         best_match = compatibility_scores[0]
#                         st.metric("Best Match", f"{best_match['score']}%",
#                                 delta=best_match['name'].split('@')[0])

#                     with col3:
#                         your_diversity = recommender.calculate_genre_diversity(fav_movies)
#                         st.metric("Your Genre Diversity", f"{your_diversity:.1f}%")

#                 else:
#                     st.info("Other members need to add favorite movies first to compare compatibility.")
#             else:
#                 st.info("No valid groups found. Try joining a group first.")
#         else:
#             if not groups:
#                 st.info("👥 Join a group to see compatibility scores!")
#             else:
#                 st.info("📽️ Add favorite movies to calculate compatibility!")
import streamlit as st
import pyrebase
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import pandas as pd
import random
import string
import plotly.express as px
import plotly.graph_objects as go
from recommendation_engine import MovieRecommender
import os
from google.cloud import firestore
from firebase_admin import credentials, firestore  

st.set_page_config(
    page_title="🎬 College Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .compatibility-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .mood-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .mood-chill { background: #E3F2FD; color: #1976D2; }
    .mood-thriller { background: #FCE4EC; color: #C2185B; }
    .mood-funny { background: #FFF9C4; color: #F57F17; }
    .mood-deep { background: #F3E5F5; color: #7B1FA2; }
    .mood-action { background: #FFEBEE; color: #D32F2F; }
    .mood-romantic { background: #FFE0E9; color: #E91E63; }


    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem 1rem;
        }
        
        .stButton button {
            width: 100%;
            margin: 0.25rem 0;
        }
        
        .stTextInput input {
            font-size: 16px !important;
        }
    }
    
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        color: white;
    }
    
    .info-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: white;
        text-align: center;
    }
    
    .group-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .user-id-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .movie-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .movie-item:hover {
        background: #e9ecef;
        transform: translateX(5px);
    }
    
    .recommendation-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .filter-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    @media (max-width: 768px) {
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    }
</style>
""", unsafe_allow_html=True)

if not os.path.exists("firebase_config.json"):
    st.error("⚠️ Firebase configuration missing! Please create `firebase_config.json` file.")
    st.stop()

if not os.path.exists("serviceAccountKey.json"):
    st.error("⚠️ Service account key missing! Please download `serviceAccountKey.json` from Firebase Console.")
    st.stop()

with open("firebase_config.json") as f:
    firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

@st.cache_resource
def load_recommender():
    return MovieRecommender("tmdb_5000_movies.csv", "tmdb_5000_credits.csv")

recommender = load_recommender()
movies_df = pd.read_csv("tmdb_5000_movies.csv", low_memory=False)

def generate_user_id():
    while True:
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        existing = db.collection("user_ids").document(user_id).get()
        if not existing.exists:
            return user_id

def get_username_by_id(user_id):
    try:
        user_id_doc = db.collection("user_ids").document(user_id).get()
        if user_id_doc.exists:
            firebase_uid = user_id_doc.to_dict().get("firebase_uid")
            user_doc = db.collection("users").document(firebase_uid).get()
            if user_doc.exists:
                return user_doc.to_dict().get("email")
        return None
    except:
        return None

def check_group_name_exists(group_name):
    groups = db.collection("groups").where("name", "==", group_name).limit(1).stream()
    return len(list(groups)) > 0
# app.py: Add this helper function near the top (e.g., after get_pending_requests_count)

def safe_parse_genres(x):
    if pd.isna(x) or not x:
        return []
    try:
        # Use ast.literal_eval to safely parse the genre JSON string
        return [d['name'] for d in ast.literal_eval(str(x)) if isinstance(d, dict) and 'name' in d]
    except Exception:
        return []
    

def get_pending_requests_count(user_id):
    """Count pending join requests for groups created by this user"""
    count = 0
    groups = db.collection("groups").where("created_by", "==", user_id).stream()
    for group in groups:
        pending = group.to_dict().get("pending_requests", [])
        count += len(pending)
    return count

if "user" not in st.session_state:
    st.session_state["user"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "custom_user_id" not in st.session_state:
    st.session_state["custom_user_id"] = None

st.markdown("""
<div class="main-header">
    <h1>🎬 College Movie Recommender</h1>
    <p style="font-size: 1.1rem; opacity: 0.95;">Discover movies with friends & get personalized ML-powered recommendations</p>
</div>
""", unsafe_allow_html=True)

if st.session_state["user"] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "🆕 Sign Up"])

        with tab1:
            st.markdown("### Welcome Back!")
            email = st.text_input("Email Address", key="login_email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

            if st.button("🚀 Login", type="primary", use_container_width=True):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state["user"] = email
                    st.session_state["user_id"] = user["localId"]

                    user_doc = db.collection("users").document(user["localId"]).get()
                    if user_doc.exists:
                        st.session_state["custom_user_id"] = user_doc.to_dict().get("custom_user_id")

                    st.success("✅ Logged in successfully!")
                    st.balloons()
                    st.rerun()

                except Exception as e:
                    st.error("❌ Login failed. Please check your credentials.")

        with tab2:
            st.markdown("### Create Your Account")
            email = st.text_input("Email Address", key="signup_email", placeholder="your.email@example.com")
            password = st.text_input("Password (min 6 characters)", type="password", key="signup_password", placeholder="Create a strong password")

            if st.button("✨ Create Account", type="primary", use_container_width=True):
                if len(password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    try:
                        user = auth.create_user_with_email_and_password(email, password)
                        
                        custom_user_id = generate_user_id()
                        
                        db.collection("users").document(user["localId"]).set({
                            "email": email,
                            "custom_user_id": custom_user_id,
                            "created_at": datetime.now(),
                            "favorite_movies": [],
                            "groups_joined": []
                        })
                        
                        db.collection("user_ids").document(custom_user_id).set({
                            "firebase_uid": user["localId"],
                            "email": email
                        })
                        
                        st.success("✅ Account created successfully!")
                        st.markdown(f"""
                        <div class="info-card">
                            <h3>🆔 Your User ID</h3>
                            <div style="font-size: 2rem; font-weight: bold; margin: 1rem 0;">{custom_user_id}</div>
                            <p>⚠️ Save this ID! You'll need it to join groups and for friends to add you.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"⚠️ Error creating account: {str(e)}")

else:
    user_doc = db.collection("users").document(st.session_state["user_id"]).get()
    user_data = user_doc.to_dict()
    custom_id = user_data.get("custom_user_id", "Unknown")
    
    # Check for pending requests
    pending_count = get_pending_requests_count(st.session_state["user_id"])
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"**👤 {st.session_state['user']}**")
    with col2:
        notification_text = f'<div class="user-id-badge">🆔 {custom_id}'
        if pending_count > 0:
            notification_text += f' <span style="background:#ff4444;color:white;border-radius:50%;padding:0.2rem 0.5rem;font-size:0.8rem;margin-left:0.5rem;">{pending_count}</span>'
        notification_text += '</div>'
        st.markdown(notification_text, unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["user"] = None
            st.session_state["user_id"] = None
            st.session_state["custom_user_id"] = None
            st.rerun()

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5, tab6,tab7= st.tabs([
        "🎬 My Favorites", 
        "👥 Movie Groups", 
        "💡 Recommendations", 
        "🎯 Group Board", 
        "💬 Group Chat",
        "📊 Analytics",
        "🤝 Compatibility" 
    ])

    
    with tab1:
        st.markdown("### 🌟 Your Favorite Movies")

        # --- SEARCH BAR ---
        search_query = st.text_input("🔍 Search movies by title, actor, genre, or company...", 
                                    placeholder="Type something like 'Inception' or 'Warner Bros.'")

        results = []
        if search_query.strip():
            with st.spinner("Searching across all filters..."):
                # Use your recommender methods (assuming they exist)
                title_results = recommender.search_movies(query=search_query)
                actor_results = recommender.search_by_actor(search_query)
                company_results = recommender.search_by_production_company(search_query)

                # Combine results uniquely by title
                seen = set()
                for group in [title_results, actor_results, company_results]:
                    if group:
                        for movie in group:
                            title = movie.get('title', '')
                            if title and title not in seen:
                                seen.add(title)
                                results.append(movie)

            if results:
                st.success(f"✅ Found {len(results)} matching movies!")
                for idx, movie in enumerate(results[:15]):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            title = movie.get('title', 'Unknown')
                            genres = movie.get('genres', [])
                            if isinstance(genres, list):
                                genres_str = ", ".join(genres)
                            else:
                                genres_str = str(genres)
                            
                            cast_info = ""
                            if 'cast' in movie and isinstance(movie['cast'], list):
                                cast_info = f"<br><small>🎭 Cast: {', '.join(movie['cast'][:3])}</small>"

                            company_info = ""
                            if 'production_companies' in movie and isinstance(movie['production_companies'], list):
                                company_info = f"<br><small>🏭 Companies: {', '.join(movie['production_companies'][:2])}</small>"

                            st.markdown(f"""
                            <div class="movie-item">
                                <strong>🎬 {title}</strong><br>
                                <small>📁 Genres: {genres_str}</small>
                                {cast_info}
                                {company_info}
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if st.button("➕ Add", key=f"add_{idx}_{title[:20]}", use_container_width=True):
                                try:
                                    db.collection("users").document(st.session_state["user_id"]).update({
                                        "favorite_movies": firestore.ArrayUnion([title])
                                    })
                                    st.success(f"✅ Added '{title}'!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error adding movie: {str(e)}")
            else:
                st.warning("❌ No matching movies found.")
        
        st.markdown("---")
        # --- FAVORITES LIST ---
        fav_movies = user_data.get("favorite_movies", [])
        if fav_movies:
            st.markdown(f"**📊 Your Collection: {len(fav_movies)} movies**")
            for m in fav_movies:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                    <div class="movie-item">
                        <span>🎬 {m}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("🗑️", key=f"del_{m}", use_container_width=True):
                        db.collection("users").document(st.session_state["user_id"]).update({
                            "favorite_movies": firestore.ArrayRemove([m])
                        })
                        st.rerun()
        else:
            st.info("🎥 No favorite movies yet. Start adding some!")


  

    with tab2:
        st.markdown("### 🎭 Movie Groups")
        
        # Show pending requests notification
        if pending_count > 0:
            st.warning(f"🔔 You have {pending_count} pending join request(s)!")
        
        create_tab, join_tab, my_groups_tab, requests_tab = st.tabs([
            "➕ Create Group", 
            "🔗 Join Group", 
            "📋 My Groups",
            f"📥 Requests ({pending_count})"
        ])
        
        with create_tab:
            st.markdown("#### Create a New Movie Club")
            group_name = st.text_input("Group Name", placeholder="e.g., Marvel Fans Club")
            
            if st.button("🎬 Create Group", type="primary", use_container_width=True):
                if not group_name.strip():
                    st.error("Please enter a group name.")
                elif check_group_name_exists(group_name.strip()):
                    st.error("❌ Group name already exists.")
                else:
                    group_ref = db.collection("groups").document()
                    group_ref.set({
                        "name": group_name.strip(),
                        "members": [st.session_state["user_id"]],
                        "pending_requests": [],
                        "group_movies": {},
                        "polls": [],
                        "chat_messages": [],
                        "created_by": st.session_state["user_id"],
                        "created_at": datetime.now()
                    })
                    
                    db.collection("users").document(st.session_state["user_id"]).update({
                        "groups_joined": firestore.ArrayUnion([group_ref.id])
                    })
                    
                    st.success(f"✅ Group '{group_name}' created!")
                    st.balloons()
                    st.rerun()
        
        with join_tab:
            st.markdown("#### Join an Existing Group")
            col1, col2 = st.columns([3, 1])
            with col1:
                join_group_name = st.text_input("Group Name", placeholder="Enter exact group name", label_visibility="collapsed")
            with col2:
                join_btn = st.button("📤 Request", type="primary", use_container_width=True)
            
            if join_btn and join_group_name.strip():
                groups_query = db.collection("groups").where("name", "==", join_group_name.strip()).limit(1).stream()
                groups_list = list(groups_query)
                
                if groups_list:
                    group_doc = groups_list[0]
                    group_id = group_doc.id
                    group_data = group_doc.to_dict()
                    
                    if st.session_state["user_id"] in group_data.get("members", []):
                        st.warning("You're already in this group!")
                    elif st.session_state["user_id"] in group_data.get("pending_requests", []):
                        st.info("Your request is pending approval.")
                    else:
                        db.collection("groups").document(group_id).update({
                            "pending_requests": firestore.ArrayUnion([st.session_state["user_id"]])
                        })
                        st.success(f"✅ Join request sent for '{join_group_name}'!")
                        st.rerun()
                else:
                    st.error("❌ Group not found.")
        
        with requests_tab:
            st.markdown("#### Pending Join Requests")
            groups = db.collection("groups").where("created_by", "==", st.session_state["user_id"]).stream()
            
            has_requests = False
            for group in groups:
                group_data = group.to_dict()
                pending = group_data.get("pending_requests", [])
                
                if pending:
                    has_requests = True
                    st.markdown(f"**Group: {group_data.get('name')}**")
                    for req_uid in pending:
                        req_doc = db.collection("users").document(req_uid).get()
                        if req_doc.exists:
                            req_data = req_doc.to_dict()
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"👤 {req_data.get('email')} ({req_data.get('custom_user_id')})")
                            with col2:
                                if st.button("✅ Accept", key=f"accept_{group.id}_{req_uid}"):
                                    db.collection("groups").document(group.id).update({
                                        "members": firestore.ArrayUnion([req_uid]),
                                        "pending_requests": firestore.ArrayRemove([req_uid])
                                    })
                                    db.collection("users").document(req_uid).update({
                                        "groups_joined": firestore.ArrayUnion([group.id])
                                    })
                                    st.success("Request approved!")
                                    st.rerun()
                            with col3:
                                if st.button("❌ Reject", key=f"reject_{group.id}_{req_uid}"):
                                    db.collection("groups").document(group.id).update({
                                        "pending_requests": firestore.ArrayRemove([req_uid])
                                    })
                                    st.success("Request rejected!")
                                    st.rerun()
                    st.markdown("---")
            
            if not has_requests:
                st.info("No pending requests.")
        
        with my_groups_tab:
            groups = user_data.get("groups_joined", [])
            if groups:
                st.markdown(f"**You're in {len(groups)} group(s)**")
                for group_id in groups:
                    try:
                        group_doc = db.collection("groups").document(group_id).get()
                        if group_doc.exists:
                            group_data = group_doc.to_dict()
                            with st.expander(f"🎬 {group_data.get('name')} ({len(group_data.get('members', []))} members)"):
                                st.markdown("**👥 Members:**")
                                for member_uid in group_data.get('members', []):
                                    m_doc = db.collection("users").document(member_uid).get()
                                    if m_doc.exists:
                                        m_data = m_doc.to_dict()
                                        is_creator = member_uid == group_data.get('created_by')
                                        creator_badge = " 👑" if is_creator else ""
                                        st.write(f"• {m_data.get('email')}{creator_badge} (ID: {m_data.get('custom_user_id')})")
                    except:
                        pass
            else:
                st.info("🎭 You haven't joined any groups yet.")
        # =====================================================================
# TAB 3: 🎬 Personalized Recommendations
# =====================================================================

    # with tab3:
    #     st.markdown("### 💡 Your Personal Recommendations")
        
    #     fav_movies = user_data.get("favorite_movies", [])
    #     user_groups = user_data.get("groups_joined", [])
        
    #     # Collect user ratings and group data
    #     user_ratings = {}
    #     all_users_ratings = {}
    #     group_favorites = []
        
    #     for group_id in user_groups:
    #         try:
    #             group_doc = db.collection("groups").document(group_id).get()
    #             if group_doc.exists:
    #                 group_data = group_doc.to_dict()
    #                 group_movies = group_data.get("group_movies", {})
                    
    #                 # FIXED: Safe handling of group_movies
    #                 if isinstance(group_movies, dict):
    #                     for movie_title, movie_data in group_movies.items():
    #                         if isinstance(movie_data, dict):
    #                             ratings = movie_data.get("ratings", {})
    #                             if isinstance(ratings, dict):
    #                                 if st.session_state["user_id"] in ratings:
    #                                     user_ratings[movie_title] = ratings[st.session_state["user_id"]]
                                    
    #                                 for uid, rating in ratings.items():
    #                                     if uid not in all_users_ratings:
    #                                         all_users_ratings[uid] = {}
    #                                     all_users_ratings[uid][movie_title] = rating
                    
    #                 # Collect group members' favorites
    #                 for member_uid in group_data.get("members", []):
    #                     try:
    #                         m_doc = db.collection("users").document(member_uid).get()
    #                         if m_doc.exists:
    #                             group_favorites.extend(m_doc.to_dict().get("favorite_movies", []))
    #                     except:
    #                         pass
    #         except Exception as e:
    #             st.error(f"Error loading group data: {str(e)}")
    #             continue
        
    #     if fav_movies or group_favorites:
    #         # Mood and Diversity Controls
    #         st.markdown("---")
    #         st.markdown("#### 🎭 Customize Your Recommendations")
            
    #         col1, col2, col3 = st.columns(3)
            
    #         with col1:
    #             rec_mode = st.selectbox(
    #                 "📊 Data Source:",
    #                 ["🎨 My Favorites Only", "👥 Group Influence", "🔬 Hybrid (Combined)"],
    #                 help="Choose what data to base recommendations on"
    #             )
            
    #         with col2:
    #             mood_filter = st.selectbox(
    #                 "🎭 Mood Filter:",
    #                 ["All Moods", "Chill", "Thriller", "Funny", "Deep", "Action", "Romantic"],
    #                 help="Filter movies by mood"
    #             )
            
    #         with col3:
    #             diversity_level = st.slider(
    #                 "🎲 Exploration Level:",
    #                 min_value=0,
    #                 max_value=100,
    #                 value=50,
    #                 help="0=Similar to favorites, 100=Explore new genres"
    #             )
            
    #         # Visual indicator for diversity
    #         if diversity_level < 30:
    #             diversity_desc = "🎯 Playing it safe - Very similar to your favorites"
    #         elif diversity_level < 70:
    #             diversity_desc = "⚖️ Balanced - Mix of familiar and new"
    #         else:
    #             diversity_desc = "🚀 Adventure mode - Exploring new territory!"
            
    #         st.markdown(f"<p style='text-align:center;color:#667eea;'><em>{diversity_desc}</em></p>", 
    #                     unsafe_allow_html=True)
            
    #         st.markdown("---")
            
    #         if st.button("✨ Get Recommendations", type="primary", use_container_width=True):
    #             with st.spinner("🤖 Analyzing your taste..."):
    #                 recommendations = []
    #                 mood_param = None if mood_filter == "All Moods" else mood_filter.lower()
                    
    #                 try:
    #                     if rec_mode == "🎨 My Favorites Only":
    #                         recommendations = recommender.get_recommendations(
    #                             fav_movies, 
    #                             top_n=10, 
    #                             mood=mood_param, 
    #                             diversity=diversity_level
    #                         )
    #                         rec_description = f"Based on your {len(fav_movies)} favorites"
                        
    #                     elif rec_mode == "👥 Group Influence":
    #                         combined_movies = list(set(fav_movies + group_favorites))
    #                         recommendations = recommender.get_recommendations(
    #                             combined_movies, 
    #                             top_n=10, 
    #                             mood=mood_param, 
    #                             diversity=diversity_level
    #                         )
    #                         rec_description = f"Based on {len(combined_movies)} movies from you and your groups"
                        
    #                     else:  # Hybrid
    #                         if user_ratings and len(all_users_ratings) > 1:
    #                             combined_movies = list(set(fav_movies + group_favorites))
    #                             recommendations = recommender.get_hybrid_recommendations(
    #                                 combined_movies, 
    #                                 user_ratings, 
    #                                 all_users_ratings, 
    #                                 top_n=10,
    #                                 mood=mood_param,
    #                                 diversity=diversity_level
    #                             )
    #                             rec_description = "Hybrid: Content + Collaborative filtering"
    #                         else:
    #                             combined_movies = list(set(fav_movies + group_favorites))
    #                             recommendations = recommender.get_recommendations(
    #                                 combined_movies, 
    #                                 top_n=10, 
    #                                 mood=mood_param, 
    #                                 diversity=diversity_level
    #                             )
    #                             rec_description = "Content-based (need more ratings for hybrid)"
                        
    #                     if recommendations:
    #                         st.markdown(f"### 🎯 Recommended For You")
    #                         st.markdown(f"*{rec_description}*")
                            
    #                         for i, rec in enumerate(recommendations, 1):
    #                             with st.expander(f"**#{i} 🎬 {rec['title']}** - {rec['score']}% match"):
    #                                 col1, col2 = st.columns([3, 1])
                                    
    #                                 with col1:
    #                                     st.markdown(f"**Genres:** {rec['genres']}")
    #                                     if 'moods' in rec:
    #                                         st.markdown(f"**Moods:** {rec['moods']}")
    #                                     if 'overview' in rec:
    #                                         st.markdown(f"**Plot:** {rec['overview']}")
                                    
    #                                 with col2:
    #                                     if st.button("➕ Add", key=f"add_rec_{rec['title']}", use_container_width=True):
    #                                         db.collection("users").document(st.session_state["user_id"]).update({
    #                                             "favorite_movies": firestore.ArrayUnion([rec['title']])
    #                                         })
    #                                         st.success("Added!")
    #                                         st.rerun()
    #                     else:
    #                         st.warning("No recommendations found with these filters. Try adjusting your settings!")
                    
    #                 except Exception as e:
    #                     st.error(f"Error generating recommendations: {str(e)}")
    #                     st.info("Try different settings or check your data.")
    #     else:
    #         st.info("👆 Add some favorite movies or join a group to get recommendations!")
    # Replace the existing tab3 section in app.py with this:

    with tab3:
        st.markdown("### 💡 Your Personal Recommendations")
        
        fav_movies = user_data.get("favorite_movies", [])
        user_groups = user_data.get("groups_joined", [])
        
        # Collect user ratings and group data
        user_ratings = {}
        all_users_ratings = {}
        group_favorites = []
        
        for group_id in user_groups:
            try:
                group_doc = db.collection("groups").document(group_id).get()
                if group_doc.exists:
                    group_data = group_doc.to_dict()
                    group_movies = group_data.get("group_movies", {})
                    
                    if isinstance(group_movies, dict):
                        for movie_title, movie_data in group_movies.items():
                            if isinstance(movie_data, dict):
                                ratings = movie_data.get("ratings", {})
                                if isinstance(ratings, dict):
                                    if st.session_state["user_id"] in ratings:
                                        user_ratings[movie_title] = ratings[st.session_state["user_id"]]
                                    
                                    for uid, rating in ratings.items():
                                        if uid not in all_users_ratings:
                                            all_users_ratings[uid] = {}
                                        all_users_ratings[uid][movie_title] = rating
                    
                    for member_uid in group_data.get("members", []):
                        try:
                            m_doc = db.collection("users").document(member_uid).get()
                            if m_doc.exists:
                                group_favorites.extend(m_doc.to_dict().get("favorite_movies", []))
                        except:
                            pass
            except Exception as e:
                st.error(f"Error loading group data: {str(e)}")
                continue
        
        if fav_movies or group_favorites:
            # Context Information Section
            st.markdown("---")
            st.markdown("#### 🌤️ Context-Aware Recommendations")
            st.info("📍 Provide context for better recommendations tailored to your current situation!")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                weather = st.selectbox(
                    "☀️ Weather:",
                    ["None", "Sunny", "Rainy", "Cloudy", "Cold", "Hot"],
                    help="Current weather condition"
                )
                weather = None if weather == "None" else weather
            
            with col2:
                day = st.selectbox(
                    "📅 Day:",
                    ["Auto-detect", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    help="Day of the week"
                )
                auto_context = day == "Auto-detect"
                day = None if day == "Auto-detect" else day
            
            with col3:
                time_of_day = st.selectbox(
                    "🕐 Time:",
                    ["Auto-detect", "Morning", "Afternoon", "Evening", "Night"],
                    help="Time of day"
                )
                if time_of_day == "Auto-detect":
                    time_of_day = None
            
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)
                if auto_context or time_of_day is None:
                    current_time = recommender.get_time_of_day()
                    current_day = recommender.get_current_day()
                    st.info(f"🤖 Auto: {current_day.title()}, {current_time.title()}")
            
            st.markdown("---")
            st.markdown("#### 🎭 Customize Your Recommendations")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rec_mode = st.selectbox(
                    "📊 Data Source:",
                    ["🎨 My Favorites Only", "👥 Group Influence", "🔬 Hybrid (Combined)"],
                    help="Choose what data to base recommendations on"
                )
            
            with col2:
                mood_filter = st.selectbox(
                    "🎭 Mood Filter:",
                    ["All Moods", "Chill", "Thriller", "Funny", "Deep", "Action", "Romantic"],
                    help="Filter movies by mood"
                )
            
            with col3:
                diversity_level = st.slider(
                    "🎲 Exploration Level:",
                    min_value=0,
                    max_value=100,
                    value=50,
                    help="0=Similar to favorites, 100=Explore new genres"
                )
            
            # Visual indicator for diversity
            if diversity_level < 30:
                diversity_desc = "🎯 Playing it safe - Very similar to your favorites"
            elif diversity_level < 70:
                diversity_desc = "⚖️ Balanced - Mix of familiar and new"
            else:
                diversity_desc = "🚀 Adventure mode - Exploring new territory!"
            
            st.markdown(f"<p style='text-align:center;color:#667eea;'><em>{diversity_desc}</em></p>", 
                        unsafe_allow_html=True)
            
            # Context Summary
            context_parts = []
            if weather:
                context_parts.append(f"☀️ {weather}")
            if day or auto_context:
                display_day = recommender.get_current_day().title() if auto_context else day
                context_parts.append(f"📅 {display_day}")
            if time_of_day or auto_context:
                display_time = recommender.get_time_of_day().title() if auto_context else time_of_day
                context_parts.append(f"🕐 {display_time}")
            
            if context_parts:
                st.markdown(f"<p style='text-align:center;color:#764ba2;'><strong>Context: {' | '.join(context_parts)}</strong></p>",
                        unsafe_allow_html=True)
            
            st.markdown("---")
            
            if st.button("✨ Get Recommendations", type="primary", use_container_width=True):
                with st.spinner("🤖 Analyzing your taste with KNN algorithm..."):
                    recommendations = []
                    mood_param = None if mood_filter == "All Moods" else mood_filter.lower()
                    
                    try:
                        if rec_mode == "🎨 My Favorites Only":
                            recommendations = recommender.get_recommendations(
                                fav_movies, 
                                top_n=10, 
                                mood=mood_param, 
                                diversity=diversity_level,
                                weather=weather,
                                day=day,
                                time_of_day=time_of_day,
                                auto_context=auto_context
                            )
                            rec_description = f"Based on your {len(fav_movies)} favorites (KNN Algorithm)"
                        
                        elif rec_mode == "👥 Group Influence":
                            combined_movies = list(set(fav_movies + group_favorites))
                            recommendations = recommender.get_recommendations(
                                combined_movies, 
                                top_n=10, 
                                mood=mood_param, 
                                diversity=diversity_level,
                                weather=weather,
                                day=day,
                                time_of_day=time_of_day,
                                auto_context=auto_context
                            )
                            rec_description = f"Based on {len(combined_movies)} movies from you and your groups (KNN)"
                        
                        else:  # Hybrid
                            if user_ratings and len(all_users_ratings) > 1:
                                combined_movies = list(set(fav_movies + group_favorites))
                                recommendations = recommender.get_hybrid_recommendations(
                                    combined_movies, 
                                    user_ratings, 
                                    all_users_ratings, 
                                    top_n=10,
                                    mood=mood_param,
                                    diversity=diversity_level,
                                    weather=weather,
                                    day=day,
                                    time_of_day=time_of_day
                                )
                                rec_description = "Hybrid: KNN + Collaborative filtering"
                            else:
                                combined_movies = list(set(fav_movies + group_favorites))
                                recommendations = recommender.get_recommendations(
                                    combined_movies, 
                                    top_n=10, 
                                    mood=mood_param, 
                                    diversity=diversity_level,
                                    weather=weather,
                                    day=day,
                                    time_of_day=time_of_day,
                                    auto_context=auto_context
                                )
                                rec_description = "KNN-based (need more ratings for hybrid)"
                        
                        if recommendations:
                            st.markdown(f"### 🎯 Recommended For You")
                            st.markdown(f"*{rec_description}*")
                            
                            for i, rec in enumerate(recommendations, 1):
                                context_tag = rec.get('context_tags', '')
                                title_display = f"**#{i} 🎬 {rec['title']}** - {rec['score']}% match"
                                if context_tag:
                                    title_display += f" {context_tag}"
                                
                                with st.expander(title_display):
                                    col1, col2 = st.columns([3, 1])
                                    
                                    with col1:
                                        st.markdown(f"**Genres:** {rec['genres']}")
                                        if 'moods' in rec:
                                            st.markdown(f"**Moods:** {rec['moods']}")
                                        if 'overview' in rec:
                                            st.markdown(f"**Plot:** {rec['overview']}")
                                        if context_tag:
                                            st.success(context_tag)
                                    
                                    with col2:
                                        if st.button("➕ Add", key=f"add_rec_{rec['title']}", use_container_width=True):
                                            db.collection("users").document(st.session_state["user_id"]).update({
                                                "favorite_movies": firestore.ArrayUnion([rec['title']])
                                            })
                                            st.success("Added!")
                                            st.rerun()
                        else:
                            st.warning("No recommendations found with these filters. Try adjusting your settings!")
                    
                    except Exception as e:
                        st.error(f"Error generating recommendations: {str(e)}")
                        st.info("Try different settings or check your data.")
        else:
            st.info("👆 Add some favorite movies or join a group to get recommendations!")

    with tab4:
        st.markdown("### 🎯 Group Movie Board & Ratings")
        
        groups = user_data.get("groups_joined", [])
        
        if groups:
            group_options = {}
            for g_id in groups:
                g_doc = db.collection("groups").document(g_id).get()
                if g_doc.exists:
                    group_options[g_doc.to_dict().get("name")] = g_id
            
            if group_options:
                selected_group_name = st.selectbox("📊 Select a Group", list(group_options.keys()))
                selected_group_id = group_options[selected_group_name]
                
                group_doc = db.collection("groups").document(selected_group_id).get()
                group_data = group_doc.to_dict()
                
                st.markdown("---")
                
                board_tab, rec_tab = st.tabs(["🎬 Movie Board & Ratings", "💡 Group Recommendations"])
                
                with board_tab:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        movie_title = st.text_input("Add Movie to Board", placeholder="Enter movie name")
                    with col2:
                       if st.button("➕ Add", type="primary"):

                        if movie_title.strip():
                            group_movies = group_data.get("group_movies", {})

                            # 🩵 FIX: Ensure group_movies is always a dictionary
                            if isinstance(group_movies, list):
                                # convert list into a dict with placeholder values
                                group_movies = {str(i): {"added_by": None, "ratings": {}, "added_at": ""} for i in group_movies}
                            elif not isinstance(group_movies, dict):
                                group_movies = {}

                            if movie_title.strip() not in group_movies:
                                group_movies[movie_title.strip()] = {
                                    "added_by": st.session_state["user_id"],
                                    "ratings": {},
                                    "added_at": datetime.now().isoformat()
                                }
                                db.collection("groups").document(selected_group_id).update({
                                    "group_movies": group_movies
                                })
                                st.success(f"✅ Added '{movie_title}'!")
                                st.rerun()

                    
                    st.markdown("---")
                    st.markdown("**📽️ Movies on Board:**")
                    
                    group_movies = group_data.get("group_movies", {})
                    if group_movies:
                        for movie_title, movie_data in group_movies.items():
                            with st.expander(f"🎬 {movie_title}"):
                                ratings = movie_data.get("ratings", {})
                                if ratings:
                                    avg_rating = sum(ratings.values()) / len(ratings)
                                    st.write(f"**Average Rating:** ⭐ {avg_rating:.1f}/5 ({len(ratings)} ratings)")
                                
                                user_rating = ratings.get(st.session_state["user_id"], 0)
                                rating = st.slider(
                                    "Your Rating",
                                    min_value=1,
                                    max_value=5,
                                    value=int(user_rating) if user_rating else 3,
                                    key=f"rating_{selected_group_id}_{movie_title}"
                                )
                                
                                if st.button("💾 Save Rating", key=f"save_{selected_group_id}_{movie_title}"):
                                    group_movies[movie_title]["ratings"][st.session_state["user_id"]] = rating
                                    db.collection("groups").document(selected_group_id).update({
                                        "group_movies": group_movies
                                    })
                                    st.success(f"✅ Rated '{movie_title}' with {rating} stars!")
                                    st.rerun()
                    else:
                        st.info("No movies on board yet.")
                
                # ---------------- UPDATED rec_tab SECTION ----------------
                with rec_tab:
                    st.markdown("#### 💡 Group Recommendations")
                    st.markdown("Get recommendations based on your entire group's preferences!")
                    
                    # Collect all favorites from group members
                    all_group_favorites = []
                    members_list = group_data.get("members", [])
                    for member_uid in members_list:
                        try:
                            m_doc = db.collection("users").document(member_uid).get()
                            if m_doc.exists:
                                member_favs = m_doc.to_dict().get("favorite_movies", [])
                                all_group_favorites.extend(member_favs)
                        except:
                            continue
                    
                    # FIXED: Handle group_movies safely
                    group_movies_data = group_data.get("group_movies", {})
                    group_movies_list = []
                    
                    if isinstance(group_movies_data, dict):
                        group_movies_list = list(group_movies_data.keys())
                    elif isinstance(group_movies_data, list):
                        # If it's accidentally stored as a list, convert
                        group_movies_list = group_movies_data
                    
                    combined_group_movies = list(set(all_group_favorites + group_movies_list))
                    
                    if combined_group_movies:
                        st.write(f"📊 Analyzing {len(combined_group_movies)} movies from {len(members_list)} members")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            rec_method = st.radio(
                                "Recommendation Method:",
                                ["🎨 Content-Based", "⭐ Rating-Based"],
                                horizontal=True
                            )
                        with col2:
                            group_diversity = st.slider(
                                "🎲 Exploration Level:",
                                min_value=0,
                                max_value=100,
                                value=50,
                                key="group_diversity"
                            )
                        
                        if st.button("✨ Get Group Recommendations", type="primary"):
                            with st.spinner("🤖 Analyzing group preferences..."):
                                if rec_method == "🎨 Content-Based":
                                    recommendations = recommender.get_recommendations(
                                        combined_group_movies, 
                                        top_n=10,
                                        diversity=group_diversity
                                    )
                                    rec_description = f"Based on content similarity from {len(combined_group_movies)} group movies"
                                else:
                                    # FIXED: Collect all ratings safely
                                    all_ratings = {}
                                    
                                    if isinstance(group_movies_data, dict):
                                        for movie, data in group_movies_data.items():
                                            if isinstance(data, dict):
                                                ratings = data.get("ratings", {})
                                                if isinstance(ratings, dict):
                                                    for uid, rating in ratings.items():
                                                        if uid not in all_ratings:
                                                            all_ratings[uid] = {}
                                                        all_ratings[uid][movie] = rating
                                    
                                    if len(all_ratings) > 1:
                                        # Use average user's ratings
                                        avg_ratings = {}
                                        for uid, ratings in all_ratings.items():
                                            if ratings:
                                                avg_ratings[uid] = sum(ratings.values()) / len(ratings)
                                        
                                        if avg_ratings:
                                            best_user = max(avg_ratings, key=avg_ratings.get)
                                            recommendations = recommender.get_collaborative_recommendations(
                                                all_ratings[best_user],
                                                all_ratings,
                                                top_n=10
                                            )
                                            rec_description = "Based on collaborative filtering from group ratings"
                                        else:
                                            recommendations = recommender.get_recommendations(
                                                combined_group_movies, 
                                                top_n=10,
                                                diversity=group_diversity
                                            )
                                            rec_description = "Content-based (no ratings available)"
                                    else:
                                        recommendations = recommender.get_recommendations(
                                            combined_group_movies, 
                                            top_n=10,
                                            diversity=group_diversity
                                        )
                                        rec_description = "Content-based (need more ratings)"
                                
                                if recommendations:
                                    st.markdown("### 🏆 Recommended for Your Group")
                                    st.markdown(f"*{rec_description}*")
                                    
                                    for i, rec in enumerate(recommendations, 1):
                                        with st.expander(f"**#{i} 🎬 {rec['title']}** - {rec['score']}% match"):
                                            st.markdown(f"**Genres:** {rec['genres']}")
                                            if 'moods' in rec:
                                                st.markdown(f"**Moods:** {rec['moods']}")
                                            if 'overview' in rec:
                                                st.markdown(f"**Plot:** {rec['overview']}")
                                            
                                            if st.button("➕ Add to Group Board", key=f"add_group_{rec['title']}"):
                                                # Initialize group_movies if needed
                                                if not isinstance(group_movies_data, dict):
                                                    group_movies_data = {}
                                                
                                                if rec['title'] not in group_movies_data:
                                                    group_movies_data[rec['title']] = {
                                                        "added_by": st.session_state["user_id"],
                                                        "ratings": {},
                                                        "added_at": datetime.now().isoformat()
                                                    }
                                                    db.collection("groups").document(selected_group_id).update({
                                                        "group_movies": group_movies_data
                                                    })
                                                    st.success(f"Added '{rec['title']}' to group board!")
                                                    st.rerun()
                                else:
                                    st.warning("No recommendations found!")
                    else:
                        st.info("Add movies to favorites or the group board first!")
        else:
            st.info("👥 Join or create a group first!")

    with tab5:
        st.markdown("### 💬 Group Chat & 🎮 Fun Zone")

        groups = user_data.get("groups_joined", [])

        if groups:
            group_options = {}
            for g_id in groups:
                g_doc = db.collection("groups").document(g_id).get()
                if g_doc.exists:
                    group_options[g_doc.to_dict().get("name")] = g_id

            if group_options:
                selected_group_name = st.selectbox("💬 Select Group", list(group_options.keys()), key="chat_group_select")
                selected_group_id = group_options[selected_group_name]

                group_ref = db.collection("groups").document(selected_group_id)

                # ==============================
                # 📊 Real-time data listeners
                # ==============================
                if "chat_messages" not in st.session_state:
                    st.session_state.chat_messages = []
                if "online_members" not in st.session_state:
                    st.session_state.online_members = []
                if "current_game" not in st.session_state:
                    st.session_state.current_game = None

                # Firestore real-time updates (mocked with polling for Streamlit)
                group_doc = group_ref.get()
                if group_doc.exists:
                    data = group_doc.to_dict()
                    st.session_state.chat_messages = data.get("chat_messages", [])
                    st.session_state.online_members = data.get("online_members", [])
                    st.session_state.current_game = data.get("current_game", None)

                # ==============================
                # 🟢 Online members section
                # ==============================
                with st.expander("🟢 Online Members", expanded=True):
                    current_user = st.session_state["user_id"]
                    if current_user not in st.session_state.online_members:
                        st.session_state.online_members.append(current_user)
                        group_ref.update({"online_members": st.session_state.online_members})
                    st.markdown(", ".join([f"✅ **{m}**" for m in st.session_state.online_members]))

                st.markdown("---")

                # ==============================
                # 💬 Chat Display
                # ==============================
                chat_container = st.container()
                with chat_container:
                    messages = st.session_state.chat_messages[-50:]
                    for msg in messages:
                        sender = msg.get("sender_id", "Unknown")
                        message = msg.get("message", "")
                        timestamp = msg.get("timestamp", "")
                        time_str = datetime.fromisoformat(timestamp).strftime("%I:%M %p") if timestamp else ""
                        st.markdown(f"""
                        <div style="background:#f8f9fa;padding:0.75rem;border-radius:8px;margin:0.5rem 0;border-left:3px solid #667eea;">
                            <strong>{sender}</strong> <span style="color:#888;font-size:0.85rem;">{time_str}</span>
                            <p style="margin:0.25rem 0 0 0;">{message}</p>
                        </div>
                        """, unsafe_allow_html=True)

                # ==============================
                # 📤 Send message box
                # ==============================
                st.markdown("---")
                col1, col2 = st.columns([5, 1])
                with col1:
                    msg = st.text_input("Type a message", key=f"chat_input_{selected_group_id}", placeholder="Share your thoughts...")
                with col2:
                    if st.button("📤 Send", key=f"send_{selected_group_id}"):
                        if msg and msg.strip():
                            new_msg = {
                                "sender_id": st.session_state["user_id"],
                                "message": msg.strip(),
                                "timestamp": datetime.now().isoformat()
                            }
                            current_messages = st.session_state.chat_messages.copy()
                            current_messages.append(new_msg)
                            group_ref.update({"chat_messages": current_messages})
                            st.rerun()

                # ==============================
                # 🎮 Guess the Movie Mini-Game
                # ==============================
                st.markdown("---")
                st.subheader("🎮 Group Game: Guess the Movie")

                if st.session_state.current_game:
                    game = st.session_state.current_game
                    st.info(f"🎭 Hint: {game['hint']}")
                    guess = st.text_input("Your guess:", key=f"guess_{selected_group_id}")
                    if st.button("✅ Submit Guess", key=f"submit_{selected_group_id}"):
                        if guess and guess.lower().strip() == game["answer"].lower():
                            st.success("🎉 Correct! You guessed the movie!")
                            group_ref.update({"current_game": firestore.DELETE_FIELD})
                            st.session_state.current_game = None
                            st.rerun()
                        else:
                            st.warning("❌ Nope, try again!")
                else:
                    st.info("No game active. Start one below!")
                    with st.expander("🎬 Start a New Game"):
                        hint = st.text_input("Enter emoji or hint for movie:", key=f"hint_{selected_group_id}")
                        answer = st.text_input("Enter correct movie name (hidden)", type="password", key=f"answer_{selected_group_id}")
                        if st.button("🎯 Start Game", key=f"start_game_{selected_group_id}"):
                            if hint and answer:
                                new_game = {"hint": hint, "answer": answer.lower()}
                                group_ref.update({"current_game": new_game})
                                st.session_state.current_game = new_game
                                st.success("Game started! Others can guess now.")
                                st.rerun()
            else:
                st.info("You haven't joined any groups yet!")
        else:
            st.info("👥 Join a group to start chatting and gaming!")



    # 📊 TAB 6: Analytics Dashboard

    with tab6:
        st.markdown("### 📊 Analytics Dashboard")

        # Personal stats summary card
        fav_movies = user_data.get("favorite_movies", [])
        groups = user_data.get("groups_joined", [])

        if fav_movies:
            # Calculate personal metrics
            genre_diversity = recommender.calculate_genre_diversity(fav_movies)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding:2rem;border-radius:15px;color:white;margin:1rem 0;">
                <h3 style="margin:0;">🎭 Your Movie Profile</h3>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
                            gap:1rem;margin-top:1rem;">
                    <div style="background:rgba(255,255,255,0.2);padding:1rem;
                                border-radius:10px;text-align:center;">
                        <div style="font-size:2rem;font-weight:bold;">{len(fav_movies)}</div>
                        <div>Total Movies</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.2);padding:1rem;
                                border-radius:10px;text-align:center;">
                        <div style="font-size:2rem;font-weight:bold;">{genre_diversity:.0f}%</div>
                        <div>Genre Diversity</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.2);padding:1rem;
                                border-radius:10px;text-align:center;">
                        <div style="font-size:2rem;font-weight:bold;">{len(groups)}</div>
                        <div>Groups Joined</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Continue with detailed analytics options
        analysis_type = st.radio("Select Analysis Type:", ["👤 Personal Analytics", "👥 Group Analytics"])
        
        # ---------------- PERSONAL ANALYTICS ----------------
        if analysis_type == "👤 Personal Analytics":
            if fav_movies:
                genre_dist = recommender.get_genre_distribution(fav_movies)
                
                if genre_dist:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🎭 Your Favorite Genres")
                        fig = px.pie(
                            values=list(genre_dist.values()),
                            names=list(genre_dist.keys()),
                            title="Genre Distribution",
                            color_discrete_sequence=px.colors.sequential.RdBu
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### 📈 Genre Breakdown")
                        fig = px.bar(
                            x=list(genre_dist.keys()),
                            y=list(genre_dist.values()),
                            title="Movies per Genre",
                            labels={'x': 'Genre', 'y': 'Count'},
                            color=list(genre_dist.values()),
                            color_continuous_scale='Viridis'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("#### 📊 Your Stats")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Movies", len(fav_movies))
                    with col2:
                        st.metric("Unique Genres", len(genre_dist))
                    with col3:
                        top_genre = max(genre_dist, key=genre_dist.get)
                        st.metric("Top Genre", top_genre)
            else:
                st.info("🎬 Add favorite movies to see your analytics!")
        
        # ---------------- GROUP ANALYTICS ----------------
        else:
            if groups:
                group_options = {}
                for g_id in groups:
                    g_doc = db.collection("groups").document(g_id).get()
                    if g_doc.exists:
                        group_options[g_doc.to_dict().get("name")] = g_id
                
                if group_options:
                    selected_group = st.selectbox("Select Group", list(group_options.keys()))
                    selected_group_id = group_options[selected_group]
                    
                    group_doc = db.collection("groups").document(selected_group_id).get()
                    group_data = group_doc.to_dict()
                    group_movies = group_data.get("group_movies", {})
                    members = group_data.get("members", [])
                    
                    all_favorites = []
                    for member_uid in members:
                        m_doc = db.collection("users").document(member_uid).get()
                        if m_doc.exists:
                            all_favorites.extend(m_doc.to_dict().get("favorite_movies", []))
                    
                    if all_favorites or group_movies:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if all_favorites:
                                st.markdown("#### 🎭 Group Genre Preferences")
                                genre_dist = recommender.get_genre_distribution(all_favorites)
                                fig = px.pie(
                                    values=list(genre_dist.values()),
                                    names=list(genre_dist.keys()),
                                    title="Combined Genre Distribution",
                                    color_discrete_sequence=px.colors.sequential.Plasma
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            if group_movies:
                                st.markdown("#### ⭐ Top Rated Movies")
                                
                                movie_ratings = []
                                for title, data in group_movies.items():
                                    ratings = data.get("ratings", {})
                                    if ratings:
                                        avg = sum(ratings.values()) / len(ratings)
                                        movie_ratings.append({
                                            "Movie": title,
                                            "Avg Rating": avg,
                                            "Votes": len(ratings)
                                        })
                                
                                if movie_ratings:
                                    df = pd.DataFrame(movie_ratings).sort_values("Avg Rating", ascending=False).head(10)
                                    fig = px.bar(
                                        df,
                                        x="Movie",
                                        y="Avg Rating",
                                        title="Top Rated Movies",
                                        color="Avg Rating",
                                        color_continuous_scale="Tealgrn"
                                    )
                                    fig.update_layout(xaxis_tickangle=-45)
                                    st.plotly_chart(fig, use_container_width=True)
                        
                        st.markdown("#### 📊 Group Stats")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Members", len(members))
                        with col2:
                            st.metric("Movies on Board", len(group_movies))
                        with col3:
                            total_ratings = sum(len(m.get("ratings", {})) for m in group_movies.values())
                            st.metric("Total Ratings", total_ratings)
                        with col4:
                            st.metric("Combined Favorites", len(all_favorites))
                    else:
                        st.info("No data available yet for this group.")
            else:
                st.info("Join a group to see group analytics!")

# =====================================================================
# TAB 7: 🤝 Movie Taste Compatibility
# =====================================================================

    with tab7:
        st.markdown("### 🤝 Movie Taste Compatibility")

        groups = user_data.get("groups_joined", [])
        fav_movies = user_data.get("favorite_movies", [])

        if groups and fav_movies:
            st.markdown("See how your movie taste compares with your friends!")

            # Collect group names from Firestore
            group_options = {}
            for g_id in groups:
                g_doc = db.collection("groups").document(g_id).get()
                if g_doc.exists:
                    group_data = g_doc.to_dict()
                    group_options[group_data.get("name", f"Group {g_id[:6]}")] = g_id

            if group_options:
                selected_group = st.selectbox("Select a Group", list(group_options.keys()))
                selected_group_id = group_options[selected_group]

                group_doc = db.collection("groups").document(selected_group_id).get()
                group_data = group_doc.to_dict()
                members = group_data.get("members", [])

                st.markdown("---")
                st.markdown("#### 💫 Your Compatibility Scores")

                # Calculate compatibility for each member
                compatibility_scores = []

                for member_uid in members:
                    if member_uid != st.session_state["user_id"]:
                        m_doc = db.collection("users").document(member_uid).get()
                        if m_doc.exists:
                            m_data = m_doc.to_dict()
                            member_favs = m_data.get("favorite_movies", [])

                            if member_favs:
                                score = recommender.calculate_taste_compatibility(
                                    fav_movies, member_favs
                                )
                                compatibility_scores.append({
                                    'name': m_data.get('email', 'Unknown User'),
                                    'user_id': m_data.get('custom_user_id', member_uid[:6]),
                                    'score': score,
                                    'movies': len(member_favs)
                                })

                # Sort results by score (highest first)
                compatibility_scores.sort(key=lambda x: x['score'], reverse=True)

                # Display results
                if compatibility_scores:
                    for comp in compatibility_scores:
                        score = comp['score']

                        # Color and label based on score
                        if score >= 70:
                            color = "#4CAF50"
                            emoji = "🎯"
                            desc = "Perfect Match!"
                        elif score >= 50:
                            color = "#FFC107"
                            emoji = "👍"
                            desc = "Good Match"
                        elif score >= 30:
                            color = "#FF9800"
                            emoji = "🤔"
                            desc = "Some Overlap"
                        else:
                            color = "#F44336"
                            emoji = "🎲"
                            desc = "Very Different"

                        st.markdown(f"""
                        <div style="background:white;padding:1rem;border-radius:10px;margin:0.5rem 0;
                                    border-left:5px solid {color};box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <div>
                                    <strong>{emoji} {comp['name']}</strong> ({comp['user_id']})
                                    <br><small>{comp['movies']} movies in their collection</small>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:2rem;font-weight:bold;color:{color};">{score}%</div>
                                    <div style="color:#666;font-size:0.9rem;">{desc}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Summary stats
                    st.markdown("---")
                    st.markdown("#### 📊 Group Summary")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        avg_compat = sum(c['score'] for c in compatibility_scores) / len(compatibility_scores)
                        st.metric("Average Compatibility", f"{avg_compat:.1f}%")

                    with col2:
                        best_match = compatibility_scores[0]
                        st.metric("Best Match", f"{best_match['score']}%",
                                delta=best_match['name'].split('@')[0])

                    with col3:
                        your_diversity = recommender.calculate_genre_diversity(fav_movies)
                        st.metric("Your Genre Diversity", f"{your_diversity:.1f}%")

                else:
                    st.info("Other members need to add favorite movies first to compare compatibility.")
            else:
                st.info("No valid groups found. Try joining a group first.")
        else:
            if not groups:
                st.info("👥 Join a group to see compatibility scores!")
            else:
                st.info("📽️ Add favorite movies to calculate compatibility!")
