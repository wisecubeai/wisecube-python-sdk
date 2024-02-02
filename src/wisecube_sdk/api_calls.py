import requests

expected_status_codes = [200, 201, 204]


def create_api_call(payload, headers, url, payload_type):
    try:
        if payload_type == "data":
            response = requests.request("POST", url, headers=headers, data=payload)
        else:
            response = requests.request("POST", url, headers=headers, json=payload)
        response.raise_for_status()
        if response.status_code in expected_status_codes:
            return response
        else:
            print(f"Unexpected Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred during the API call:", e)
        return None
