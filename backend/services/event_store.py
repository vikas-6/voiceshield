"""MongoDB Event Store Integration"""
import logging
from typing import List, Dict, Any
from datetime import datetime
import asyncio
from bson import ObjectId

logger = logging.getLogger(__name__)

class MongoEventStore:
    """MongoDB storage for emergency events"""
    
    def __init__(self, db_client=None):
        """Initialize event store with MongoDB connection
        
        Args:
            db_client: MongoDB database client
        """
        self.db = None
        if db_client is not None:
            self.db = db_client
            logger.info("MongoEventStore initialized with MongoDB connection")
    
    def set_db(self, db_client):
        """Set the database client after initialization
        
        Args:
            db_client: MongoDB database client
        """
        self.db = db_client
        logger.info("MongoEventStore database client set")
    
    async def add_event(self, event: Dict[str, Any]) -> None:
        """Add an event to the store
        
        Args:
            event: Event dictionary to store
        """
        if self.db is None:
            logger.error("MongoEventStore not initialized with database connection")
            return
            
        try:
            # Add timestamp if not present
            if 'timestamp' not in event:
                event['timestamp'] = datetime.utcnow().isoformat()
                
            # Insert into MongoDB collection
            result = await self.db.events.insert_one(event)
            logger.info(f"Event added to MongoDB: {event['id']} with _id {result.inserted_id}")
        except Exception as e:
            logger.error(f"Error adding event to MongoDB: {e}", exc_info=True)
    
    async def get_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent events
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        if self.db is None:
            logger.error("MongoEventStore not initialized with database connection")
            return []
            
        try:
            # Query MongoDB for recent events
            cursor = self.db.events.find({}).sort('_id', -1).limit(limit)
            events_list = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string for JSON serialization
            for event in events_list:
                if '_id' in event:
                    event['_id'] = str(event['_id'])
                    
            logger.info(f"Retrieved {len(events_list)} events from MongoDB")
            return events_list
        except Exception as e:
            logger.error(f"Error retrieving events from MongoDB: {e}", exc_info=True)
            return []
    
    async def clear(self) -> None:
        """Clear all events from store"""
        if self.db is None:
            logger.error("MongoEventStore not initialized with database connection")
            return
            
        try:
            result = await self.db.events.delete_many({})
            logger.info(f"Cleared {result.deleted_count} events from MongoDB")
        except Exception as e:
            logger.error(f"Error clearing events from MongoDB: {e}", exc_info=True)

# Global event store instance
event_store = MongoEventStore()