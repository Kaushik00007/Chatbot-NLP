# 🤖 Chatbot with NLP 

A **Machine Learning-powered chatbot** that understands **text & voice inputs**, supports **topic-based conversations**, and provides **real-time responses** using **Natural Language Processing (NLP)**.  

## ✨ Features
 **Interactive Chat UI** – Built with **Streamlit** for a sleek & modern interface.  
 **Text & Voice Input** – Supports **typing & speech recognition** (voice input works on desktop).  
 **Machine Learning Model** – Uses **Logistic Regression + TF-IDF** for intent classification.  
 **Topic-Based Chatting** – Choose categories like **Coding 💻, Business 📊, Health ❤️, Entertainment 🎭**, etc.  
 **Chat History** – Stores conversations and allows users to review past interactions.  
 **Mobile-Friendly** – Works seamlessly across devices, with **voice input disabled on mobile to prevent crashes**.  
 **Deployable on Streamlit Cloud** – Easily accessible with a **single URL**.


## 📌 Tech Stack
🔹 **Languages & Frameworks**: Python, Streamlit  
🔹 **Machine Learning**: Scikit-learn, Logistic Regression, TF-IDF Vectorizer  
🔹 **NLP**: NLTK, SpeechRecognition (for voice input)  
🔹 **Data Storage**: JSON (for intents), CSV (for chat logs)  
🔹 **Deployment**: Streamlit Cloud, GitHub  


## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Kaushik00007/Chatbot-NLP
cd Chatbot-NLP

```bash
### 2️⃣ Install Dependencies
pip install -r requirements.txt

```bash
## 3️⃣ Run the Chatbot
streamlit run chatbot.py

🛠️ How It Works
1️⃣ User asks a question (via text or voice)
2️⃣ The chatbot classifies the intent using Logistic Regression
3️⃣ It retrieves a relevant response based on pre-defined intents in intents.json
4️⃣ User can select topics to filter responses for better conversation flow
5️⃣ Conversation is logged and stored in chat_log.csv

## 📂 Project Structure
📁 Chatbot-NLP/
│-- chatbot.py                # Main chatbot application
│-- train_model.py            # ML Model training script
│-- intents.json              # Dataset for chatbot responses
│-- requirements.txt          # Dependencies
│-- chat_log.csv              # Chat history storage

## 📖 Learning Outcomes
 **NLP & Machine Learning** – Implemented TF-IDF vectorization and Logistic Regression.
 **Speech Recognition** – Integrated Google Speech-to-Text API.
 **Web Development** – Built an interactive chatbot UI using Streamlit.
 **Deployment** – Successfully deployed the chatbot on Streamlit Cloud.

## 💙 Contributing
Want to improve this chatbot? Fork & pull requests are welcome! 🚀

## 🔗 Connect With Me
**Email:** kaushi00007@gmail.com
**LinkedIn:** [linkedin.com/in/yourprofile](https://www.linkedin.com/in/kaushik-k-dev/)

### Star ⭐ this repo if you found it helpful!





