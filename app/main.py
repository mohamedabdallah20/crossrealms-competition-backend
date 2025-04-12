from fastapi import FastAPI, Depends,Request,APIRouter,HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse,PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routes.chat_routes import chatroutes 
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handler for HTTPException
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # print(f"Caught HTTPException: {exc.detail}")  # Log to console
    if exc.status_code == 500:
        # Configure logging
        logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')
        # Log the unexpected exception
        logging.exception(f"Caught unexpected exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error please try again later"},
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# Generic handler for all other unhandled exceptions_handlers (500)
@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    # Catch all other exceptions_handlers to prevent app crash

    # Configure logging
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')
    # Log the unexpected exception
    logging.exception(f"Caught unexpected exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

@app.get("/")
async def root():
    return {"message": "CrossRealms Competition API : please use /docs to use the app within the browser",
            "ps" : "Don't forget to set the environment variable GROQ_API_KEY and make sure that mongoDB is up and running with the correct credentials in the .env file" }
app.include_router(chatroutes, prefix="/api/chat", tags=["chat"])

