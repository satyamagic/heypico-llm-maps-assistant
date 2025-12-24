"""
Query router for handling user queries
"""
from fastapi import APIRouter, HTTPException
from app.schemas.models import UserQuery, QueryResponse, Place
from app.services.llm_service import llm_service
from app.services.google_maps_service import google_maps_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def process_query(query: UserQuery):
    """
    Process a user query and return AI-powered place recommendations
    
    Flow:
    1. Extract intent from natural language using LLM
    2. Search Google Maps for places
    3. Calculate distances and travel times
    4. Generate AI response
    5. Return structured results
    """
    try:
        # Step 1: Extract intent using LLM
        logger.info(f"Processing query: {query.query}")
        intent = await llm_service.extract_intent(query.query)
        
        if not intent:
            raise HTTPException(
                status_code=400,
                detail="Could not understand the query. Please try rephrasing."
            )
        
        logger.info(f"Extracted intent: {intent}")
        
        # Step 2: Search for places
        places = await google_maps_service.search_places(
            query=intent.query,
            location=intent.location,
            max_results=5
        )
        
        if not places:
            return QueryResponse(
                ai_response=f"I couldn't find any {intent.query} places near {intent.location}. Try a different location or search term.",
                places=[],
                user_location={
                    "lat": query.user_lat,
                    "lng": query.user_lng
                } if query.user_lat and query.user_lng else None
            )
        
        # Step 3: Calculate distances if user location is provided
        if query.user_lat and query.user_lng:
            places = await google_maps_service.calculate_distances(
                origin_lat=query.user_lat,
                origin_lng=query.user_lng,
                places=places
            )
        
        # Step 4: Generate AI response
        ai_response = _generate_response(intent, places, has_distances=bool(query.user_lat))
        
        # Step 5: Return results
        return QueryResponse(
            ai_response=ai_response,
            places=places,
            user_location={
                "lat": query.user_lat,
                "lng": query.user_lng
            } if query.user_lat and query.user_lng else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your query: {str(e)}"
        )


def _generate_response(intent, places: list[Place], has_distances: bool) -> str:
    """Generate a natural language response"""
    num_places = len(places)
    
    if num_places == 0:
        return f"I couldn't find any {intent.query} places near {intent.location}."
    
    response = f"I found {num_places} great {intent.query} place"
    if num_places > 1:
        response += "s"
    response += f" near {intent.location}. "
    
    if has_distances:
        # Find the closest place
        closest = min(places, key=lambda p: float('inf') if not p.walk_time else int(p.walk_time.split()[0]))
        if closest.recommended_transport:
            response += f"The closest is {closest.name}, best reached by {closest.recommended_transport}."
    else:
        response += "Here are my top recommendations for you."
    
    return response
