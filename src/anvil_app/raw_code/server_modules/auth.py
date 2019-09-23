import anvil.stripe
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server


def login_request(data):
  if not data:
    return None, anvil.server.HttpResponse(400, "Invalid request. You must submit a JSON body")  
  
  try:
    email = data.get('email')
    api_key = data.get('api_key')
    
    if not email or not api_key:
      return None,anvil.server.HttpResponse(403, "Email and api_key not found")  
       
    user = app_tables.users.get(email=email)
    if not user or not api_key or not user['api_key'] == api_key:
      return None,anvil.server.HttpResponse(403, "Invalid login")  
    
    return user, None
  except Exception as x:
    return None, anvil.server.HttpResponse(403, "Invalid login: {}".format(x))  
