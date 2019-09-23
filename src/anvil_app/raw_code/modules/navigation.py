import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from AddMeasurementComponent import AddMeasurementComponent
from HomeAnonComponent import HomeAnonComponent
from CompareComponent import CompareComponent
from AccountComponent import AccountComponent
from HomeDetailsComponent import HomeDetailsComponent
from SetHeightComponent import SetHeightComponent
from SetHeightComponent import SetHeightComponent
import data_access

home_form = None

def get_form():
  if not home_form:
    raise Exception("You must set the home form first.")
    
  return home_form
            
def go_add():
  set_title("Add Measurement")
  set_active_nav('add')
  
  user = require_account()
  if not user:
    go_home()
    return
  
  form = get_form()
  form.load_component(AddMeasurementComponent())
  
def go_home():
  set_active_nav('home')
  set_title("")
  form = get_form()
  user = anvil.users.get_user()
  if user:
    form.load_component(HomeDetailsComponent())
  else:
    form.load_component(HomeAnonComponent())

def go_compare():
  set_active_nav('compare')
  set_title("Compare")
  
  user = require_account()
  if not user:
    go_home()
    return
  
  if not user['gender']:
    go_set_details()
    return
    
  form = get_form()
  form.load_component(CompareComponent())

def go_account():
  set_active_nav('account')
  set_title("Your account")
  
  user = require_account()
  if not user:
    go_home()
    return
  
  if not user['gender']:
    go_set_details()
    return
  
  form = get_form()
  form.load_component(AccountComponent())

  
def go_set_details():
  set_active_nav(None)
  set_title(None)
  form = get_form()
  form.load_component(SetHeightComponent())
  
  
def set_active_nav(state):
  form = get_form()
  form.set_active_nav(state)
  
def set_title(text):
  form = get_form()
  base_title = form.base_title
  
  if text:
    form.label_title.text = base_title + " - " +  text
  else:
    form.label_title.text = base_title

    
def require_account():
    user = data_access.the_user()
    if user:
      return user
    
    user = anvil.users.login_with_form(allow_cancel=True)
    form = get_form()
    form.set_account_state(user)
    return user
    
    