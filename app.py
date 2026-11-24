
import streamlit as st
import requests
from training import recommend, new_df

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="YASIN CINEMA AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "")
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 5%, #252052 0%, transparent 35%),
        radial-gradient(circle at 90% 30%, #172b55 0%, transparent 35%),
        #080b18;
    color: #f4f5ff;
}

header {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #11152d, #090d1d);
    border-right: 1px solid #292d50;
}

.brand {
    font-size: 38px;
    font-weight: 900;
    text-align: center;
    letter-spacing: 2px;
    color: #a78bfa;
    margin-bottom: 0;
}

.brand span {
    color: #38bdf8;
}

.tagline {
    text-align: center;
    color: #a5b4d4;
    font-size: 15px;
    margin-bottom: 30px;
}

.hero {
    background: linear-gradient(120deg, #211a50, #142d59, #11152e);
    border: 1px solid #41416f;
    border-radius: 22px;
    padding: 35px;
    margin: 15px 0 30px 0;
}

.hero h1 {
    color: white;
    font-size: 38px;
    font-weight: 900;
    margin-bottom: 10px;
}

.hero p {
    color: #c5c9e8;
    font-size: 16px;
}

.section-heading {
    font-size: 25px;
    font-weight: 800;
    color: #c4b5fd;
    margin: 25px 0 15px 0;
}

.movie-name {
    color: #e9e7ff;
    font-size: 17px;
    font-weight: 800;
}

.movie-info {
    color: #a5b4d4;
    font-size: 13px;
}

div.stButton > button {
    background: linear-gradient(100deg, #7c3aed, #2563eb);
    color: white;
    border: 1px solid #8b7cf6;
    border-radius: 11px;
    font-weight: 800;
    min-height: 45px;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #38bdf8;
    color: white;
    transform: translateY(-2px);
}

[data-testid="stSelectbox"] {
    background: #151a35;
    border-radius: 10px;
}

div[data-testid="stImage"] img {
    border-radius: 13px;
}

hr {
    border-color: #30365d;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TMDB API
# --------------------------------------------------

@st.cache_data(ttl=86400)
def get_movie_details(movie_id, api_key):

    if not api_key:
        return None

    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}"

    try:
        response = requests.get(
            url,
            params={"api_key": api_key},
            timeout=20
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException:
        return None


# --------------------------------------------------
# MOVIE DATA
# --------------------------------------------------

movie_ids = dict(
    zip(new_df["title"], new_df["movie_id"])
)

movie_titles = new_df["title"].drop_duplicates().tolist()

if not movie_titles:
    st.error("Movie dataset is empty. Please check your dataset.")
    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="brand">YASIN <span>CINEMA</span></div>',
        unsafe_allow_html=True
    )

    st.caption("YOUR PERSONAL AI MOVIE DISCOVERY")

    st.divider()

    st.markdown("### 🎬 Explore Cinema")

    st.write("🏠 Home")
    st.write("🍿 Movie Recommendations")
    st.write("🔎 Discover Movies")

    st.divider()

    st.markdown("### ✨ About")

    st.caption(
        "Discover movies using an intelligent "
        "content-based recommendation engine."
    )

    st.divider()

    st.caption("Powered by TMDB movie data.")

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    '<div class="brand">YASIN <span>CINEMA AI</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">'
    'DISCOVER MOVIES • EXPLORE STORIES • ENJOY CINEMA'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
    <h1>Your Next Favorite Movie Awaits.</h1>
    <p>
        Explore thousands of movies and discover personalized
        recommendations powered by AI-based movie similarity.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MOVIE SELECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">🔎 Discover Your Movie</div>',
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "Choose a movie to explore",
    movie_titles,
    index=movie_titles.index("Avatar")
    if "Avatar" in movie_titles else 0
)

selected_id = movie_ids[selected_movie]

# --------------------------------------------------
# SELECTED MOVIE DETAILS
# --------------------------------------------------

selected_details = get_movie_details(
    selected_id,
    TMDB_API_KEY
)

if selected_details:

    left, right = st.columns([1, 2])

    with left:

        poster = selected_details.get("poster_path")

        if poster:
            st.image(
                TMDB_IMAGE_URL + poster,
                use_container_width=True
            )
        else:
            st.info("Poster not available.")

    with right:

        st.markdown(
            f"## {selected_details.get('title', selected_movie)}"
        )

        rating = selected_details.get("vote_average", "N/A")
        release = selected_details.get("release_date", "N/A")

        genres = selected_details.get("genres", [])

        genre_names = ", ".join(
            genre["name"] for genre in genres
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("⭐ Rating", rating)
        col2.metric("📅 Release", release[:4] if release else "N/A")
        col3.metric("🎭 Genres", len(genres))

        st.markdown("### Movie Overview")

        st.write(
            selected_details.get(
                "overview",
                "Overview not available."
            )
        )

        st.caption("Genres: " + (genre_names or "N/A"))

else:

    st.warning(
        "Movie details could not be loaded. "
        "Check your TMDB API key and internet connection."
    )

# --------------------------------------------------
# RECOMMENDATION ENGINE
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-heading">🍿 Discover Similar Movies</div>',
    unsafe_allow_html=True
)

st.write(
    "Select your movie and let YASIN CINEMA AI "
    "find movies with similar content."
)

if st.button(
    "✨ GENERATE MY RECOMMENDATIONS",
    use_container_width=True
):

    try:
        results = recommend(selected_movie)

        st.session_state["yasin_recommendations"] = results
        st.session_state["yasin_selected_movie"] = selected_movie

    except Exception as error:
        st.session_state["yasin_recommendations"] = []
        st.error(f"Recommendation error: {error}")

# --------------------------------------------------
# DISPLAY RECOMMENDATIONS
# --------------------------------------------------

if (
    st.session_state.get("yasin_selected_movie")
    == selected_movie
    and "yasin_recommendations" in st.session_state
):

    recommendations = st.session_state["yasin_recommendations"]

    if recommendations:

        st.success(
            f"Movies selected for fans of {selected_movie}"
        )

        columns = st.columns(5)

        for index, movie in enumerate(recommendations):

            with columns[index % 5]:

                movie_id = movie_ids.get(movie)

                if movie_id is None:
                    st.write(movie)
                    continue

                details = get_movie_details(
                    movie_id,
                    TMDB_API_KEY
                )

                with st.container(border=True):

                    if details:

                        poster = details.get("poster_path")

                        if poster:
                            st.image(
                                TMDB_IMAGE_URL + poster,
                                use_container_width=True
                            )
                        else:
                            st.info("Poster unavailable")

                        st.markdown(
                            f"**{details.get('title', movie)}**"
                        )

                        rating = details.get(
                            "vote_average", "N/A"
                        )

                        release = details.get(
                            "release_date", "N/A"
                        )

                        st.caption(
                            f"⭐ {rating} | "
                            f"{release[:4] if release else 'N/A'}"
                        )

                    else:
                        st.write(movie)
                        st.caption("Movie details unavailable")

    else:
        st.warning("No recommendations found.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#9ca3c7; padding:20px;">
        <h3 style="color:#a78bfa;">YASIN CINEMA AI</h3>
        Discover Movies. Explore Stories. Enjoy Cinema.
        <br><br>
        Movie data and images provided by TMDB.
        This product uses the TMDB API but is not endorsed
        or certified by TMDB.
    </div>
    """,
    unsafe_allow_html=True
)
