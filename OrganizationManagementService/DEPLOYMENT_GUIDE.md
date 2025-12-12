# Deployment Guide

This guide will help you deploy your Organization Management Service to **Render** (Free Tier available) using the Dockerfile.

## PREREQUISITIES
1.  **GitHub Account**: You must have the code pushed to a GitHub repository.
2.  **MongoDB Atlas**: You already have this! Keep your connection string handy.
    - Connection String: `mongodb+srv://kv2365_db_user:Kv%409063321@cluster0.y4y5jmu.mongodb.net/?appName=Cluster0`

## Step 1: Push Code to GitHub
1.  Initialize Git in your project folder (if not done):
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on [GitHub.com](https://github.com/new).
3.  Push your code:
    ```bash
    git remote add origin <your-repo-url>
    git branch -M main
    git push -u origin main
    ```

## Step 2: Deploy on Render.com
1.  Sign up/Log in to [Render](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Select **Build and deploy from a Git repository**.
4.  Connect your GitHub account and select your repository.
5.  **Configuration**:
    - **Name**: `organization-service` (or any name)
    - **Region**: Closest to you (e.g., Singapore)
    - **Branch**: `main`
    - **Runtime**: `Docker` (It should detect the Dockerfile automatically)
    - **Instance Type**: `Free`
6.  **Environment Variables** (Crucial!):
    - Scroll down to "Environment Variables" section.
    - Add Key: `MONGODB_URL`
    - Add Value: `mongodb+srv://kv2365_db_user:Kv%409063321@cluster0.y4y5jmu.mongodb.net/?appName=Cluster0`
    - Add Key: `SECRET_KEY`
    - Add Value: `any-secure-random-string`
7.  Click **Create Web Service**.

## Step 3: Verification
1.  Render will build the Docker image (takes a few minutes).
2.  Once deployed, it will give you a URL (e.g., `https://organization-service.onrender.com`).
3.  Go to `https://<YOUR-URL>/docs` to see the live API!
