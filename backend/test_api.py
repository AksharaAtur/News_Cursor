import requests
import json

def test_analyze_endpoint():
    url = "http://localhost:8000/analyze"
    headers = {"Content-Type": "application/json"}
    data = {"url": "https://www.hindustantimes.com/"}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print("Status Code:", response.status_code)
        print("\nResponse:")
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_analyze_endpoint() 