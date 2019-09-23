import anvil.stripe
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import auth


@anvil.server.http_endpoint("/load_average")
def load_average():  
  data = anvil.server.request.body_json
  if not data:
    return anvil.server.HttpResponse(400, "Invalid request. You must submit a JSON body")  
  
  user, error_response = auth.login_request(data)
  
  if error_response:
    return error_response
  
  weight_in_lbs = float(data.get('weight_in_lbs'))
  height_in_inches = int(data.get('height_in_inches'))
  gender = data.get('gender')
  rate = int(data.get('rate'))
  
  result = save_average(gender, height_in_inches, weight_in_lbs, rate)
  
  return {
    'weight_in_lbs': weight_in_lbs,
    'height_in_inches': height_in_inches,
    'gender': gender, 
    'result': result
  }


@anvil.server.http_endpoint("/count_averages")
def count_averages():
  return {'count': len(app_tables.averages.search())}


def save_average(gender, height_in_inches, weight_in_lbs, rate):
  entry = app_tables.averages.get(Gender=gender, Height=height_in_inches)
  if entry:
    entry["Weight"] = weight_in_lbs
    entry["Rate"] = rate
    return "updated"
  else:
    app_tables.averages.add_row(Gender=gender,Height=height_in_inches, Weight=weight_in_lbs, Rate=rate)
    return "added"

