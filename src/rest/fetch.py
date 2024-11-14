import requests
import json

def fetch_url_text(url, data):
    try:
        # Ensure data is a dictionary
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        # Send POST request with JSON data and appropriate headers
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except ValueError as ve:
        print(f"Invalid data: {ve}")
        return None

if __name__ == "__main__":
    test_url = "http://127.0.0.1:8000/vep"
    response_text = fetch_url_text(test_url, {"chrom": "chr1", "pos": 9721354, "ref": "C", "alt": "G"})
    print(response_text)
    print(type(response_text))
