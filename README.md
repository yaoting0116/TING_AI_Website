# TING‑AI Media Web 🎵🖼️

## Overview  
TING‑AI is a simple yet powerful personal multimedia website built with Python/Flask (backend) and Vue.js (frontend).  
It allows you to:  
- Display AI‑generated images (e.g. from Stable Diffusion) under `static/images/`.  
- Show a music player that automatically loads all audio files in `static/music/`, with playlist, play/pause, next/previous, shuffle, repeat, volume control, and progress bar.  
- Support responsive design — works on both desktop and mobile, adapting layout accordingly.  
- Run without a database: everything is based on static files — makes it easy to deploy and maintain.

## Features 🎯  
- **Image gallery**: Automatically list all images in `static/images/` for browsing.  
- **Music player & playlist**: Automatically detect audio files, generate a scrollable playlist, and offer full-featured controls.  
- **Responsive layout**: Desktop layout with fixed side‑menu; mobile layout with collapsible menu and adaptive UI.  
- **Lightweight and easy to deploy**: Minimal dependencies, no database needed — just Flask + static assets + minimal frontend code.  

## Project Structure  

```

/ (project root)
├── app.py                # Flask main application
├── templates/            # Jinja HTML templates
│   ├── index.html
│   ├── music.html
│   └── ... other pages
├── static/               # Static assets
│   ├── images/           # AI‑generated images
│   ├── music/            # Audio files
│   └── ... (CSS, JS, other resources, if any)
└── README.md             # This README file

````

## Hosting / Deployment — Hosted on Render  

This website is currently hosted on Render as a web service. The deployment setup is as follows:  

- Use Render’s **Web Service** to run the Flask backend. :contentReference[oaicite:1]{index=1}  
- Typical configuration:  
  - **Build Command**: `pip install -r requirements.txt` :contentReference[oaicite:2]{index=2}  
  - **Start Command**: `gunicorn app:app` — assuming your Flask app object is defined in `app.py`. :contentReference[oaicite:3]{index=3}  
- Once deployed, the site becomes live at a `*.onrender.com` URL. Any push to the linked GitHub branch triggers an automatic rebuild & deploy. :contentReference[oaicite:4]{index=4}  
- This setup makes updates easy: to add or update images/music, just place files under `static/`, commit & push → Render rebuilds and serves the updated content.

## Getting Started (Locally) 🚀  

### Prerequisites  
- Python 3.8+  
- Flask  

### Setup & Run Locally  

```bash
git clone https://github.com/your‑username/your‑repo.git
cd your‑repo
python3 -m venv venv
source venv/bin/activate     # (on Windows use: .\venv\Scripts\activate)
pip install flask
python app.py
````

Then open your browser at `http://127.0.0.1:5000/`.

### Usage

* Place your **images** in `static/images/` → they will appear automatically on the homepage.
* Place your **music files** (mp3 / wav / …) in `static/music/` → they will show up in the music playlist automatically.
* Use the built-in UI to play music, control volume, skip tracks, shuffle, repeat, and browse the playlist. Works on desktop & mobile.

