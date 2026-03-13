# 🤖 HELLO-BOT — AI Chatbot with Interactive Robot Mascot

A stylish, premium AI chatbot powered by **Google Gemini 2.5 Flash**, built with Flask and a fully custom animated front-end featuring a futuristic floating robot mascot.

---

## ✨ Features

### 🧠 AI Chat
- Powered by **Google Gemini 2.5 Flash** via the `google-generativeai` SDK
- Supports **custom AI personas** via a system prompt input
- Markdown rendering with syntax-highlighted code blocks (via `marked.js` + `highlight.js`)
- Clean message history flowing downward from the input bar

### 🤖 Interactive Robot Mascot (HELLO-BOT)
- Cute, futuristic floating robot character with:
  - Glossy rounded head with a glowing LED face display
  - Capsule-style body with animated glowing core
  - Curved arms with swing/wave animations
  - Animated antenna light

#### Face Expressions
The robot dynamically switches between **10 emoji-style expressions**:

| Key | Expression  |
|-----|-------------|
| `1` | 😄 Happy     |
| `2` | 😢 Sad       |
| `3` | 😠 Angry     |
| `4` | 😍 Love      |
| `5` | 🤔 Thinking  |
| —   | 😐 Neutral   |
| —   | 😉 Wink      |
| —   | 💤 Sleep     |
| —   | 😲 Surprised |
| —   | 😕 Confused  |

#### Robot Animations
- **Idle float** — gentle up/down floating when idle
- **Head tilt** — tilts toward cursor when nearby
- **Wave** — arm wave on click or when sending a message
- **Blink** — random blink every ~3 seconds
- **Greeting** — nod animation on page load
- **Auto cycling** — expression changes automatically every 10 seconds

#### Mouse Interactions
- Robot **looks toward your cursor** in real time
- **Click** the robot to trigger a wave + happy expression
- Robot **slightly tilts** its head when your cursor is close

### ⚙️ Robot Studio (Settings Panel)
Click the **gear icon** in the top-left of the header to open the Robot Studio panel:

| Control         | Description                          |
|-----------------|--------------------------------------|
| Face Color      | Color picker — changes neon LED glow |
| Robot Size      | Slider — scale from 0.5× to 2×       |
| Expression      | Dropdown — all 10 expressions        |
| Floating Toggle | Enable / disable floating animation  |
| Follow Mouse    | Enable / disable cursor tracking     |

### 🖱️ Draggable Robot
The robot character is **fully draggable** — grab it and move it anywhere inside the chat window. Works on both mouse and touch devices.

---

## 🗂️ Project Structure

```
llm ai chatbot/
├── app.py                  # Flask backend — serves UI and handles /chat API
├── requirements.txt        # Python dependencies
├── gemini api key.txt      # Your Gemini API key (not committed to git)
├── config.example.txt      # Example config reference
├── templates/
│   └── index.html          # Main UI — all styles, robot component, and JS in one file
├── static/
│   ├── css/
│   │   └── style.css       # Legacy stylesheet (retained for reference)
│   └── js/
│       └── app.js          # Legacy JS (retained for reference)
└── test_models.py          # Utility script to test available Gemini models
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- A valid [Google Gemini API key](https://aistudio.google.com/app/apikey)

### 2. Clone / Download the project

```bash
git clone <your-repo-url>
cd "llm ai chatbot"
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create (or edit) the file named **`gemini api key.txt`** in the project root and paste your API key inside:

```
YOUR_GEMINI_API_KEY_HERE
```

### 5. Run the app

```bash
python app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000
```

---

## ⌨️ Keyboard Shortcuts

| Key   | Action                     |
|-------|----------------------------|
| `1`   | Set expression → Happy     |
| `2`   | Set expression → Sad       |
| `3`   | Set expression → Angry     |
| `4`   | Set expression → Love      |
| `5`   | Set expression → Thinking  |
| `Enter` | Send message (in chat box) |
| `Shift + Enter` | New line in chat box |

---

## 🛠️ Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python 3, Flask                   |
| AI Model    | Google Gemini 2.5 Flash           |
| Frontend    | HTML5, CSS3, Vanilla JavaScript   |
| Markdown    | marked.js                         |
| Code Highlight | highlight.js (atom-one-dark)   |
| Fonts       | Google Fonts — Inter              |

---

## 🔑 API Key Security

- The API key is read from a local text file (`gemini api key.txt`) and is **never hardcoded** in source files.
- Add `gemini api key.txt` to your `.gitignore` before pushing to any public repository.

```gitignore
gemini api key.txt
.venv/
```

---

## ⚠️ Known Notes

- The `google-generativeai` SDK shows a `FutureWarning` about deprecation — the app still works fully. Migration to `google.genai` is planned for a future update.
- This app runs Flask in **debug mode** — intended for local development only. Use a production WSGI server (e.g., Gunicorn) for deployment.

---

## 📄 License

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
