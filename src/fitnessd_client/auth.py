from typing import Optional
import json
import os

email: Optional[str] = None
api_key: Optional[str] = None


def is_authorized() -> bool:
    global email, api_key
    return email is not None and api_key is not None


def save_auth(email_address, key):
    global email, api_key
    email = email_address
    api_key = key

    with open('account.json', 'w', encoding='utf-8') as fout:
        data = dict(email=email_address, api_key=key)
        json.dump(data, fout)

    return


def load_auth():
    global email, api_key
    email = None
    api_key = None

    if not os.path.exists('account.json'):
        return

    with open('account.json', 'r', encoding='utf-8') as fin:
        data = json.load(fin)

    email = data.get('email')
    api_key = data.get('api_key')
