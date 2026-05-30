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
import base64

# --- Setup Page Config (MUST BE FIRST) ---
st.set_page_config(
    page_title="AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

ssl._create_default_https_context = ssl._create_unverified_context

nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt', quiet=True)

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
            st.info("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            return recognizer.recognize_google(audio)
    except sr.RequestError:
        return "Speech service is unavailable."
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except Exception as e:
        return f"Error: {str(e)}"

def inject_custom_css():
    try:
        with open("style.css", "r") as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def render_chat_message(role, message):
    if role == "user":
        avatar = "👤"
        css_class = "user"
        actions = ""
    else:
        avatar = "✨"
        css_class = "bot"
        actions = """
        <div class="chat-actions">
            <span title="Copy Response" onclick="navigator.clipboard.writeText(this.parentElement.parentElement.querySelector('p').innerText)">📋</span>
            <span title="Regenerate Response">🔄</span>
        </div>
        """
        
    html = f"""
    <div class="chat-message {css_class}">
        <div class="chat-avatar">{avatar}</div>
        <div class="chat-bubble">
            <p>{message}</p>
            {actions}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def main():
    inject_custom_css()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "selected_topic" not in st.session_state:
        st.session_state["selected_topic"] = "Daily Life"
        
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # --- SIDEBAR REDESIGN ---
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 2rem;">
            <div style="font-size: 2rem;">✨</div>
            <h2 style="margin: 0; font-weight: 700; background: linear-gradient(90deg, #7C3AED, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Nexus AI</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Custom Sidebar Navigation
        if st.button("💬 Chat", use_container_width=True, type="primary" if st.session_state.current_page == "Home" else "secondary"):
            st.session_state.current_page = "Home"
            st.rerun()
            
        if st.button("🕰️ History", use_container_width=True, type="primary" if st.session_state.current_page == "History" else "secondary"):
            st.session_state.current_page = "History"
            st.rerun()
            
        if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.current_page == "About" else "secondary"):
            st.session_state.current_page = "About"
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 0;'>", unsafe_allow_html=True)
        
        voice_btn = st.button("🎙️ Voice Input", help="Push to Talk", use_container_width=True)
        if voice_btn:
            with st.spinner("Listening..."):
                voice_text = recognize_speech()
                if "timed out" not in voice_text and "couldn't understand" not in voice_text and "not available" not in voice_text:
                    st.session_state.chat_history.append({"role": "user", "message": voice_text})
                    st.session_state.current_page = "Home"
                    st.rerun()
                else:
                    st.warning(voice_text)
            
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <div style="width: 35px; height: 35px; border-radius: 50%; background: #1E293B; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">👤</div>
            <div>
                <div style="font-size: 0.9rem; font-weight: 600; color: #F8FAFC;">Guest User</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Free Plan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- MAIN PAGE LOGIC ---
    if st.session_state.current_page == "Home":
        # Empty State / Suggestions
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="text-align: center; padding: 4rem 0 2rem 0;">
                <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;">How can I help you today?</h1>
                <p style="color: #94A3B8; font-size: 1.2rem;">Select a topic below or just start typing.</p>
            </div>
            """, unsafe_allow_html=True)
            
            topics = [
                {"topic": "Coding", "icon": "💻", "desc": "Debug, explain and generate code"},
                {"topic": "Health", "icon": "❤️", "desc": "Wellness, fitness and health guidance"},
                {"topic": "Science", "icon": "🔬", "desc": "Physics, chemistry and biology"},
                {"topic": "Daily Life", "icon": "💬", "desc": "General knowledge and routines"},
                {"topic": "Business", "icon": "📊", "desc": "Finance, strategy and marketing"},
                {"topic": "Entertainment", "icon": "🎭", "desc": "Movies, games and pop culture"},
                {"topic": "Sports", "icon": "⚽", "desc": "Athletics, teams and scores"},
                {"topic": "Productivity", "icon": "⚡", "desc": "Time management and workflows"}
            ]
            
            cols = st.columns(4)
            for i, item in enumerate(topics):
                with cols[i % 4]:
                    # We use Streamlit native buttons but they will be styled by our CSS
                    if st.button(f"{item['icon']} {item['topic']}\\n\\n{item['desc']}", key=f"btn_{item['topic']}", use_container_width=True):
                        st.session_state["selected_topic"] = item['topic']
                        st.rerun()
                        
            st.markdown(f"<div style='text-align: center; margin-top: 2rem; color: var(--secondary); font-weight: 600;'>Currently specialized in: {st.session_state['selected_topic']}</div>", unsafe_allow_html=True)

        else:
            # Chat History Container
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for entry in st.session_state.chat_history:
                render_chat_message(entry["role"], entry["message"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Bottom Input Area
        # Use columns for text input and voice button to mimic a floating dock
        st.markdown("<br><br><br>", unsafe_allow_html=True) # Spacer for floating input
        
        user_input = st.chat_input("Ask anything...")

        if user_input:
            # Display user message instantly
            st.session_state.chat_history.append({"role": "user", "message": user_input})
            st.rerun() # Rerun to show user message and trigger bot response

        # Bot Response Logic (triggered if last message was from user)
        if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
            user_msg = st.session_state.chat_history[-1]["message"]
            
            # Show typing indicator
            st.markdown("""
            <div class="chat-message bot">
                <div class="chat-avatar">✨</div>
                <div class="chat-bubble">
                    <div class="typing">
                      <div class="dot"></div>
                      <div class="dot"></div>
                      <div class="dot"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1) # Fake delay for typing effect
            
            response = chatbot(user_msg, st.session_state["selected_topic"])
            st.session_state.chat_history.append({"role": "assistant", "message": response})
            
            # Log conversation
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("chat_log.csv", "a", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_msg, response, timestamp])
                
            st.rerun() # Rerun to replace typing indicator with actual message

    elif st.session_state.current_page == "History":
        st.markdown("""
        <h1 style="font-weight: 700; margin-bottom: 2rem;">Conversation History</h1>
        """, unsafe_allow_html=True)
        
        if os.path.exists("chat_log.csv"):
            with open("chat_log.csv", "r", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader, None) # skip header
                
                for row in reversed(list(csv_reader)): # Show newest first
                    if len(row) >= 3:
                        st.markdown(f"""
                        <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border-color); margin-bottom: 1rem;">
                            <div style="color: var(--text-secondary); font-size: 0.8rem; margin-bottom: 0.5rem;">{row[2]}</div>
                            <div style="margin-bottom: 1rem;"><strong>👤 You:</strong> {row[0]}</div>
                            <div><strong>✨ Nexus AI:</strong> {row[1]}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No conversation history found.")

    elif st.session_state.current_page == "About":
        st.markdown("""
        <h1 style="font-weight: 700; margin-bottom: 2rem;">About Nexus AI</h1>
        <div style="background: var(--card-bg); padding: 2rem; border-radius: 12px; border: 1px solid var(--border-color);">
            <h3 style="color: var(--primary);">Next-Gen Conversational Interface</h3>
            <p style="color: var(--text-secondary); line-height: 1.6;">
                Nexus AI represents a leap forward in conversational UX, blending standard Streamlit simplicity with a premium, futuristic SaaS aesthetic.
            </p>
            <ul style="color: var(--text-secondary); line-height: 1.8;">
                <li>🧠 Powered by advanced NLP & Machine Learning</li>
                <li>🎙️ Seamless Voice Integration via Google Speech-to-Text</li>
                <li>🎯 Dynamic Topic Filtering for contextual conversations</li>
                <li>✨ Glassmorphism UI with responsive design</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
