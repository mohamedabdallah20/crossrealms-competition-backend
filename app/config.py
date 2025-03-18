import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()
class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Chat settings
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    SYSTEM_MESSAGE = """
you are a good packet analyzer and expert in network security.
you will be asked to analyze a packet and give a summary of the packet.
"""
    # MODEL_NAME = os.getenv("MODEL_NAME")
    MODEL_NAME = "llama3-8b-8192"
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")

    # Checkpoint MongoDB settings
    CHECKPOINTS_MONGODB_CONN_STRING= os.getenv("CHECKPOINTS_MONGODB_CONN_STRING", "mongodb://localhost:27017")
    CHECKPOINTS_MONGODB_DB_NAME= os.getenv("CHECKPOINTS_MONGODB_DB_NAME", "crossrealms")
    CHECKPOINTS_MONGODB_COLLECTION_NAME= os.getenv("CHECKPOINTS_MONGODB_COLLECTION_NAME", "checkpoints")
    MAX_TOKENS_TRIMMER = int(os.getenv("MAX_TOKENS_TRIMMER", 10000))

# Create an instance of the settings
settings = Settings()
