import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does
from whitenoise import WhiteNoise   #for serving static files on Heroku

# my header
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## Instantiate dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY]) 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

df_country = pd.read_csv("https://raw.githubusercontent.com/smbillah/ist526/main/gapminder.csv")

my_fig = px.bar(
  data_frame = df_country, 
  y="pop",         # gdp per capita
  x="continent",           # life expectancy  
  #size="pop",            # population
  color="country",     # group/label
  hover_name="country",
  #log_x=True, 
  #size_max=55, 
  #range_x=[100,100000], 
  #range_y=[25,90],
  title= "GDP Per Captia vs Life Expectancy of Countries", 
  
  # animation control
  #animation_frame="year", 
  #animation_group="country",
)

app.layout = html.Div([
  # first row: header
  html.H1('Shai Sundar\'s Custom Dashboard'),

  # second row: <scratter-plot> <empty> <bar chart> 
  html.Div([            
    # scratter plot                      
    html.Div([
      dcc.Dropdown(),

      dcc.Graph(
        id='scatter-graph',
        figure=px.scatter()
      )
    ], className='three columns'),

    # # one blank column
    # html.Div([
    #     html.Div(id='empty-div', children='')
    # ], className='one column'),
    html.Div([
      dcc.Dropdown(),

      dcc.Graph(
        id='my-graph',
        figure=px.scatter()
      )
    ], className='three columns'),

    # bar chart
    html.Div([
        dcc.Dropdown(),

        dcc.Graph(
          id='my_fig', 
          figure=my_fig
        )
    ], className='six columns')
    
  ], className = 'row'),

])

  
# run the code
# uncomment the following line to run in Google Colab
app.run_server(mode='inline', port=8030)

# Run dash app
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)
 
