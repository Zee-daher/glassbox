# main.py — exposes the knowledge-based engine as an HTTP service

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from engine import infer

app = FastAPI(title="GlassBox AI — Explainable Game AI")

class Situation(BaseModel):
    enemy_hp: int = 100
    enemies_nearby: int = 0
    player_distance: float = 999
    escape_route_open: bool = True

@app.get("/")
def health():
    return {"status": "GlassBox AI is running"}

@app.post("/decide")
def decide(situation: Situation):
    facts = situation.model_dump()
    return infer(facts)

# serve the web demo (the "static" folder) at /ui
app.mount("/ui", StaticFiles(directory="static", html=True), name="ui")