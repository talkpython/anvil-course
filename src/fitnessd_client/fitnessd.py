import datetime

import svc
import auth


def main():
    auth.load_auth()
    if not auth.is_authorized():
        auth_data = get_auth_data()
        email = auth_data.get('email')
        password = auth_data.get('password')
        api_key = svc.authenticate(email, password)
        auth.save_auth(email, api_key)
    else:
        email = auth.email
        api_key = auth.api_key

    if not api_key:
        print("Invalid login")
        return

    data = get_user_data()
    print(api_key)
    result = svc.save_measurement(api_key, email, data)
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
