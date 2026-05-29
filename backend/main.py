from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from database import (
    initialize_db, register_user, check_login,
    get_all_problems, add_problem, problem_exists, update_problem_confidence, delete_problem,
    search_problems_by_pattern, search_problems_by_title, search_problems_by_confidence
)
from leetcode_sync import sync_user_problems
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_default_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For localhost dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

class SyncRequest(BaseModel):
    leetcode_username: str
    limit: Optional[int] = 20

class UpdateRequest(BaseModel):
    slug: str
    pattern: Optional[str] = ""
    notes: Optional[str] = ""
    confidence: Optional[int] = 0

class RegisterRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_username(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

@app.on_event("startup")
def startup_event():
    initialize_db()

@app.post("/register")
def register(req: RegisterRequest):
    success, msg = register_user(req.username, req.password)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"msg": msg}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not check_login(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/sync")
def sync(sync_req: SyncRequest, username: str = Depends(get_current_username)):
    sync_user_problems(username, sync_req.leetcode_username, sync_req.limit)
    return {"message": f"Synced recent problems for username={username} from LeetCode={sync_req.leetcode_username}."}

@app.get("/problems")
def get_problems(username: str = Depends(get_current_username)):
    rows = get_all_problems(username)
    def row_to_dict(row):
        return {
            "id": row[0], "username": row[1], "problem_id": row[2], "title": row[3],
            "slug": row[4], "timestamp": row[5], "pattern": row[6], "notes": row[7], "confidence": row[8]
        }
    return [row_to_dict(row) for row in rows]

@app.put("/update")
def update_problem(req: UpdateRequest, username: str = Depends(get_current_username)):
    if not problem_exists(username, req.slug):
        raise HTTPException(status_code=404, detail="Problem not found.")
    update_problem_confidence(username, req.slug, req.pattern, req.notes, req.confidence)
    return {"message": f"Updated problem '{req.slug}'."}

@app.delete("/delete/{slug}")
def delete_problem_route(slug: str, username: str = Depends(get_current_username)):
    if not problem_exists(username, slug):
        raise HTTPException(status_code=404, detail="Problem not found.")
    delete_problem(username, slug)
    return {"message": f"Deleted problem '{slug}'."}

@app.get("/search")
def search(pattern: Optional[str] = None, title: Optional[str] = None, confidence: Optional[int] = None, username: str = Depends(get_current_username)):
    results = []
    if pattern:
        results.extend(search_problems_by_pattern(username, pattern))
    if title:
        results.extend(search_problems_by_title(username, title))
    if confidence is not None:
        results.extend(search_problems_by_confidence(username, confidence))
    # Remove duplicates by slug
    unique = {}
    def row_to_dict(row):
        return {
            "id": row[0], "username": row[1], "problem_id": row[2], "title": row[3],
            "slug": row[4], "timestamp": row[5], "pattern": row[6], "notes": row[7], "confidence": row[8]
        }
    for row in results:
        unique[row[4]] = row_to_dict(row)
    return list(unique.values())