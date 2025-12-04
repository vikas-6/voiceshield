from dotenv import load_dotenv
from pathlib import Path
import os

# CRITICAL: Load .env BEFORE importing any services that use environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from contextlib import asynccontextmanager
import uuid
from datetime import datetime, timezone

# Import voice routes and WebSocket manager AFTER loading .env
from routes.voice import router as voice_router
from websocket.ws_manager import manager
from services.event_store import event_store

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate required environment variables
def validate_environment():
    """Validate that all required environment variables are set"""
    required_vars = {
        'MONGO_URL': 'MongoDB connection URL',
        'DB_NAME': 'Database name',
        'ELEVENLABS_API_KEY': 'ElevenLabs API key for voice processing',
        'GEMINI_API_KEY': 'Google Gemini API key for response generation'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(f"  - {var}: {description}")
    
    if missing_vars:
        error_msg = "Missing required environment variables:\n" + "\n".join(missing_vars)
        error_msg += "\n\nPlease add these to your backend/.env file"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("All required environment variables are set")

# MongoDB connection (will be initialized in lifespan)
client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global client, db
    
    # Startup
    logger.info("Starting Voice Emergency Assistant Backend...")
    
    # Validate environment variables
    validate_environment()
    
    # Initialize MongoDB connection
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Set the database connection for the event store
    event_store.set_db(db)
    
    logger.info("Voice Emergency Assistant Backend started successfully")
    
    yield
    
    # Shutdown
    if client:
        client.close()
        logger.info("Voice Emergency Assistant Backend shutdown")

# Create the main app with lifespan
app = FastAPI(
    title="Voice Emergency Assistant", 
    description="Real-Time Voice Emergency Detection System",
    lifespan=lifespan
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Health check routes
@api_router.get("/")
async def root():
    return {"message": "Voice Emergency Assistant Backend", "status": "operational"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Include voice processing routes
api_router.include_router(voice_router, tags=["voice"])

# WebSocket endpoint for real-time events
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time event streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            logging.info(f"Received from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logging.info("Client disconnected from WebSocket")
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)