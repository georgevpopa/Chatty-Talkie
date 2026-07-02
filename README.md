# 🗣️ Chatty Talkie

A free, offline translation application for **Romanian**, **Spanish**, and **English**.

Powered by Meta's NLLB-200 (No Language Left Behind) AI model, Chatty Talkie runs entirely on your local machine — no API keys, no usage limits, no internet required after initial setup.

---

## ✨ Features

- **6 translation directions**: EN↔RO, EN↔ES, RO↔ES
- **Completely offline** after first model download
- **Free forever** — no subscriptions, no API costs
- **Fast translations** (2-5 seconds on CPU)
- **Clean, modern web interface**
- **Keyboard shortcut**: `Ctrl + Enter` to translate
- **Swap languages** with one click
- **Copy to clipboard** button
- **5000 character limit** per translation
- **Lightweight** — ~2GB RAM usage while running

---

## 📋 Requirements

| Requirement | Minimum |
|---|---|
| Operating System | Windows 10/11, macOS, Linux |
| Python | 3.10 or higher |
| RAM | 4 GB free (8+ GB total recommended) |
| Disk Space | ~3 GB (model + dependencies) |
| Internet | Only for initial setup/download |

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/chatty-talkie.git
cd chatty-talkie
```

Or download and extract the ZIP file from GitHub.

### Step 2: Create a Virtual Environment (recommended)

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

> ⏳ This will download PyTorch (~2GB) and other packages. Takes 5-10 minutes depending on your connection.

### Step 4: Start the Application

**Option A — One-click launch (recommended):**

Simply double-click `start.bat` in the project root. It will:
- Create the virtual environment (first time only)
- Install dependencies (first time only)
- Start the server
- Open your browser automatically

**Option B — Manual launch:**

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

> ⏳ **First launch only**: The NLLB model (~1.2GB) will be automatically downloaded and cached. This takes 3-10 minutes. Subsequent launches load from cache in ~30 seconds.

### Step 5: Open in Browser

Navigate to:

```
http://127.0.0.1:8000
```

The Chatty Talkie interface will appear and show "✓ Model loaded — Ready to translate" when ready.

---

## 📖 Usage Guide

### Basic Translation

1. **Select source language** from the left dropdown (English, Romanian, or Spanish)
2. **Select target language** from the right dropdown
3. **Type or paste** your text in the left text box
4. **Click "Translate"** or press `Ctrl + Enter`
5. The translation appears in the right text box

### Interface Controls

| Control | Action |
|---|---|
| **⇄ Swap button** | Swaps source/target languages and text |
| **✕ Clear button** | Clears both text boxes |
| **📋 Copy button** | Copies translation to clipboard |
| **Ctrl + Enter** | Keyboard shortcut for translate |
| **Character counter** | Shows current / max characters (5000) |

### Status Indicators

| Status | Meaning |
|---|---|
| ✓ Green | Model loaded, ready to translate |
| ⏳ Orange | Model is loading, please wait |
| ✕ Red | Cannot connect to backend server |

---

## 🏗️ Project Structure

```
Chatty Talkie/
├── start.bat                # One-click launcher (Windows)
├── backend/
│   ├── main.py              # FastAPI server & API endpoints
│   ├── translator.py        # NLLB model wrapper
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Application UI
│   ├── style.css            # Styling
│   └── app.js              # Frontend logic
└── README.md               # This file
```

---

## ⚙️ Configuration

### Change Port

```bash
uvicorn main:app --host 127.0.0.1 --port 9000
```

Then update `API_BASE` in `frontend/app.js` to match.

### Enable Network Access

To allow other devices on your network to use Chatty Talkie:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Access from other devices using your PC's local IP (e.g., `http://192.168.1.100:8000`).

---

## 🔧 Troubleshooting

### "Cannot connect to backend"
- Make sure the server is running (`uvicorn main:app ...`)
- Check that port 8000 is not used by another application

### "Model is still loading"
- The model takes 20-60 seconds to load on startup
- First run downloads the model (~1.2GB), which takes longer

### Slow translations
- Normal speed on CPU: 2-5 seconds per translation
- Close other heavy applications to free RAM
- Longer texts take more time

### Out of memory
- The model uses ~2GB RAM
- Make sure you have at least 4GB free
- Close other applications if needed

---

## 🧰 Tech Stack

- **Backend**: Python 3.13, FastAPI, Uvicorn
- **AI Model**: Meta NLLB-200 (distilled 600M parameters)
- **ML Framework**: PyTorch, Hugging Face Transformers
- **Frontend**: Vanilla HTML, CSS, JavaScript (no frameworks)

---

## 📝 License

MIT License — Free to use, modify, and distribute.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 🗺️ Roadmap

- [ ] Language auto-detection
- [ ] Translation history
- [ ] Dark/light theme toggle
- [ ] More languages (French, Italian, Portuguese, etc.)
- [ ] Document file translation (.txt, .docx)
- [ ] Desktop app (Electron or Tauri)

---

Made with ❤️ by Chatty Talkie Team

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=georgevpopa/Chatty-Talkie&type=Date)](https://star-history.com/#georgevpopa/Chatty-Talkie&Date)
