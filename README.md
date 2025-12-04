# 🛡️ VoiceShield AI

> **Real-time voice-powered emergency detection and response system using AI**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Voice_AI-blue)](https://elevenlabs.io)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange)](https://ai.google.dev)

VoiceShield is an intelligent emergency response assistant that listens to voice input, detects emergency situations in real-time, classifies them by type and severity, and provides immediate AI-generated guidance with voice responses.

![VoiceShield Demo](https://via.placeholder.com/800x400?text=VoiceShield+AI+Demo)

## ✨ Features

- 🎙️ **Real-time Voice Recording** - Browser-based microphone input
- 🔊 **Speech-to-Text** - ElevenLabs Scribe V2 for accurate transcription
- 🧠 **AI Emergency Classification** - Detects Fire, Medical, Violence, Accident emergencies
- 🤖 **Intelligent Response** - Google Gemini AI generates contextual emergency guidance
- 🔈 **Text-to-Speech** - ElevenLabs voices deliver natural audio responses
- 📡 **Real-time Updates** - WebSocket-powered live event feed
- 💾 **Persistent Storage** - MongoDB Atlas for event history

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   React Frontend │◀──────▶│  FastAPI Backend │◀──────▶│  MongoDB Atlas  │
│   (Voice UI)     │   WS   │   (Processing)   │        │   (Storage)     │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ ElevenLabs  │ │   Gemini    │ │ ElevenLabs  │
            │    STT      │ │     AI      │ │    TTS      │
            └─────────────┘ └─────────────┘ └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account
- ElevenLabs API key
- Google Gemini API key

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
MONGO_URL=your_mongodb_connection_string
DB_NAME=voice_assistant_db
CORS_ORIGINS=*
EOF

# Run server
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
yarn install

# Create .env file
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env

# Run development server
yarn start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🎯 How It Works

1. **User speaks** into the microphone
2. **ElevenLabs STT** transcribes speech to text
3. **Keyword classifier** detects emergency type:
   - 🔥 **FIRE** - fire, smoke, burning, flames
   - 🏥 **MEDICAL** - hurt, injured, pain, unconscious
   - ⚠️ **VIOLENCE** - attack, threat, weapon, danger
   - 🚗 **ACCIDENT** - crash, collision, vehicle
   - ✅ **NORMAL** - no emergency detected
4. **Gemini AI** generates appropriate emergency response
5. **ElevenLabs TTS** converts response to speech
6. **WebSocket** broadcasts event to all connected clients

## 📁 Project Structure

```
voiceshield/
├── backend/
│   ├── server.py              # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── routes/
│   │   └── voice.py           # Voice processing endpoints
│   ├── services/
│   │   ├── complete_flow.py   # Main processing pipeline
│   │   ├── elevenlabs_stt.py  # Speech-to-text service
│   │   ├── elevenlabs_tts.py  # Text-to-speech service
│   │   ├── gemini_response.py # AI response generation
│   │   └── event_store.py     # MongoDB operations
│   └── websocket/
│       └── ws_manager.py      # WebSocket management
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   └── services/          # API services
│   └── package.json
├── LICENSE
└── README.md
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/voice` | Process voice recording |
| `GET` | `/api/events` | Get recent events |
| `GET` | `/api/audio/{id}` | Get audio response |
| `WS` | `/ws` | Real-time event stream |

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **ElevenLabs** - Voice AI (STT + TTS)
- **Google Gemini** - AI response generation
- **MongoDB** - NoSQL database
- **WebSockets** - Real-time communication

### Frontend
- **React 19** - UI framework
- **TailwindCSS** - Styling
- **Radix UI** - Accessible components
- **Axios** - HTTP client

## 🔒 Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb+srv://...
DB_NAME=voice_assistant_db
CORS_ORIGINS=*
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io) - Voice AI platform
- [Google AI](https://ai.google.dev) - Gemini API
- [MongoDB](https://mongodb.com) - Database

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/vikas-6">Vikas Kumar</a>
</p>