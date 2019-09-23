import anvil.stripe
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import uuid
import datetime
import auth


@anvil.server.http_endpoint('/authorize')
def authorize():
  data = anvil.server.request.body_json
  if not data:
    return anvil.server.HttpResponse(400, 'You must submit a JSON body via POST')
  
  email = data.get('email')
  password = data.get('password')
  
  if not email or not password:
    return anvil.server.HttpResponse(400, 'Email and password are required')
  
  try:
    user = anvil.users.login_with_email(email, password)
    if not user:
      return anvil.server.HttpResponse(403, 'Invalid login.')
  except anvil.users.AuthenticationFailed:
      return anvil.server.HttpResponse(403, 'Invalid login.')
  
  api_key_mode = "existing"
  if not user['api_key']:
    user['api_key'] = str(uuid.uuid4())
    api_key_mode = "created"
    
  return {'api_key': user['api_key'], "mode": api_key_mode}
  



@anvil.server.http_endpoint('/add_measurement')
def add_measurement():
  data = anvil.server.request.body_json
  user, error = auth.login_request(data)
  
  if error:
    return error
  
  weight = int(data.get('weight', 0))
  rate = int(data.get('rate', 0))
  recorded = datetime.datetime.strptime(data.get('recorded'), '%Y-%m-%d').date()
  
  app_tables.measurements.add_row(
    User=user,
    CreatedDate=datetime.datetime.now(), 
    RecordDate=recorded, 
    RestingHeartRate=rate, 
    WeightInPounds=weight)
  
  return {
    'success': True
  }


@anvil.server.http_endpoint('/hello/:name')
def hello(name, **query_params):
  return {
    'message': 'Hello {} from the API'.format(name),
    'body': anvil.server.request.body_json,
    'query': query_params
  }


