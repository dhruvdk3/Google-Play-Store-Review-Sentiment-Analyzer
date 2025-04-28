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


Markup : * Unofficial Scraping : google-play-scraper, which depends on Google’s HTML structure—can break if Google updates their site.
          * Throttling
          * Bullet list item 2
          * Bullet list item 2
          * Bullet list item 2
          * Bullet list item 2

	2.	
	•	Too many requests to Google Play may get throttled or blocked.
	•	No retry or IP-rotation implemented.
	3.	Regional Limitations
	•	Reviews fetched are US/English-only (hardcoded); results can differ by region or language.
	4.	Recent Reviews Only
	•	Fetches only the latest 100 reviews; does not reflect historical sentiment.
	5.	Model Accuracy
	•	Sentiment model (nlptown/bert-base-multilingual-uncased-sentiment) may miss nuances like sarcasm, slang, or emojis.
	•	Provides only a general sentiment rating (1–5).
	6.	Performance
	•	Runs sentiment analysis locally; can become slow if scaled beyond current scope.
	•	No GPU or performance optimizations implemented.
	7.	No Caching
	•	Results aren’t cached; repeated requests re-fetch and re-analyze each time.
	8.	No Security Measures
	•	Backend API lacks authentication or rate limits—currently open for unrestricted access.