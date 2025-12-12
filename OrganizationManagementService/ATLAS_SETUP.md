# MongoDB Atlas Setup Guide

This guide will help you create a free cloud database to deploy your application.

## Step 1: Create an Account
1.  Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register).
2.  Sign up for a free account.

## Step 2: Create a Cluster
1.  After logging in, click **+ Create** (or Build a Database).
2.  Select the **M0 Free** option (Shared Cluster).
3.  Choose a Cloud Provider (AWS, Google Cloud, or Azure) and a Region.
4.  Click **Create Deployment**.

## Step 3: Configure Security (Crucial!)
You will be prompted to set up security. Do NOT skip this.

### A. Create a Database User
1.  Enter a **Username** (e.g., `admin`).
2.  Enter a **Password**. **Important: specific special characters in passwords might break the connection string. Use alphanumeric characters to be safe.**
3.  Click **Create Database User**.

### B. Network Access (IP Whitelist)
1.  Scroll down to "Network Access" or click it in the sidebar.
2.  Click **+ Add IP Address**.
3.  Select **Allow Access from Anywhere** (IP Address `0.0.0.0/0`).
    - *Why?* Because cloud hosting services (like Railway or Render) change IPs frequently.
4.  Click **Confirm**.

## Step 4: Get Connection String
1.  Go back to the **Database** tab (click "Database" in the sidebar).
2.  Click the **Connect** button on your Cluster card.
3.  Select **Drivers**.
4.  Under "Select your driver and version", choose:
    - **Driver**: Python
    - **Version**: 3.6 or later
5.  **Copy the Connection String**. It will look like this:
    ```
    mongodb+srv://admin:<db_password>@cluster0.xyz.mongodb.net/?retryWrites=true&w=majority
    ```

## Step 5: Connect Your Application
1.  Paste the string into a text editor.
2.  Replace `<db_password>` with the password you created in Step 3A.
    - Example: If password is `secure123`, the string becomes:
      `mongodb+srv://admin:secure123@cluster0.xyz.mongodb.net/?retryWrites=true&w=majority`
3.  **For Deployment**: Copy this final string and use it as the value for the `MONGODB_URL` environment variable.
