from pydantic import BaseModel
from typing import Optional
from app.config import settings
from typing import List

# Configuration model
class ModelConfig(BaseModel):
    model_name: str = settings.MODEL_NAME
    model_provider: str = settings.MODEL_PROVIDER

# Request and response models
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

class NewThreadResponse(BaseModel):
    thread_id: str
class CreateNewThread(BaseModel):
    thread_name: Optional[str] = None

class ThreadInfo(BaseModel):
    thread_id: str
    thread_name: Optional[str] = None
class ChatHistoryResponse(BaseModel):
    thread_id: str
    chat_history: dict
