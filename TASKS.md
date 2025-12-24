# HeyPico AI Maps LLM - Development Tasks

## Phase 1: Project Setup & Foundation
- [x] Create TASKS.md
- [ ] Set up root-level .gitignore
- [ ] Create backend directory structure
- [ ] Create frontend directory structure
- [ ] Create .env.example files

## Phase 2: Backend - FastAPI Foundation
- [ ] Initialize FastAPI app with CORS
- [ ] Set up Pydantic schemas for request/response
- [ ] Create routers structure
- [ ] Implement health check endpoint
- [ ] Configure environment variable loading

## Phase 3: Backend - LLM Integration
- [ ] Create llm_service.py for Open WebUI integration
- [ ] Implement async LLM query function
- [ ] Add JSON parsing and validation
- [ ] Handle LLM errors and fallbacks
- [ ] Test structured output extraction

## Phase 4: Backend - Google Maps Integration
- [ ] Create google_maps_service.py
- [ ] Implement Places API text search
- [ ] Implement Places API nearby search (fallback)
- [ ] Add error handling for API limits
- [ ] Test with various location queries

## Phase 5: Backend - Distance Matrix & Transport Logic
- [ ] Implement Distance Matrix API calls
- [ ] Calculate distances for multiple places
- [ ] Implement transport recommendation logic:
  - Walking ≤ 7 min → walk
  - Biking ≤ 10 min → bike
  - Else → drive
- [ ] Handle missing/invalid distance data
- [ ] Return structured place data with recommendations

## Phase 6: Backend - API Routers
- [ ] Create /api/query endpoint
- [ ] Integrate LLM + Google Maps + Distance Matrix
- [ ] Add request validation
- [ ] Add response formatting
- [ ] Test end-to-end flow

## Phase 7: Frontend - Next.js Foundation
- [ ] Initialize Next.js with App Router
- [ ] Configure Tailwind CSS with dark theme
- [ ] Set up custom color palette
- [ ] Create root layout with dark background
- [ ] Configure environment variables

## Phase 8: Frontend - Core Components
- [ ] Create ChatInput component with dark styling
- [ ] Create PlaceCard component with transport badges
- [ ] Create MapView component with Google Maps Embed
- [ ] Create LoadingState component
- [ ] Create ErrorMessage component

## Phase 9: Frontend - Main Page Logic
- [ ] Implement user input handling
- [ ] Add geolocation API integration
- [ ] Call backend /api/query endpoint
- [ ] Display AI response text
- [ ] Render place cards with results
- [ ] Show embedded map with pins

## Phase 10: Frontend - UX Enhancements
- [ ] Add loading skeletons
- [ ] Implement smooth transitions
- [ ] Add hover effects on cards
- [ ] Highlight recommended transport option
- [ ] Add "Open in Google Maps" buttons
- [ ] Test responsive layout

## Phase 11: Security & Environment
- [ ] Create backend/.env.example
- [ ] Create frontend/.env.example
- [ ] Update .gitignore files
- [ ] Verify API keys are server-side only
- [ ] Test with dummy environment variables

## Phase 12: Documentation
- [ ] Write ASSUMPTIONS.md
  - Location handling strategy
  - Transport recommendation thresholds
  - API rate limits
  - Fallback behavior
- [ ] Write comprehensive README.md
  - Architecture diagram
  - Data flow explanation
  - Setup instructions
  - Security considerations
- [ ] Add inline code comments
- [ ] Create API documentation

## Phase 13: Testing & Polish
- [ ] Test with various queries
- [ ] Verify error handling
- [ ] Check edge cases (no results, invalid location)
- [ ] Validate dark theme consistency
- [ ] Final code review

## Phase 14: Deployment Preparation
- [ ] Add requirements.txt for backend
- [ ] Add package.json scripts
- [ ] Document local setup steps
- [ ] Document LLM setup (Ollama + Open WebUI)
- [ ] Final integration test
