import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_title(url):
    """
    Fetches the video title using YouTube oEmbed API.
    """
    try:
        response = requests.get(f"https://www.youtube.com/oembed?url={url}&format=json")
        if response.status_code == 200:
            return response.json().get('title', 'Unknown_Video')
    except Exception as e:
        print(f"Error fetching video title: {e}")
    return 'Unknown_Video'

def sanitize_filename(title):
    """
    Sanitizes the title to be used as a valid filename.
    """
    # Remove characters that are not alphanumeric, spaces, hyphens, or underscores
    sanitized = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    return sanitized[:100]  # Limit length

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    Supports standard, short, and embed links.
    """
    patterns = [
        r'(?:v=|\/|embed\/|youtu.be\/)([0-9A-Za-z_-]{11})(?:[?&]|\b|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_transcript(video_id):
    """
    Fetches the transcript for a given video ID.
    Returns a string of the full transcript or None if failed.
    """
    try:
        # Use instance method fetch as per version 0.6.3+
        transcript_list = YouTubeTranscriptApi().fetch(video_id)
        # Join all parts of the transcript into a single string
        full_transcript = " ".join([entry.text for entry in transcript_list])
        return full_transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def format_prompt(transcript):
    """
    Formats the prompt for the AI to analyze the transcript in Markdown.
    """
    prompt = f"""
    Analyze the following YouTube video transcript and provide a detailed response in professional Markdown format.
    The response must include:
    1. ## Summary: A concise summary of the key points.
    2. ## Key Technical Terms: A list of key technical terms used and their brief explanations.
    3. ## Major Challenges & Solutions: Identification of major challenges discussed and how they were tackled.
    4. ## Lessons Learned: Actions or lessons learned from the content.

    Transcript:
    \"\"\"{transcript}\"\"\"

    Output MUST be pure Markdown without any HTML tags.
    """
    return prompt
