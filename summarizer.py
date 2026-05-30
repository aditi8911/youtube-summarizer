import os
import re
from dotenv import load_dotenv
from groq import Groq
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

def get_summary(url):
    video_id = extract_video_id(url)
    
    if not video_id:
        return "Invalid YouTube URL. Please check the link."

    print(f"Found Video ID: {video_id}")
    print("Fetching transcript...")
    
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        transcript = transcript_list.find_transcript(['en', 'hi', 'en-US', 'en-GB', 'te', 'ta', 'kn', 'ml', 'mr', 'bn', 'gu', 'pa', 'ur', 'fr', 'de', 'es', 'ja', 'ko', 'zh', 'ar', 'ru', 'pt'])
        data = transcript.fetch()
        full_text = " ".join([i.text for i in data])
        
        print("Summarizing with AI...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Summarize the following video transcript into 3 clear, concise bullet points."},
                {"role": "user", "content": f"Transcript: {full_text[:15000]}"}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("GROQ API Key not found! Please check your .env file.")
    else:
        print("--- YouTube AI Summarizer ---")
        link = input("Enter YouTube URL: ")
        print("\n--- SUMMARY ---")
        result = get_summary(link)
        print(result)