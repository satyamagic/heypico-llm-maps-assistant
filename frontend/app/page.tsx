'use client'

import { useState } from 'react'
import ChatInput from '@/components/ChatInput'
import PlaceCard from '@/components/PlaceCard'
import MapView from '@/components/MapView'
import LoadingSkeleton from '@/components/LoadingSkeleton'

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

interface QueryResponse {
  ai_response: string
  places: Place[]
  user_location?: { lat: number; lng: number }
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [response, setResponse] = useState<QueryResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null)
  const [locationName, setLocationName] = useState<string | null>(null)
  const [locationLoading, setLocationLoading] = useState(false)

  // Get user location on first load
  const getUserLocation = (): Promise<{ lat: number; lng: number } | null> => {
    return new Promise((resolve) => {
      if ('geolocation' in navigator) {
        setLocationLoading(true)
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const location = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            }
            setUserLocation(location)
            
            // Reverse geocode to get city name via backend
            try {
              const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
              const response = await fetch(`${apiUrl}/api/geocode`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  lat: location.lat,
                  lng: location.lng,
                }),
              })
              
              if (response.ok) {
                const data = await response.json()
                setLocationName(data.city)
              }
            } catch (err) {
              console.log('Geocoding error:', err)
            }
            
            setLocationLoading(false)
            resolve(location)
          },
          (error) => {
            console.log('Geolocation error:', error)
            setLocationLoading(false)
            resolve(null)
          }
        )
      } else {
        resolve(null)
      }
    })
  }

  const handleQuery = async (query: string) => {
    setIsLoading(true)
    setError(null)

    try {
      // Get user location if not already available
      let location = userLocation
      if (!location) {
        location = await getUserLocation()
      }

      // Call backend API
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const res = await fetch(`${apiUrl}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          user_lat: location?.lat,
          user_lng: location?.lng,
        }),
      })

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: 'An error occurred' }))
        throw new Error(errorData.detail || 'Failed to process query')
      }

      const data: QueryResponse = await res.json()
      setResponse(data)
    } catch (err) {
      console.error('Query error:', err)
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const mapsApiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_EMBED_API_KEY

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="text-center space-y-4 py-8">
        <h2 className="text-3xl font-semibold text-text-primary">
          Find Places with AI
        </h2>
        <p className="text-text-secondary max-w-2xl mx-auto">
          Ask where you want to go, and we'll find the best places with intelligent transport recommendations
        </p>
        
        {/* User Location Display */}
        {locationLoading && (
          <div className="flex items-center justify-center gap-2 text-sm text-text-muted">
            <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Detecting your location...
          </div>
        )}
        {userLocation && locationName && !locationLoading && (
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-dark-surface border border-dark-border rounded-full text-sm">
            <span className="text-2xl">📍</span>
            <span className="text-text-secondary">Your location:</span>
            <span className="text-accent font-medium">{locationName}</span>
            <button
              onClick={() => getUserLocation()}
              className="ml-2 text-text-muted hover:text-accent transition-colors"
              title="Refresh location"
            >
              🔄
            </button>
          </div>
        )}
        {!userLocation && !locationLoading && (
          <button
            onClick={() => getUserLocation()}
            className="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 border border-accent/30 rounded-full text-sm text-accent hover:bg-accent/20 transition-colors"
          >
            <span className="text-xl">📍</span>
            Enable Location for Better Results
          </button>
        )}
      </div>

      {/* Chat Input */}
      <div className="max-w-3xl mx-auto">
        <ChatInput onSubmit={handleQuery} isLoading={isLoading} />
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="max-w-5xl mx-auto">
          <LoadingSkeleton />
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="max-w-3xl mx-auto">
          <div className="bg-red-900/20 border border-red-700/50 rounded-xl p-4">
            <p className="text-red-400">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {response && !isLoading && (
        <div className="max-w-5xl mx-auto space-y-8">
          {/* AI Response */}
          <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
            <p className="text-text-primary text-lg">{response.ai_response}</p>
          </div>

          {/* Places Grid */}
          {response.places.length > 0 && (
            <div className="grid gap-4 md:grid-cols-2">
              {response.places.map((place, index) => (
                <PlaceCard
                  key={place.place_id || index}
                  place={place}
                  userLocation={response.user_location || userLocation || undefined}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!response && !isLoading && !error && (
        <div className="max-w-3xl mx-auto text-center py-12">
          <div className="text-6xl mb-4">🗺️</div>
          <p className="text-text-muted">
            Start by asking where you want to go
          </p>
          <div className="mt-6 space-y-2">
            <p className="text-sm text-text-muted">Try examples like:</p>
            <div className="flex flex-wrap gap-2 justify-center">
              {[
                locationName ? `Ramen near ${locationName}` : 'Where can I eat ramen near me?',
                locationName ? `Coffee shops in ${locationName}` : 'Find coffee shops near me',
                locationName ? `Best pizza in ${locationName}` : 'Best pizza places near me',
              ].map((example) => (
                <button
                  key={example}
                  onClick={() => handleQuery(example)}
                  className="px-4 py-2 bg-dark-surface border border-dark-border rounded-lg
                           hover:border-accent/50 hover:bg-dark-border/50
                           text-sm text-text-secondary
                           transition-all duration-200"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
