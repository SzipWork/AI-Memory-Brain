# AI-Memory-Brain
A personal AI assistant that remembers user information across conversations using Neo4j as a memory store and Gemini AI for natural language processing.

## Features

- **Long-term Memory**: Stores user preferences, interests, goals, and personal facts in Neo4j graph database
- **Intelligent Memory Filtering**: Uses AI to determine what information is worth remembering
- **Natural Conversations**: Powered by Google's Gemini AI for natural language understanding
- **Dockerized Setup**: Easy deployment with Docker Compose
- **Web Interface**: Streamlit-based chat interface for intuitive interaction
- **Modular Architecture**: Clean separation of concerns with FastAPI backend


## Project Structure
```
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env
├── requirements.txt
├── front.py
app
  ├── main.py
  ├── config.py
  ├── gemini_llm.py
  ├── memory_router.py
  ├── memory_store.py
  └── schemas.py
```
## Initializatoin

### Prerequisites

- Docker and Docker Compose
- Google Gemini API key
- Python

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-memory-brain.git
cd ai-memory-brain
```
### 2. Set Up Environment Variables
Create a .env file in the root directory:
```
# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Neo4j Configuration (matches docker-compose)
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4jpassword
```

### 3. Build and Run with Docker Compose
```
docker-compose up --build
```
**This will start three services:**
- Neo4j: Graph database at http://localhost:7474
- Backend: FastAPI server at http://localhost:8000
- Frontend: Streamlit app at http://localhost:8501

## Data Flow
- User sends message via Streamlit frontend.
- FastAPI backend receives message with user ID.
- System checks if message contains memory recall triggers.
- If recalling: retrieves memories and generates response.
- If not recalling: routes through memory filter.
- Important personal facts are stored in Neo4j.
- Response is sent back to user.
