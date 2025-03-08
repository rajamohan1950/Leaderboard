
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Redis
#r = redis.Redis(host='localhost', port=6379, decode_responses=True)

REDIS_URL = os.getenv("REDIS_URL", "redis://default:yourpassword@your-upstash-url:6379")
r = redis.Redis.from_url(REDIS_URL)


# Model for leaderboard entry
class ScoreEntry(BaseModel):
    user: str
    score: int

# Add score to leaderboard
@app.post("/submit")
def submit_score(entry: ScoreEntry):
    r.zadd("leaderboard", {entry.user: entry.score})
    return {"message": "Score submitted"}

# Get top N players
@app.get("/top/{count}")
def get_top_scores(count: int):
    top_scores = r.zrevrange("leaderboard", 0, count - 1, withscores=True)
    return [{"user": user, "score": int(score)} for user, score in top_scores]

# Reset leaderboard (Admin only)
@app.delete("/reset")
def reset_leaderboard():
    r.delete("leaderboard")
    return {"message": "Leaderboard reset"}

