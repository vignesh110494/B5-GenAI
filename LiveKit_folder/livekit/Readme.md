# 🎙️ LiveKit + OpenAI Voice Agent (Local Python)

A fully working AI Voice Assistant built using:

* 🎤 Microphone input (`sounddevice`)
* 🧠 OpenAI Speech-to-Text (`gpt-4o-mini-transcribe`)
* 🤖 OpenAI LLM (`gpt-4o-mini`)
* 🔊 OpenAI Text-to-Speech (`gpt-4o-mini-tts`)
* 📡 LiveKit Python SDK
* 🐍 Async Python

---

# 🚀 What This Project Does

1. Records your voice (4 seconds)
2. Converts speech → text
3. Sends text to AI
4. Generates response
5. Converts response → voice
6. Plays AI voice locally

---

# 🏗️ Architecture

```
User Voice
   ↓
Microphone (sounddevice)
   ↓
WAV Buffer (Memory)
   ↓
OpenAI STT
   ↓
OpenAI LLM
   ↓
OpenAI TTS
   ↓
Speaker Output
```

LiveKit connection is established for future real-time streaming support.

---

# 📦 Requirements

* Python 3.9+
* Docker
* Microphone + Speaker
* OpenAI API Key

---

# 🐳 Step 1 — Run LiveKit Server

```bash
docker run --rm -p 7880:7880 livekit/livekit-server --dev
```

Verify:

```
http://localhost:7880
```

You should see: `OK`

---

# 🐍 Step 2 — Setup Python Environment

### Create Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install openai livekit livekit-api sounddevice soundfile numpy
```

---

# 🔐 Step 3 — Set OpenAI API Key (Recommended)

**Windows**

```bash
set OPENAI_API_KEY=your_openai_key
```

**Mac/Linux**

```bash
export OPENAI_API_KEY=your_openai_key
```

---

# ▶️ Step 4 — Run the Voice Agent

```bash
python voice_agent.py
```

Expected Output:

```
Connecting to LiveKit...
✅ Connected to LiveKit

🎤 Speak for 4 seconds...
📝 Transcribing...
You: Hello
🤖 Thinking...
AI: Hi! How can I help you?
🔊 Speaking...
```

---

# 📁 Project Structure

```
voice-agent/
│
├── voice_agent.py
├── README.md
└── requirements.txt
```

---

# 🛠 Troubleshooting

### LiveKit Not Connecting

* Ensure Docker is running
* Ensure port 7880 is available
* Ensure API secret matches server

### Microphone Not Working

* Check system permissions
* Verify default input device

### OpenAI Errors

* Check API key
* Ensure internet connection
* Verify model names

---

# 🚀 Future Improvements

* 🎧 Voice Activity Detection
* 🧠 Conversation memory
* 🌐 Stream audio into LiveKit room
* 🐳 Dockerize assistant
* 🔐 Use `.env` file
* ⚡ Real-time streaming STT
* 🎤 Wake-word detection

---

# ✅ Current Status

✔ LiveKit Connected
✔ Microphone Recording
✔ STT Working
✔ LLM Working
✔ TTS Working

You now have a fully working local AI Voice Assistant.

---

Built with ❤️ using Python + OpenAI + LiveKit
