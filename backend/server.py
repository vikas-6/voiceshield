from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone

# Import voice routes and WebSocket manager
from routes.voice import router as voice_router
from websocket.ws_manager import manager
from services.event_store import event_store

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection - get from environment with proper error handling
mongo_url = os.environ.get('MONGO_URL')
db_name = os.environ.get('DB_NAME', 'voice_assistant_db')

if not mongo_url:
    raise ValueError("MONGO_URL environment variable is required. Set it in Render Dashboard > Environment.")

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Set the database connection for the event store
event_store.set_db(db)

# Create the main app without a prefix
app = FastAPI(title="Voice Emergency Assistant", description="Real-Time Voice Emergency Detection System")

# Root health check for Render
@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "Voice Emergency Assistant"}

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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Voice Emergency Assistant Backend started successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("Voice Emergency Assistant Backend shutdown")