import os
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

def get_transcript(video_url: str) -> str:
    video_id = video_url.split("v=")[-1].split("&")[0]
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    transcript = transcript_list.find_transcript(['en', 'hi', 'en-US', 'en-GB', 'te', 'ta', 'kn', 'ml', 'mr', 'bn', 'gu', 'pa', 'ur', 'fr', 'de', 'es', 'ja', 'ko', 'zh', 'ar', 'ru', 'pt'])
    data = transcript.fetch()
    return " ".join([f"[{int(t.start)}s] {t.text}" for t in data])

def summarize(transcript: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Summarize this YouTube transcript. Return: 1. A 3-sentence TL;DR 2. 5 key points with timestamps 3. Any action items\n\nTranscript:\n{transcript[:12000]}"
        }]
    )
    return response.choices[0].message.content

@app.post("/summarize")
def summarize_video(req: VideoRequest):
    transcript = get_transcript(req.url)
    summary = summarize(transcript)
    return {"summary": summary}