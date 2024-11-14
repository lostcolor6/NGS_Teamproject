import requests
import json

def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.text  # Return the raw content of the response as a string
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def json_to_dict(json_string):
    try:
        # Parse the JSON string into a Python list of dictionaries
        if not json_string:
            return {}
        list_of_dicts = json.loads(json_string)
        return list_of_dicts
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

def apifetch(url):
    string = fetch_data_from_api(url)
    dicts = json_to_dict(string)
    return dicts

if __name__ == "__main__":
    print("Fetching hpo with id = HP:0033997")
    data = apifetch("http://127.0.0.1:8000/hpo_id/HP:0033997")
    for i in data:
        print(i)
