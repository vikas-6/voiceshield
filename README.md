# 🎙️ VoiceShield AI - Real-Time Voice Emergency Assistant

## Overview

VoiceShield AI is a full-stack voice emergency detection system that processes voice recordings, classifies emergency types, and provides real-time assistant responses. The application uses WebSocket for live event streaming and is currently built with **mock functions** for easy integration with external APIs.

### Current Status: Mock Version

**Mock Functions** (Ready for Integration):
- ✅ Mock Speech-to-Text (STT) - Ready for **ElevenLabs STT** integration
- ✅ Mock Emergency Classifier - Ready for **Google Gemini API** integration
- ✅ In-memory Event Store - Ready for **Firestore** integration

**Fully Functional**:
- ✅ WebSocket real-time event broadcasting
- ✅ Web Audio API microphone recording
- ✅ Professional/Medical UI design
- ✅ Emergency classification (5 types: FIRE, MEDICAL, VIOLENCE, ACCIDENT, NORMAL)
- ✅ Severity scoring (1-10)

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Python) - REST API and WebSocket server
- **Motor** - Async MongoDB driver
- **Websockets** - Real-time event broadcasting
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Shadcn/UI** - Component library
- **Web Audio API** - Microphone recording
- **Axios** - HTTP client
- **WebSocket** - Real-time event streaming
- **date-fns** - Date formatting
- **Sonner** - Toast notifications

---

## 📁 Folder Structure

```
/app/
├── backend/
│   ├── server.py                 # Main FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   ├── services/
│   │   ├── mock_stt.py          # Mock Speech-to-Text (TODO: ElevenLabs)
│   │   ├── mock_classifier.py   # Mock Classifier (TODO: Gemini)
│   │   └── event_store.py       # In-memory event storage (TODO: Firestore)
│   ├── routes/
│   │   └── voice.py             # Voice processing endpoints
│   └── websocket/
│       └── ws_manager.py        # WebSocket connection manager
│
├── frontend/
│   ├── package.json             # Node dependencies
│   ├── .env                     # Environment variables
│   ├── public/                  # Static assets
│   └── src/
│       ├── App.js               # Main app component
│       ├── App.css              # Global styles
│       ├── index.css            # Tailwind imports
│       ├── pages/
│       │   └── Home.jsx         # Main home page
│       ├── components/
│       │   ├── MicRecorder.jsx  # Audio recording component
│       │   ├── EmergencyCard.jsx # Event display card
│       │   ├── EventFeed.jsx    # Real-time event feed
│       │   ├── StatusBadge.jsx  # Emergency type badge
│       │   └── ui/              # Shadcn components
│       └── services/
│           └── api.js           # API service
│
└── README.md                     # This file
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (running locally or remote)
- Yarn package manager

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd /app/backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   The `.env` file should already be configured:
   ```env
   MONGO_URL="mongodb://localhost:27017"
   DB_NAME="test_database"
   CORS_ORIGINS="*"
   ```

4. **Start the backend**:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Check backend logs**:
   ```bash
   tail -f backend.log
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd /app/frontend
   ```

2. **Install dependencies** (if needed):
   ```bash
   yarn install
   ```

3. **Configure environment**:
   The `.env` file should already be configured:
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

4. **Start the frontend**:
   ```bash
   yarn start
   ```

5. **Access the application**:
   Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

---

## 🧪 How to Test

### Test Recording Flow

1. **Open the application** in your browser
2. **Allow microphone permissions** when prompted
3. **Click the microphone button** to start recording
4. **Speak into your microphone** (the mock will simulate different scenarios)
5. **Click the button again** to stop recording
6. **View results**:
   - Transcript appears in the Emergency Card
   - Emergency type and severity are displayed
   - AI assistant response is shown
   - Event appears in the real-time feed

### Test WebSocket Connection

1. **Check the status indicator** in the header (green = connected, red = disconnected)
2. **Open multiple browser tabs** with the application
3. **Record in one tab** and watch events appear in all tabs in real-time

### Test API Endpoints

**Test voice processing**:
```bash
# Create a test audio file
echo "test audio data" > test_audio.webm

# Send to API
curl -X POST http://localhost:8000/api/voice \
  -F "audio=@test_audio.webm" \
  -H "Content-Type: multipart/form-data"
