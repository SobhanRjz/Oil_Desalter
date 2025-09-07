# Desalter Landing (FastAPI + Static Frontend)

A minimal landing page with a full-screen background video, centered title, and a call-to-action button. FastAPI serves the static frontend and exposes a small `/api/ping` endpoint.

## Project Structure
```
desalter_landing/
├─ backend/
│  ├─ main.py
│  └─ requirements.txt
└─ frontend/
   ├─ index.html
   ├─ styles.css
   ├─ app.js
   └─ assets/
      ├─ hero.mp4          # put your high-quality minimal background video here
      └─ hero_fallback.jpg # optional fallback image
```

## Run locally

1) Create and activate a virtualenv (optional), then install backend deps:

```bash
cd backend
python -m pip install -r requirements.txt
```

2) Start the server:

```bash
uvicorn main:app --reload --port 8000
```

3) Open http://127.0.0.1:8000 in your browser.

## Replace the background video
Put your own **hero.mp4** into `frontend/assets/`. Aim for:
- H.264 (mp4) 1080p or 1440p, ~4–8 Mbps
- short loop (8–20s), visually calm
- ensure it's muted, autoplay-friendly

## Notes
- The page respects **prefers-reduced-motion** and hides the video for those users.
- JS pauses the video if the tab is hidden to save resources.
