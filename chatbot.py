import os
import json
import datetime
import csv
import time
import nltk
import ssl
import sys
import random
import joblib
import streamlit as st
import speech_recognition as sr

ssl._create_default_https_context = ssl._create_unverified_context

nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

file_path = "intents.json"
try:
    with open(file_path, "r") as file:
        intents = json.load(file)
except FileNotFoundError:
    st.error("Error: 'intents.json' file not found.")
    intents = {"intents": []}

try:
    model = joblib.load("chatbot_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    encoder = joblib.load("label_encoder.pkl")
except FileNotFoundError:
    st.error("Error: Model or vectorizer file not found. Please retrain the chatbot.")
    model = None
    vectorizer = None
    encoder = None

def chatbot(input_text, topic):
    if model is None or vectorizer is None or encoder is None:
        return "Chatbot is not properly configured. Please retrain the model."
    
    try:
        input_text_transformed = vectorizer.transform([input_text])
        tag_index = model.predict(input_text_transformed)[0]
        tag = encoder.inverse_transform([tag_index])[0]

        matching_responses = []
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                intent_topic = intent.get("topic", "General")
                responses = intent.get("responses", [])

                if intent_topic == topic or intent_topic == "General":
                    matching_responses.extend(responses)

        if matching_responses:
            return random.choice(matching_responses)
    except Exception as e:
        return f"Error: {str(e)}"
    
    return "Sorry, I don't understand that."

def recognize_speech():
    if sr is None:
        st.warning("⚠️ Voice input is not available because SpeechRecognition is missing.")
        return "Voice input not available."

    recognizer = sr.Recognizer()

    if "browser" in st.runtime.scriptrunner.get_script_run_ctx().session_id:
        st.warning("⚠️ Voice input is not supported on Streamlit Cloud. Please use text input instead.")
        return "Voice input not supported."

    try:
        with sr.Microphone() as source:
            st.write("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            return recognizer.recognize_google(audio)
    except sr.RequestError:
        return "Speech service is unavailable."
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except Exception as e:
        return f"Error: {str(e)}"
    
def main():
    st.title("Chatbot with NLP")

    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome! Type a message or use voice input.")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Topic Selection
        st.markdown("### Topics")
        topics = {
            "Daily Life": "💬",
            "Health": "❤️",
            "Knowledge": "📚",
            "Business": "📊",
            "Coding": "💻",
            "Entertainment": "🎭",
            "Science": "🔬",
            "Sports": "⚽"
        }

        if "selected_topic" not in st.session_state:
            st.session_state["selected_topic"] = "Daily Life"

        topic_list = list(topics.items())
        cols = st.columns(4)
        for i, (topic, icon) in enumerate(topic_list):
            with cols[i % 4]:  
                if st.button(f"{icon} {topic}"):
                    st.session_state["selected_topic"] = topic
                    st.rerun()  

        st.write(f" Currently chatting about: **{st.session_state['selected_topic']}**")

        user_input = st.text_input("You:")
        if st.button("🎙️ Push to Talk"):
            voice_text = recognize_speech()
            if "timed out" in voice_text or "couldn't understand" in voice_text:
                st.warning(voice_text)
            else:
                st.text(f"You (Voice): {voice_text}")
                user_input = voice_text 

        if user_input:
            with st.spinner("Chatbot is typing..."):
                time.sleep(1)  
            response = chatbot(user_input, st.session_state["selected_topic"])

            st.session_state.chat_history.append({"role": "user", "message": user_input})
            st.session_state.chat_history.append({"role": "assistant", "message": response})

            for entry in st.session_state.chat_history:
                st.chat_message(entry["role"]).markdown(entry["message"])

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("chat_log.csv", "a", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input, response, timestamp])

            if response.lower() in ["goodbye", "bye"]:
                st.write("Thank you for chatting! Have a great day! 🎉")
                st.stop()

    elif choice == "Conversation History":
        st.header("Conversation History")
        if os.path.exists("chat_log.csv"):
            with open("chat_log.csv", "r", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader, None)  
                for row in csv_reader:
                    if len(row) >= 3:
                        st.markdown(f"**👤 You:** {row[0]}")
                        st.markdown(f"**🤖 Chatbot:** {row[1]}")
                        st.caption(f"🕒 {row[2]}")
                        st.markdown("---")
        else:
            st.write("No conversation history found.")

    elif choice == "About":
        st.write("""
        ### Chatbot with NLP, Topics, and Voice
        - Uses NLP and Machine Learning
        - Supports Text & Voice Input
        - Uses Google Speech-to-Text for Voice Recognition
        - Includes **Topic-Based Chat Filtering** for better conversations
        
        **Developed with Python & Streamlit**
        """)

if __name__ == "__main__":
    main()
