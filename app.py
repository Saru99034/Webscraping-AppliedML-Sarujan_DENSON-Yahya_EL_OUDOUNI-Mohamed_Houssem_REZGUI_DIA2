import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Charger les fichiers CSV
try:
    hotels = pd.read_csv('C:/A5 ESILV/Webscraping & Applied ML/Projet/paris_hotels_final.csv')
    restaurants = pd.read_csv('C:/A5 ESILV/Webscraping & Applied ML/Projet/paris_restaurants_final.csv')
except FileNotFoundError:
    st.error("Les fichiers CSV ne sont pas trouvés. Assurez-vous qu'ils sont au bon endroit.")
    st.stop()

# Vérification des données chargées
if hotels.empty or restaurants.empty:
    st.error("Les fichiers CSV sont vides ou mal formatés. Veuillez vérifier leur contenu.")
    st.stop()

# Ajouter la colonne Eco_responsable
def is_eco_responsible(row):
    eco_keywords = ['végétarien', 'bio']
    text_data = f"{row['Description']} {row['Menu']} {row['Avis']}".lower()
    contains_eco_keywords = any(keyword in text_data for keyword in eco_keywords)
    meets_rating_criteria = row['Mark'] >= 9
    meets_avg_criteria = np.mean([row['Ambiance'], row['Plats'], row['Service']]) >= 9
    return "Oui" if contains_eco_keywords and meets_rating_criteria and meets_avg_criteria else "Non"

restaurants['Eco_responsable'] = restaurants.apply(is_eco_responsible, axis=1)

# NLP - Préparer les données textuelles des restaurants
restaurants['Informations_textuelles'] = (
    restaurants['Description'].fillna('') + ' ' + 
    restaurants['Menu'].fillna('') + ' ' + 
    restaurants['Avis'].fillna('')
)

# TF-IDF Vectorizer pour le français
try:
    french_stop_words = ['le', 'la', 'les', 'de', 'des', 'du', 'un', 'une', 'à', 'en', 'et', 'pour', 'avec', 'sur', 'dans']
    tfidf = TfidfVectorizer(stop_words=french_stop_words)
    tfidf_matrix = tfidf.fit_transform(restaurants['Informations_textuelles'])
except Exception as e:
    st.error(f"Erreur lors de la création de la matrice TF-IDF : {e}")
    st.stop()

# Fonction pour filtrer les restaurants proches géographiquement
def get_nearby_restaurants(hotel_lat, hotel_lon, max_distance=2.0):
    distances = np.sqrt(
        (restaurants['latitude_restaurant'] - hotel_lat) ** 2 +
        (restaurants['longitude_restaurant'] - hotel_lon) ** 2
    )
    return restaurants[distances <= max_distance]

# Fonction de recommandation
def recommend_restaurant(user_query, nearby_restaurants):
    user_query_vec = tfidf.transform([user_query])
    similarities = cosine_similarity(user_query_vec, tfidf_matrix[nearby_restaurants.index])
    nearby_restaurants = nearby_restaurants.copy()
    nearby_restaurants['Similarité'] = similarities.flatten()
    recommended = nearby_restaurants.sort_values(
        ['Similarité', 'Mark', 'Ambiance', 'Plats', 'Service'], ascending=False
    )
    return recommended.head(3)

# Streamlit App
st.title("Recommandation de Restaurants à Paris")

# Étape 1 : Sélectionner un hôtel
st.sidebar.header("Choisissez un hôtel")
hotel_choice = st.sidebar.selectbox("Sélectionnez un hôtel :", hotels['name'])

if hotel_choice:
    hotel_info = hotels[hotels['name'] == hotel_choice].iloc[0]
    st.sidebar.subheader("Détails de l'hôtel sélectionné")
    st.sidebar.write(f"**Nom :** {hotel_info['name']}")
    st.sidebar.write(f"**Latitude :** {hotel_info['latitude']}")
    st.sidebar.write(f"**Longitude :** {hotel_info['longitude']}")
    st.sidebar.write(f"**Rating :** {hotel_info['rating']} /5")

    # Étape 2 : Barre de recherche
    st.header("Exprimez vos préférences alimentaires")
    user_query = st.text_input(
        "Entrez ce que vous recherchez (par exemple : sushi, ambiance calme, bio, végétarien, etc.)"
    )

    if user_query:
        st.header("Restaurants recommandés")
        nearby_restaurants = get_nearby_restaurants(
            hotel_info['latitude'], hotel_info['longitude']
        )

        if not nearby_restaurants.empty:
            recommendations = recommend_restaurant(user_query, nearby_restaurants)

            if not recommendations.empty:
                for _, row in recommendations.iterrows():
                    st.subheader(row['Title'])
                    st.write(f"**Adresse :** {row['Address']}")
                    st.write(f"**Prix moyen :** {row['Price']} €")
                    st.write(f"**Type de cuisine :** {row['Type_of_Restaurant']}")
                    st.write(f"**Note :** {row['Mark']} (Ambiance : {row['Ambiance']}, Plats : {row['Plats']}, Service : {row['Service']})")
                    st.write(f"**Description :** {row['Description']}")
                    st.write(f"[Plus d'infos sur TheFork]({row['Link']})")
                    
                    # Afficher si le restaurant est éco-responsable
                    if row['Eco_responsable'] == "Oui":
                        st.markdown("🌱 **Ce restaurant est éco-responsable !** 🌱")
            else:
                st.write("Aucun restaurant correspondant n'a été trouvé.")
        else:
            st.write("Aucun restaurant trouvé à proximité.")
else:
    st.write("Veuillez sélectionner un hôtel pour commencer.")
