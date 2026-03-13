#!/usr/bin/env python3
"""
HelloBot - Single-file Streamlit Launcher
==========================================
Combines app.py (Flask backend + routes) and chatbot.py (AIChatbot class)
into one file. Run with:   streamlit run streamlit_app.py

How it works:
  - Flask server starts in a background thread on port 5000
  - Streamlit embeds the full Flask UI (robot, animations, chat) via iframe
  - All existing features are preserved exactly as-is
"""

import streamlit as st
import threading
import os
import re
import sys
import time

import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


# ═══════════════════════════════════════════════════════════════
#  API KEY LOADING  (from app.py)
# ═══════════════════════════════════════════════════════════════

def load_api_key():
    """Load Gemini API key from secrets file, environment variable, or Streamlit secrets."""
    # 1. Try reading from key file (supports plain key OR GEMINI_API_KEY = "..." format)
    API_KEY_FILE = 'gemini api key.txt'
    try:
        with open(API_KEY_FILE, 'r') as f:
            content = f.read().strip()
        match = re.search(r'GEMINI_API_KEY\s*=\s*["\']?([^"\' \n]+)["\']?', content)
        if match:
            return match.group(1)
        elif content and not content.startswith('#'):
            return content  # plain key fallback
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Warning reading key file: {e}")

    # 2. Try environment variable
    key = os.environ.get('GEMINI_API_KEY')
    if key:
        return key

    # 3. Try Streamlit secrets (when deployed on Streamlit Cloud)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    print("Error: GEMINI_API_KEY not found in key file, environment, or Streamlit secrets.")
    return None


# ═══════════════════════════════════════════════════════════════
#  AIChatbot CLASS  (from chatbot.py — conversation history mode)
# ═══════════════════════════════════════════════════════════════

class AIChatbot:
    """
    LLM-Powered AI Chatbot using Google Gemini.
    Supports streaming responses and persistent conversation history.
    """

    def __init__(self, api_key: str, system_prompt: str = None):
        """
        Initialize the chatbot with Google Gemini API.

        Args:
            api_key:       Your Google Gemini API key
            system_prompt: Optional system instructions for the chatbot
        """
        genai.configure(api_key=api_key)

        if system_prompt is None:
            system_prompt = (
                "You are a helpful AI assistant.\n"
                "You provide clear, concise answers.\n"
                "You are friendly and professional in your responses."
            )

        self.system_prompt = system_prompt

        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={
                'temperature': 0.7,
                'top_p': 1,
                'top_k': 1,
                'max_output_tokens': 2048,
            }
        )

        self.chat = self.model.start_chat(history=[])
        self._initialize_with_system_prompt()

    def _initialize_with_system_prompt(self):
        """Seed the chat session with the system prompt."""
        initial_message = (
            f"System Instructions: {self.system_prompt}\n\n"
            "Please acknowledge these instructions briefly."
        )
        self.chat.send_message(initial_message)

    def send_message(self, message: str, stream: bool = False):
        """
        Send a message and return the chatbot's response.

        Args:
            message: User's message text
            stream:  If True, streams chunks to stdout and returns full text

        Returns:
            The chatbot's response as a string
        """
        try:
            if stream:
                response = self.chat.send_message(message, stream=True)
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        print(chunk.text, end='', flush=True)
                        full_response += chunk.text
                print()
                return full_response
            else:
                response = self.chat.send_message(message)
                return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self):
        """Return the full conversation history."""
        return self.chat.history

    def clear_history(self):
        """Clear conversation history and restart chat session."""
        self.chat = self.model.start_chat(history=[])
        self._initialize_with_system_prompt()


# ═══════════════════════════════════════════════════════════════
#  FLASK APP  (from app.py — serves index.html + /chat endpoint)
# ═══════════════════════════════════════════════════════════════

GEMINI_API_KEY = load_api_key()
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

flask_app = Flask(__name__)
CORS(flask_app, resources={r"/chat": {"origins": "*"}})

# Stateless Gemini model for the web UI endpoint (gemini-2.5-flash)
_model = genai.GenerativeModel('gemini-2.5-flash')

# Optional: shared AIChatbot instance (conversation-history mode) available for
# programmatic use or future Streamlit-native UI extension.
_chatbot_instance = None
if GEMINI_API_KEY:
    try:
        _chatbot_instance = AIChatbot(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Warning: Could not initialise AIChatbot instance: {e}")


@flask_app.route("/")
def home():
    """Serve the main HelloBot frontend."""
    return render_template("index.html")


@flask_app.route("/chat", methods=["POST"])
def chat():
    """Handle chat requests from the frontend."""
    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API key is missing or invalid on the server."}), 500

    data = request.get_json()
    user_message = data.get("message")
    system_prompt = data.get(
        "system_prompt",
        "You are a helpful, smart, and friendly AI assistant."
    )

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        prompt = f"System Instructions: {system_prompt}\n\nUser Message: {user_message}"
        response = _model.generate_content(prompt)

        if response.text:
            return jsonify({
                "choices": [{
                    "message": {
                        "content": response.text
                    }
                }]
            })
        else:
            return jsonify({"error": "No response text generated by Gemini"}), 500

    except Exception as e:
        print(f"Generation error: {e}")
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════════════════════
#  BACKGROUND FLASK THREAD
# ═══════════════════════════════════════════════════════════════

def _run_flask():
    """Run Flask silently in a daemon thread."""
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)          # suppress Flask request noise in Streamlit console
    flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


_flask_thread_started = False


def _start_flask_once():
    """Start the Flask thread only once per Streamlit session (uses st.session_state)."""
    global _flask_thread_started
    if not _flask_thread_started:
        t = threading.Thread(target=_run_flask, daemon=True)
        t.start()
        time.sleep(1.5)                  # wait for Flask to be ready
        _flask_thread_started = True


# ═══════════════════════════════════════════════════════════════
#  STREAMLIT PAGE
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="HelloBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome so only the embedded app is visible
st.markdown(
    """
    <style>
        #MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; height: 0; }
        .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
        section[data-testid="stMain"] > div { padding: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar: status info
with st.sidebar:
    st.title("HelloBot Status")
    if GEMINI_API_KEY:
        st.success("✅ Gemini API key loaded")
    else:
        st.error("❌ API Key not found")
        st.info(
            "Add your key to **gemini api key.txt** as:\n"
            "```\nGEMINI_API_KEY = \"AIza...\"\n```\n"
            "or to **.streamlit/secrets.toml**."
        )
    st.divider()
    st.caption("HelloBot v1.0 · Powered by Gemini 2.5 Flash")
    st.caption("Run locally:  `streamlit run streamlit_app.py`")

# Start Flask backend
_start_flask_once()

# ── Load index.html and patch the /chat fetch to absolute URL ──
_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
try:
    with open(_html_path, "r", encoding="utf-8") as _f:
        _html_content = _f.read()
    # Replace relative /chat fetch with absolute Flask URL so the browser can reach it
    _html_content = _html_content.replace("fetch('/chat'", "fetch('http://localhost:5000/chat'")
    st.components.v1.html(_html_content, height=980, scrolling=False)
except FileNotFoundError:
    st.error("templates/index.html not found — make sure you run from the project folder.")
    st.code("streamlit run streamlit_app.py")
