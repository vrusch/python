import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from datas import *
from dash import dash_table

load_figure_template("cyborg")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

dx = pd.DataFrame(data)
all_channels = dx.channels.unique()
mask = dx.channels.isin(dx.channels.unique())
dx['DASH'] = dx.apply(lambda row: row.dash_kalt + row.dash_brpk, axis=1)
dx['HLS'] = dx.apply(lambda row: row.hls_kalt + row.hls_brpk, axis=1)

dxDASH = dx.loc[:,['dates', 'channels' ,'dash_kalt', 'dash_kalt_be', 'dash_brpk', 'DASH']]
dxHLS = dx.loc[:,['dates', 'channels' ,'hls_kalt', 'hls_kalt_be', 'hls_brpk', 'HLS']]
dxDASHmax = (dxDASH.nlargest(5, columns = ['DASH'])) 
dxHLSmax = (dxHLS.nlargest(5, columns = ['HLS']))

fig = px.line(dx[mask], x="dates", y=["DASH", "HLS"], color='channels', markers=True)

#fig.update_layout(
    #plot_bgcolor=colors['background'],
    #paper_bgcolor=colors['background'],
    #font_color=colors['text']
#)

app.layout = html.Div([
    html.H4("HLS & DASH for all channels:"),
    dcc.Graph(id='graph-all-channel', figure=fig),
    html.Br(),html.Br(),
    html.H6("Max values fof DASH:"),
    dash_table.DataTable(data=dxDASHmax.to_dict('records'),columns=[{'id': c, 'name': c} for c in dxDASHmax.columns], 
    style_table={'Width': '50%'},
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    }),
    html.Br(),
    html.H6("Max values fof HLS:"),
    dash_table.DataTable(data=dxHLSmax.to_dict('records'),columns=[{'id': c, 'name': c} for c in dxHLSmax.columns],
    style_table={'Width': '50%'},
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    }),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)