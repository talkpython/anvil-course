import csv
import json
import os
from collections import namedtuple, defaultdict
from typing import List

import requests

Average = namedtuple("Average", 'height, weight, gender, rate')


def main():
    print("Data loader!")
    print("Checking for existing data...")
    if data_exists():
        print("Data exists, skipping upload.")
        return

    print("No data found, loading new data")
    entries = load_csv_data()
    print("Loaded {:,} entries".format(len(entries)))

    email, password = load_auth()
    if not email:
        print("You need to login:")
        email = input('email: ')
        password = input('password: ')
        save_auth(email, password)

    averaged_entries = average_entries(entries)
    for a in averaged_entries:
        print("Uploading {}".format(a))
        upload_average(a, email, password)

    print("Done, uploaded {:,} averages.".format(len(averaged_entries)))


def upload_average(a: Average, email, password):
    data = {
        'api_key': 'abc',
        'weight_in_lbs': a.weight,
        'resting_heart_rate': a.rate,
        'height_in_inches': a.height,
        'rate': a.rate,
        'gender': a.gender,
        'email': email,
        'password': password,
    }

    resp = requests.post('https://plastic-careless-kodiak-bear.anvil.app/_/api/load_average', json=data)
    print(resp.status_code, resp.text)
    resp.raise_for_status()


def save_auth(email, password):
    with open('account.json', 'w', encoding='utf-8') as fout:
        data = dict(email=email, password=password)
        json.dump(data, fout)

    return data.get('email'), data.get('password')


def load_auth():
    if not os.path.exists('account.json'):
        return None, None

    with open('account.json', 'r', encoding='utf-8') as fin:
        data = json.load(fin)

    return data.get('email'), data.get('password')


def data_exists():
    url = 'https://plastic-careless-kodiak-bear.anvil.app/_/api/count_averages'
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.json().get('count') > 0


def load_csv_data() -> List[Average]:
    entries = []
    with open('weight-height.csv') as fin:
        reader = csv.DictReader(fin)
        for r in reader:
            height = float(r['Height'])
            weight = float(r['Weight'])
            gender = r['Gender'].strip()
            rate = 80  # Just got with the average for people for now.

            height_in_inches = int(height)  # * 2.54 * 100)
            weight_in_lbs = weight  # * 2.20462)

            entries.append(Average(height=height_in_inches, weight=weight_in_lbs, rate=rate, gender=gender))

    return entries


def average_entries(entries: List[Average]) -> List[Average]:
    averaged = []

    data = defaultdict(list)
    for e in entries:
        data[(e.gender, e.height)].append(e)
        # print(type(data[(e.gender, e.weight)]), data[(e.gender, e.weight)])

    for k, v in data.items():
        # print(k, v)
        weight = sum(i.weight for i in v) / len(v)
        averaged.append(Average(height=k[1], weight=weight, gender=k[0], rate=v[0].rate))

    return averaged


if __name__ == '__main__':
    main()
