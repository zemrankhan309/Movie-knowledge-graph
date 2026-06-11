import networkx as nx
import streamlit as st

# Comprehensive In-Memory Structured Dataset
MOVIES_DATABASE = [
    {
        "title": "Inception",
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "genres": ["Sci-Fi", "Action", "Thriller"],
        "year": 2010,
        "summary": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "title": "The Dark Knight",
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Gary Oldman"],
        "genres": ["Action", "Drama", "Crime"],
        "year": 2008,
        "summary": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "year": 2014,
        "summary": "When Earth becomes uninhabitable, a team of explorers travels through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        "title": "The Revenant",
        "director": "Alejandro G. Iñárritu",
        "cast": ["Leonardo DiCaprio", "Tom Hardy", "Domhnall Gleeson"],
        "genres": ["Drama", "Adventure", "Western"],
        "year": 2015,
        "summary": "A frontiersman on a fur trading expedition in the 1820s fights for survival after being mauled by a bear and left for dead by members of his own hunting team."
    },
    {
        "title": "Catch Me If You Can",
        "director": "Steven Spielberg",
        "cast": ["Leonardo DiCaprio", "Tom Hanks", "Christopher Walken"],
        "genres": ["Biography", "Crime", "Drama"],
        "year": 2002,
        "summary": "A seasoned FBI agent pursues Frank Abagnale Jr. who, before his 19th birthday, successfully forged millions of dollars' worth of checks while posing as a Pan Am pilot, a doctor, and a legal prosecutor."
    },
    {
        "title": "Saving Private Ryan",
        "director": "Steven Spielberg",
        "cast": ["Tom Hanks", "Matt Damon", "Tom Sizemore"],
        "genres": ["Drama", "War"],
        "year": 1998,
        "summary": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action."
    }
]

@st.cache_resource
def build_knowledge_graph():
    """Builds the background graph structures for fast relationship querying."""
    G = nx.Graph()
    for movie in MOVIES_DATABASE:
        title = movie["title"]
        G.add_node(title, type="Movie", year=movie["year"], summary=movie["summary"], genres=movie["genres"])
        G.add_node(movie["director"], type="Director")
        G.add_edge(movie["director"], title, relation="DIRECTED")
        
        for actor in movie["cast"]:
            G.add_node(actor, type="Actor")
            G.add_edge(actor, title, relation="ACTED_IN")
            
        for genre in movie["genres"]:
            G.add_node(genre, type="Genre")
            G.add_edge(title, genre, relation="BELONGS_TO")
            
    return G

def search_by_actor(G, actor_name):
    """Finds all movies connected to an actor node."""
    if not G.has_node(actor_name):
        return []
    return [n for n in G.neighbors(actor_name) if G.nodes[n].get("type") == "Movie"]

def search_by_director(G, director_name):
    """Finds all movies connected to a director node."""
    if not G.has_node(director_name):
        return []
    return [n for n in G.neighbors(director_name) if G.nodes[n].get("type") == "Movie"]

def search_by_genre(G, genre_name):
    """Finds all movies connected to a genre node."""
    if not G.has_node(genre_name):
        return []
    return [n for n in G.neighbors(genre_name) if G.nodes[n].get("type") == "Movie"]