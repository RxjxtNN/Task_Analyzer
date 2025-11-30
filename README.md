# Smart Task Analyzer

## Overview
The Smart Task Analyzer is a Django-based application that intelligently prioritizes tasks using a custom "Dynamic Gravity" algorithm. It helps users decide what to work on first by balancing urgency, importance, effort, and dependencies.

## How to Run

1.  **Prerequisites**: Python 3.8+ installed.
2.  **Setup**:
    ```bash
    # Create and activate virtual environment
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```
3.  **Run Server**:
    ```bash
    python manage.py runserver
    ```
4.  **Access App**: Open `frontend/index.html` in your browser (or go to `http://127.0.0.1:8000/frontend/index.html` if served statically).

## The "Brain": Dynamic Gravity Algorithm

Our scoring algorithm (`tasks/scoring.py`) goes beyond simple addition to model real-world pressure.

### 1. ROI (Return on Investment)
We calculate `Importance / Estimated Hours`.
*   **Why?** High-importance tasks that take little time are "Quick Wins" and should be done early to clear the deck.

### 2. Exponential Urgency
We use a logarithmic curve: `1 + (4 / ln(days_until_due + 2))`.
*   **Why?** Urgency isn't linear. A task due in 30 days is very different from one due in 2 days. As the deadline approaches, the score spikes exponentially.
*   **Past Due**: Tasks due in the past (e.g., 1990) get a fixed high multiplier (5x) to ensure they are flagged immediately.

### 3. Dependency Inheritance
If Task A blocks Task B, Task A inherits **50% of Task B's score**.
*   **Why?** You cannot finish a critical project if a small "low priority" task is blocking it. This feature bubbles up blockers so they don't cause bottlenecks.

## API Endpoints

*   `POST /api/tasks/analyze/`: Accepts a list of tasks, calculates scores, and returns them sorted.
*   `GET /api/tasks/suggest/`: Returns the top 3 tasks for today.

## Project Structure
*   `backend/`: Django settings and configuration.
*   `tasks/`: The logic app containing models, views, and the scoring algorithm.
*   `frontend/`: A clean, responsive UI with sorting controls.
