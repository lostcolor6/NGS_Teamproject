import requests

# FIXME: add timeout
def annotate_vcf_data(data) -> list[dict]:

    url = "http://127.0.0.1:8000/vep/homo_sapiens/hgvs_list"

    try:
        print(data)
        response = requests.post(url, json=data, timeout=30)
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}") 
        return []

    return response.json()