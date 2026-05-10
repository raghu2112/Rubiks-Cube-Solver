# 🧊 AI Rubik's Cube Solver

A premium, production-ready Single-Page Application (SPA) designed to help you scan, solve, and analyze both standard and pocket Rubik's Cubes. Powered by computer vision and optimal search algorithms, this tool provides a seamless, interactive experience for both beginners and speedcubers.

---

## ✨ Features

* **Multi-Cube Support**: Fully supports solving both **3×3 (Standard)** and **2×2 (Pocket Cube)** puzzles.
* **Advanced Algorithmic Engines**:
  * **3×3**: Utilizes Herbert Kociemba's Two-Phase Algorithm, guaranteeing a near-optimal solution in **≤ 22 moves**.
  * **2×2**: Utilizes a custom-built Bidirectional BFS (Breadth-First Search) engine, finding the mathematically optimal solution in **≤ 11 moves**.
* **Computer Vision Scanning**: Capture your cube's state directly via webcam. Features real-time **Confidence Scoring** that analyzes pixel variance to warn you about bad lighting or blurry captures.
* **Interactive 3D Walkthrough**: Step through the generated solution with an embedded 3D interactive viewer (`cubing/twisty`). Features plain-English translations for every move (e.g., translates `R2` to *"Rotate the RIGHT face 180°"*).
* **Solve Analytics Dashboard**: Automatically tracks your session history, displaying your Total Solves, Average Move Count, and a line chart of your move-count trends.
* **Famous Patterns Library**: A curated library of beautiful 3×3 algorithms (e.g., *Superflip*, *Checkerboard*, *Cube in a Cube*) with live 3D previews.
* **Premium UI/UX**: Features a beautiful responsive layout with a global **Dark/Light Mode toggle**, smooth state transitions, and an intuitive linear flow.

---

## 🛠️ Tech Stack

* **Frontend / UI**: [Streamlit](https://streamlit.io/) (Python-based SPA architecture)
* **Computer Vision**: [OpenCV](https://opencv.org/) & NumPy (Color extraction and contour mapping)
* **Algorithmic Backend**: 
  * `pykociemba` (Python implementation of the Two-Phase algorithm)
  * Custom IDA* / BFS Python implementations
* **3D Rendering**: [cubing.js](https://js.cubing.net/) (via HTML/JS injection)

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.9 or higher
* A working webcam (for color detection)

### Setup Instructions

1. **Clone the repository** (or download the source code).
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install streamlit opencv-python numpy
   # Note: The pykociemba package is bundled within the /solver directory.
   ```
4. **Run the Application**:
   ```bash
   streamlit run ui/app.py
   ```
5. **Access the UI**: Open your browser and navigate to `http://localhost:8501`.

---

## 📖 Usage Guide

1. **Select Cube Type**: Use the sidebar to toggle between 2×2 and 3×3 modes.
2. **Camera Capture**: 
   * Hold the cube in front of the camera, aligning it within the on-screen grid.
   * Check the **Confidence Bars**. If they are red/yellow, adjust your lighting to ensure the AI detects the colors correctly.
   * Click **Capture** for all 6 faces (Up, Right, Front, Down, Left, Back).
3. **Edit & Validate**: Review the 2D flattened net of your cube. If the camera misidentified a color due to glare, you can manually correct it using the dropdown menus.
4. **Solve**: Click "Solve Cube". The engine will validate that your cube is physically possible (no twisted corners or flipped edges) and calculate the optimal path.
5. **Walkthrough**: Use the `Previous` and `Next` buttons to walk through the physical turns needed to solve the cube, while watching the 3D animation.

---

## 📂 Project Architecture

```text
├── config/
│   └── settings.py           # Global constants (FACES, DEFAULT_SIZE)
├── detection/
│   └── color_detection.py    # OpenCV logic for face extraction and confidence scoring
├── solver/
│   ├── engine.py             # Kociemba 3x3 dispatch and validation wrapper
│   ├── pocket_cube.py        # Custom Bidirectional BFS solver for 2x2
│   └── pykociemba/           # Bundled Two-Phase 3x3 algorithm library
├── ui/
│   ├── app.py                # Main Streamlit application and layout routing
│   ├── session_history.py    # JSON-based persistence for solve analytics
│   └── styles.py             # Dynamic CSS generation for Light/Dark themes
├── utils/
│   └── colors.py             # Color mapping and HEX definitions
├── visualization/
│   └── cube_visualizer.py    # 2D flattened cube net renderer
└── solve_history.json        # Local storage database for user sessions
```

---
*Built with ❤️ for speedcubers and puzzle enthusiasts.*
