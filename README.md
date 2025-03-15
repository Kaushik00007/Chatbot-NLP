# 🤖 AI Chatbot with NLP 

 A **Machine Learning-powered chatbot** that understands **text & voice inputs**, supports **topic-based conversations**, and provides **real-time responses** using **Natural Language Processing (NLP)**.

🌐 **Live App:** [Chatbot-NLP](https://chatbot-nlp-kaushik.streamlit.app)

---

## ✨ Features
- 💬 **Interactive Chat UI** – Built with **Streamlit** for a sleek & modern interface.
- 🎙 **Text & Voice Input** – Supports **typing & speech recognition** (voice input works on desktop).
- 🧠 **Machine Learning Model** – Uses **Logistic Regression + TF-IDF** for intent classification.
- 📚 **Topic-Based Conversations** – Choose from categories like **Coding 💻, Business 📊, Health ❤️, Entertainment 🎭**, etc.
- 📝 **Chat History** – Stores past conversations for review.
- 📱 **Mobile-Friendly** – Works on all devices, with **voice input disabled on mobile** to prevent crashes.
- 🚀 **Cloud Deployment** – Easily accessible via **Streamlit Cloud**.

---

## 🛠️ Tech Stack
| Component       | Technology Used  |
|----------------|-----------------|
| **Frontend**   | Streamlit       |
| **Backend**    | Python, Flask   |
| **Machine Learning** | Scikit-learn, Logistic Regression, TF-IDF Vectorizer |
| **NLP**        | NLTK, SpeechRecognition |
| **Data Storage** | JSON (intents), CSV (chat logs) |
| **Deployment** | Streamlit Cloud, GitHub |

---

## 🛠️ Tools & Technologies Used
- **Python** – Core language for chatbot development  
- **Streamlit** – Web framework for UI  
- **Scikit-learn** – Machine learning model for intent classification  
- **NLTK** – Natural Language Processing toolkit  
- **SpeechRecognition** – Converts speech to text  
- **Joblib** – Saves and loads ML models  
- **GitHub** – Version control & collaboration  
- **Streamlit Cloud** – Deployment platform  

---

## 🔧 Installation & Setup
### Prerequisites
- **Python (>=3.8)**
- **Git Installed**
- **A Streamlit Cloud Account** (for deployment)

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Kaushik00007
cd Chatbot-NLP
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Run the Chatbot
```sh
streamlit run chatbot.py
```

## 📌 Usage
```
Ask a question via text or voice input.
Chatbot classifies the intent and selects a relevant response.
Users can filter responses by choosing a topic (e.g., Business, Coding, Sports, etc.).
Chat history is stored in chat_log.csv.
```
## 🚀 Deployment on Streamlit Cloud
```
Frontend:
Hosted on Streamlit Cloud – Visit Live App

Steps to Deploy
Push your project to GitHub
Go to Streamlit Cloud → Click "New App"
Select GitHub repo & enter chatbot.py as Main File Path
Click "Deploy"
```
## 📂 Project Structure
### 📁 Chatbot-NLP/
│-- **chatbot.py**                # Main chatbot application
│-- **train_model.py**            # ML Model training script
│-- **intents.json**              # Dataset for chatbot responses
│-- **requirements.txt**          # Dependencies
│-- **chat_log.csv**              # Chat history storage
│-- **README.md**                 # Project Documentation

## 🛠️ Methodology

- Data Collection: structured chatbot responses using an intents.json file, grouping user queries by category (intent).
- Text Preprocessing: Applied tokenization, stemming, and TF-IDF vectorization to transform text into machine-readable form.
- Model Training: Used Logistic Regression to classify user inputs into predefined intents.
- User Interaction: Implemented Streamlit UI for a simple and engaging chat experience.
- Voice Recognition: Integrated Google Speech-to-Text API for voice input.
- Deployment: Hosted the chatbot on Streamlit Cloud for easy access.

## Learning Outcomes
 - NLP & Machine Learning – Implemented TF-IDF vectorization and Logistic Regression.
 - Speech Recognition – Integrated Google Speech-to-Text API.
 - Web Development – Built an interactive chatbot UI using Streamlit.
 - Deployment – Successfully deployed the chatbot on Streamlit Cloud.

## 🙌 Contributions
Contributions are welcome! Follow these steps:
```
Fork the repository
Create a new branch 
Commit your changes
Open a pull request
```
## 📧 Contact
For any queries, reach out via:

- 📧 Email: kaushi00007@gmail.com  
- 🔗 LinkedIn: https://www.linkedin.com/in/kaushik-k-dev
- 🌍 GitHub: https://github.com/Kaushik00007/Kaushik00007

## Built with ❤️ using Python, Machine Learning, and Streamlit. 
