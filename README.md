## Google Play Store Review Sentiment Analyzer

A simple web app that fetches the 100 most recent Google Play reviews for a given Android app, runs sentiment analysis locally using a HuggingFace model, and displays the average sentiment score.

### Features

- **Autocomplete** of app names via Play Store search.  
- **Review scraping** of the 100 newest reviews using `google-play-scraper`  
- **Sentiment analysis** with `nlptown/bert-base-multilingual-uncased-sentiment`
- **Average score** and review count displayed. 
- **Legend** explaining what each score (1–5) means

### Tech Stack

- **Backend**: FastAPI, Uvicorn, google-play-scraper, Transformers & PyTorch  
- **Frontend**: Next.js, React  

### Sentiment Analysis Model

We use the Hugging Face Transformers pipeline with the **`nlptown/bert-base-multilingual-uncased-sentiment`** model for local sentiment inference.


### Installation

```bash
# Clone the repo
git clone https://github.com/dhruvdk3/Google-Play-Store-Review-Sentiment-Analyzer.git
cd google-play-sentiment-analyzer
```

## Backend ##

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The backend API will now be available at http://localhost:8000


## Frontend ##
```bash
cd frontend
npm install
npm run dev
```
The frontend UI will now be available at http://localhost:3000.





## API Endpoints ##
- GET /suggest-app?name=<query>&limit=<num>
Returns up to <limit> matching apps for autocomplete:
```bash
{ "results": [{ "appId": "...", "title": "..." }, …] }
```

- POST /analyze-reviews
Request body:
```bash
{ "appName": "Google Chrome" }
```

Response:

```bash
{
    "average_score":3.53,
    "review_count":100
}
```



## Backend Check ##
Now to check if the Backend is running properly we call for API to fetch the 5 keyword relevent the the Passed named in the structure mentioned.
```bash
curl "http://localhost:8000/suggest-app?name=Chrome&limit=5"
```
Then we will call for POST to get out response
```bash
curl -X POST http://localhost:8000/analyze-reviews \
     -H "Content-Type: application/json" \
     -d '{"appName":"Google Chrome"}'
```
These both should give a 200 OK Response in the termina

### Play Store Data Access

1. __Choosing the Data Source__ : Google’s Play Developer API only surfaces limited metadata and doesn’t expose full user review text without publishing credentials and options like SerpAPI or Apify exist, but they introduce ongoing costs and lock us into external SLAs. So the best decision was to go with __scraping__—it’s free, gives direct access to all review text, and keeps us in full control of the pipeline.

2. __Picking a Scraper Library__ : We evaluated raw HTTP+BeautifulSoup vs. community tools. And __google-play-scraper__ (JoMingyu) stood out: zero-config, supports search & review endpoints, and is battle-tested by thousands of projects. This saves hundreds of lines of custom parsing, auto-retries basic errors, and handles pagination out of the box.

3. __Resolving App Names → Package IDs__ : Play Store URLs are indexed by package ID (`com.example.app`), not human names. So we used `search(appName, n_hits=…)` from the library to map "Google Chrome" → `com.android.chrome`. By automating this lookup, users can type colloquial names and still get precise results.

4. __Fetching the 100 Most Recent Reviews__ : Library’s `reviews(appId, sort=Sort.NEWEST, count=100)` taps into Google’s undocumented JSON endpoints. We extract only the `content` field (review text) because that’s all our sentiment model needs.  

5. __Concurrent, Rate-Limited Processing__  : We wrap each single-review inference in an `asyncio.Semaphore(MAX_CONCURRENT)` and insert a small `await asyncio.sleep(delay)` between completions. This Keeps our pipeline responsive (non-blocking FastAPI), avoids hammering Google, and spreads load evenly across CPU/IO.

6. __Local Sentiment Inference__: We chose the `nlptown/bert-base-multilingual-uncased-sentiment` model via Hugging Face Transformers for offline inference. Because its cost-free & private(no API calls or data leakage) and has multilingual support. But it has a larger download (~400 MB) and CPU-bound performance.



### Limitations

1. __Unofficial Scraping__ : google-play-scraper, which depends on Google’s HTML structure—can break if Google updates their site.
2. __Throttling__  : Too many requests to Google Play may get throttled or blocked also for this there is no retry or IP-rotation implemented.
3.	__Regional Limitations__ : Reviews fetched are US/English-only (hardcoded); results can differ by region or language.
4.	__Model Accuracy__ : Sentiment model (nlptown/bert-base-multilingual-uncased-sentiment) may miss nuances like sarcasm, slang, or emojis.
5.	__No Caching__ : Results aren’t cached; repeated requests re-fetch and re-analyze each time.


<video controls width="600">
  <source src="https://github.com/dhruvdk3/Google-Play-Store-Review-Sentiment-Analyzer/blob/main/Demo/Demo.mp4?raw=true" type="video/mp4">
</video>
