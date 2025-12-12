import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def log(msg, data=None):
    print(f"\n[TEST] {msg}")
    if data:
        print(json.dumps(data, indent=2))

def test_flow():
    # 1. Create Organization
    org_name = f"test_inc_{int(time.time())}"
    create_payload = {
        "organization_name": org_name,
        "email": f"admin@{org_name.replace('_', '-')}.com",
        "password": "secret_password"
    }
    
    log("Creating Organization...", create_payload)
    try:
        resp = requests.post(f"{BASE_URL}/org/create", json=create_payload)
        print(f"DEBUG: Status Code: {resp.status_code}")
        print(f"DEBUG: Response Text: {resp.text}")
    except Exception as e:
        print(f"DEBUG: Request failed: {e}")
        return

    if resp.status_code != 200:
        log("Creation Failed", resp.json() if resp.text else "Empty Response")
        return
    log("Creation Success", resp.json())
    
    # 2. Admin Login
    login_payload = {
        "email": f"admin@{org_name.replace('_', '-')}.com",
        "password": "secret_password"
    }
    log("Logging in...", login_payload)
    resp = requests.post(f"{BASE_URL}/admin/login", json=login_payload)
    if resp.status_code != 200:
        log("Login Failed", resp.json())
        return
    token_data = resp.json()
    log("Login Success", token_data)
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Get Organization
    log(f"Fetching Organization: {org_name}...")
    resp = requests.get(f"{BASE_URL}/org/get", params={"organization_name": org_name}, headers=headers)
    log("Get Result", resp.json())
    assert resp.status_code == 200, "Failed to get organization"
    
    # 4. Update Organization (Rename)
    new_org_name = f"{org_name}_renamed"
    update_payload = {
        "organization_name": new_org_name,
        "email": f"admin@{org_name.replace('_', '-')}.com", # Keeping email same for now
        "password": "new_secret_password"
    }
    log(f"Updating Organization to: {new_org_name}...", update_payload)
    resp = requests.put(f"{BASE_URL}/org/update", json=update_payload, headers=headers)
    log("Update Result", resp.json())
    if resp.status_code != 200:
        return
        
    # 5. Verify Rename (Login with new info? No email didn't change, but token might have claimed old org name)
    # The current token has "org_name" inside it. 
    # If we access /org/get with OLD token but NEW name, logic says:
    # "if organization_name != current_admin.org_name: 403"
    # So technically, after a rename, the old token is invalid for the new name.
    # We need to re-login? The Requirements didn't specify token invalidation behavior on update.
    # But for this test, let's see if we can get the NEW name with OLD token? 
    # It will fail our check: `if organization_name != current_admin.org_name`.
    # Let's try to login again.
    
    login_payload["password"] = "new_secret_password" # Password changed
    log("Logging in again...", login_payload)
    resp = requests.post(f"{BASE_URL}/admin/login", json=login_payload)
    log("Re-Login Result", resp.json())
    new_token = resp.json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}
    
    # 6. Delete Organization using NEW name
    log(f"Deleting Organization: {new_org_name}...")
    resp = requests.delete(f"{BASE_URL}/org/delete", params={"organization_name": new_org_name}, headers=new_headers)
    log("Delete Result", resp.json())
    assert resp.status_code == 200, "Failed to delete organization"

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(e)
