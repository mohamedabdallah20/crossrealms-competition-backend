from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat_schema import ChatRequest, ChatResponse,NewThreadResponse
from app.services.chat_service import chat, fetch_chat_history,start_new_thread,get_threads,update_thread_name,delete_thread
from app.dependency.chat_dep import get_chat_app
from app.schemas.chat_schema import ChatHistoryResponse,CreateNewThread,ThreadInfo
from typing import List,Dict

chatroutes = APIRouter()

@chatroutes.get("/threads", response_model=List[ThreadInfo])
async def get_threads_endpoint():
    """Endpoint to get all threads"""
    threads = await get_threads()
    return threads
@chatroutes.patch("/update-thread-name/{thread_id}", response_model=ThreadInfo)
async def update_thread_name_endpoint(thread_id: str, thread_name: str):
    """Endpoint to update the name of a thread."""
    return await update_thread_name(thread_id, thread_name)

@chatroutes.delete("/delete-thread/{thread_id}", response_model=bool)
async def delete_thread_endpoint(thread_id: str):
    """Endpoint to delete a thread."""
    return await delete_thread(thread_id)
@chatroutes.post("/new-thread", response_model=NewThreadResponse)
async def new_chat_endpoint(
    new_thread: CreateNewThread,
):
    """Endpoint to start a new chat."""
    thread_id = await start_new_thread(new_thread)
    return NewThreadResponse(thread_id=thread_id)

@chatroutes.post("/chat/{thread_id}", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    app=Depends(get_chat_app),
    thread_id: str = None
):
    """Endpoint to interact with the chatbot."""
    response = await chat(request.query, {'thread_id': thread_id}, app)
    return ChatResponse(response=response)

@chatroutes.get("/chat-history/{thread_id}", response_model=ChatHistoryResponse)
async def get_chat_history(thread_id: str):
    """Endpoint to fetch chat history for a given thread_id."""
    chat_data = await fetch_chat_history(thread_id)
    
    if chat_data is None:
        raise HTTPException(status_code=404, detail="No chat history found for the given thread_id")
    
    return ChatHistoryResponse(thread_id=thread_id, chat_history=chat_data)