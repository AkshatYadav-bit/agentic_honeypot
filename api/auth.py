from fastapi import Header, HTTPException
import os

# In production, load from env
API_KEY = os.getenv("HONEYPOT_API_KEY", "CHANGE_ME")


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
