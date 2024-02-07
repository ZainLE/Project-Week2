import openai
from config import OPENAI_API_KEY


api_key = OPENAI_API_KEY

openai.api_key = api_key

def chat_with_gpt(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a travel assistant. Your role is to help users plan trips, collect their preferences,and generate a travel plan. Ensure the generated plan is detailed and user-friendly. After user says greets you,your introductory line is Hello! I'm Tibi, your travel assistant,How can i help you? then after second or third message ask user multiple questions based on their preferences, such as where they would want to go, what kind of activities they like to doon a trip, and their budget. Then, provide them with a personalized trip accordingly "},
            {"role": "assistant","content": "Hi, I'm Tibi, your travel assistant. How can I help you today?"},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
        max_tokens=400  
    )
    return response['choices'][0]['message']['content']
\
user_input = input("You: ")

while user_input.lower() != 'exit':
   
    response = chat_with_gpt(user_input)

    print(f"TIBI: {response}")

    user_input = input("You: ")

print("Conversation ended.")







