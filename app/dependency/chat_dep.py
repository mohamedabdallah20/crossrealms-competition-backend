import os
from typing import Dict, List, Any, Optional
from app.config import settings
from langchain.chat_models import init_chat_model
from langchain_core.messages import trim_messages, AIMessage
from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from fastapi import Depends
from langgraph.graph import START, MessagesState, StateGraph, END
# from app.dependency.chat_tools import get_tools
from langgraph.prebuilt import ToolNode
from app.schemas.chat_schema import ModelConfig
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB configuration
MONGO_URI = settings.CHECKPOINTS_MONGODB_CONN_STRING
DB_NAME = settings.CHECKPOINTS_MONGODB_DB_NAME
COLLECTION_NAME = settings.CHECKPOINTS_MONGODB_COLLECTION_NAME

# Initialize async MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_URI)

# Initialize MongoDB saver
mongo_saver = AsyncMongoDBSaver(client=mongo_client, db_name=DB_NAME, collection_name=COLLECTION_NAME)

# Dependency for configuration
def get_Model_config() -> ModelConfig:
    return ModelConfig()

# Dependency for chat model without tools (will bind tools later)
async def get_base_chat_model(Model_config: ModelConfig = Depends(get_Model_config)):
    """Initialize and return the base chat model without tools."""
    try:
        return init_chat_model(
            Model_config.model_name, 
            model_provider=Model_config.model_provider, 
            api_key=settings.GROQ_API_KEY
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize chat model: {e}")

async def get_workflow(model = Depends(get_base_chat_model)) -> StateGraph:
    """Create and return the workflow graph."""
    workflow = StateGraph(state_schema=MessagesState)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                settings.SYSTEM_MESSAGE,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    trimmer = trim_messages(
        strategy="last",
        token_counter=len,
        max_tokens=1,
        start_on="human",
        include_system=True,
        allow_partial=False,
    )
        
    
    # Function to call model
    async def call_model(state: MessagesState):
        """Call the model with trimmed messages."""
        # trimmed_messages = trimmer.invoke(state["messages"])
        # prompt = prompt_template.invoke(trimmed_messages)
        # response = await model_with_tools.ainvoke(prompt)
        # return {"messages": [response]}
        messages = state.get("messages", [])
        
        # Apply trimming if needed
        if len(messages) > 2:  
        # if False:  
            trimmed_messages = trimmer.invoke(messages)
        else:
            trimmed_messages = messages
        
        # Format with prompt template
        prompt = prompt_template.invoke(trimmed_messages)
        
        # Get response from model
        response = await model.ainvoke(prompt)
        # Return updated state with all original messages plus the new response
        return {"messages": messages + [response]}
    
    
    # Add nodes to workflow
    workflow.add_node("model", call_model)
    workflow.add_edge(START, "model")
    
    return workflow

# Dependency for the chat app
async def get_chat_app(
    workflow: StateGraph = Depends(get_workflow),
) -> StateGraph:
    """Compile and return the chat application."""
    return workflow.compile(checkpointer=mongo_saver)