```

**Get recent events**:
```bash
curl http://localhost:8000/api/events
```

### Test WebSocket Directly

Using a WebSocket client or browser console:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => console.log('Received:', event.data);
ws.onopen = () => console.log('Connected');
```

---

## 📊 API Endpoints

### REST Endpoints

#### `POST /api/voice`
Process voice recording and classify emergency.

**Request**:
- Content-Type: `multipart/form-data`
- Body: `audio` (audio file)

**Response**:
```json
{
  "id": "uuid",
  "transcript": "string",
  "type": "FIRE | MEDICAL | VIOLENCE | ACCIDENT | NORMAL",
  "severity": 1-10,
  "assistant_reply": "string",
  "timestamp": "ISO datetime"
}
```

#### `GET /api/events`
Get recent emergency events.

**Query Parameters**:
- `limit` (optional): Maximum events to return (default: 50)

**Response**:
```json
{
  "events": [
    {
      "id": "uuid",
      "transcript": "string",
      "type": "string",
      "severity": 1-10,
      "assistant_reply": "string",
      "timestamp": "ISO datetime"
    }
  ],
  "count": 0
}
```

### WebSocket Endpoint

#### `WS /ws`
Real-time event streaming.

**Connection**: `ws://localhost:8000/ws`

**Messages**: Server broadcasts new events to all connected clients:
```json
{
  "id": "uuid",
  "transcript": "string",
  "type": "string",
  "severity": 1-10,
  "assistant_reply": "string",
  "timestamp": "ISO datetime"
}
```

---

## 🔌 Future Integrations

### ElevenLabs Speech-to-Text
**File**: `backend/services/mock_stt.py`

Replace the `mock_stt()` function with ElevenLabs API:
```python
import requests

def elevenlabs_stt(audio_data):
    # Integrate ElevenLabs STT API
    # Return transcript string
    pass
```

### Google Gemini API Classifier
**File**: `backend/services/mock_classifier.py`

Replace the `mock_classifier()` function with Gemini API:
```python
import google.generativeai as genai

def gemini_classifier(transcript):
    # Integrate Gemini API for classification
    # Return {type, severity, assistant_reply}
    pass
```

### Firestore Database
**File**: `backend/services/event_store.py`

Replace the in-memory EventStore with Firestore:
```python
from google.cloud import firestore

class FirestoreEventStore:
    def __init__(self):
        self.db = firestore.Client()
    
    def add_event(self, event):
        self.db.collection('events').add(event)
    
    def get_events(self, limit=50):
        return self.db.collection('events').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).get()
```

---

## 🎨 Design Features

- **Professional/Medical Theme**: Clean whites, blues, trust-building colors
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Real-time Updates**: WebSocket-powered live event feed
- **Accessibility**: Proper ARIA labels and keyboard navigation
- **Micro-interactions**: Smooth animations and transitions
- **Toast Notifications**: User-friendly feedback messages

---

## 🐛 Troubleshooting

### Backend not starting
```bash
# Check logs
tail -f backend.log

# Restart backend
pkill -f "uvicorn server:app"
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend not loading
```bash
# Check if frontend is running
ps aux | grep "yarn start"

# Restart frontend
cd frontend && yarn start
```

### WebSocket not connecting
- Check that backend is running
- Verify CORS settings in backend `.env`
- Check browser console for WebSocket errors

### Microphone not working
- Ensure browser has microphone permissions
- Use HTTPS (required for Web Audio API)
- Check browser compatibility

---

## 📝 Notes

- This is a **mock version** ready for integration
- All external API calls are currently simulated
- Event storage is in-memory (resets on server restart)
- WebSocket provides real-time updates across all connected clients
- Mock functions simulate realistic emergency scenarios for demo purposes

---

## 🔐 Security Considerations for Production

When integrating real APIs:
- Store API keys in environment variables
- Implement authentication and authorization
- Add rate limiting
- Validate and sanitize all inputs
- Use HTTPS everywhere
- Implement proper error handling
- Add logging and monitoring

---

## 📄 License

This project is built for demonstration and integration purposes.

---

## 👨‍💻 Development

For development with hot reload:
- Backend: FastAPI with `uvicorn --reload`
- Frontend: React with Vite dev server

Both services auto-reload on file changes (except for `.env` and dependency changes).

---

**Built with ❤️ for emergency response and safety**