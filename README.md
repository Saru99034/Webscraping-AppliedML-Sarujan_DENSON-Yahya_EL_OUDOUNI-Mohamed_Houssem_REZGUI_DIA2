# Paris Restaurant Recommendation System

## Project Overview
Paris is one of the most visited cities in the world, attracting approximately 38 million tourists annually. While the city offers an incredible food scene, visitors often face challenges in finding good restaurants near their hotels. Many end up at overpriced or low-quality establishments.

To solve this issue, we developed a framework using a Streamlit app to help users find the best restaurants in Paris based on their hotel selection. This app uses two data sources:
- The **Amadeus for Developers API** for hotel data.
- **Web-scraped data from TheFork.fr** for restaurant information.

Our goal is to enhance the dining experience for tourists by matching top-rated hotels with excellent dining options, ensuring a stress-free and enjoyable exploration of Paris’s gastronomy.

---

## Use Case Description
The project is designed to assist tourists in finding restaurants based on:
1. Their preferred hotel in Paris.
2. Their preferences for cuisine type, budget, and proximity.

### Features:
- Users can select a hotel from a pre-populated list of 45 five-star hotels located within 6 km of central Paris.
- Based on the user's preferences and hotel location, the app recommends nearby restaurants that match their criteria.
- The recommendations are based on fields such as restaurant type, ratings, reviews, and average prices.

This tool simplifies the decision-making process for tourists and ensures they can enjoy high-quality meals without hassle.

---

## Data Sources and Collection
### 1. **Hotels Data**
We used the **Amadeus for Developers API** to gather data for 45 five-star hotels in Paris, including:
- Hotel name and ID.
- Geographic coordinates (latitude and longitude).
- Dining-related amenities.

**API Details:**
- **Method:** GET  
- **Endpoint:** `/reference-data/locations/hotels/by-city`  
- **Parameters:**  
  - `cityCode`: "PAR" (Paris)  
  - `radius`: "6" (6 km from the city center)  
  - `radiusUnit`: "KM"  
  - `amenities`: "RESTAURANT"  
  - `ratings`: "5"  
  - `hotelSource`: "ALL"  

### 2. **Restaurants Data**
We scraped restaurant data from [TheFork.fr](https://www.thefork.fr/restaurants/parisc415144) using a combination of Selenium and BeautifulSoup. The collected fields include:
- Name.
- Address.
- Type of cuisine (e.g., Indian, Chinese, Japanese).
- Average price.
- Ratings and reviews.

This data is essential for providing personalized recommendations to users.

---

## Ecological and Responsible Dimension
Our project also promotes sustainable tourism by:
- Highlighting eco-friendly hotels and restaurants.
- Including filters for establishments that prioritize sustainability and environmentally friendly practices.

---

## Installation and Usage

### Prerequisites
- Python 3.8 or above
- Required Python libraries (listed in `requirements.txt`)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Saru99034/Webscraping-AppliedML-Sarujan_DENSON-Yahya_EL_OUDOUNI-Mohamed_Houssem_REZGUI_DIA2.git
   ```
   
2. Install the dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app
   ```bash
   streamlit run app.py
   ```
4. Access the app through the URL provided in the terminal (e.g., http://localhost:8501).


## Overview of the application

![image](https://github.com/user-attachments/assets/4cfa3265-6d94-4166-b2e9-c6aaf8cef619)

### Filtres avancés
![image](https://github.com/user-attachments/assets/7de17192-2d77-481f-9d32-2a93d40380f3)

### Recommandations de restaurants
![image](https://github.com/user-attachments/assets/298b3a06-9ace-43bc-8885-7976fe8b7478)  

## Files in the Repository

* app.py: The main Python file for the Streamlit app.
* paris_hotels_final.csv: Contains hotel data retrieved from the Amadeus API.
* paris_restaurants_final.csv: Contains restaurant data scraped from TheFork.fr.
* Webscraping_for_TheFork.ipynb: Jupyter notebook for scraping restaurant data.
* requirements.txt: Contains the list of required Python libraries.
* README.md: This file, detailing the project.

## Conclusion

This project provides an intuitive and user-friendly recommendation system to enhance the dining experience of tourists in Paris. By combining hotel and restaurant data, the app simplifies the decision-making process and ensures a seamless exploration of Paris’s renowned culinary scene.
   
