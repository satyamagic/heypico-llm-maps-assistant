"""
Google Maps Service for Places and Distance Matrix APIs
"""
import googlemaps
import logging
from typing import List, Optional, Dict, Tuple
from app.utils.env_config import get_google_maps_api_key
from app.schemas.models import Place, TransportOption

logger = logging.getLogger(__name__)


class GoogleMapsService:
    """Service for Google Maps Places and Distance Matrix APIs"""
    
    def __init__(self):
        api_key = get_google_maps_api_key()
        self.client = googlemaps.Client(key=api_key)
    
    async def search_places(
        self,
        query: str,
        location: str,
        max_results: int = 5
    ) -> List[Place]:
        """
        Search for places using Google Places API
        
        Args:
            query: Search query (e.g., "ramen")
            location: Location string (e.g., "Blok M Jakarta")
            max_results: Maximum number of results to return
            
        Returns:
            List of Place objects
        """
        try:
            # First, geocode the location to get lat/lng
            geocode_result = self.client.geocode(location)
            
            if not geocode_result:
                logger.warning(f"Could not geocode location: {location}")
                return []
            
            location_coords = geocode_result[0]['geometry']['location']
            lat = location_coords['lat']
            lng = location_coords['lng']
            
            # Search for places
            places_result = self.client.places(
                query=f"{query} near {location}",
                location=(lat, lng),
                radius=5000  # 5km radius
            )
            
            places = []
            results = places_result.get('results', [])[:max_results]
            
            for result in results:
                place = self._parse_place(result)
                if place:
                    places.append(place)
            
            logger.info(f"Found {len(places)} places for query: {query} near {location}")
            return places
            
        except Exception as e:
            logger.error(f"Error searching places: {e}")
            return []
    
    def _parse_place(self, result: dict) -> Optional[Place]:
        """Parse a place result from Google Maps API"""
        try:
            place_id = result.get('place_id', '')
            name = result.get('name', 'Unknown')
            address = result.get('formatted_address', result.get('vicinity', ''))
            
            location = result.get('geometry', {}).get('location', {})
            lat = location.get('lat', 0.0)
            lng = location.get('lng', 0.0)
            
            rating = result.get('rating')
            user_ratings_total = result.get('user_ratings_total')
            
            # Generate Google Maps URL
            maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            
            return Place(
                name=name,
                address=address,
                place_id=place_id,
                lat=lat,
                lng=lng,
                rating=rating,
                user_ratings_total=user_ratings_total,
                maps_url=maps_url
            )
        except Exception as e:
            logger.error(f"Error parsing place: {e}")
            return None
    
    async def calculate_distances(
        self,
        origin_lat: float,
        origin_lng: float,
        places: List[Place]
    ) -> List[Place]:
        """
        Calculate distances and travel times from origin to each place
        
        Args:
            origin_lat: Origin latitude
            origin_lng: Origin longitude
            places: List of places to calculate distances to
            
        Returns:
            Updated list of places with distance and time information
        """
        if not places:
            return places
        
        try:
            origin = (origin_lat, origin_lng)
            destinations = [(place.lat, place.lng) for place in places]
            
            # Get distance matrix for all transport modes
            walking = self.client.distance_matrix(
                origins=[origin],
                destinations=destinations,
                mode="walking"
            )
            
            bicycling = self.client.distance_matrix(
                origins=[origin],
                destinations=destinations,
                mode="bicycling"
            )
            
            driving = self.client.distance_matrix(
                origins=[origin],
                destinations=destinations,
                mode="driving"
            )
            
            # Update each place with distance/time info
            for i, place in enumerate(places):
                walk_elem = walking['rows'][0]['elements'][i]
                bike_elem = bicycling['rows'][0]['elements'][i]
                drive_elem = driving['rows'][0]['elements'][i]
                
                if walk_elem['status'] == 'OK':
                    place.distance = walk_elem['distance']['text']
                    place.walk_time = walk_elem['duration']['text']
                    walk_seconds = walk_elem['duration']['value']
                    
                if bike_elem['status'] == 'OK':
                    place.bike_time = bike_elem['duration']['text']
                    bike_seconds = bike_elem['duration']['value']
                    
                if drive_elem['status'] == 'OK':
                    place.drive_time = drive_elem['duration']['text']
                    drive_seconds = drive_elem['duration']['value']
                
                # Determine recommended transport
                place.recommended_transport = self._recommend_transport(
                    walk_elem.get('duration', {}).get('value', float('inf')),
                    bike_elem.get('duration', {}).get('value', float('inf')),
                    drive_elem.get('duration', {}).get('value', float('inf'))
                )
            
            return places
            
        except Exception as e:
            logger.error(f"Error calculating distances: {e}")
            return places
    
    def _recommend_transport(
        self,
        walk_seconds: int,
        bike_seconds: int,
        drive_seconds: int
    ) -> str:
        """
        Recommend transport mode based on duration
        
        Rules:
        - Walking ≤ 7 minutes → recommend walking
        - Else if biking ≤ 10 minutes → recommend biking
        - Else → recommend driving
        """
        walk_minutes = walk_seconds / 60
        bike_minutes = bike_seconds / 60
        
        if walk_minutes <= 7:
            return "walk"
        elif bike_minutes <= 10:
            return "bike"
        else:
            return "drive"


# Singleton instance
google_maps_service = GoogleMapsService()
