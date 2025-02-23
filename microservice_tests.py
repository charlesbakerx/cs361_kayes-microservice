import requests

BASE_URL = "http://127.0.0.1:5000"

# Test data
TEST_USER = {
    "username": "testuser",
    "password": "testpassword"
}

INVALID_USER = {
    "username": "invaliduser",
    "password": "invalidpassword"
}


def test_register():
    """Test user registration."""
    print("Registering user...")
    response = requests.post(f"{BASE_URL}/register", json=TEST_USER)
    print("Response:", response.status_code, response.json())

    if response.status_code == 201:
        print("✔ User registered successfully.")
    elif response.status_code == 400:
        print("✔ User already exists.")
    else:
        print("✖ Registration failed.")


def test_login(user=TEST_USER):
    """Test user login and retrieve access token."""
    print("Logging in...")
    response = requests.post(f"{BASE_URL}/login", json=user)
    print("Response:", response.status_code, response.json())

    if response.status_code == 200:
        token = response.json().get('access_token')
        print("✔ Login successful. Token retrieved.")
        return token
    else:
        print("✖ Login failed.")
        return None


def test_get_tasks(token):
    """Test fetching tasks using the token."""
    print("Fetching tasks...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    print("Response:", response.status_code, response.json())

    if response.status_code == 200:
        print("✔ Tasks retrieved successfully.")
    elif response.status_code == 401:
        print("✖ Unauthorized request (Invalid or missing token).")
    else:
        print("✖ Failed to fetch tasks.")


def test_logout(token):
    """Test user logout."""
    print("Logging out...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    print("Response:", response.status_code, response.json())

    if response.status_code == 200:
        print("✔ Logout successful.")
    elif response.status_code == 401:
        print("✖ Unauthorized request (Invalid or missing token).")
    else:
        print("✖ Logout failed.")


if __name__ == "__main__":
    print(f"\nTesting registration for a new user: {TEST_USER['username']}...")
    test_register()
    print(f"\nTesting registration for an existing user: {
          TEST_USER['username']}...")
    test_register()

    print(f"\nTesting login for an invalid user: {
          INVALID_USER['username']}...")
    invalid = test_login(INVALID_USER)
    print(f"\nTesting login for a valid user: {TEST_USER['username']}...")
    token = test_login()

    if token:
        print(f"\nTesting task fetching for user: {
              TEST_USER['username']} with token: {token}...")
        test_get_tasks(token)

        print(f"\nTesting logout for user: {
              TEST_USER['username']} with token: {token}...")
        test_logout(token)

    print(f"\nTesting task fetching for user {
          TEST_USER['username']} after logout...")
    test_get_tasks(token)

    print(f"\nTesting logging back in for user: {TEST_USER['username']}...")
    token = test_login()

    print(f"\nTesting task fetching for user: {
          TEST_USER['username']} with token: {token}...")
    test_get_tasks(token)

    print("\nTesting task fetching with no access token...")
    token = ""
    test_get_tasks(token)
