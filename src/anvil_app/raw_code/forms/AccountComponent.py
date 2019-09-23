from anvil import *
import stripe.checkout
import anvil.users
import data_access
import navigation

class AccountComponent(AccountComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    user = data_access.the_user()
    height = user['height']
    
    self.label_value_inches.text = \
      self.label_value_inches.text.format(value=height)
    self.label_gender.text = user['gender']
    self.label_account_type.text = "Pro" if user['is_pro'] else 'Basic'
    self.button_go_pro.visible = user['is_pro'] is None or not user['is_pro'] 

  def button_go_pro_click(self, **event_args):
    self.label_error.visible = False
    
    try:
      # Take a payment of $9.99
      user = data_access.the_user()
      charge = stripe.checkout.charge(amount=999,
                                      data_email=user['email'],
                                      allow_remember_me=False,
                            currency="USD",
                            title="Fitnessd",
                            description="Fitnessd Pro")
  
      if charge.get('result') == 'succeeded':
        data_access.go_pro()
        navigation.go_account()
      else:
        self.label_error.visible = True
        self.label_error.text = "Oops, that failed."
    except Exception as x:
      if 'Stripe checkout failed' in str(x):
        self.label_error.text = "Purchase cancelled."  
      else:
        self.label_error.text = "Error: {}".format(x)  
    
    
    
    
    
    
    