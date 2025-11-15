# Desalter Landing (FastAPI + Static Frontend)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-blue)](https://sobhanrjz.github.io/Oil_Desalter/)

**Live Demo:** https://sobhanrjz.github.io/Oil_Desalter/

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

## Development Workflow

### Editing HTML/CSS/JS Files
1. **Edit source files** in `frontend/html/`, `frontend/css/`, `frontend/js/`
2. **Sync to static folder**: Run `python sync_static.py`
3. **Commit and push** to deploy to GitHub Pages

### Replace the background video
Put your own **hero.mp4** into `frontend/assets/`. Aim for:
- H.264 (mp4) 1080p or 1440p, ~4–8 Mbps
- short loop (8–20s), visually calm
- ensure it's muted, autoplay-friendly

### GitHub Pages Deployment
- **Source**: `static/` folder
- **URL**: `https://sobhanrjz.github.io/Oil_Desalter/`
- **Auto-deploy**: Triggers on push to `main` branch
- **Permissions**: Requires `id-token: write` for authentication

## Build Standalone Executable with Nuitka

Nuitka is a Python compiler that creates standalone executables with faster startup times and smaller sizes compared to PyInstaller.

### Quick Build (Recommended)
```bash
# Install Nuitka
pip install nuitka

# Build executable (includes fallback to PyInstaller)
python build_exe.py

# Executable will be created at: dist/desalter.exe
```

### Advanced Nuitka Options
```bash
# Use dedicated Nuitka script for more options
python build_nuitka.py

# Options available:
# 1. Standalone + Onefile (Recommended)
# 2. Minimal build
# 3. Debug build
```

### Nuitka vs PyInstaller Comparison

| Feature | Nuitka | PyInstaller |
|---------|--------|-------------|
| Startup Speed | ⚡ Faster | 🐌 Slower |
| Executable Size | 📦 Smaller | 📦 Larger |
| Build Time | 🕐 Longer | ⚡ Faster |
| Dependencies | 📋 More complex | ✅ Simpler |
| Performance | 🚀 Better | ⚖️ Good |

### Manual Nuitka Commands

```bash
# Basic build
python -m nuitka --onefile launcher.py

# Advanced build with data inclusion
python -m nuitka \
  --standalone \
  --onefile \
  --windows-disable-console \
  --include-data-dir=frontend=frontend \
  --include-data-dir=backend=backend \
  --output-dir=dist \
  launcher.py
```

## Notes
- The page respects **prefers-reduced-motion** and hides the video for those users.
- JS pauses the video if the tab is hidden to save resources.
- Nuitka executables typically start 2-3x faster than PyInstaller executables
