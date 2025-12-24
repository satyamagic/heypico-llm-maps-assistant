'use client'

interface Place {
  name: string
  lat: number
  lng: number
  place_id: string
}

interface MapViewProps {
  places: Place[]
  apiKey?: string
}

export default function MapView({ places, apiKey }: MapViewProps) {
  if (!apiKey || places.length === 0) {
    return null
  }

  // Calculate center point
  const centerLat = places.reduce((sum, p) => sum + p.lat, 0) / places.length
  const centerLng = places.reduce((sum, p) => sum + p.lng, 0) / places.length

  // Build markers query string
  const markers = places
    .map(p => `markers=color:red%7Clabel:${places.indexOf(p) + 1}%7C${p.lat},${p.lng}`)
    .join('&')

  const mapUrl = `https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${centerLat},${centerLng}&zoom=14&${markers}`

  return (
    <div className="w-full h-96 rounded-xl overflow-hidden border border-dark-border">
      <iframe
        width="100%"
        height="100%"
        style={{ border: 0 }}
        loading="lazy"
        allowFullScreen
        referrerPolicy="no-referrer-when-downgrade"
        src={mapUrl}
      />
    </div>
  )
}
