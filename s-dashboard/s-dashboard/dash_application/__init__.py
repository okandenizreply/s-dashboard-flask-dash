import dash
import dash_core_components as dcc
import dash_html_components as html
from flask_login.utils import login_required
import plotly.express as px
import pandas as pd

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Month": ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December', 'January', 
          'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December'],
        "A/C Usage (kWh/m²)": [36,44,34,36,41,33,38,43,36,
        47,46,40,40,48,45,42,37,40,43,44,30,36,37,47],
        "Type": ["Heating","Heating","Heating","Heating","Heating",
        "Heating","Heating","Heating","Heating","Heating","Heating",
        "Heating","Cooling","Cooling","Cooling","Cooling","Cooling",
        "Cooling","Cooling","Cooling","Cooling","Cooling","Cooling","Cooling"],
    }
)
def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
    dash_app.layout = html.Div(
        children=[
            html.H1(children="Sustainability Dashboard: A/C Usage"),
            html.Div(
                children="""
            Below is the Reply A/C Usage for the year: 2021.
        """
            ),
            dcc.Graph(
                id="example-graph",
                figure=px.bar(df, x="Month", y="A/C Usage (kWh/m²)", color="Type", barmode="group"),
            ),
        ]
    )

    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app
