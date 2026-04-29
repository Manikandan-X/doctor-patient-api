from time import time
from fastapi import Request, HTTPException

# simple in-memory store
requests_log = {}

def rate_limiter(request: Request):
    ip = request.client.host
    now = time()

    window = 3   # seconds
    limit = 10    # allow 10 requests per 3 seconds

    if ip not in requests_log:
        requests_log[ip] = []

    # remove old requests
    requests_log[ip] = [
        t for t in requests_log[ip]
        if now - t < window
    ]

    if len(requests_log[ip]) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment."
        )

    requests_log[ip].append(now)