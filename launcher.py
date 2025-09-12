import sys
import time
import webbrowser
import uvicorn
from pathlib import Path

def main():
    """Launch the FastAPI server and open browser."""
    try:
        # Get the directory where the executable is located
        base_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent

        # Add the base directory to Python path
        if str(base_dir) not in sys.path:
            sys.path.insert(0, str(base_dir))

        # Import the FastAPI app
        from backend.main import app

        # Open browser first
        print("Opening browser...")
        webbrowser.open("http://127.0.0.1:7000")

        # Wait a moment for browser to open
        time.sleep(1)

        print("Starting server on http://127.0.0.1:7000")
        print("Press Ctrl+C to stop the server")

        # Start uvicorn server directly
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=7000,
            reload=False,  # Disable reload for production
            log_level="info"
        )

    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error: {e}")
        if not getattr(sys, 'frozen', False):
            input("Press Enter to exit...")
        else:
            # In frozen mode, give user time to see the error
            time.sleep(5)

if __name__ == "__main__":
    main()
