# 💬 Navya AI — Personalized Assistant Chatbot

Navya AI is a lightweight, privacy-friendly chatbot framework powered by [GROQ's LLaMA3](https://groq.com/llama3/). It's designed to act as your personal assistant — whether a best friend, digital partner, or career guide — based solely on the persona you define during setup.

---

## ✨ Features

* 🔧 Fully configurable persona (name, tone, role, tech stack, hobbies, etc.)
* 🤖 Powered by Groq API with LLaMA3 backend
* 🌐 API endpoint (`/chat`) for seamless frontend integration
* 🛡️ Out-of-context reply detection + alert email system
* 🔒 `.env` secrets management
* 🚀 One-command setup wizard

---

## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/navya-ai.git
cd navya-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Setup Wizard

```bash
python setup.py
```

This will:

* Create `config.json` with your assistant's knowledge and behavior
* Generate `.env` to store secret keys securely

### 4. Start the Server

```bash
python run.py
```

Server runs at: `http://localhost:5001`

---

## 🧠 How It Works

1. The setup wizard collects user preferences, tone, knowledge, and keywords
2. On each `/chat` request:

   * A system prompt is dynamically created using `prompt.py`
   * Groq's LLaMA3 model generates the assistant's reply
   * `helper.py` checks for forbidden phrases or off-topic responses
   * Alerts are sent via Gmail if context is violated

---

## 🛠️ Project Structure

```
navya-ai/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── helper.py           # Context check + email alerts
│   ├── prompt.py           # Dynamic system prompt
│   ├── routes.py           # /chat route handler
├── config.json             # Assistant knowledge/persona
├── .env                    # API keys and Gmail creds
├── run.py                  # Starts Flask app
├── setup.py                # Interactive configuration wizard
├── requirements.txt
```

---

## 🧪 API Usage

### Endpoint

```
POST /chat
```

### Payload

````json
{
  "message": "What does Naveen love doing on weekends?"
}

### Response
```json
{
  "response": "Aww, my Naveen loves going on bike rides and listening to music! 🎶"
}
````

---

## 📄 Environment Variables

Stored in `.env`:

```
GROQ_API_KEY=your_groq_key
MONITOR_EMAIL=bot_email@gmail.com
MONITOR_EMAIL_PASSWORD=your_app_password
ALERT_RECEIVER_EMAIL=your_email@gmail.com
```

---

## 💌 Alert System

If the assistant replies out of character (missing keywords or using forbidden phrases), an email alert is triggered to the receiver email.

---

## ⚙️ CORS Configuration

You can control allowed frontend domains in `config.json`:

```json
"cors_origins": ["http://localhost:3000", "https://your-frontend.app"]
```

---

## 🛡️ Privacy Note

Navya AI does not store conversations. All prompts are generated in-memory and sent securely to Groq's API.

---

## 💡 Example Use Cases

* Personal AI profile/portfolio bot
* Private relationship simulator
* Mental health journaling companion
* Career-focused assistant for devs

---

## 📦 To-Do / Future Ideas

* Optional frontend UI with React
* Memory or conversation history
* Role presets (e.g., friend, coach, therapist)

---

## 🙋‍♂️ Contributing

Pull requests are welcome! Please open issues first for any major changes.

---

## 📄 License

[MIT](./LICENSE)
