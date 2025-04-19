import asyncio
import logging
from typing import List, Optional, Type

import motor.motor_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.app import settings
from src.app.database.schemas.url import UrlSchema

logger = logging.getLogger(__name__)

db_state = {"initialized": False}


class MongoDBConnection:
    """
    Singleton class for MongoDB connection using Beanie
    """

    _instance: Optional["MongoDBConnection"] = None
    _client: Optional[AsyncIOMotorClient] = None
    _db = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    async def initialize(self):
        """Initialize the MongoDB connection if not already initialized"""
        if self._initialized:
            return

        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.get_connection_string
        )
        self._db = self._client[settings.database]

        models: List[Type] = [UrlSchema]
        await init_beanie(database=self._db, document_models=models)

        self._initialized = True
        db_state["initialized"] = True
        logger.info("MongoDB connection initialized")

    @property
    def client(self) -> AsyncIOMotorClient:
        """Get the motor client instance"""
        if not self._initialized:
            raise RuntimeError(
                "Database connection not initialized. Call 'await initialize()' first."
            )
        return self._client

    @property
    def db(self):
        """Get the database instance"""
        if not self._initialized:
            raise RuntimeError(
                "Database connection not initialized. Call 'await initialize()' first."
            )
        return self._db

    async def close(self):
        """Close the MongoDB connection"""
        if self._client and self._initialized:
            self._client.close()
            self._initialized = False
            db_state["initialized"] = False
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")


# Singleton instance that should be used throughout the application
mongodb = MongoDBConnection()


# Helper function for serverless environments
async def ensure_db_connected():
    """Ensure the database is connected - useful for serverless environments"""
    if not db_state["initialized"]:
        try:
            await mongodb.initialize()
        except RuntimeError as re:
            if "Event loop is closed" in str(re):
                logger.info("Reconnecting due to closed event loop")
                asyncio.set_event_loop(asyncio.new_event_loop())
                await mongodb.initialize()
            else:
                logger.error(f"Failed to initialize MongoDB: {str(re)}")
                raise
