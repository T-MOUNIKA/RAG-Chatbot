import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test chat endpoint with a question about Docker
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"question": "What is Docker?"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Docker question: {response.status_code}")
        if response.status_code == 200:
            print(f"Answer: {response.json()['answer']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Docker question failed: {e}")
    
    # Test with a question not in documents
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"question": "What is the weather today?"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Weather question: {response.status_code}")
        if response.status_code == 200:
            print(f"Answer: {response.json()['answer']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Weather question failed: {e}")

if __name__ == "__main__":
    test_api()