from anvil import *
import stripe.checkout
import data_access

class CompareComponent(CompareComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
    user = data_access.the_user()
    self.label_subtitle.text = self.label_subtitle.text.format(
        gender=user['gender'], height=self.compute_feet(user['height'])  
      )
    self.label_no_data.text = self.label_no_data.text.format(
      gender=user['gender'], height=self.compute_feet(user['height'])  
      )
    
    ave = data_access.average_for_me()
    
    measurements = data_access.my_measurements()
    measurement = None
    if measurements and ave:
      self.label_weight.text = self.label_weight.text.format(value = ave['Weight'])
      self.label_rate.text = self.label_rate.text.format(value = ave['Rate'])
      
      measurement = measurements[0]
      w = measurement['WeightInPounds']
      dw = w - ave['Weight']
      self.label_your_weight.text = self.label_your_weight.text.format(
        original=w,
      sign=self.compute_sign(dw),
      value=abs(dw))
      
      r = measurement['RestingHeartRate']
      dr = r - ave['Rate']
      self.label_your_rate.text = self.label_your_rate.text.format(
        original=r,
      sign=self.compute_sign(dr),
      value=abs(dr))
      
    self.card_no_data.visible = measurement is None
    self.card_data.visible = measurement is not None
    
  def compute_feet(self, inches):
    feet = int(inches / 12)
    inches = int(inches % 12)
    
    return "{} feet, {} inches".format(feet, inches)
    
  def compute_sign(self, num):
    if num > 0:
      return '+'
    elif num < 0:
      return '-'
    else:
      return ''
