import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

st.markdown(
    """
    <style>
    /* Style pour les cartes des restaurants */
    .restaurant-card {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        background-color: #2c2f33; /* Couleur de fond sombre */
        color: white; /* Texte en blanc */
        transition: transform 0.2s, box-shadow 0.2s; /* Animation au survol */
    }
    .restaurant-card:hover {
        transform: scale(1.02); /* Légère augmentation de taille au survol */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Ombre au survol */
    }

    /* Style pour les titres des restaurants */
    .restaurant-title {
        font-size: 20px;
        color: #ffffff;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Style pour les notes */
    .restaurant-note {
        color: #f1c40f; /* Jaune pour les notes */
        font-weight: bold;
    }

    /* Style pour les liens */
    a {
        color: #3498db; /* Bleu pour les liens */
        text-decoration: none;
        transition: color 0.2s ease-in-out, text-decoration 0.2s ease-in-out;
    }
    a:hover {
        color: #1abc9c; /* Vert au survol */
        text-decoration: underline;
    }

    /* Bordure verte pour les restaurants éco-responsables */
    .restaurant-card.eco {
        border: 2px solid #2ecc71; /* Bordure verte pour les éco-responsables */
    }

    /* Style pour la barre de navigation */
    .navbar {
        background-color: #34495e;
        padding: 10px 20px;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 10;
        display: flex;
        align-items: center;
    }
    .navbar a {
        color: white;
        margin-right: 20px;
        text-decoration: none;
    }
    .navbar a:hover {
        color: #1abc9c;
    }

    /* Bouton "Retour en haut" */
    .back-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #3498db;
        color: white;
        padding: 10px 15px;
        border-radius: 50%;
        text-align: center;
        cursor: pointer;
        transition: background-color 0.3s;
        font-size: 20px;
    }
    .back-to-top:hover {
        background-color: #1abc9c;
    }

    /* Personnalisation des boutons Streamlit */
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #27ae60;
    }

    /* Style pour le fond de la page */
    body {
        background: linear-gradient(to bottom, #1e1e1e, #2c3e50); /* Dégradé */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Charger les fichiers CSV
try:
    hotels = pd.read_csv('C:/Users/houss/OneDrive/Bureau/Webscrapping_Project/Webscraping-AppliedML-Sarujan_DENSON-Yahya_EL_OUDOUNI-Mohamed_Houssem_REZGUI_DIA2/paris_hotels_final.csv')
    restaurants = pd.read_csv('C:/Users/houss/OneDrive/Bureau/Webscrapping_Project/Webscraping-AppliedML-Sarujan_DENSON-Yahya_EL_OUDOUNI-Mohamed_Houssem_REZGUI_DIA2/paris_restaurants_final.csv')
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

##########################################################

# Filtres avancés dans la barre latérale
with st.sidebar.expander("Filtres avancés", expanded=False):
    eco_filter = st.checkbox("Afficher uniquement les restaurants éco-responsables")
    price_range = st.slider("Plage de prix (€)", 10, 100, (20, 50))
    cuisine_filter = st.multiselect(
        "Type de cuisine",
        options=restaurants['Type_of_Restaurant'].unique(),
        default=None
    )


if hotel_choice:
    hotel_info = hotels[hotels['name'] == hotel_choice].iloc[0]

    # Afficher les détails de l'hôtel dans la barre latérale
    st.sidebar.markdown(f"""
    ### Détails de l'hôtel sélectionné
    - **Nom :** {hotel_info['name']}
    - **Country Code :** {hotel_info['countryCode']}
    - **Latitude:** {hotel_info['latitude']}
    - **Longitude :** {hotel_info['longitude']}
    - **Note :** ⭐ {hotel_info['rating']} / 5
    """)

    # Étape 2 : Barre de recherche
    st.header("Exprimez vos préférences alimentaires")
    user_query = st.text_input(
        "Entrez ce que vous recherchez (par exemple : sushi, ambiance calme, bio, végétarien, etc.)"
    )

    if user_query:
       
        nearby_restaurants = get_nearby_restaurants(
            hotel_info['latitude'], hotel_info['longitude']
        )

        # Appliquer les filtres avancés
        if eco_filter:
            nearby_restaurants = nearby_restaurants[nearby_restaurants['Eco_responsable'] == "Oui"]

        if price_range:
            nearby_restaurants = nearby_restaurants[
                (nearby_restaurants['Price'] >= price_range[0]) &
                (nearby_restaurants['Price'] <= price_range[1])
            ]

        if cuisine_filter:
            nearby_restaurants = nearby_restaurants[
                nearby_restaurants['Type_of_Restaurant'].isin(cuisine_filter)
            ]

        if not nearby_restaurants.empty:


            with st.spinner("Chargement des recommandations..."):
                 recommendations = recommend_restaurant(user_query, nearby_restaurants)
            st.success("Recommandations prêtes !")

            if not recommendations.empty:
                st.header("Voici vos recommandations de restaurants :")

                for _, row in recommendations.iterrows():
                    # Créer des colonnes pour structurer l'affichage
                    col1, col2 = st.columns([1, 3])

                    with col1:

                        # Ajouter une image 
                        # st.image(row['Image'], width=150, caption=row['Title'])

                        if row['Eco_responsable'] == "Oui":
                            st.markdown("🌱 **Éco-responsable**")

                    with col2:
                        # Afficher les informations du restaurant
                        
                        st.markdown(
                        f"""
                        <div class="restaurant-card">
                            <div class="restaurant-title">{row['Title']} {'🌱' if row['Eco_responsable'] == 'Oui' else ''}</div>
                            <p><strong>Adresse :</strong> {row['Address']}</p>
                            <p><strong>Prix moyen :</strong> {row['Price']} €</p>
                            <p><strong>Type de cuisine :</strong> {row['Type_of_Restaurant']}</p>
                            <p><strong>Note :</strong> <span class="restaurant-note">⭐ {row['Mark']} / 10</span></p>
                            <p><strong>Description :</strong> {row['Description']}</p>
                            <p><a href="{row['Link']}" target="_blank">Plus d'infos sur TheFork</a></p>
                        </div>
                        """,
                        unsafe_allow_html=True ) 

                    # ligne de séparation pour chaque restaurant
                    st.markdown("---")



            else:
                st.write("Aucun restaurant correspondant n'a été trouvé.")
        else:
            st.write("Aucun restaurant trouvé à proximité.")
else:
    st.write("Veuillez sélectionner un hôtel pour commencer.")