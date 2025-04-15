# CrossRealms Backend

## Prerequisites

- Python 3.13 (for local development)
- Docker and Docker Compose (for containerized deployment)
- MongoDB (for local development only)

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mohamedabdallah20/crossrealms-competition-backend.git
   cd crossrealms-competition-backend
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration values.

5. Start MongoDB (for local development):
   ```bash
   # Make sure MongoDB is running on your system
   # Default connection: mongodb://localhost:27017
   ```

6. Run the application:
   ```bash
   source venv/bin/activate  # If not already activated
   uvicorn app.main:app --reload --port 8002
   ```

7. Access the API documentation:
   - Swagger UI: http://localhost:8002/docs
   - ReDoc: http://localhost:8002/redoc

## Docker Deployment (Recommended)

### Using Docker Compose

1. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration values.

2. Start the services:
   ```bash
   docker compose up
   ```

3. The services will be available at:
   - API: http://localhost:8002
   - API Documentation: http://localhost:8002/docs
   - MongoDB: localhost:27017

4. Data persistence:
   - MongoDB data is persisted in a Docker volume named `mongodb_data`
   - The volume is automatically created and managed by Docker Compose

### Using Docker Directly

1. Run MongoDB container:
   ```bash
   docker run -d --name mongodb -p 27017:27017 -v mongodb_data:/data/db mongo:latest
   ```

2. Run the application container:
   ```bash
   docker run -p 8002:8002 \
     --env-file .env \
     -e DATABASE_URL=mongodb://host.docker.internal:27017/crossrealms \
     -e CHECKPOINTS_MONGODB_CONN_STRING=mongodb://host.docker.internal:27017/ \
     mohamedabdallah0/crossrealms-backend:1.0
   ```

## Environment Variables

Required environment variables in `.env`:
- `DATABASE_URL`: MongoDB connection string
- `GROQ_API_KEY`: Your Groq API key
- `MODEL_NAME`: Name of the model to use
- `MODEL_PROVIDER`: Model provider (e.g., "groq")
- `CHECKPOINTS_MONGODB_CONN_STRING`: MongoDB connection string for checkpoints
- `CHECKPOINTS_MONGODB_DB_NAME`: Database name for checkpoints
- `CHECKPOINTS_MONGODB_COLLECTION_NAME`: Collection name for checkpoints

## Development Notes

- The application uses FastAPI framework
- MongoDB is required for data persistence
- Python 3.13 is required for local development
- Docker deployment uses pre-built image `mohamedabdallah0/crossrealms-backend:1.0`
- MongoDB data is persisted using Docker volumes
