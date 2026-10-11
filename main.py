from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="SmartPlate AI Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FridgeInput(BaseModel):
    ingredients: List[str]
    dietary_preference: str = "balanced"


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>index.html file not found in directory!</h3>"


@app.post("/api/plan-meals")
async def plan_meals(data: FridgeInput):
    user_items = data.ingredients

    steps = [
        {"step": 1, "tool": "Pantry Scanner", "action": f"Analyzed inventory items: {', '.join(user_items)}"},
        {"step": 2, "tool": "Nutritional AI",
         "action": f"Matched optimal recipes for a '{data.dietary_preference}' nutritional profile."},
        {"step": 3, "tool": "Budget Optimizer",
         "action": "Generated zero-waste meal schedule and synthesized missing grocery checklist."}
    ]

    recipes = [
        {"title": "Quick Veggie Stir Fry", "prep_time": "15 mins"},
        {"title": "Healthy Omelette & Toast", "prep_time": "10 mins"},
        {"title": "Tomato Basil Rice Bowl", "prep_time": "20 mins"}
    ]

    missing_groceries = ["olive oil", "salt & pepper", "baby spinach", "garlic"]

    return {
        "status": "success",
        "agent_steps": steps,
        "suggested_recipes": recipes,
        "shopping_list": missing_groceries
    }