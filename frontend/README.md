# Frontend README

## HeyPico AI Maps Frontend

Next.js frontend for AI-powered location search interface.

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file:
```bash
cp .env.example .env.local
```

3. Configure environment variables:
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_GOOGLE_MAPS_EMBED_API_KEY`: Google Maps Embed API key

### Running the App

Development mode:
```bash
npm run dev
```

Build for production:
```bash
npm run build
npm start
```

App will be available at: http://localhost:3000

## Features

- **Chat Interface**: Natural language input for location queries
- **AI Responses**: Conversational responses with place recommendations
- **Place Cards**: Detailed information with ratings and transport options
- **Transport Recommendations**: Highlighted best transport mode (walk/bike/drive)
- **Distance & Duration**: Real-time calculations for all transport modes
- **Google Maps Integration**: Embedded map view and directions
- **Geolocation**: Automatic user location detection
- **Dark Theme**: Professional dark UI optimized for developers

## Architecture

### Components
- `ChatInput`: Search input with submit handling
- `PlaceCard`: Individual place display with transport info
- `MapView`: Embedded Google Maps with place pins
- `LoadingSkeleton`: Loading state animation

### Page Flow
1. User enters natural language query
2. Browser geolocation API captures user location
3. Frontend calls backend `/api/query` endpoint
4. Backend returns AI response + structured places
5. Frontend displays results with map
