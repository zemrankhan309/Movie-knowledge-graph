import streamlit as st
from graph_utils import (
    build_knowledge_graph,
    search_by_actor,
    search_by_director,
    search_by_genre,
    MOVIES_DATABASE
)

# --- Streamlit Presentation Setup ---
st.set_page_config(
    page_title="Cinematic Graph Search Engine",
    page_icon="🔍",
    layout="wide"
)

# --- Initialize Background Graph ---
G = build_knowledge_graph()

# --- Extract Dropdown Options ---
all_actors = sorted(list({n for n, d in G.nodes(data=True) if d.get("type") == "Actor"}))
all_directors = sorted(list({n for n, d in G.nodes(data=True) if d.get("type") == "Director"}))
all_genres = sorted(list({n for n, d in G.nodes(data=True) if d.get("type") == "Genre"}))

# --- Top Banner Application UI ---
st.markdown("<h1 style='color: #E50914; margin-bottom:0;'>🎬 Cinematic Graph Search Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #A0A0A0; font-size:1.1rem; margin-bottom:2rem;'>Query hidden relationship networks instantly to get clean, structured data dashboards.</p>", unsafe_allow_html=True)

# --- Search Strategy Control Center ---
st.markdown("### 🔍 Select Search Parameters")
tab_actor, tab_director, tab_genre, tab_all = st.tabs([
    "👤 Search by Actor", 
    "🎥 Search by Director", 
    "🍿 Filter by Genre",
    "🗂️ View Master Database"
])

# Container variables for matching results
matched_movie_titles = []
search_context = ""

with tab_actor:
    target_actor = st.selectbox("Choose an Actor:", ["Select an Actor..."] + all_actors)
    if target_actor != "Select an Actor...":
        matched_movie_titles = search_by_actor(G, target_actor)
        search_context = f"Filmography for actor: {target_actor}"

with tab_director:
    target_director = st.selectbox("Choose a Director:", ["Select a Director..."] + all_directors)
    if target_director != "Select a Director...":
        matched_movie_titles = search_by_director(G, target_director)
        search_context = f"Directed works by: {target_director}"

with tab_genre:
    target_genre = st.selectbox("Choose a Genre:", ["Select a Genre..."] + all_genres)
    if target_genre != "Select a Genre...":
        matched_movie_titles = search_by_genre(G, target_genre)
        search_context = f"Catalogued under genre: {target_genre}"

with tab_all:
    st.markdown("#### Complete Localized System Footprint")
    if st.button("Display Entire Database Content 📋"):
        matched_movie_titles = [m["title"] for m in MOVIES_DATABASE]
        search_context = "Complete Movie Catalog"

# --- Output Presentation Layer ---
st.markdown("---")
if matched_movie_titles:
    st.markdown(f"### 📊 Results: <span style='color:#1E90FF;'>{search_context}</span>", unsafe_allow_html=True)
    st.caption(f"Found {len(matched_movie_titles)} matching titles via relational graph lookup.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Loop over database records to render complete details for matching items
    for movie in MOVIES_DATABASE:
        if movie["title"] in matched_movie_titles:
            with st.container():
                c1, c2 = st.columns([1, 5])
                with c1:
                    st.markdown(f"<h2 style='margin:0; text-align:center; background-color:#262730; padding:15px; border-radius:10px; border: 2px solid #E50914;'>🎬<br><span style='font-size:1.1rem;'>{movie['year']}</span></h2>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<h3 style='margin:0; color:#E50914;'>{movie['title']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"**Director:** {movie['director']} | **Genres:** {', '.join(movie['genres'])}")
                    st.markdown(f"**Starring Cast:** {', '.join(movie['cast'])}")
                    st.markdown(f"*Summary:* {movie['summary']}")
                st.markdown("<div style='margin-bottom:1.5rem; border-bottom:1px solid #444;'></div>", unsafe_allow_html=True)
else:
    st.info("💡 Choose any search criteria parameter inside the tabs above to pull real-time results from the underlying dataset.")