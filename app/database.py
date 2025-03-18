from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from app.config import settings
MONGO_DETAILS = settings.DATABASE_URL

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.crossrealms

# Example collection
thread_collection = database.get_collection("threads")
