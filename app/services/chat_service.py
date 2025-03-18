import logging
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from fastapi import HTTPException
from bson import ObjectId
from app.config import settings
from typing import Optional, List,Dict
from app.schemas.chat_schema import CreateNewThread,NewThreadResponse,ThreadInfo
from app.database import thread_collection
logger = logging.getLogger(__name__)

async def chat(
    query: str,
    config: dict,
    app: StateGraph,
) -> str:
    """Handle the chat interaction."""
    try:
        input_messages = [HumanMessage(content=query)]
        output = await app.ainvoke(
            {"messages": input_messages},
            {"configurable": {"thread_id": config["thread_id"]}},
        )
        return output["messages"][-1].content
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during chat.")
    
async def fetch_chat_history(thread_id: str) -> Optional[dict]:
    async with AsyncMongoDBSaver.from_conn_string(
        settings.CHECKPOINTS_MONGODB_CONN_STRING,
        db_name=settings.CHECKPOINTS_MONGODB_DB_NAME,
    ) as saver:
        config = {"configurable": {"thread_id": thread_id}}
        checkpoint_tuple = await saver.aget_tuple(config)
        
        if checkpoint_tuple is None:
            return None
        
        checkpoint = checkpoint_tuple.checkpoint
        return {"checkpoint": checkpoint}

# assgin new thread_id and save it to the database and return the thread_id
async def start_new_thread(data: CreateNewThread) -> str:
    thread_id = await thread_collection.insert_one(data.dict())
    return str(thread_id.inserted_id)
    
# get the threads
async def get_threads() -> List[ThreadInfo]:
    # Assuming thread_collection is a MongoDB collection
    cursor = thread_collection.find()
   
    # Convert the cursor to a list of documents
    threads = await cursor.to_list(length=None)
   
    # Extract _id (as thread_id) and thread_name from each document
    result = [
        {"thread_id": str(thread["_id"]), "thread_name": thread.get("thread_name", "")}
        for thread in threads
    ]
    return result

async def update_thread_name(thread_id: str, thread_name: str) -> ThreadInfo:
    thread = await thread_collection.find_one({"_id": ObjectId(thread_id)})
    if thread:
        await thread_collection.update_one({"_id": ObjectId(thread_id)}, {"$set": {"thread_name": thread_name}})
        return {"thread_id": str(thread["_id"]), "thread_name": thread_name}
    raise HTTPException(status_code=404, detail="thread not found")

async def delete_thread(thread_id: str) -> bool:
    thread = await thread_collection.find_one({"_id": ObjectId(thread_id)})
    if thread:
        await thread_collection.delete_one({"_id": ObjectId(thread_id)})
        return True

    raise HTTPException(status_code=404, detail="thread not found")

# async def fetch_chat_history(thread_id: str,app: StateGraph) -> Optional[dict]:
#     config = {"configurable": {"thread_id": thread_id}}
#     state = await app.aget_state(config)
        
#     if state["messages"] is None:
#         return None

#     checkpoint = state["messages"]
#     return {"checkpoint": checkpoint}