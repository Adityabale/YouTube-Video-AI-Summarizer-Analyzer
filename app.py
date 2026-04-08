import os
from flask import Flask, request, render_template, jsonify
from utils import extract_video_id, get_youtube_transcript, format_prompt, get_video_title, sanitize_filename
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (from .env file if it exists)
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if not GEMINI_API_KEY:
        return jsonify({"error": "API Key is missing. Please set the GEMINI_API_KEY environment variable."}), 400

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL."}), 400

    transcript = get_youtube_transcript(video_id)
    if not transcript:
        return jsonify({"error": "Could not fetch transcript for this video."}), 400

    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # Format the prompt
        prompt = format_prompt(transcript)
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Save transcript and analysis report
        video_title = get_video_title(url)
        safe_title = sanitize_filename(video_title)
        
        # Define directories
        transcript_dir = 'transcripts'
        analysis_dir = 'analysis_reports'
        
        os.makedirs(transcript_dir, exist_ok=True)
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Save transcript (.txt)
        with open(os.path.join(transcript_dir, f"{safe_title}.txt"), "w", encoding="utf-8") as f:
            f.write(transcript)
            
        # Save analysis (.md)
        with open(os.path.join(analysis_dir, f"{safe_title}.md"), "w", encoding="utf-8") as f:
            f.write(f"# {video_title}\n\n")
            f.write(f"**Original Video:** {url}\n\n")
            f.write(response.text)
        
        # Return the transcript and the AI's HTML analysis
        return jsonify({
            "transcript": transcript,
            "analysis_html": response.text,
            "video_title": video_title
        })
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": f"Failed to generate analysis: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
