import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from datetime import datetime
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from datas import *

load_figure_template("cyborg")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

dx = pd.DataFrame(data)
all_channels = dx.channels.unique()
dd = dx['dates']
#print(dd)

dates = ['03-02-2021', '03-03-2021', '03-04-2021', '03-05-2021', '03-06-2021', '03-07-2021']
mytotaldates = {i:datetime.strptime(x, "%m-%d-%Y").date() for i,x in enumerate(dates)}
a = (list(mytotaldates.keys()))
#print(mytotaldates)

app.layout = html.Div(children=[ 
    html.H1("Dash Bootstrap Template Demo", className="bg-primary text-white p-2"), 
    dcc.RangeSlider(
        id='Dateslider',
        min=a[0],
        max=a[-1],
        marks=mytotaldates,
        value=[a[0], a[-1]]
    ),
    html.Div(id='OutputContainer'),
    dcc.Graph(id="line-chart")
])

@app.callback(
    Output('OutputContainer', 'children'),
    [Input('Dateslider', 'value')])

def rangerselection(val):
    val = [mytotaldates[val[0]], mytotaldates[val[1]]]
    return f'Selected Date: {val}'

def update_line_chart(): 
    mask = dx.channels.isin(dx.channels.unique())
    interpolation = 'linear' # linear, spline, vhv, hvh, vh, hv
    fig = px.line(dx[mask], x="dates", y=["DASH", "HLS"], color='channels', markers=True, line_shape=interpolation)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)