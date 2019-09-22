from collections import namedtuple

import requests

base_url = 'https://fresh-zealous-song.anvil.app/_/api/'
Average = namedtuple("Average", 'height, weight, gender, rate')


def upload_average(a: Average, email, api_key):
    url = base_url + 'load_average'
    data = {
        'api_key': api_key,
        'weight_in_lbs': a.weight,
        'resting_heart_rate': a.rate,
        'height_in_inches': a.height,
        'rate': a.rate,
        'gender': a.gender,
        'email': email
    }

    resp = requests.post(url, json=data)
    print(resp.status_code, resp.text)
    resp.raise_for_status()


def authorize(email, password):
    url = base_url + 'authorize'

    data = {
        'email': email,
        'password': password,
    }

    resp = requests.post(url, json=data)
    resp.raise_for_status()

    api_key = resp.json().get('api_key')

    return api_key


def data_exists():
    url = base_url + 'count_averages'
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.json().get('count') > 0
