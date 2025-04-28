from transformers import pipeline
from fastapi.concurrency import run_in_threadpool

# Initialize the sentiment-analysis pipeline once (downloads on first run)
_sentiment_pipe = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

async def analyze_sentiments(texts: list[str]) -> list[int]:
    """
    Analyze a batch of review texts and return sentiment scores (1 to 5).
    Runs the HuggingFace pipeline in a threadpool to avoid blocking the FastAPI event loop.
    """
    results = await run_in_threadpool(_sentiment_pipe, texts)

    scores: list[int] = []
    for res in results:
        label = res.get("label", "")
        try:
            score = int(label.split()[0])
        except Exception:
            score = 3  # fallback to neutral
        scores.append(score)

    return scores