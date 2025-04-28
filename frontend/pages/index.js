// frontend/pages/index.js

import { useState, useEffect, useRef } from "react";

export default function Home() {
  const [appName, setAppName] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [average, setAverage] = useState(null);
  const [count, setCount] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const debounceRef = useRef(null);

  // Fetch autocomplete suggestions
  useEffect(() => {
    if (appName.length < 2) {
      setSuggestions([]);
      return;
    }
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      try {
        const res = await fetch(
          `http://localhost:8000/suggest-app?name=${encodeURIComponent(
            appName
          )}&limit=5`
        );
        if (!res.ok) throw new Error("Failed to load suggestions");
        const data = await res.json();
        setSuggestions(data.results);
      } catch {
        setSuggestions([]);
      }
    }, 300);
    return () => clearTimeout(debounceRef.current);
  }, [appName]);

  // Handle form submit → analyze reviews
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setAverage(null);
    setCount(null);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/analyze-reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ appName }),
      });
      const body = await res.json();
      if (!res.ok) throw new Error(body.detail || "Analysis failed");

      setAverage(body.average_score);
      setCount(body.review_count);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Google Play Sentiment Analyzer</h1>

      <form onSubmit={handleSubmit}>
        <label htmlFor="appName">App Name:</label>
        <input
          id="appName"
          name="appName"
          list="apps"
          value={appName}
          onChange={(e) => setAppName(e.target.value)}
          style={{ width: "100%", padding: "0.5rem", margin: "0.5rem 0" }}
          required
        />
        <datalist id="apps">
          {suggestions.map((s) => (
            <option key={s.appId} value={s.title} />
          ))}
        </datalist>

        <button
          type="submit"
          disabled={loading}
          style={{ padding: "0.5rem 1rem" }}
        >
          {loading ? "Analyzing…" : "Analyze Reviews"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {average !== null && (
        <div style={{ marginTop: "1.5rem" }}>
          {/* Sentiment Scale Legend */}
          <div style={{ marginBottom: "1rem" }}>
            <strong>Sentiment Scale:</strong>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.9rem", marginTop: "0.5rem" }}>
              <span>1   Very Negative</span>
              <span>2   Negative</span>
              <span>3   Neutral</span>
              <span>4   Positive</span>
              <span>5   Very Positive</span>
            </div>
          </div>

          {/* Results */}
          <p>
            <strong>Average Sentiment Score:</strong> {average}
          </p>
          <p>
            <strong>Reviews Analyzed:</strong> {count}
          </p>
        </div>
      )}
    </div>
  );
}