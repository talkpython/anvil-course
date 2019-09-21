import datetime

import svc


def main():
    auth_data = get_auth_data()
    api_key = svc.authenticate(auth_data)
    if not api_key:
        print("Invalid login")
        return

    data = get_user_data()
    print(api_key)
    result = svc.save_measurement(api_key, auth_data.get('email'), data)
    if result:
        print("Done!")
    else:
        print("Could not save measurement")


def get_user_data() -> dict:
    print("Enter a measurement:")
    rate = int(input("Resting heart rate: "))
    weight = int(input("Weight in pounds: "))
    recorded = datetime.date.today().isoformat()

    return {
        'rate': rate,
        'weight': weight,
        'recorded': recorded,
    }


def get_auth_data() -> dict:
    email = input("What is your email: ")
    password = input("What is your password: ")
    print()
    return {
        'email': email,
        'password': password,
    }


if __name__ == '__main__':
    main()
