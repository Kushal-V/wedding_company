# Organization Management Service

## Overview
A Backend Service built with **FastAPI** and **MongoDB** for managing multi-tenant organizations.
Features include creating organizations with dynamic collections, authenticating admins via JWT, and handling data migrations during updates.

## Requirements
- Python 3.10+
- MongoDB (running on localhost:27017)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup Environment Variables:
   Create a `.env` file in the `app` folder or root (already provided):
   ```
   MONGODB_URL=mongodb://localhost:27017
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ```

## Running the Application

Start the server using:
```bash
python run.py
```
Or directly with uvicorn:
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`
API Documentation (Swagger UI): `http://localhost:8000/docs`

## API Endpoints

- **POST** `/org/create`: Create a new Organization (Master DB + Dynamic Collection).
- **POST** `/admin/login`: Login as Org Admin (Returns JWT).
- **GET** `/org/get`: Get Organization details (Protected).
- **PUT** `/org/update`: Update Organization details. Renaming triggers collection migration (Protected).
- **DELETE** `/org/delete`: Delete Organization and its collection (Protected).

## Architecture

- **Master Database**: Stores metadata (`organizations` collection).
- **Dynamic Collections**: Each organization gets a dedicated collection `org_<name>`.
- **Authentication**: JWT based. Passwords hashed using PBKDF2 (SHA256).

## Testing

### Option 1: Visual Testing (Recommended)
FastAPI provides an automatic interactive API documentation.
1. Run the app: `python run.py`.
2. Open your browser to: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.
3. You can click on endpoints, click "Try it out", fill in data, and see the response.

### Option 2: Script
Run the verification script:
```bash
python test_api.py
```

## Database Query ("How it works")
You do not need to manually "create" a database in MongoDB.
- MongoDB is **schema-less** and uses **lazy creation**.
- When the code executes `insert_one(new_org)`, MongoDB checks if the database exists. If not, it creates it.
- Then it checks if the collection (table) exists. If not, it creates it.
- This is why you didn't have to run any `CREATE DATABASE` commands.

## Deployment (Optional)

To deploy this service (e.g., on Railway, Render, or Heroku), you need:
1.  **Cloud Database**: Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/atlas/database).
    - Get the Connection String (e.g., `mongodb+srv://user:pass@cluster...`).
2.  **Environment Variables**:
    - Set `MONGODB_URL` to your Atlas Connection String in the cloud provider's settings.
    - Set `SECRET_KEY` to a secure string.
3.  **Deploy**:
    - Push this code to GitHub.
    - Connect your GitHub repo to the Cloud Provider.
    - It will detect the `Dockerfile` or `requirements.txt` and build automatically.
