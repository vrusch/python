import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("cyborg")

df = px.data.gapminder()

all_continents = df.continent.unique()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

graphs = html.Div([
    dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x} 
                 for x in all_continents],
        value=all_continents[3:],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart"),
])

@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])
def update_line_chart(continents):
    mask = df.continent.isin(continents)
    fig = px.line(df[mask], 
        x="year", y="lifeExp", color='country')
    return fig

app.layout = dbc.Container(fluid=True, children=[graphs])

if __name__ == "__main__":
    app.run_server(debug=True)