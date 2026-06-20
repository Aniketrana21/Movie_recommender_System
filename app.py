# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import os
# st.image(
#     "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba",
#     use_container_width=True
# )
# st.markdown("""
# <style>
#
# /* Main Background */
# .stApp {
#     background-color: #0E1117;
# }
#
# /* Title */
# h1 {
#     text-align: center;
#     color: white;
# }
#
# /* Recommendation Card */
# .movie-card {
#     background-color: #1E1E1E;
#     padding: 15px;
#     border-radius: 15px;
#     box-shadow: 0px 4px 10px rgba(255,255,255,0.1);
#     text-align: center;
#     transition: transform 0.3s ease;
# }
#
# /* Movie Name */
# .movie-title {
#     color: white;
#     font-size: 20px;
#     font-weight: bold;
# }
#
# /* Rating */
# .rating {
#     color: gold;
#     font-weight: bold;
# }
#
# /* Match Score */
# .match-score {
#     color: #00ff88;
#     font-weight: bold;
# }
#
# .movie-card:hover {
#     transform: scale(1.05);
# }
# </style>
# """, unsafe_allow_html=True)
# API_KEY = "1afde1a7c96a6a1945685566f8935b60"
# st.set_page_config(
#     page_title="Movie Recommender",
#     page_icon="🎬",
#     layout="wide"
# )
# st.markdown("""<h1>🎬 AI Movie Recommendation System</h1><p style='text-align:center;color:gray;'>Discover movies using Machine Learning
# </p>
# """, unsafe_allow_html=True)
# st.markdown(
#     "Get personalized movie recommendations using Machine Learning and TMDB."
# )
#
# # def fetch_poster(movie_id):
# #     try:
# #         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1afde1a7c96a6a1945685566f8935b60&language=en-US"
# #
# #         response = requests.get(url, timeout=10)
# #         response.raise_for_status()
# #
# #         data = response.json()
# #
# #         if data.get('poster_path'):
# #             return "https://image.tmdb.org/t/p/w500" + data['poster_path']
# #
# #         return None
# #
# #     except Exception as e:
# #         st.error(f"TMDB Error: {e}")
# #         return None
#
# session = requests.Session()
# @st.cache_data(show_spinner=False)
# def fetch_movie_details(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
#
#         response = session.get(url, timeout=30)
#         response.raise_for_status()
#
#         data = response.json()
#         poster = None
#         if data.get("poster_path"):
#             poster = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
#
#         return {
#             "poster": poster,
#             "rating": data.get("vote_average", "N/A"),
#             "release_date": data.get("release_date", "N/A"),
#             "overview": data.get("overview", "No description available")
#         }
#
#
#
#     except requests.exceptions.Timeout:
#         return {
#             "poster": None,
#             "rating": "N/A",
#             "release_date": "N/A",
#             "overview": "Unable to fetch movie details"
#         }
#
#
#     except requests.exceptions.HTTPError:
#         return {
#             "poster": None,
#             "rating": "N/A",
#             "release_date": "N/A",
#             "overview": "Unable to fetch movie details"
#         }
#
#
#     except requests.exceptions.RequestException:
#         return {
#             "poster": None,
#             "rating": "N/A",
#             "release_date": "N/A",
#             "overview": "Unable to fetch movie details"
#         }
#     except Exception as e:
#         print("TMDB Error:", e)
#
#         return {
#             "poster": None,
#             "rating": "N/A",
#             "release_date": "N/A",
#             "overview": "No description available"
#         }
#
# movie_list = pickle.load(open('movies.pkl', 'rb'))
# similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
# def recommend(movie):
#     movie_index = movie_list[movie_list['title'] == movie].index[0]
#     distances = similarity_matrix[movie_index]
#     similarity_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_score = []
#     recommended_movies=[]
#     recommended_movies_details=[]
#     for i in similarity_list:
#         movie_id = movie_list.iloc[i[0]].movie_id
#         recommended_movies.append(movie_list.iloc[i[0]].title)
#         recommended_movies_details.append(fetch_movie_details(movie_id))
#         recommended_score.append(round(i[1] * 100,2))
#     return recommended_movies, recommended_movies_details,recommended_score
#
# movie_list_name = movie_list["title"].values
#
#
# selected_movies_name = st.selectbox(
#     "🎬 Select a Movie",
#     movie_list_name,
#     index=None,
#     placeholder="Select your favorite movie..."
# )
# if selected_movies_name is None:
#     st.warning("Please select a movie.")
#     st.stop()
#
# with st.container():
#     st.subheader("Recommended Movies")
#     if st.button('Recommend'):
#         with st.spinner("Finding Similar Movies..."):
#             names,details,score = recommend(selected_movies_name)
#             # st.metric("Movies", len(movie_list))
#             # st.metric("Features", len(movie_list.columns))
#             cols = st.columns(5)
#
#             for col, movie_name, movie_detail,score in zip(cols, names, details,score):
#
#                 with col:
#
#                     st.markdown(f"""<div class="movie-card">
#                         <div class="movie-title">{movie_name}</div>
#                     </div>
#                     """, unsafe_allow_html=True)
#
#                     if movie_detail["poster"]:
#                         st.image(movie_detail["poster"],use_container_width=True)
#
#                     st.markdown(
#                         f"<div class='rating'>⭐ Rating: {movie_detail['rating']}</div>",
#                         unsafe_allow_html=True
#                     )
#
#                     st.write(f"📅 Release: {movie_detail['release_date']}")
#
#                     overview = movie_detail["overview"]
#
#                     if len(overview) > 150:
#                         overview = overview[:150] + "..."
#
#                     st.caption(overview)
#
#                     st.markdown(
#                         f"<div class='match-score'>🎯 Match Score: {score}%</div>",
#                         unsafe_allow_html=True
#                     )
#
# col1, col2 = st.columns(2)
# st.markdown("""
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)
# with col1:
#     st.metric("Movies", len(movie_list))
#
# with col2:
#     st.metric("Features", len(movie_list.columns))







