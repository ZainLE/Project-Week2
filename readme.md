# TIBI - Your Own Travel Assistant

## Introduction
TIBI is your personal travel assistant designed to help you plan your trips, collect preferences, and generate detailed travel plans. The assistant is powered by OpenAI's GPT-4 model to provide intelligent and personalized responses.

## Features
- **Intelligent Conversations:** Engages in natural language conversations to understand travel preferences.
- **Location Extraction:** Utilizes spaCy and regular expressions to extract locations from user responses.
- **Location Refinement:** Refines extracted locations to improve accuracy.
- **Map Integration:** Displays an interactive map with markers for refined locations.

## Usage
1. Run the code using a Python environment.
2. TIBI will introduce itself and ask how it can assist you.
3. Answer the questions prompted by TIBI to gather information about your travel preferences.
4. Once you've decided on your destination, TIBI will provide a detailed itinerary for the specified travel duration.
5. TIBI will extract locations from the conversation, refine them, and display them on an interactive map.

## Dependencies
- OpenAI GPT-4
- Streamlit
- spaCy
- geopy
- folium
- streamlit-folium

## Setup
1. Install the required dependencies using:
    ```bash
    pip install openai streamlit spacy geopy folium streamlit-folium
    ```
2. Obtain your OpenAI API key and update `config.py` with your key.

## How to Run
Execute the code using:
```bash
streamlit main.py



