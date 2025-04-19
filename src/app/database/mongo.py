import asyncio
import logging
from typing import List, Optional, Type

import motor.motor_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.app import settings
from src.app.database.schemas.url import UrlSchema

logger = logging.getLogger(__name__)

# Global state tracker - not reliable in serverless environments between requests
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

    async def is_connection_valid(self):
        """Test if the connection is actually valid"""
        if not self._initialized or not self._client:
            return False

        try:
            await self._client.admin.command("ping")
            return True
        except Exception as e:
            logger.warning(f"MongoDB connection check failed: {str(e)}")
            self._initialized = False
            db_state["initialized"] = False
            return False

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


mongodb = MongoDBConnection()


async def ensure_db_connected():
    """Ensure the database is connected - useful for serverless environments"""
    if settings.is_vercel or not db_state["initialized"]:
        if mongodb._initialized:
            is_valid = await mongodb.is_connection_valid()
            if is_valid:
                logger.info("Existing MongoDB connection is valid")
                return
            else:
                logger.info("Existing MongoDB connection is invalid, reconnecting")

        try:
            await mongodb.initialize()
        except RuntimeError as re:
            if "Event loop is closed" in str(re):
                logger.info("Reconnecting due to closed event loop")
                try:
                    # Create a new event loop
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    await mongodb.initialize()
                except Exception as e:
                    logger.error(
                        f"Failed to initialize MongoDB after event loop reset: {str(e)}"
                    )
                    raise
            else:
                logger.error(f"Failed to initialize MongoDB: {str(re)}")
                raise
