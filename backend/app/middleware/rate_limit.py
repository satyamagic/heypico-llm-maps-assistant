"""
Rate limiting middleware to protect API endpoints
"""
from fastapi import Request, HTTPException
from collections import defaultdict
import time
from typing import Dict, Tuple

# In-memory store: {ip: (request_count, window_start_time)}
request_store: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, time.time()))

# Configuration
RATE_LIMIT_REQUESTS = 20  # requests per window
RATE_LIMIT_WINDOW = 60  # seconds

async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limit requests per IP address
    
    Limits: 20 requests per 60 seconds per IP
    """
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)
    
    # Get client IP
    client_ip = request.client.host
    
    # Get current window data
    current_time = time.time()
    count, window_start = request_store[client_ip]
    
    # Reset window if expired
    if current_time - window_start > RATE_LIMIT_WINDOW:
        request_store[client_ip] = (1, current_time)
        return await call_next(request)
    
    # Check if limit exceeded
    if count >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds."
        )
    
    # Increment counter
    request_store[client_ip] = (count + 1, window_start)
    
    return await call_next(request)
