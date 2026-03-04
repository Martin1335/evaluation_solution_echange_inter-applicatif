from fastapi import Header, HTTPException

SECRET_TOKEN = "TOKEN_SECRET"

def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Non autorisé")