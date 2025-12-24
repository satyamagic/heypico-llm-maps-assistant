"""
Query router for handling user queries
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.models import UserQuery, QueryResponse, Place
from app.services.llm_service import llm_service
from app.services.google_maps_service import google_maps_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class LocationRequest(BaseModel):
    lat: float
    lng: float


class LocationResponse(BaseModel):
    city: str
    formatted_address: str


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
        # Preprocess query: replace "near me" with actual location if coordinates provided
        processed_query = query.query
        user_location_name = None
        
        # If user location is provided, always get the location name for better results
        if query.user_lat and query.user_lng:
            # Reverse geocode to get location name
            try:
                geocode_result = google_maps_service.client.reverse_geocode((query.user_lat, query.user_lng))
                if geocode_result:
                    # Extract city name
                    for component in geocode_result[0].get('address_components', []):
                        if 'locality' in component.get('types', []) or 'administrative_area_level_2' in component.get('types', []):
                            user_location_name = component.get('long_name')
                            break
                    
                    if user_location_name:
                        # If query doesn't already specify a location, add it
                        if "near me" in query.query.lower() or "nearby" in query.query.lower():
                            processed_query = processed_query.replace("near me", f"near {user_location_name}")
                            processed_query = processed_query.replace("Near me", f"near {user_location_name}")
                            processed_query = processed_query.replace("nearby", f"near {user_location_name}")
                        elif "near" not in query.query.lower() and "in" not in query.query.lower():
                            # No location specified at all, append the user's location
                            processed_query = f"{processed_query} near {user_location_name}"
                        
                        logger.info(f"Using user location '{user_location_name}': {processed_query}")
            except Exception as e:
                logger.warning(f"Could not geocode user location: {e}")
        
        # Step 1: Extract intent using LLM
        logger.info(f"Processing query: {processed_query}")
        intent = await llm_service.extract_intent(processed_query)
        
        if not intent:
            raise HTTPException(
                status_code=400,
                detail="Could not understand the query. Please try rephrasing."
            )
        
        logger.info(f"Extracted intent: {intent}")
        
        # Override location with user's actual location if available
        search_location = user_location_name if user_location_name else intent.location
        
        # Step 2: Search for places
        places = await google_maps_service.search_places(
            query=intent.query,
            location=search_location,
            max_results=5
        )
        
        if not places:
            return QueryResponse(
                ai_response=f"I couldn't find any {intent.query} places near {search_location}. Try a different location or search term.",
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
        
        # Step 4: Generate AI response (use actual search location)
        # Create a modified intent with the actual search location for response generation
        from app.schemas.models import LLMIntent
        response_intent = LLMIntent(
            query=intent.query,
            location=search_location,
            category=intent.category
        )
        ai_response = _generate_response(response_intent, places, has_distances=bool(query.user_lat))
        
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


@router.post("/geocode", response_model=LocationResponse)
async def reverse_geocode(location: LocationRequest):
    """
    Reverse geocode coordinates to get city name and address
    
    Args:
        location: Latitude and longitude
        
    Returns:
        City name and formatted address
    """
    try:
        logger.info(f"Reverse geocoding: {location.lat}, {location.lng}")
        
        # Use Google Maps client to reverse geocode
        result = google_maps_service.client.reverse_geocode((location.lat, location.lng))
        
        if not result:
            raise HTTPException(status_code=404, detail="Location not found")
        
        # Extract city name from address components
        city = None
        for component in result[0].get('address_components', []):
            if 'locality' in component.get('types', []):
                city = component.get('long_name')
                break
            elif 'administrative_area_level_2' in component.get('types', []):
                city = component.get('long_name')
        
        if not city:
            city = "Unknown Location"
        
        formatted_address = result[0].get('formatted_address', '')
        
        logger.info(f"Geocoded to: {city}")
        
        return LocationResponse(
            city=city,
            formatted_address=formatted_address
        )
        
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        raise HTTPException(status_code=500, detail="Failed to geocode location")

