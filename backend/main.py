from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from database import (
    initialize_db, get_all_problems, add_problem, problem_exists,
    update_problem_confidence, delete_problem, search_problems_by_pattern,
    search_problems_by_title, search_problems_by_confidence
)
from leetcode_sync import sync_user_problems

app = FastAPI()

class SyncRequest(BaseModel):
    username: str
    limit: Optional[int] = 20

class UpdateRequest(BaseModel):
    slug: str
    pattern: Optional[str] = ""
    notes: Optional[str] = ""
    confidence: Optional[int] = 0

def row_to_dict(row):
    return {
        "id": row[0],
        "problem_id": row[1],
        "title": row[2],
        "slug": row[3],
        "timestamp": row[4],
        "pattern": row[5],
        "notes": row[6],
        "confidence": row[7],
    }

@app.on_event("startup")
def startup_event():
    initialize_db()

@app.get("/")
def read_root():
    return {"msg": "LeetCode Tracker FastAPI backend is running."}

@app.post("/sync")
def sync(sync_req: SyncRequest):
    sync_user_problems(sync_req.username, sync_req.limit)
    return {"message": f"Synced recent problems for {sync_req.username}."}

@app.get("/problems")
def get_problems():
    rows = get_all_problems()
    return [row_to_dict(row) for row in rows]

@app.put("/update")
def update_problem(req: UpdateRequest):
    if not problem_exists(req.slug):
        raise HTTPException(status_code=404, detail="Problem not found.")
    update_problem_confidence(req.slug, req.pattern, req.notes, req.confidence)
    return {"message": f"Updated problem '{req.slug}'."}

@app.delete("/delete/{slug}")
def delete_problem_route(slug: str):
    if not problem_exists(slug):
        raise HTTPException(status_code=404, detail="Problem not found.")
    delete_problem(slug)
    return {"message": f"Deleted problem '{slug}'."}

@app.get("/search")
def search(pattern: Optional[str] = None,
           title: Optional[str] = None,
           confidence: Optional[int] = None):
    results = []
    if pattern:
        results.extend(search_problems_by_pattern(pattern))
    if title:
        results.extend(search_problems_by_title(title))
    if confidence is not None:
        results.extend(search_problems_by_confidence(confidence))
    # Remove duplicates by slug
    unique = {}
    for row in results:
        unique[row[3]] = row_to_dict(row)
    return list(unique.values())