import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="CineMatch — AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SECURITY: never hardcode API keys. Use Streamlit secrets or env vars.
# Add this to .streamlit/secrets.toml -> TMDB_API_KEY = "your_key_here"
API_KEY = st.secrets.get("TMDB_API_KEY", os.environ.get("TMDB_API_KEY", ""))

# ============================================================
# DESIGN SYSTEM — CSS
# ============================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-primary: #0A0B0F;
    --bg-secondary: #13151C;
    --bg-card: #181B24;
    --bg-card-hover: #1E222D;
    --accent-1: #7C5CFF;
    --accent-2: #FF5C8A;
    --accent-gradient: linear-gradient(135deg, #7C5CFF 0%, #FF5C8A 100%);
    --gold: #FFC857;
    --text-primary: #F4F4F6;
    --text-secondary: #9A9DA8;
    --text-muted: #5C5F6B;
    --border-subtle: rgba(255,255,255,0.06);
    --success: #3DDC97;
}

/* ---------- Global ---------- */
.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(124,92,255,0.12) 0%, transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(255,92,138,0.10) 0%, transparent 40%),
        var(--bg-primary);
    font-family: 'Inter', sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding-top: 1.5rem !important;
    max-width: 1280px;
}

/* ---------- Hero ---------- */
.hero-wrap {
    text-align: center;
    padding: 2.2rem 1rem 1.6rem 1rem;
    margin-bottom: 0.5rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(124,92,255,0.12);
    border: 1px solid rgba(124,92,255,0.3);
    color: #B9A8FF;
    font-size: 12.5px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 100px;
    margin-bottom: 1.1rem;
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    line-height: 1.1;
    margin: 0;
    background: linear-gradient(135deg, #FFFFFF 30%, #B9A8FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1.05rem;
    margin-top: 0.7rem;
    font-weight: 400;
}

/* ---------- Stat strip ---------- */
.stat-strip {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin: 1.6rem 0 0.5rem 0;
    flex-wrap: wrap;
}
.stat-pill {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 0.85rem 1.6rem;
    text-align: center;
    min-width: 130px;
}
.stat-pill .num {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
}
.stat-pill .label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 2px;
}

