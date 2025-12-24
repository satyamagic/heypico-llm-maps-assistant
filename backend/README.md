# Backend README

## HeyPico AI Maps Backend

FastAPI backend for AI-powered location search with Google Maps integration.

## Setup

### Prerequisites
- Python 3.11+
- Ollama installed and running locally
- Google Maps API key

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Configure environment variables in `.env`:
- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key
- `OLLAMA_BASE_URL`: Ollama API endpoint (default: http://localhost:11434)
- `LLM_MODEL`: LLM model name (e.g., llama3.2:latest)

### Running the Server

```bash
uvicorn app.main:app --reload --port 8000
```

API will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

## Architecture

### Services
- **LLM Service**: Extracts structured intent from natural language
- **Google Maps Service**: Searches places and calculates distances

### API Endpoints
- `POST /api/query`: Process user query and return places

### Data Flow
1. User submits natural language query
2. LLM extracts structured intent (query, location, category)
3. Google Places API searches for places
4. Google Distance Matrix API calculates travel times
5. Transport recommendation logic determines best option
6. Structured response returned to frontend
