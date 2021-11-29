import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from datas import *
import dash_table

load_figure_template("cyborg")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

dx = pd.DataFrame(data)
all_channels = dx.channels.unique()
all_channels = dx.channels.unique()
mask = dx.channels.isin(dx.channels.unique())
#Try using .loc[row_indexer,col_indexer] = value instead



dxDASH = dx[['dates', 'channels' ,'dash_kalt', 'dash_kalt_be', 'dash_brpk']]
dxHLS = dx[['dates', 'channels' ,'hls_kalt', 'hls_kalt_be', 'hls_brpk']]
dxDASH['DASH'] = dxDASH.apply(lambda row: row.dash_kalt + row.dash_brpk, axis=1)
dxHLS['HLS'] = dxHLS.apply(lambda row: row.hls_kalt + row.hls_brpk, axis=1)
dxDASHmax = (dx.nlargest(5, columns = ['DASH'])) 
dxHLSmax = (dx.nlargest(5, columns = ['HLS']))


fig = px.line(dx[mask], x="dates", y=["DASH", "HLS"], color='channels', markers=True)

#fig.update_layout(
    #plot_bgcolor=colors['background'],
    #paper_bgcolor=colors['background'],
    #font_color=colors['text']
#)

app.layout = html.Div([
    dcc.Graph(id='graph-all-channel', figure=fig),
    dash_table.DataTable(data=dxDASHmax.to_dict('records'),columns=[{'id': c, 'name': c} for c in dxDASHmax.columns]),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)