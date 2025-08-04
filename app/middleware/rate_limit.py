from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from collections import defaultdict, deque
from typing import Dict, Deque

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)
        self.limits = {
            "auth": {"requests": 5, "window": 60},  # 5 requests per minute for auth
            "api": {"requests": 100, "window": 60},  # 100 requests per minute for API
            "sync": {"requests": 10, "window": 300}  # 10 sync requests per 5 minutes
        }
    
    def is_allowed(self, key: str, limit_type: str = "api") -> bool:
        """Check if request is allowed based on rate limits"""
        now = time.time()
        limit_config = self.limits.get(limit_type, self.limits["api"])
        
        # Clean old requests outside the window
        while (self.requests[key] and 
               now - self.requests[key][0] > limit_config["window"]):
            self.requests[key].popleft()
        
        # Check if under limit
        if len(self.requests[key]) < limit_config["requests"]:
            self.requests[key].append(now)
            return True
        
        return False
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host

rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next, limit_type: str = "api"):
    """Rate limiting middleware"""
    client_ip = rate_limiter.get_client_ip(request)
    
    if not rate_limiter.is_allowed(client_ip, limit_type):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )
    
    response = await call_next(request)
    return response