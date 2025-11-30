# Deployment Guide (Render.com)

This guide explains how to deploy your **Smart Task Analyzer** to Render for free.

## 1. Prepare Your Code (Already Done!)
I have already:
*   Installed `gunicorn` (Production Server) and `whitenoise` (Static Files).
*   Configured `settings.py` to allow all hosts and serve static files.
*   Created a `.gitignore` file.
*   Updated `requirements.txt`.

## 2. Push to GitHub
1.  Create a new repository on [GitHub](https://github.com/new). Name it `task-analyzer`.
2.  Open your terminal in the `task-analyzer` folder and run:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/task-analyzer.git
    git push -u origin main
    ```

## 3. Deploy on Render
1.  Sign up/Log in to [Render.com](https://render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub account and select the `task-analyzer` repo.
4.  **Configuration**:
    *   **Name**: `smart-task-analyzer` (or similar)
    *   **Region**: Closest to you.
    *   **Branch**: `main`
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    *   **Start Command**: `gunicorn backend.wsgi:application`
    *   **Instance Type**: Free
5.  Click **Create Web Service**.

## Important Note on Database
Since we are using **SQLite** (a file-based database) on the Free Tier:
*   **Data Persistence**: Render's free tier filesystem is *ephemeral*. This means **every time you deploy or the app restarts, your tasks will be wiped.**
*   **Solution**: For a permanent app, you would need a PostgreSQL database (Render offers a free trial for 90 days, or paid plans). For this demo, SQLite is fine, just know that data resets.
