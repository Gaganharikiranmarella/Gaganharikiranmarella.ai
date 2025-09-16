# 📝 Smart Summarizer

A real-time voice-to-notepad assistant with instant AI-powered bullet summaries.

---

## 🚀 Features

- **Real-Time Speech Transcription:**  
  Instantly capture and log spoken words as text.

- **Live Notepad Logging:**  
  Every word you say is appended to a digital notepad.

- **AI-Powered Bullet Summaries:**  
  Periodically condense your transcription into actionable bullet points using [Mistral Small 3.2 24B (free) via OpenRouter](https://openrouter.ai/).

- **Modular & Secure:**  
  Easy to extend, with secrets and config in `.env` for safety.

---

## 📁 Project Structure

smart_summarizer/
│
├── .env # API keys and config
├── main.py # Orchestrator script
├── speech_recorder.py # Handles microphone and transcription
├── notepad.py # Notepad logging
├── summarizer.py # OpenRouter API summarization
├── requirements.txt
└── utils.py # Utilities/helpers


---

## 🛠️ Installation

1. **Clone this repo:**  

git clone https://github.com/your-username/smart_summarizer.git
cd smart_summarizer


2. **Create a virtual environment and activate it:**

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate


3. **Install dependencies:**  

pip install -r requirements.txt


4. **Configure your API key and model:**  
Create a `.env` file as shown:

OPENROUTER_API_KEY=sk-xxxxxxxxxxxx
OPENROUTER_MODEL=mistralai/mistral-small-3.2-24b-instruct:free


---

## ▶️ Usage

python main.py


- Start speaking; your notes & bullet summaries appear and update live!

---

## 🤖 Model Info

- Uses: [Mistral Small 3.2 24B (free)](https://openrouter.ai/mistralai/mistral-small-3.2-24b-instruct:free) via OpenRouter API

---

## 📄 License

MIT

---

> Made with ❤️ for seamless productivity and smarter note taking!
