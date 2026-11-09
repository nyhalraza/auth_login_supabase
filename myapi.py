import os
from fastapi import FastAPI, HTTPException, Request, Header, Depends, Response
from dotenv import load_dotenv
from supabase import create_client
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from supabase_auth.errors import AuthApiError

load_dotenv()

app = FastAPI()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class Credentials(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={'error' : exc.detail})

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.post("/auth/signup", status_code=201)
def signup(creds: Credentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and Password Required")
    try:
        result = supabase.auth.sign_up({'email' : creds.email, 'password' : creds.password})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result.user.model_dump()

@app.post("/auth/login", status_code=200)
def login(creds: Credentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and Password Required")
    try:
        result = supabase.auth.sign_in_with_password({'email' : creds.email, 'password' : creds.password})
    except AuthApiError:
        raise HTTPException(status_code=401, detail="Invalid login credentials")
    return {"access_token": result.session.access_token, "refresh_token": result.session.refresh_token }

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Access token required")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(status_code=401, detail="Access token required")
    token = parts[1]

    try:
        result = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if result is None or result.user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return result.user

@app.get('/protected/profile')
def profile(user = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "created_at": user.created_at}

@app.get('/protected/dashboard')
def dashboard(user = Depends(get_current_user)):
    return {"message": f"Welcome {user.email}"}

@app.post("/auth/logout", status_code=204)
def logout(user = Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    return Response(status_code=204)

    
