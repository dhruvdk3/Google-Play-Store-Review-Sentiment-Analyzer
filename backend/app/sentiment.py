import asyncio
from transformers import pipeline
from fastapi.concurrency import run_in_threadpool

# Instantiate once
_sentiment_pipe = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

MAX_CONCURRENT = 5
BATCH_DELAY = 0.2

async def analyze_sentiments(texts: list[str]) -> list[int]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async def analyze_one(text: str):
        async with sem:
            res = await run_in_threadpool(_sentiment_pipe, text)
            label = res[0].get("label", "3")
            return int(label.split()[0])

    tasks = [asyncio.create_task(analyze_one(t)) for t in texts]
    scores = []

    for task in asyncio.as_completed(tasks):
        score = await task
        scores.append(score)
        await asyncio.sleep(BATCH_DELAY)

    return scores