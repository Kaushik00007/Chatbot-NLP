import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
import joblib

ssl._create_default_https_context = ssl._create_unverified_context

nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

file_path = "intents.json"  
with open(file_path, "r") as file:
    intents = json.load(file)

model = joblib.load("chatbot_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = model.predict(input_text)[0]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "Sorry, I don't understand that."

counter = 0

def main():
    global counter
    st.title("Chatbot with NLP")

    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome! Type a message and press Enter to chat.")

        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:
            response = chatbot(user_input)
            st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input, response, timestamp])

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting! Have a great day!")
                st.stop()

    elif choice == "Conversation History":
        st.header("Conversation History")
        if os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  
                for row in csv_reader:
                    st.text(f"User: {row[0]}")
                    st.text(f"Chatbot: {row[1]}")
                    st.text(f"Timestamp: {row[2]}")
                    st.markdown("---")
        else:
            st.write("No conversation history found.")

    elif choice == "About":
        st.write("""
        ### Chatbot using NLP and Machine Learning
        - Uses Logistic Regression for intent classification
        - Streamlit for web-based interface
        - Stores chat history in `chat_log.csv`
        - Trained using labeled intents from `intents.json`
        """)

if __name__ == '__main__':
    main()
