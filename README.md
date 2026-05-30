# YouTube AI Summarizer 🎬

Paste any YouTube URL and get an AI-powered summary with key points instantly.

## Features
- Supports multiple languages (English, Hindi, Telugu, Tamil and more)
- Returns clean bullet point summaries
- REST API built with FastAPI

## Tech Stack
- Python, FastAPI, Groq LLaMA, youtube-transcript-api

## How to Run
1. Clone the repo
2. Add GROQ_API_KEY to .env file
3. Run: uvicorn main:app --reload
4. Visit: http://localhost:8000/docs
