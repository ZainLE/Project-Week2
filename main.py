import openai
from config import OPENAI_API_KEY
import streamlit as st
import uuid
import random

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
# user_input_key = str(uuid.uuid4())


# PART OF MESSAGES

questions=["What is destination of choice?","How many days are you planning to travel?","What is Your Budget?","Who do you plan on traveling with on your next adventure?","Which activities are you interested in?"]
recommended_countries = ["Italy", "France", "Japan", "Spain", "Canada", "Australia", "Brazil", "India", "South Africa", "New Zealand", "Germany", "Mexico", "Thailand", "Greece", "United States"]
random_country = random.choice(recommended_countries)


# INSTRUCTIONS FOR TEXT AND MODEL

def chat_with_gpt(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
          messages=[
            {
                "role": "system",
                "content": f"You are a travel assistant. Your role is to help users plan trips, "
                           f"collect their preferences, and generate a travel plan. Ensure the generated plan "
                           f"is detailed and user-friendly. After introductory messages, ask the user the following questions:\n\n"
                           f"{', '.join(questions)}if user had already answered any of thsoe questions dont ask that question again,when user has dicided on the destination\n\n"
                           f"give the user itineary for the total travelling he decided for the place he decided on \n\n"
                           f"If you're looking for recommendations, I can suggest countries like {', '.join(random_country)}."
            },
            {"role": "assistant", "content": "Hi, I'm Tibi, your travel assistant. How can I help you today?"},
            {"role": "user", "content": user_input},
        ],
   
        temperature=0.7,
        max_tokens=3800
    )   
    return response['choices'][0]['message']['content']



# STREAMLIT SETUP 

def main():
    st.subheader("")
    # st.text("Hello! I'm Tibi, your travel assistant. How can I help you today?")

    # Use st.form to create a form
    with st.form(key='user_input_form'):
        user_input = st.text_area("You:", height=30)  
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            response = chat_with_gpt(user_input)
            st.text_area("TIBI:", value=response, height=350, max_chars=None)  

if __name__ == "__main__":
    main()







