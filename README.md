# 🎥 YouTube Video AI Summarizer & Analyzer

A powerful, modern web application that leverages **Google Gemini AI** to transcribe and analyze YouTube videos. Built with Flask, this tool extracts key insights, technical terms, challenges, and lessons learned from any YouTube video in seconds.

---

## ✨ Features

- 📝 **Automated Transcription**: Fetches full transcripts from YouTube videos using their URL.
- 🤖 **AI-Powered Analysis**: Uses **Gemini 2.0 Flash** to provide structured summaries.
- 🔍 **Deep Insights**:
  - **Key Points**: A concise breakdown of the video's core message.
  - **Technical Terms**: Identifies and explains jargon used in the video.
  - **Challenges & Solutions**: Highlights major hurdles discussed and how they were overcome.
  - **Lessons Learned**: Distills actionable takeaways.
- 🎨 **Premium UI/UX**:
  - ✨ Glassmorphism design with backdrop blur.
  - 🌓 Dark mode optimized.
  - 📱 Fully responsive layout.
  - 🔄 Real-time processing status and loading animations.
  - 📑 Tabbed view for toggling between AI reports and raw transcripts.

---

## 🛠️ Tech Stack

- **Backend**: Python, [Flask](https://flask.palletsprojects.com/)
- **AI Model**: [Google Gemini 1.5 Flash](https://ai.google.dev/models/gemini)
- **APIs**: `youtube-transcript-api`, `google-generativeai`
- **Frontend**: Vanilla HTML5, CSS3 (Custom Design System), JavaScript (ES6+)

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8 or higher.
- A **Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/)).

### 2. Installation

1. Create and activate a Virtual Environment (recommended):
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add your API key:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```

### 3. Running the App

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 📂 Project Structure

```text
.
├── transcripts/        # Automatically saved raw transcripts
├── analysis_reports/   # Automatically saved AI analysis reports (.md)
├── app.py              # Main Flask application
├── utils.py            # Helper functions for transcript & AI logic
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (private)
├── static/
│   ├── css/            # Modern Glassmorphic CSS
│   └── js/             # Frontend logic & API interaction
└── templates/
    └── index.html      # Main user interface
```

---

## 💡 How It Works

1. **Input**: Paste any YouTube video URL into the interface.
2. **Transcript Extraction**: The backend identifies the video ID and uses `youtube-transcript-api` to pull the raw text.
3. **AI Processing**: The text is sent to Gemini AI with a specialized prompt to analyze the content and return structured HTML.
4. **Display**: The result is rendered in a beautiful, tabbed interface for easy reading.

---

## 📝 License

This project is part of a technical assignment.

---
