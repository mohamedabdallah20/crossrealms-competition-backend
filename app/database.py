from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from app.config import settings
MONGO_DETAILS = settings.DATABASE_URL

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.finance

# Example collection
user_collection = database.get_collection("users")
thread_collection = database.get_collection("threads")
refresh_tokens_collection = database.get_collection("refresh_tokens")


# Store refresh token in DB
def store_refresh_token(user_id: str, refresh_token: str):
    refresh_token_doc = {
        "user_id": user_id,
        "refresh_token": refresh_token,
        "revoked": False,
        "created_at": datetime.utcnow()
    }
    refresh_tokens_collection.insert_one(refresh_token_doc)

# Revoke a refresh token
def revoke_refresh_token(refresh_token: str):
    refresh_tokens_collection.update_one(
        {"refresh_token": refresh_token},
        {"$set": {"revoked": True}}
    )