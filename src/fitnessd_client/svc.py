from typing import Optional

import requests

base_url = 'https://fresh-zealous-song.anvil.app/_/api/'


def authenticate(email, password) -> Optional[str]:
    body = {
        'email': email,
        'password': password,
    }
    url = base_url + 'authorize'
    resp = requests.post(url, json=body)
    if not resp.status_code == 200:
        return None

    return resp.json().get('api_key')


def save_measurement(api_key: str, email: str, data: dict):
    url = base_url + 'add_measurement'
    auth = {
        "email": email,
        "api_key": api_key,
    }
    data.update(auth)

    resp = requests.post(url, json=data)
    print("Server response", resp.text)
    return resp.status_code == 200
