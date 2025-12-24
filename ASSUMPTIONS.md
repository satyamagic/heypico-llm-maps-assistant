# Assumptions & Design Decisions

## Location Handling

### User Location
- **Primary Method**: Browser Geolocation API
  - Requests permission from user on first query
  - Provides accurate real-time coordinates
  - Required for distance/duration calculations

- **Fallback Method**: LLM-extracted location
  - Used when geolocation is unavailable or denied
  - Less accurate but functional
  - Places will still be found, but without distance/duration data

- **Privacy**: User location is never stored or persisted
  - Only used for the current query session
  - Sent to backend only for distance calculations
  - Not logged or saved in any database

### Location Parsing
- LLM extracts location from natural language
- Geocoded by Google Maps API to get coordinates
- Default location: "Jakarta" if not specified

## Transport Recommendation Logic

### Thresholds
Based on practical urban mobility patterns:

- **Walking**: Recommended if ≤ 7 minutes
  - Comfortable walking distance in tropical climate
  - No additional cost
  - Good for short distances

- **Biking**: Recommended if ≤ 10 minutes (and walking > 7 min)
  - Fast and eco-friendly
  - Practical for medium distances
  - Assumes bike-sharing availability

- **Driving**: Recommended if > 10 minutes biking
  - For longer distances
  - Includes ride-hailing options
  - Most convenient for time-sensitive trips

### Calculation Method
- Uses Google Distance Matrix API for accurate real-world times
- Considers traffic patterns
- Accounts for road networks and walking paths

## API Rate Limits & Quotas

### Google Maps API
- **Assumed Free Tier Usage**: 
  - Places API: ~17,000 requests/month free
  - Distance Matrix API: ~40,000 elements/month free
  - Embed API: Unlimited with proper key restrictions

- **Mitigation Strategies**:
  - Limit to 5 places per query (reduces Distance Matrix calls)
  - No pagination or infinite scroll
  - Results cached in memory for single session
  - No background/automatic refreshes

### Ollama/LLM
- **Local Model**: No rate limits
- **Timeout**: 30 seconds per query
- **Fallback**: Simple regex-based extraction if LLM fails

## LLM Selection

### Recommended Model: Llama 3.2
- **Why?**
  - Excellent structured output capability
  - Lightweight and fast
  - Good at following JSON format instructions
  - Available via Ollama

- **Alternative Models**:
  - Mistral 7B: Faster, slightly less accurate
  - Phi-3: Very lightweight, good for low-spec systems
  - Llama 3.1: More powerful, slower

### JSON Enforcement
- Uses Ollama's `format: "json"` parameter
- Strict system prompt with examples
- Fallback parser for non-JSON responses
- Validation with Pydantic schemas

## Error Handling & Fallbacks

### LLM Failures
- **Fallback**: Simple keyword extraction
  - Extracts common food types (ramen, pizza, coffee, etc.)
  - Default location: Jakarta
  - Always returns valid structure

### API Failures
- **No Places Found**: 
  - Returns friendly message
  - Suggests trying different location
  - No map shown

- **Distance Matrix Failures**:
  - Places still shown without distance/time
  - No transport recommendation
  - Direct links to Google Maps still work

- **Geolocation Denied**:
  - App continues to work
  - Uses LLM-extracted location only
  - Shows places without personalized distances

## Security Considerations

### API Keys
- **Backend Keys**: Stored in environment variables only
  - Never exposed to client
  - Loaded via python-dotenv
  - Example files provided for setup

- **Frontend Keys**: 
  - Embed API key is client-safe (with proper restrictions)
  - Restricted to specific domains in Google Cloud Console
  - Separate from backend API key

### CORS
- Configured explicitly for frontend origin
- Default: `http://localhost:3000`
- Configurable via environment variable

### Input Validation
- Pydantic models validate all inputs
- Query length limits enforced
- No SQL or code injection vectors (no database)

## Performance Considerations

### Response Times
- **LLM**: ~2-5 seconds (local Ollama)
- **Places API**: ~500ms
- **Distance Matrix**: ~800ms
- **Total Expected**: 3-6 seconds

### Optimization Strategies
- Async/await throughout
- Parallel API calls where possible
- Limited results (5 places max)
- No unnecessary data transfer

## Browser Compatibility

### Minimum Requirements
- Modern browser with ES6+ support
- Geolocation API support (optional)
- Fetch API support

### Tested On
- Chrome 100+
- Firefox 90+
- Safari 14+
- Edge 100+

## Mobile Considerations

### Responsive Design
- Mobile-first Tailwind CSS
- Touch-friendly buttons
- Readable text sizes
- Collapsible sections

### Geolocation
- More accurate on mobile devices
- Better user experience with GPS
- Fallback still works without permissions

## Data Privacy

### No User Tracking
- No analytics
- No cookies
- No user accounts
- No data persistence

### Temporary Data
- Query results stored in component state only
- Cleared on page refresh
- Not shared with third parties

## Future Enhancements (Out of Scope)

### Not Implemented
- User authentication
- Saved searches or favorites
- Multi-language support
- Offline mode
- Push notifications
- Social sharing
- Reviews and ratings submission
- Route optimization for multiple stops
- Public transit information
- Real-time traffic updates

These were excluded to maintain focus on core AI-to-tool automation demonstration.
