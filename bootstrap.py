"""
Apply Bootstrap theme to figures with one line of code! See more info at dash-bootstrap-templates GitHub
pip install dash-bootstrap-templates
"""

import dash
from dash import dcc
from dash import html
import plotly.express as px
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

# This loads the "cyborg" themed figure template from dash-bootstrap-templates library,
# adds it to plotly.io and makes it the default figure template.
load_figure_template("cyborg")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

df = px.data.gapminder()

dff = df[df.year.between(1952, 1982)]
dff = dff[dff.continent.isin(df.continent.unique()[1:])]
line_fig = px.line(
    dff, x="year", y="gdpPercap", color="continent", line_group="country"
)

dff = dff[dff.year == 1982]
scatter_fig = px.scatter(
    dff, x="lifeExp", y="gdpPercap", size="pop", color="pop", size_max=60
).update_traces(marker_opacity=0.8)

avg_lifeExp = (dff["lifeExp"] * dff["pop"]).sum() / dff["pop"].sum()
map_fig = px.choropleth(
    dff,
    locations="iso_alpha",
    color="lifeExp",
    title="%.0f World Average Life Expectancy was %.1f years" % (1982, avg_lifeExp),
)

hist_fig = px.histogram(dff, x="lifeExp", nbins=10, title="Life Expectancy")

graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=line_fig), lg=6),
                dbc.Col(dcc.Graph(figure=scatter_fig), lg=6),
            ],
            className="mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=hist_fig), lg=6),
                dbc.Col(dcc.Graph(figure=map_fig), lg=6),
            ],
            className="mt-4",
        ),
    ]
)

app.layout = dbc.Container(fluid=True, children=[graphs])


if __name__ == "__main__":
    app.run_server(debug=True)