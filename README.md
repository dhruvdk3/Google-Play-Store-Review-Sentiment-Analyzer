## Google Play Store Review Sentiment Analyzer

A simple web app that fetches the 100 most recent Google Play reviews for a given Android app, runs sentiment analysis locally using a HuggingFace model, and displays the average sentiment score.

### Features

- <mark>Autocomplete</mark> of app names via Play Store search  
- **Review scraping** of the 100 newest reviews using `google-play-scraper`  
- **Sentiment analysis** with `nlptown/bert-base-multilingual-uncased-sentiment` (local inference)  
- **Average score** and review count displayed in a friendly UI  
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





API Endpoints
• GET /suggest-app?name=<query>&limit=<num>
Returns up to <limit> matching apps for autocomplete:
```bash
{ "results": [{ "appId": "...", "title": "..." }, …] }
```

•POST /analyze-reviews
Request body:

{ "appName": "Google Chrome" }

Response:

```bash
{
    "average_score":3.53,
    "review_count":100
}
```