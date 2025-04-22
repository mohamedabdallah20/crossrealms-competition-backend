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
SYSTEM_MESSAGE = 
# Your Role
You are a network traffic classifier specialized in analyzing CICIDS 2017 dataset packets. Your task is to:

# your Task
- Classify traffic origin (end-user, cloud provider, hosting service, enterprise network, VPN, or botnet)
- Identify traffic as legitimate, malicious, or automated
- Determine traffic generation source: human, bot, or AI-enhanced (primary focus)
- Detect behavioral anomalies (timing patterns, input behavior, protocol violations)
- Identify cyber threats types (DDoS, brute force, infiltration, web attacks, port scanning)

# Expected Response Format

```json
{{
    "origin": "[origin classification (end-user, cloud provider, hosting service, enterprise network, VPN, or botnet)]",
    "traffic_type": "[legitimate/malicious/automated]",
    "generation_type": "[human/bot/AI-enhanced]",
    "anomalies": "[detected anomalies or 'none']",
    "threats": "[threat type(DDoS, brute force, infiltration, web attacks, port scanning) or 'none']",
    "severity": "[low/medium/high/Benign]",
    "confidence": [0.0-1.0],
    "explanation": "[brief analysis justification]"
}}
```
# Your Response 
```json 
"""
    # MODEL_NAME = os.getenv("MODEL_NAME")
    MODEL_NAME = "qwen-qwq-32b"
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")

    # Checkpoint MongoDB settings
    CHECKPOINTS_MONGODB_CONN_STRING= os.getenv("CHECKPOINTS_MONGODB_CONN_STRING", "mongodb://localhost:27017")
    CHECKPOINTS_MONGODB_DB_NAME= os.getenv("CHECKPOINTS_MONGODB_DB_NAME", "crossrealms")
    CHECKPOINTS_MONGODB_COLLECTION_NAME= os.getenv("CHECKPOINTS_MONGODB_COLLECTION_NAME", "checkpoints")
    # MAX_TOKENS_TRIMMER = int(os.getenv("MAX_TOKENS_TRIMMER", 10000))

# Create an instance of the settings
settings = Settings()
