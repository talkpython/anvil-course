import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

__measurements = []
__user = None
__my_ave = None

def my_measurements():
  global __measurements
  
  if __measurements:
    # print("Using {} cached measurements".format(len(__measurements)))
    return __measurements
  
  __measurements = list(anvil.server.call('my_measurements'))
  return __measurements


def add_measurement(record_date, weight_in_pounds, resting_heart_rate):
  global __measurements
  __measurements = []
  
  anvil.server.call('add_measurement', record_date, weight_in_pounds, resting_heart_rate)

  
def set_details(height, gender):
  global __user
  anvil.server.call('set_details', height, gender)
  __user = None
  
def the_user():
  global __user
  
  if __user:
    # print("Using cached user: {}".format(__user['email']))
    return __user
  
  __user = anvil.users.get_user()
  return __user

def logout():
  global __user, __my_ave, __measurements
  __measurements = []
  __my_ave = None
  __user = None
  
def average_for_me():
  global __my_ave
  if __my_ave:
    return __my_ave
  
  __my_ave = anvil.server.call('averge_for_me')
  return __my_ave


def go_pro():
  global __user
  __user = None
  
  anvil.server.call('go_pro')