/* ---------- Selector section ---------- */
.section-label {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
    margin-top: 2rem;
}

div[data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    min-height: 54px;
}
div[data-baseweb="select"] > div:hover {
    border-color: var(--accent-1) !important;
}
/* Selected value + typed search text */
div[data-baseweb="select"] * {
    color: var(--text-primary) !important;
}
div[data-baseweb="select"] input {
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
}
div[data-baseweb="select"] svg {
    fill: var(--text-secondary) !important;
}
/* Dropdown menu (the list of options) */
ul[data-testid="stSelectboxVirtualDropdown"] li,
div[data-baseweb="popover"] li {
    color: var(--text-primary) !important;
    background-color: var(--bg-card) !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: var(--bg-card-hover) !important;
}
div[data-baseweb="popover"] > div {
    background-color: var(--bg-card) !important;
}

/* Recommend button */
.stButton > button {
    background: var(--accent-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    box-shadow: 0 8px 24px rgba(124,92,255,0.35) !important;
    transition: all 0.25s ease !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(124,92,255,0.5) !important;
}

/* ---------- Movie Cards ---------- */
.movie-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    min-height: 560px;
    display: flex;
    flex-direction: column;
}
/* Force equal-width, equal-height columns for the result row */
div[data-testid="column"] {
    display: flex;
    flex-direction: column;
}
div[data-testid="column"] > div {
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-6px);
    border-color: rgba(124,92,255,0.4);
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}
.poster-wrap {
    position: relative;
    border-radius: 18px 18px 0 0;
    overflow: hidden;
    aspect-ratio: 2/3;
    background: var(--bg-secondary);
}
.poster-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}
.match-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(10,11,15,0.85);
    backdrop-filter: blur(6px);
    border: 1px solid var(--success);
    color: var(--success);
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 100px;
}
.card-body {
    padding: 14px 16px 18px 16px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}
.movie-title {
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary);
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 6px;
    min-height: 2.6em;
}
.meta-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 13px;
}
.rating-chip {
    color: var(--gold);
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 3px;
}
.release-chip {
    color: var(--text-muted);
}
.overview-text {
    color: var(--text-secondary);
    font-size: 12.5px;
    line-height: 1.5;
    margin-bottom: 10px;
    flex-grow: 1;
    min-height: 3.4em;
}
.score-bar-track {
    background: rgba(255,255,255,0.07);
    border-radius: 100px;
    height: 6px;
    width: 100%;
    overflow: hidden;
    margin-top: auto;
}
.score-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: var(--accent-gradient);
}
.score-label {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ---------- Empty state ---------- */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-muted);
}
.empty-state .icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    opacity: 0.6;
}

