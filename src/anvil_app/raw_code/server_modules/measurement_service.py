import anvil.stripe
import datetime
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

@anvil.server.callable
def my_measurements():
  user = anvil.users.get_user()
  if not user:
    return []
  
  measurements = app_tables.measurements.search(
    tables.order_by("RecordDate", ascending=True), 
    User=user)
  
  return measurements


@anvil.server.callable
def set_details(height, gender):
  user = anvil.users.get_user()
  if not user:
    raise Exception("You must be logged in.")
  
  user['gender'] = gender
  user['height'] = height
  
  return


@anvil.server.callable
def add_measurement(record_date, weight_in_pounds, resting_heart_rate):
  created_date = datetime.datetime.now()
  user = anvil.users.get_user()
  if not user:
    raise Exception("You must log in to call this method.")
    
  app_tables.measurements.add_row(CreatedDate=created_date, 
                                  RecordDate=record_date, 
                                  RestingHeartRate=resting_heart_rate,
                                  WeightInPounds=weight_in_pounds, 
                                  User=user)


@anvil.server.callable
def averge_for_me():
  user = anvil.users.get_user()
  if not user:
    return None
  
  if not user['height'] or not user['gender']:
    raise Exception("You must set your gender and height.")
  
  ave = app_tables.averages.get(Gender=user['gender'], Height=user['height'])
  return ave


@anvil.server.callable
def go_pro():
  user = anvil.users.get_user()
  if not user:
    return None
  
  user['is_pro'] = True
  

