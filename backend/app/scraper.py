from google_play_scraper import search, reviews, Sort
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool

async def search_apps(name: str, n_results: int = 10) -> list[dict]:
    """
    Return up to `n_results` matching apps for autocomplete.
    Each dict has 'appId' and 'title'.
    """
    results = await run_in_threadpool(
        search,
        name,
        n_hits=n_results,
        lang='en',
        country='us'
    )
    return [{"appId": r["appId"], "title": r["title"]} for r in results]


async def fetch_app_id(app_name: str, n_results: int = 5) -> str:
    """
    Search by human-readable name and return the top match's package ID.
    Raises 404 if nothing is found.
    """
    apps = await run_in_threadpool(
        search,
        app_name,
        n_hits=n_results,
        lang='en',
        country='us'
    )
    if not apps:
        raise HTTPException(status_code=404, detail="No matching app found")
    return apps[0]["appId"]


async def fetch_reviews_for_app(app_id: str, count: int = 100) -> list[str]:
    """
    Fetch the latest `count` reviews for the given package ID,
    returning just the review text.
    """
    result, _ = await run_in_threadpool(
        reviews,
        app_id,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=count
    )
    return [r["content"] for r in result]