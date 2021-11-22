import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from datetime import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dates = ['03-02-2021', '03-03-2021', '03-04-2021', '03-05-2021', '03-06-2021', '03-07-2021']
mytotaldates = {i:datetime.strptime(x, "%m-%d-%Y").date() for i,x in enumerate(dates)}

a = (list(mytotaldates.keys()))

app = dash.Dash()

app.layout = html.Div(children=[   
    dcc.RangeSlider(
        id='Dateslider',
        min=a[0],
        max=a[-1],
        marks=mytotaldates,
        value=[a[0], a[-1]]
    ),
    html.Div(id='OutputContainer')
])


@app.callback(
    Output('OutputContainer', 'children'),
    [Input('Dateslider', 'value')])

def rangerselection(val):
    val = [mytotaldates[val[0]], mytotaldates[val[1]]]
    return f'Selected Date: {val}'


if __name__ == '__main__':
    app.run_server(debug=True)