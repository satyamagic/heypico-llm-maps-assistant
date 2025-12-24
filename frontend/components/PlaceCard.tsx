'use client'

interface Place {
  name: string
  address: string
  place_id: string
  lat: number
  lng: number
  rating?: number
  user_ratings_total?: number
  distance?: string
  walk_time?: string
  bike_time?: string
  drive_time?: string
  recommended_transport?: string
  maps_url: string
}

interface PlaceCardProps {
  place: Place
  userLocation?: { lat: number; lng: number }
}

export default function PlaceCard({ place, userLocation }: PlaceCardProps) {
  const getDirectionsUrl = () => {
    if (!userLocation) return place.maps_url
    
    return `https://www.google.com/maps/dir/?api=1&origin=${userLocation.lat},${userLocation.lng}&destination=${place.lat},${place.lng}&destination_place_id=${place.place_id}`
  }

  const getTransportIcon = (mode: string) => {
    switch (mode) {
      case 'walk': return '🚶'
      case 'bike': return '🚴'
      case 'drive': return '🚗'
      default: return '🚶'
    }
  }

  const getTransportLabel = (mode: string) => {
    switch (mode) {
      case 'walk': return 'Walking'
      case 'bike': return 'Biking'
      case 'drive': return 'Driving'
      default: return 'Walking'
    }
  }

  return (
    <div className="bg-dark-surface border border-dark-border rounded-xl p-6 
                  hover:border-accent/50 transition-all duration-200
                  hover:shadow-lg hover:shadow-accent/5">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-text-primary mb-1">
            {place.name}
          </h3>
          <p className="text-sm text-text-secondary">
            {place.address}
          </p>
        </div>
        {place.rating && (
          <div className="flex items-center gap-1 ml-4">
            <span className="text-yellow-400">★</span>
            <span className="text-text-primary font-medium">{place.rating}</span>
            {place.user_ratings_total && (
              <span className="text-text-muted text-sm">
                ({place.user_ratings_total})
              </span>
            )}
          </div>
        )}
      </div>

      {place.distance && (
        <div className="mb-4 pb-4 border-b border-dark-border">
          <p className="text-sm text-text-muted mb-2">Distance: {place.distance}</p>
          <div className="flex gap-3 text-sm">
            {place.walk_time && (
              <div className={`flex items-center gap-1 ${
                place.recommended_transport === 'walk' 
                  ? 'text-accent font-medium' 
                  : 'text-text-secondary'
              }`}>
                🚶 {place.walk_time}
              </div>
            )}
            {place.bike_time && (
              <div className={`flex items-center gap-1 ${
                place.recommended_transport === 'bike' 
                  ? 'text-accent font-medium' 
                  : 'text-text-secondary'
              }`}>
                🚴 {place.bike_time}
              </div>
            )}
            {place.drive_time && (
              <div className={`flex items-center gap-1 ${
                place.recommended_transport === 'drive' 
                  ? 'text-accent font-medium' 
                  : 'text-text-secondary'
              }`}>
                🚗 {place.drive_time}
              </div>
            )}
          </div>
        </div>
      )}

      {place.recommended_transport && (
        <div className="mb-4">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 
                        bg-accent/10 border border-accent/30 rounded-lg">
            <span className="text-lg">
              {getTransportIcon(place.recommended_transport)}
            </span>
            <span className="text-sm text-accent font-medium">
              Recommended: {getTransportLabel(place.recommended_transport)}
            </span>
          </div>
        </div>
      )}

      <div className="flex gap-3">
        <a
          href={getDirectionsUrl()}
          target="_blank"
          rel="noopener noreferrer"
          className="flex-1 px-4 py-2 bg-accent text-white rounded-lg
                   hover:bg-blue-600 active:bg-blue-700
                   text-center text-sm font-medium
                   transition-colors duration-200"
        >
          Get Directions
        </a>
        <a
          href={place.maps_url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 border border-dark-border rounded-lg
                   hover:border-accent/50 hover:bg-dark-border/50
                   text-center text-sm font-medium text-text-secondary
                   transition-all duration-200"
        >
          View on Map
        </a>
      </div>
    </div>
  )
}
