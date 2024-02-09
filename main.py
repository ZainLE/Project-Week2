import openai
from config import OPENAI_API_KEY
import streamlit as st
import random
import spacy
import re
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium

# Logo
logo = "Tibi.png"
st.image(logo, width=90,)

# Top Lines
st.subheader("TIBI", divider='blue')
st.subheader('YOUR OWN TRAVEL ASSISTANT!')
# st.background()
with st.chat_message("TIBI"):
    # avatar= "Tibi.png"
    # st.image(avatar, width=50, caption="TIBI")
    st.write("Hi, I'm Tibi, your travel assistant. How can I help you today?")


# API KEYS

api_key = OPENAI_API_KEY
openai.api_key = api_key

# PART OF MESSAGES

questions=["What is destination of choice?","How many days are you planning to travel?","What is Your Budget?","Who do you plan on traveling with on your next adventure?","Which activities are you interested in?"]
recommended_countries = ["Italy", "France", "Japan", "Spain", "Canada", "Australia", "Brazil", "India", "South Africa", "New Zealand", "Germany", "Mexico", "Thailand", "Greece", "United States"]
random_country = random.choice(recommended_countries)


# INSTRUCTIONS FOR TEXT AND MODEL

messages = [{ "role": "system",
                "content": f"You are a travel assistant. Your role is to help users plan trips, "
                           f"collect their preferences, and generate a travel plan. Ensure the generated plan "
                           f"is detailed and user-friendly. After introductory messages, ask the user the following questions:\n\n"
                           f"{', '.join(questions)}if user had already answered any of thsoe questions dont ask that question again,when user has dicided on the destination\n\n"
                           f"give the user itineary for the total travelling he decided for the place he decided on \n\n"
                           f"If you're looking for recommendations, I can suggest countries like {', '.join(random_country)}.,"}]

def chat_with_gpt(user_input,conversation_history):
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        
        messages=messages,
   
        temperature=0.7,
        max_tokens=3800
    )   
    return response['choices'][0]['message']['content']

# EXTRACTING LOCATION

def Extracting_names(response):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(response)
    
    location_names = set()

    for ent in doc.ents:
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            main_word = ent.root.text
            location_names.add(main_word)
    
    regex_patterns = [
        re.compile(r'\b(?:location|place|city|town|village):?\s*([^\n,]+)\b', flags=re.IGNORECASE),
        re.compile(r'\b(?:visit|explore|head to)\s*(\b[A-Z][^\n,]+)\b', flags=re.IGNORECASE)
    ]

    for pattern in regex_patterns:
        additional_locations = pattern.findall(response)
        location_names.update(additional_locations)

    return list(location_names)

# REFINING LOCATIONS

def refineLocationExtraction(location_names):
    refined_location_names = set()

    for location in location_names:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(location)

        for ent in doc.ents:
            if ent.label_ == "GPE" or ent.label_ == "LOC":
                refined_location_names.add(ent.text)

    return list(refined_location_names)


# GETTING COORDINATES

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="TIBI")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

# CREATING MAP

def create_map(coordinates_list):
    if not coordinates_list:
        return None
    
    m = folium.Map(location=coordinates_list[0], zoom_start=10)
    for coordinates in coordinates_list:
        folium.Marker(location=coordinates).add_to(m)

    return m


# STREAMLIT SETUP

def main():
    st.subheader("")
    # st.text("Hello! I'm Tibi, your travel assistant. How can I help you today?")
    
    with st.form(key="user_input"):
        user_input = st.text_area("You:", height=30)  
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            user_message = {"role": "user", "content": user_input}
            messages.append(user_message)

            response = chat_with_gpt(user_input, messages)
            assistant_message = {"role": "assistant", "content": response}
            messages.append(assistant_message)

            location_names = Extracting_names(response)
            print("First Extraction: ")
            for name in location_names:
                print(f"- {name}")

            refined_locations = refineLocationExtraction(location_names)
            print("Second Extraction: ")
            for refined_name in refined_locations:
                print(f"- {refined_name}")

            coordinates_list = [get_coordinates(name) for name in refined_locations if get_coordinates(name)]

            st.text_area("TIBI:", value=response, height=350, max_chars=None)

            folium_map = create_map(coordinates_list)
            if folium_map:
                folium_static(folium_map)
                               
if __name__ == "__main__":
    main()







