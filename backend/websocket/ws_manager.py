"""WebSocket Connection Manager"""
import logging
import json
from typing import Set
from fastapi import WebSocket
from bson import ObjectId

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        logger.info("ConnectionManager initialized")
    
    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection
        
        Args:
            websocket: WebSocket connection to add
        """
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection
        
        Args:
            websocket: WebSocket connection to remove
        """
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients
        
        Args:
            message: Dictionary message to broadcast
        """
        if not self.active_connections:
            logger.warning("No active connections to broadcast to")
            return
        
        # Convert ObjectId to string for JSON serialization
        def convert_objectid(obj):
            if isinstance(obj, dict):
                return {key: convert_objectid(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_objectid(item) for item in obj]
            elif isinstance(obj, ObjectId):
                return str(obj)
            else:
                return obj
        
        message_serializable = convert_objectid(message)
        message_json = json.dumps(message_serializable)
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
        
        logger.info(f"Broadcast sent to {len(self.active_connections)} clients")

# Global connection manager instance
manager = ConnectionManager()