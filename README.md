# 💬 Navia AI — Personalized Assistant Chatbot

Navia AI is a lightweight, privacy-friendly chatbot framework powered by [GROQ's LLaMA3](https://groq.com/llama3/). It's designed to act as your personal assistant — whether a best friend, digital partner, or career guide — based solely on the persona you define during setup.

---

## ✨ Features

* 🔧 Fully configurable persona (name, tone, role, tech stack, hobbies, etc.)
* 🤖 Powered by Groq API with LLaMA3 backend
* 🌐 API endpoint (`/chat`) for seamless frontend integration
* 🛡️ Out-of-context reply detection with alert email system
* 🔐 Environment variable management using `.env`
* ⚡ One-command setup wizard for configuration

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Navin82005/Navia-The-Bot.git
cd Navia-The-Bot
```

### 2. Run the Setup Wizard

```bash
navya init
```
# or
```bash
.\navya init
```
# or
```bash
python setup.py
```

This will:

* Create a `config.json` file for assistant personality/knowledge
* Generate a `.env` file to store API keys securely

### 3. Start the Server
The setup wizard will start the server for you. If not you can run the server by:

```bash
python run.py
```

Server runs at: `http://localhost:5001`

---

## 🧠 How It Works

1. The setup wizard collects your assistant’s persona details.
2. On every `/chat` request:

   * A system prompt is generated from `prompt.py`
   * Groq’s LLaMA3 model provides a response
   * `helper.py` checks for forbidden/off-topic content
   * If triggered, an email alert is sent to the receiver

---

## 🛠️ Project Structure

```
navia-ai/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── helper.py           # Context checks + alert logic
│   ├── prompt.py           # System prompt generator
│   ├── routes.py           # Route: /chat
├── config.json             # Assistant persona configuration
├── .env                    # Environment secrets
├── run.py                  # App runner
├── setup.py                # Interactive setup wizard
├── requirements.txt        # Dependencies
```

---

## 🧪 API Usage

### Endpoint

```
POST /chat
```

### Payload

```json
{
  "message": "What does Naveen love doing on weekends?"
}
```

### Response

```json
{
  "response": "Aww, Naveen loves going on bike rides and listening to music! 🎶"
}
```

---

## 📄 Environment Variables

Stored in `.env`:

```env
GROQ_API_KEY=your_groq_key
MONITOR_EMAIL=bot_email@gmail.com
MONITOR_EMAIL_PASSWORD=your_app_password
ALERT_RECEIVER_EMAIL=your_email@gmail.com
```

---

## 💌 Alert System

If the assistant replies out of character (e.g., missing keywords, forbidden topics), an email alert will be sent to the receiver to ensure privacy and safety.

---

## ⚙️ CORS Configuration

Control frontend access in `config.json`:

```json
"cors_origins": [
  "http://localhost:3000",
  "https://your-frontend.app"
]
```

---

## 🛡️ Privacy Note

Navia AI does **not store** conversations. All prompts are processed in-memory and securely sent to Groq’s API.

---

## 💡 Example Use Cases

* AI profile bot for personal portfolio
* Private relationship simulator
* Journaling or emotional support companion
* Career-focused assistant for developers

---

## 📦 To-Do / Future Ideas

* Optional React-based frontend UI
* In-memory conversation history
* Prebuilt role presets (friend, therapist, coach)

---

## ❗️ Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

## 📄 License

[MIT](./LICENSE)
