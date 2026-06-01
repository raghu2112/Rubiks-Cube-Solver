# main.py
# Entry point for the Rubik's Cube Solver application.
# Launches the FastAPI backend and opens the React frontend.

import sys
import os
import subprocess
import webbrowser
import time
import threading

def open_browser(url, delay=2):
    """Open the browser after a short delay to let the server start."""
    time.sleep(delay)
    webbrowser.open(url)

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(project_dir, "server.py")

    print("=" * 55)
    print("  🧊 Rubik's Cube Solver")
    print("=" * 55)
    print("  Starting FastAPI backend on http://localhost:8000")
    print("  React frontend at http://localhost:5173")
    print("  API docs at http://localhost:8000/docs")
    print("=" * 55)
    print()
    print("  📌 Make sure to start the React dev server:")
    print("     cd frontend && npm run dev")
    print("=" * 55)

    # Open browser to frontend
    threading.Thread(target=open_browser, args=("http://localhost:5173",), daemon=True).start()

    # Launch FastAPI server
    subprocess.run([
        sys.executable, "-m", "uvicorn", "server:app",
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ], cwd=project_dir)
