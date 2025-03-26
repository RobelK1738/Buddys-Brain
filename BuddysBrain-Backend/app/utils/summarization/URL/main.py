import os
import requests
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')


TRUNCATE_LIMIT = 30000  # approx. 12,000–15,000 words
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_chat_summary(messages, max_tokens):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def summarize_article(url, max_tokens=300):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text[:TRUNCATE_LIMIT]

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes the **educational content** of web pages for university students. Focus only on the main topics, arguments, and insights. Ignore formatting, layout, or non-relevant details."
            },
            {
                "role": "user",
                "content": (
                    f"Please summarize the **subject matter** and **key ideas** in the following web page content. "
                    f"Keep your summary clear, focused, and under 200 words:\n\n{content}"
                )
            }
        ]
        return get_chat_summary(messages, max_tokens)

    except Exception as e:
        return f"❌ Error processing {url}: {e}"

def extract_video_id(video_url):
    if "youtu.be" in video_url:
        return video_url.split('/')[-1].split('?')[0]
    return video_url.split('v=')[1].split('&')[0]

def summarize_video(video_url, max_tokens=300):
    try:
        video_id = extract_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(item['text'] for item in transcript)[:TRUNCATE_LIMIT]

        messages = [
            {
                "role": "system",
                "content": "You are an assistant that summarizes the **educational content** of YouTube video transcripts for students. Focus on concepts, explanations, and examples. Keep it clear and ignore filler or intros."
            },
            {
                "role": "user",
                "content": (
                    f"Summarize the **key educational content** of this YouTube video transcript in a way that’s helpful to students. "
                    f"Limit your summary to 200 words. Be clear, thorough, and content-focused:\n\n{transcript_text}"
                )
            }
        ]
        return get_chat_summary(messages, max_tokens)

    except Exception as e:
        return f"❌ Error summarizing video: {e}"
