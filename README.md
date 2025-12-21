# 🎯 Algorithm Playground

Interactive web application to **visualize and understand algorithms in real-time**.  
Built with **Flask (Python)** and **HTML/CSS/JavaScript (Canvas API)**, this project focuses on helping a **single learner** deeply learn Data Structures and Algorithms through animation, stats, and experiments.

---

## ✨ Current Features (v1.0.0)

### 🔄 Sorting Visualizer

Visualizes how classic sorting algorithms work step by step on a bar chart.

- **Implemented Algorithms**
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
  - Merge Sort
  - Quick Sort

- **Features**
  - Adjustable array size (10–200 elements)
  - Speed control (0.1x – 3x)
  - Random array generation
  - Real-time drawing using HTML5 Canvas
  - Color-coded states:
    - Blue: default
    - Red: comparing
    - Green: sorted
    - Yellow: special/pivot
  - Live statistics:
    - Comparisons
    - Swaps
    - Time taken (ms)
    - Status messages (Ready / Sorting / Sorted)

---

### 🗺️ Pathfinding Visualizer

Visualizes graph traversal and shortest path algorithms on a grid.

- **Implemented Algorithms**
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Dijkstra’s Algorithm

- **Grid & Interaction**
  - 20×20 grid (Canvas based)
  - Left-click to toggle walls
  - “Set Start” → click grid to choose start node (green)
  - “Set End” → click grid to choose end node (red)
  - “Clear Walls” to reset only walls
  - “Reset All” to reset everything

- **Visualization**
  - Black: walls
  - Light blue: explored nodes
  - Yellow: final path
  - Green: start
  - Red: end

- **Statistics**
  - Nodes visited
  - Path length (number of steps)
  - Time taken (ms)
  - Status messages (Ready / Searching / Path Found / No Path)

---

### 🧱 Tech Stack

- **Backend**
  - Python 3.9+
  - Flask
  - Flask-CORS
  - Gunicorn (for deployment)

- **Frontend**
  - HTML5
  - CSS3 (responsive design, gradients, cards, dark navbar)
  - Vanilla JavaScript
  - Canvas API (sorting bars, grid rendering)

- **Deployment**
  - Local: `python app.py`
  - Cloud: Ready for Render.com or Railway.app

---

## 📦 Project Structure
algorithm-playground/
├── app.py # Flask backend (serves index.html)
├── config.py # Configuration (dev/prod)
├── requirements.txt # Python dependencies
├── Procfile # For Gunicorn / cloud deploy
├── runtime.txt # Python version for deploy
├── .env.example # Environment variables template
├── .gitignore # Git ignore rules
├── LICENSE # MIT License
│
├── templates/
│ └── index.html # Single-page app (home + sorting + pathfinding)
│
├── static/ # (Will be used when JS/CSS split into files)
│ ├── css/
│ └── js/
│
├── README.md # This file
├── CONTRIBUTING.md # Contribution guidelines
└── DEPLOYMENT.md # Deployment instructions

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- pip
- Git (optional but recommended)
- A modern browser (Chrome / Firefox / Edge / Safari)

### 2. Installation
Clone the repository
git clone https://github.com/YOUR-USERNAME/algorithm-playground.git
cd algorithm-playground

(Optional) Create a virtual environment
python -m venv venv

Windows: venv\Scripts\activate
Linux/macOS:
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Run the app
python app.py

Visit in browser
http://localhost:5000

---

## 🖥️ Usage

### Sorting Visualizer

1. Go to **Sorting** page.
2. Move **Array Size** slider to choose number of bars.
3. Move **Speed** slider to control animation speed.
4. Choose algorithm from **Algorithm** dropdown.
5. Click **Generate New Array** to create random array.
6. Click **Start Sorting** to watch the algorithm.
7. Observe:
   - Bar movements and colors
   - Comparisons, swaps, and total time updating live
   - Final state where all bars become green (sorted)

### Pathfinding Visualizer

1. Go to **Pathfinding** page.
2. Click **Set Start** and then click a grid cell.
3. Click **Set End** and click another grid cell.
4. Draw walls by clicking on grid cells.
5. Select an algorithm from **Algorithm** dropdown (BFS / DFS / Dijkstra).
6. Click **Find Path** to start visualization.
7. Watch:
   - Explored nodes turn light blue
   - Final path becomes yellow
   - Stats update: visited nodes, path length, time

---

## 🧠 Learning Goals

This project helps you:

- Understand **how algorithms actually behave** step-by-step.
- Connect **Big‑O complexity** with:
  - Number of comparisons/swaps
  - Nodes visited
  - Real time taken