hr.divider {
    border: none;
    border-top: 1px solid var(--border-subtle);
    margin: 2.2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">✨ Machine Learning · Content-Based Filtering</div>
    <h1 class="hero-title">CineMatch</h1>
    <p class="hero-subtitle">Discover your next favorite film — powered by similarity scoring & TMDB</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_resource(show_spinner=False)
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

try:
    movie_list, similarity_matrix = load_data()
except FileNotFoundError:
    st.error("⚠️ Required model files (`movies.pkl`, `similarity.pkl`) were not found in the app directory.")
    st.stop()

session = requests.Session()

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_movie_details(movie_id):
    if not API_KEY:
        return {"poster": None, "rating": "N/A", "release_date": "N/A",
                 "overview": "TMDB API key not configured.", "error": "no_api_key"}
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        poster = None
        if data.get("poster_path"):
            poster = "https://image.tmdb.org/t/p/w500" + data["poster_path"]

        return {
            "poster": poster,
            "rating": data.get("vote_average", "N/A"),
            "release_date": data.get("release_date", "N/A"),
            "overview": data.get("overview") or "No description available.",
            "error": None
        }
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        return {"poster": None, "rating": "N/A", "release_date": "N/A",
                 "overview": "Unable to fetch movie details right now.",
                 "error": f"HTTP {status}"}
    except requests.exceptions.RequestException as e:
        return {"poster": None, "rating": "N/A", "release_date": "N/A",
                 "overview": "Unable to fetch movie details right now.",
                 "error": f"Network error: {type(e).__name__}"}
    except Exception as e:
        return {"poster": None, "rating": "N/A", "release_date": "N/A",
                 "overview": "No description available.",
                 "error": f"{type(e).__name__}: {e}"}


def recommend(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    similarity_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies, recommended_details, recommended_score = [], [], []
    for i in similarity_list:
        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movies.append(movie_list.iloc[i[0]].title)
        recommended_details.append(fetch_movie_details(movie_id))
        recommended_score.append(round(i[1] * 100, 1))
    return recommended_movies, recommended_details, recommended_score


movie_list_name = movie_list["title"].values

# ============================================================
# STAT STRIP
# ============================================================
st.markdown(f"""
<div class="stat-strip">
    <div class="stat-pill"><div class="num">{len(movie_list):,}</div><div class="label">Movies Indexed</div></div>
    <div class="stat-pill"><div class="num">{len(movie_list.columns)}</div><div class="label">Features Used</div></div>
    <div class="stat-pill"><div class="num">Top 5</div><div class="label">Matches Returned</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================
# SELECTOR
# ============================================================
st.markdown("<div class='section-label'>Choose a film you love</div>", unsafe_allow_html=True)

col_select, col_btn = st.columns([4, 1], vertical_alignment="bottom")
with col_select:
    selected_movies_name = st.selectbox(
        " ",
        movie_list_name,
        index=None,
        placeholder="Search for a movie title...",
        label_visibility="collapsed"
    )
with col_btn:
    go = st.button("🎯 Recommend", use_container_width=True)

# ============================================================
# RESULTS
# ============================================================
if selected_movies_name is None:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🍿</div>
        Pick a movie above to get five personalized recommendations.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if go:
    with st.spinner("Analyzing similarity patterns..."):
        names, details, scores = recommend(selected_movies_name)

    st.markdown(f"<div class='section-label'>Because you liked “{selected_movies_name}”</div>", unsafe_allow_html=True)

    cols = st.columns(5, gap="medium")
    errors_seen = []
    for col, movie_name, movie_detail, score in zip(cols, names, details, scores):
        if movie_detail.get("error"):
            errors_seen.append(f"**{movie_name}** → {movie_detail['error']}")
        with col:
            poster_html = (
                f"<img src='{movie_detail['poster']}' />"
                if movie_detail["poster"]
                else "<div style='display:flex;align-items:center;justify-content:center;height:100%;color:#5C5F6B;font-size:2rem;'>🎬</div>"
            )

            overview = movie_detail["overview"]
            if len(overview) > 110:
                overview = overview[:110].rsplit(" ", 1)[0] + "…"

            rating_val = movie_detail["rating"]
            rating_display = f"{rating_val:.1f}" if isinstance(rating_val, (int, float)) else rating_val

            st.markdown(f"""
            <div class="movie-card">
                <div class="poster-wrap">
                    {poster_html}
                    <div class="match-badge">{score}% match</div>
                </div>
                <div class="card-body">
                    <div class="movie-title">{movie_name}</div>
                    <div class="meta-row">
                        <span class="rating-chip">⭐ {rating_display}</span>
                        <span class="release-chip">📅 {movie_detail['release_date']}</span>
                    </div>
                    <div class="overview-text">{overview}</div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill" style="width:{score}%;"></div>
                    </div>
                    <div class="score-label">Similarity score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    if errors_seen:
        with st.expander("⚠️ Some poster/details lookups failed — click to see why"):
            for line in errors_seen:
                st.markdown(line)
            st.caption(
                "Common causes: API key not set in `.streamlit/secrets.toml`, "
                "an invalid/expired TMDB key, or a network/firewall block on api.themoviedb.org."
            )