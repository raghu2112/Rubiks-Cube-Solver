# main.py
# Entry point for the Rubik's Cube Solver application.
# This is a Streamlit app — it must be launched via `streamlit run`.
# Running `python main.py` will automatically invoke the correct command.

import sys
import os
import subprocess

if __name__ == "__main__":
    # Get the directory where this script lives
    project_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(project_dir, "ui", "app.py")

    print("=" * 50)
    print("  🧊 Rubik's Cube Solver")
    print("=" * 50)
    print(f"  Starting Streamlit server...")
    print(f"  Open http://localhost:8501 in your browser")
    print("=" * 50)

    # Launch Streamlit properly as a subprocess
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.headless", "true"
    ], cwd=project_dir)
