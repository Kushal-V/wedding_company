# Backend Intern Assignment - Organization Management Service

A robust, multi-tenant backend service built with **FastAPI** and **MongoDB**, deployed on **Render**.

## 🚀 Live Demo
**Base URL**: https://wedding-company-72b6.onrender.com  
**Interactive API Documentation (Swagger UI)**: [https://wedding-company-72b6.onrender.com/docs](https://wedding-company-72b6.onrender.com/docs)

> **Note for Evaluators**: The application is hosted on a free instance, so the first request might take 30-50 seconds to wake up the server. Please be patient!

---

## 📋 How to Evaluate (Verification Guide)

I have implemented all functional requirements including dynamic collection creation and data migration. Follow these steps to verify:

### 1. Create an Organization
- Go to `/docs` -> **POST /org/create**
- **Payload**:
  ```json
  {
    "organization_name": "my_company",
    "email": "admin@mycompany.com",
    "password": "secure_password"
  }
  ```
- **Result**: Creates a new MongoDB collection `org_my_company` and returns success.

### 2. Login as Admin
- Go to **POST /admin/login**
- **Payload**: Use the same email and password.
- **Result**: Returns a **JWT Access Token**.
- **Action**: Copy the `access_token` (without quotes).

### 3. Authorize
- Click the **Authorize** button (Green padlock) at the top right of Swagger UI.
- Paste the token in the value box.
- Click **Authorize**, then **Close**.

### 4. Verify Protected Endpoints
- **GET /org/get**: Returns your organization details.
- **PUT /org/update**: Try changing the `organization_name` to `my_company_renamed`.
    - **Backend Magic**: This triggers a migration that **renames the underlying MongoDB collection** while preserving data.
- **DELETE /org/delete**: Deletes the organization and drops its collection.

---

## 🛠 Tech Stack
- **Framework**: FastAPI (Python 3.10)
- **Database**: MongoDB (Motor Async Driver)
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: Password hashing with PBKDF2 (SHA256)
- **Deployment**: Dockerized on Render.com

## ✨ Key Features
| Feature | Implementation Details |
| :--- | :--- |
| **Multi-tenancy** | "Shared Database, Separate Collections" architecture. Each Org gets its own collection `org_<name>`. |
| **Dynamic Creation** | Collections are created programmatically upon Organization registration. |
| **Data Migration** | Updating an Organization Name triggers a database-level collection rename to maintain consistency. |
| **Security** | API is protected via OAuth2 (Bearer Token). Admin passwords are encrypted. |

## 🏗 Architecture & Design
For a deep dive into the system architecture, design choices, scalability analysis, and trade-offs, please refer to the **[Design Document (DESIGN.md)](DESIGN.md)**.

## 📦 Local Installation

If you prefer to run it locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kushal-V/wedding_company.git
   cd wedding_company
   ```

2. **Setup Environment**
   Create a `.env` file:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   SECRET_KEY=dev_secret_key
   ```

3. **Run with Docker** (Recommended)
   ```bash
   docker build -t org-service .
   docker run -p 8000:8000 org-service
   ```

4. **Run with Python**
   ```bash
   pip install -r requirements.txt
   python run.py
   ```
