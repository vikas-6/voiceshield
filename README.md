# Voice Emergency Assistant

A real-time voice emergency detection system that uses advanced voice processing to identify emergency situations and provide appropriate responses.

## Features

- Real-time voice recording and processing
- Emergency classification based on keywords (Fire, Medical, Violence, Accident)
- Text-to-speech response generation using ElevenLabs
- Persistent event storage with MongoDB
- Real-time event feed via WebSocket
- Responsive web interface built with React

## Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB Atlas account
- ElevenLabs API key

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```
   MONGO_URL="your_mongodb_connection_string"
   DB_NAME="voice_assistant_db"
   CORS_ORIGINS="*"
   ```

4. Start the backend server:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   yarn install
   ```

3. Configure environment variables in `.env`:
   ```
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   yarn start
   ```

## Production Deployment

### Quick Deploy

This application is configured for deployment to:
- **Frontend**: Vercel (free tier)
- **Backend**: Render (free tier)

**📖 Complete deployment guide**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed step-by-step instructions.

### Environment Variables

Copy `.env.example` files and update with your credentials:

**Backend** (`backend/.env`):
```bash
MONGO_URL=your_mongodb_connection_string
DB_NAME=voice_assistant_db
ELEVENLABS_API_KEY=your_elevenlabs_api_key
GEMINI_API_KEY=your_gemini_api_key
CORS_ORIGINS=*
```

**Frontend** (`frontend/.env`):
```bash
REACT_APP_BACKEND_URL=http://localhost:8000
```

### Local Development

Run the deployment script:
```bash
./deploy.sh
```

This will:
- Install all dependencies
- Build production versions of both frontend and backend
- Start both services in the background
- Log output to the `logs/` directory

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Click the microphone button to start recording
3. Speak an emergency phrase (e.g., "There's a fire in the building")
4. View the classified emergency and AI response
5. Monitor real-time events in the event feed

## API Endpoints

### Voice Processing
- `POST /api/voice` - Process voice recording
  - Form data: `audio` (webm audio file)
  - Returns: Emergency event object

### Events
- `GET /api/events` - Get recent emergency events
  - Query param: `limit` (default: 50)
  - Returns: List of events

### Status
- `GET /api/status` - Get system status checks
- `POST /api/status` - Create new status check

### WebSocket
- `WS /ws` - Real-time event streaming

## Architecture

```
┌─────────────┐    HTTP    ┌──────────────┐
│   React     │ ──────────▶│   FastAPI    │
│  Frontend   │            │   Backend    │
└─────────────┘            └──────────────┘
                                │
                           ┌────▼────┐
                           │ MongoDB │
                           │   Atlas │
                           └─────────┘
```

## Services

- **ElevenLabs STT**: Speech-to-text conversion with fallback to mock STT
- **Keyword Classifier**: Classifies emergencies based on transcript keywords
- **ElevenLabs TTS**: Text-to-speech response generation
- **MongoDB Event Store**: Persistent storage of emergency events
- **WebSocket Manager**: Real-time event broadcasting

## Development

### Backend Structure
```
backend/
├── routes/          # API route handlers
├── services/        # Business logic and external services
├── websocket/       # WebSocket connection management
├── server.py        # Main application entry point
└── requirements.txt # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/  # React UI components
│   ├── pages/       # Page components
│   ├── services/    # API service clients
│   └── App.js       # Main application component
└── package.json     # Node dependencies
```

## License

This project is proprietary and confidential.