## Google Play Store Review Sentiment Analyzer

A simple web app that fetches the 100 most recent Google Play reviews for a given Android app, runs sentiment analysis locally using a HuggingFace model, and displays the average sentiment score.

### Features

- **Autocomplete** of app names (up to 5 suggestions) via Play Store search  
- **Review scraping** of the 100 newest reviews using `google-play-scraper`  
- **Sentiment analysis** with `nlptown/bert-base-multilingual-uncased-sentiment` (local inference)  
- **Average score** and review count displayed in a friendly UI  
- **Legend** explaining what each score (1–5) means  

### Tech Stack

- **Backend**: FastAPI, Uvicorn, google-play-scraper, Transformers & PyTorch  
- **Frontend**: Next.js, React  

### Prerequisites

- **Node.js** (v16+) & **npm**  
- **Python** (v3.8+)  
- Optional: GPU with MPS or CUDA for faster HF inference  

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/google-play-sentiment-analyzer.git
cd google-play-sentiment-analyzer

Backend

cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

Frontend

cd frontend
npm install

Running Locally
	1.	Start the backend

cd backend
source venv/bin/activate
uvicorn app.main:app --reload

The API will be available at http://localhost:8000.

	2.	Start the frontend (in a new terminal)

cd frontend
npm run dev

The web UI will be at http://localhost:3000.

API Endpoints
	•	GET /suggest-app?name=<query>&limit=<num>
Returns up to <limit> matching apps for autocomplete:

{ "results": [{ "appId": "...", "title": "..." }, …] }


	•	POST /analyze-reviews
Request body:

{ "appName": "Spotify" }

Response:

{
  "average_score": 4.23,
  "review_count": 100
}



Limitations & Notes
	•	Relies on an unofficial scraper; subject to Google Play throttling or schema changes.
	•	Model checkpoint (~400 MB) must download on first run.
	•	Analysis is done locally—consider using a hosted LLM API for higher throughput in production.
	•	Currently fetches a fixed 100 reviews; you can expose this as a parameter if desired.

⸻

Feel free to tweak or expand as needed! Once you’ve added this, the final step is to record a short screencast (30–60 s) showing:
	1.	Typing in an app name → selecting from autocomplete
	2.	Clicking “Analyze Reviews”
	3.	Viewing the average score + legend

Let me know when you’re ready to wrap up or if you’d like any adjustments.