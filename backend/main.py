from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Desalter Landing Backend")

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
ASSETS_DIR = FRONTEND_DIR / "assets"

# Specific routes for assets to ensure they're served correctly
@app.api_route("/assets/{filename}", methods=["GET", "HEAD"])
async def serve_asset(filename: str):
    file_path = ASSETS_DIR / filename
    if file_path.exists():
        if filename.endswith('.mp4'):
            return FileResponse(file_path, media_type='video/mp4')
        elif filename.endswith(('.jpg', '.jpeg')):
            return FileResponse(file_path, media_type='image/jpeg')
        elif filename.endswith('.png'):
            return FileResponse(file_path, media_type='image/png')
        elif filename.endswith('.svg'):
            return FileResponse(file_path, media_type='image/svg+xml')
    return JSONResponse({"error": "File not found"}, status_code=404)

# Mount static files (but not at root to avoid conflicts)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Serve the main HTML file
@app.api_route("/", methods=["GET", "HEAD"])
async def read_root():
    return FileResponse(FRONTEND_DIR / "html" / "index.html", media_type="text/html")

# Serve the input page
@app.api_route("/input", methods=["GET", "HEAD"])
async def read_input():
    return FileResponse(FRONTEND_DIR / "html" / "input-page.html", media_type="text/html")

# Serve the results page
@app.api_route("/results", methods=["GET", "HEAD"])
async def read_results():
    return FileResponse(FRONTEND_DIR / "html" / "result.html", media_type="text/html")

@app.get("/api/ping")
def ping():
    return JSONResponse({"message": "Desalter backend is alive", "ok": True})
