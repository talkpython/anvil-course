from anvil import *
import stripe.checkout
import data_access
import navigation

class SetHeightComponent(SetHeightComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_save_click(self, **event_args):
    if not self.text_box_height.text:
      self.label_error.text = "You must set your height"
      return
    
    if self.drop_down_gender.selected_value == self.drop_down_gender.items[0]:
      self.label_error.text = "You must set your gender"
      return
    
    height = int(self.text_box_height.text)
    gender = self.drop_down_gender.selected_value
    
    data_access.set_details(height, gender)
    navigation.go_account()
