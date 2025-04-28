from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .scraper import search_apps, fetch_app_id, fetch_reviews_for_app
from .sentiment import analyze_sentiments

class AnalyzeRequest(BaseModel):
    appName: str

app = FastAPI(
    title="Google Play Sentiment Analyzer",
    description="Fetches latest reviews for an Android app and computes average sentiment.",
)

# Allow our Next.js frontend (or any localhost client) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/suggest-app")
async def suggest_app(name: str, limit: int = 10):
    """
    Autocomplete endpoint: returns up to `limit` apps matching `name`.
    """
    results = await search_apps(name, n_results=limit)
    return {"results": results}


@app.post("/analyze-reviews")
async def analyze_reviews(req: AnalyzeRequest):
    """
    Given {"appName": "..."}:
    1. Resolve to a package ID
    2. Fetch 100 most recent reviews
    3. Analyze sentiments (scores 1–5)
    4. Return average score and review count
    """
    try:
        app_id = await fetch_app_id(req.appName)
    except HTTPException:
        raise HTTPException(status_code=404, detail=f"App not found: {req.appName}")

    reviews = await fetch_reviews_for_app(app_id, count=100)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this app")
    
    scores = await analyze_sentiments(reviews)

    average = sum(scores) / len(scores)
    return {
        "average_score": round(average, 2),
        "review_count": len(scores)
    }