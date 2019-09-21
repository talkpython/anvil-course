import datetime

import svc
import auth
import dateutil.parser
from gooey import Gooey, GooeyParser


@Gooey(program_name="Fitnessd Local", show_success_modal=False)
def main():
    auth.load_auth()

    parser = GooeyParser(description="Fitnessd local edition - record your health on the go!")

    if not auth.is_authorized():
        parser.add_argument("Email", default=auth.email)
        parser.add_argument("Password", widget="PasswordField")

    parser.add_argument('Rate', help="Resting heart rate", type=int)
    parser.add_argument('Weight', help="Weight in pounds", type=int)
    parser.add_argument('Date', help="Date of measurement", widget="DateChooser", default=datetime.date.today())

    data = parser.parse_args()
    rate = int(data.Rate)
    weight = int(data.Weight)
    recorded = dateutil.parser.parse(data.Date)

    if not auth.is_authorized():
        email = data.Email
        password = data.Password
        api_key = svc.authenticate(email, password)
        if not api_key:
            print("Error authenticating")
            return
        else:
            print("Login successful")
        auth.save_auth(email, api_key)

    result = svc.save_measurement(auth.api_key, auth.email, rate, weight, recorded)
    if result:
        print("Done!")
    else:
        print("Error: Could not save measurement")



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
