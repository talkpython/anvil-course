import csv
from collections import defaultdict
from typing import List

import auth
import svc


def main():
    print("Data loader!")
    print("Checking for existing data...")
    if svc.data_exists():
        print("Data exists, skipping upload.")
        return

    print("No data found, loading new data")
    entries = load_csv_data()
    print("Loaded {:,} entries".format(len(entries)))

    auth.load_auth()
    if not auth.email:
        print("You need to login:")
        email = input('email: ')
        password = input('password: ')

        api_key = svc.authorize(email, password)
        auth.save_auth(email, api_key)
        print("Login successful.", flush=True)

    averaged_entries = average_entries(entries)
    print("Computed {:,} averages from raw data.".format(len(averaged_entries)))

    for a in averaged_entries:
        print("Uploading {}".format(a))
        svc.upload_average(a, auth.email, auth.api_key)

    print("Done, uploaded {:,} averages.".format(len(averaged_entries)))


def load_csv_data() -> List[svc.Average]:
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

            entries.append(svc.Average(height=height_in_inches, weight=weight_in_lbs, rate=rate, gender=gender))

    return entries


def average_entries(entries: List[svc.Average]) -> List[svc.Average]:
    averaged = []

    data = defaultdict(list)
    for e in entries:
        data[(e.gender, e.height)].append(e)
        # print(type(data[(e.gender, e.weight)]), data[(e.gender, e.weight)])

    for k, v in data.items():
        # print(k, v)
        weight = sum(i.weight for i in v) / len(v)
        averaged.append(svc.Average(height=k[1], weight=weight, gender=k[0], rate=v[0].rate))

    return averaged


if __name__ == '__main__':
    main()