- Practice **full‑stack development**:
  - Flask routing and templating
  - Canvas-based front-end animations
  - Deployment to cloud platforms

---

## 🔮 Roadmap – Future Features & Enhancements

This section describes **planned upgrades**. They are not yet implemented but are part of the long-term vision.

### TIER 1 – Quick Wins (UI/UX & Learning)  

**UI / UX Improvements**
- Dark Mode toggle (light/dark themes)
- Color theme customization (user-chosen palette)
- Fullscreen canvas mode for maximum viewing area
- Even better responsive mobile layout
- FPS indicator and animation smoothness limiter
- Grid size adjustment for pathfinding (e.g., 10×10, 30×30)
- Option to show numerical values on top of bars
- Sidebar menu with collapsible sections for controls
- Richer home page with introduction & quick guide

**Statistics & Tracking (single-user, local)**
- Count of **total algorithm runs** (local history)
- Mark **favorite algorithms** for quick access
- Track **personal best times** per algorithm
- Visual **complexity comparison chart** (e.g., n vs time)
- Export stats as **CSV/JSON** (download)
- Show **estimated memory usage**
- Show **step counter / iteration count**
- Sorting **progress bar**

**Algorithm Explanations**
- Pseudocode display for each algorithm
- Complexity calculator (estimate operations for given n)
- Real-world examples / typical use-cases
- “Did you know?” tips per algorithm
- “Related algorithms” suggestions
- Visual **space-complexity** indication
- Best / worst / average case explanations and sample inputs

---

### TIER 2 – Medium Features (Interaction & More Algorithms)

**Interactive Features**
- Custom input: type or paste your own array
- Algorithm comparison mode (run 2–3 algorithms side by side)
- Pause / resume and step-by-step execution mode
- Reverse animation (replay sorting backwards)
- More granular speed control
- Element highlight: click a value to track it through the sort
- Sound effects on comparisons/swaps
- Heatmap view: color intensity = activity level
- Grid overlay and interactive legend for pathfinding

**Additional Sorting & Searching Algorithms**
- Heap Sort
- Shell Sort
- Counting Sort
- Radix Sort
- Bucket Sort
- Cocktail Sort
- Comb Sort
- Linear Search visualization
- Binary Search visualization
- Insertion Sort variants

**Data Visualization**
- Tree visualization for tree algorithms
- Graph/network view for graph algorithms
- Matrix heatmap for 2D DP / matrix problems
- Animated transitions for smoother movements
- Trail effects and minimap for large visualizations
- Zoom and pan support for complex boards

---

### TIER 3 – Advanced Learning Features

**Educational Tools**
- Interactive tutorial mode (guided steps per algorithm)
- Quiz system (multiple-choice & practical challenges)
- Challenge mode (e.g., “sort under X comparisons”)
- Downloadable PDF cheat-sheets
- Video links / embedded tutorials per algorithm
- Interactive coding exercises (pseudo-code to complete)
- Algorithm complexity game (“guess the Big‑O”)

**Advanced Functionality**
- Algorithm benchmarking panel (run many sizes & plot results)
- Performance profiling (detailed metrics)
- Automatic worst/best case input generator
- Random seed control for reproducible runs
- Batch testing mode (run multiple algorithms over many inputs)
- Algorithm variants & hybrid strategies (Timsort, Introsort, etc.)

---

### TIER 4 – Platform Features (Optional / Long‑Term)

These are **optional** and may be added later if the project becomes multi-user:

- Multi-language (i18n) support
- Accessibility (A11y) improvements (keyboard nav, ARIA, contrast)
- Offline / PWA support
- User accounts and saved progress
- Analytics dashboard (for usage insights)
- API endpoints for external use

For now, the project is designed as a **single-user learning tool**, with most data stored locally (no login required).

---

## 🧪 Development & Contribution

### Run in Development Mode
Activate venv if you use one
source venv/bin/activate # or venv\Scripts\activate on Windows

Run Flask directly
python app.py

Default URL: `http://localhost:5000`

### Contributions

Contributions are welcome! Please see `CONTRIBUTING.md` for guidelines.

General rules:

- Keep code simple and readable.
- Add comments explaining non-trivial parts of algorithms.
- Keep UI consistent with existing design.
- Test new features thoroughly before opening a pull request.

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it, personally or commercially, as long as the license text is included.

See the `LICENSE` file for details.

---

## 👤 Author

**Your Name**  
- GitHub: https://github.com/YOUR-USERNAME  
- LinkedIn: (optional)  
- Email: (optional)

---

If this project helped you learn algorithms, consider starring the repo ⭐ and sharing it with friends or classmates.

**Happy coding and happy visualizing!** 🚀
