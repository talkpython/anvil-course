from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import navigation
import data_access

class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.base_title = self.label_title.text
    user = data_access.the_user()
    self.set_account_state(user)
    navigation.home_form = self
    navigation.go_home()

  def link_add_click(self, **event_args):
    navigation.go_add()
    
  def link_home_click(self, **event_args):
    navigation.go_home()

  def link_compare_click(self, **event_args):
    navigation.go_compare()

  def link_account_click(self, **event_args):
    navigation.go_account()

  def link_register_click(self, **event_args):
    user = anvil.users.signup_with_form(allow_cancel=True)
    self.set_account_state(user)
    navigation.go_home()

  def link_login_click(self, **event_args):
    user = anvil.users.login_with_form(allow_cancel=True)
    self.set_account_state(user)
    navigation.go_home()

  def link_logout_click(self, **event_args):
    anvil.users.logout()
    self.set_account_state(None)
    data_access.logout()
    navigation.go_home()
  
  def set_active_nav(self, state):
    self.link_home.role = 'selected' if state == 'home' else None
    self.link_add.role = 'selected' if state == 'add' else None
    self.link_compare.role = 'selected' if state == 'compare' else None
  
  def load_component(self, cmpt):
    self.column_panel_content.clear()
    self.column_panel_content.add_component(cmpt)
    
    if data_access.the_user():
      self.set_account_state(data_access.the_user())

  def set_account_state(self, user):
    self.link_account.visible = user is not None
    self.link_logout.visible = user is not None
    self.link_login.visible = user is None
    self.link_register.visible = user is None





