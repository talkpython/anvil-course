from anvil import *
import stripe.checkout
import plotly.graph_objs as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import data_access
import navigation

class HomeDetailsComponent(HomeDetailsComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    measurements = data_access.my_measurements()

    self.card_no_data.visible = len(measurements) == 0
    self.card_with_data.visible = len(measurements) > 0
    
    self.setup_graph()
    self.load_data()

  def setup_graph(self):
    # Configure the plot layout
    self.plot_weight_history.layout.title = 'Your quantitative self'
    
    self.plot_weight_history.layout.xaxis.title = 'Day'
    self.plot_weight_history.layout.xaxis.showgrid = True
    self.plot_weight_history.layout.xaxis.zeroline=True,
    self.plot_weight_history.layout.xaxis.showline=True
    self.plot_weight_history.layout.xaxis.mirror='ticks'
    self.plot_weight_history.layout.xaxis.gridcolor='#bdbdbd'
    self.plot_weight_history.layout.xaxis.gridwidth=2
    self.plot_weight_history.layout.xaxis.zerolinecolor='#969696'
    self.plot_weight_history.layout.xaxis.zerolinewidth=4
    self.plot_weight_history.layout.xaxis.linecolor='#636363'
    self.plot_weight_history.layout.xaxis.linewidth=6
    
    self.plot_weight_history.layout.yaxis.title = 'Lbs and BPM'
    self.plot_weight_history.layout.yaxis.showgrid=True,
    self.plot_weight_history.layout.yaxis.zeroline=True
    self.plot_weight_history.layout.yaxis.showline=True
    self.plot_weight_history.layout.yaxis.mirror='ticks'
    self.plot_weight_history.layout.yaxis.gridcolor='#bdbdbd'
    self.plot_weight_history.layout.yaxis.gridwidth=2
    self.plot_weight_history.layout.yaxis.zerolinecolor='#969696'
    self.plot_weight_history.layout.yaxis.zerolinewidth=4
    self.plot_weight_history.layout.yaxis.linecolor='#636363'
    self.plot_weight_history.layout.yaxis.linewidth=6
    
    
  def load_data(self):
    measurements = data_access.my_measurements()
    if not measurements:
      return
    
    x = []
    h = []
    w = []
    for idx, m in enumerate(measurements):
      x.append(idx + 1)
      h.append(m['RestingHeartRate'])
      w.append(m['WeightInPounds'])
      
    self.plot_weight_history.data = [
      go.Scatter(
      x = x,
      y = h,
      name='Heart rate'),
      go.Bar(
        x = x,
        y = w,
        name="Weight (lbs)"
      )
    ]
    
  def button_add_measurement_click(self, **event_args):
    navigation.go_add()

  
  
  
  
  