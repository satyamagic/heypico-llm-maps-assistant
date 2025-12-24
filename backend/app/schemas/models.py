"""
Pydantic schemas for request/response validation
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    """User's natural language query"""
    query: str = Field(..., min_length=1, description="Natural language query from user")
    user_lat: Optional[float] = Field(None, description="User's latitude")
    user_lng: Optional[float] = Field(None, description="User's longitude")


class LLMIntent(BaseModel):
    """Structured intent extracted by LLM"""
    query: str = Field(..., description="Search query (e.g., 'ramen')")
    location: str = Field(..., description="Location string (e.g., 'Blok M Jakarta')")
    category: str = Field(default="restaurant", description="Category type")


class TransportOption(BaseModel):
    """Transport duration and distance"""
    mode: str = Field(..., description="Transport mode: walk, bike, or drive")
    duration: str = Field(..., description="Duration text (e.g., '5 mins')")
    distance: str = Field(..., description="Distance text (e.g., '1.2 km')")
    duration_seconds: int = Field(..., description="Duration in seconds")


class Place(BaseModel):
    """A place result with distance and transport info"""
    name: str
    address: str
    place_id: str
    lat: float
    lng: float
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    distance: Optional[str] = None
    walk_time: Optional[str] = None
    bike_time: Optional[str] = None
    drive_time: Optional[str] = None
    recommended_transport: Optional[str] = None
    maps_url: str


class QueryResponse(BaseModel):
    """Complete response with AI text and places"""
    ai_response: str = Field(..., description="Natural language response from AI")
    places: List[Place] = Field(default_factory=list, description="List of suggested places")
    user_location: Optional[dict] = Field(None, description="User's location used for query")


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
