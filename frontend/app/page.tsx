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

  // Get user location on first load
  const getUserLocation = (): Promise<{ lat: number; lng: number } | null> => {
    return new Promise((resolve) => {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const location = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            }
            setUserLocation(location)
            resolve(location)
          },
          (error) => {
            console.log('Geolocation error:', error)
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

          {/* Map View */}
          {response.places.length > 0 && mapsApiKey && (
            <div className="mt-8">
              <h3 className="text-xl font-semibold text-text-primary mb-4">
                View on Map
              </h3>
              <MapView places={response.places} apiKey={mapsApiKey} />
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
                'Where can I eat ramen near Blok M?',
                'Find coffee shops in Menteng',
                'Best pizza places in Sudirman',
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
