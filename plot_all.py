
import mysql.connector
from numpy import NaN
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#DB connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)
mycursor = mydb.cursor()

sql = "SELECT date, channel_name, DASH_KALT, DASH_KALT_BE, DASH_BRPK, HLS_KALT, HLS_KALT_BE, HLS_BRPK FROM mydatabase.channel_test_upr"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print("Zaznamu nacteno z DB: "+str(len(myresult)))

dates = []
channels = []
dash_kalt = []
dash_kalt_be = []
dash_brpk = []
hls_kalt = []
hls_kalt_be = []
hls_brpk = []

for x in myresult:
  #dates.append(x[0])
  dates.append(pd.to_datetime(x[0]))
  channels.append(x[1])
  dash_kalt.append(float(x[2]))
  dash_kalt_be.append(float(x[3]))
  dash_brpk.append(float(x[4]))
  hls_kalt.append(float(x[5]))
  hls_kalt_be.append(float(x[6]))
  hls_brpk.append(float(x[7]))

  data = {}
  data['dates'] = dates
  data['channels'] = channels
  data['dash_kalt'] = dash_kalt
  data['dash_kalt_be'] = dash_kalt_be
  data['dash_brpk'] = dash_brpk
  data['hls_kalt'] = hls_kalt
  data['hls_kalt_be'] = hls_kalt_be
  data['hls_brpk'] = hls_brpk

dx = pd.DataFrame(data)
dx['DASH'] = dx.apply(lambda row: row.dash_kalt + row.dash_brpk, axis=1)
dx['HLS'] = dx.apply(lambda row: row.hls_kalt + row.hls_brpk, axis=1)
all_channels = dx.channels.unique()

dt_range = ''
dt_min = ''
dt_max = ''
dt = dx[(dx['dates'] > '2021-11-20 14:00:00') & (dx['dates'] <= '2021-11-20 15:00:00')]
#print(dt)

#print(dx.nlargest(1, 'DASH'))
#print(dx.nsmallest(1, 'DASH'))
#print(dx ["DASH"].mean())
#print(dx ["HLS"].mean())



dxv = dx[(dx.channels == 'RTS1HD')]
print(dxv.nlargest(1, 'DASH'))
print(dxv.nsmallest(1, 'DASH'))
print(dxv["DASH"].mean())
print(dxv["HLS"].mean())
print(dxv["dash_kalt"].hasnans)
print(dxv["dash_kalt_be"].hasnans)
print(dxv["dash_brpk"].hasnans)
print(dxv["hls_kalt"].hasnans)
print(dxv["hls_kalt_be"].hasnans)
print(dxv["hls_brpk"].hasnans)
#print(dxv)

#indexed_dx = dx.set_index(['channels'])



mask = dx.channels.isin(dx.channels.unique())

interpolation = 'linear' # linear, spline, vhv, hvh, vh, hv
#fig = px.line(dxv, x="dates", y=["DASH", "HLS", "dash_kalt", "dash_kalt_be", "dash_brpk", "hls_kalt", "hls_kalt_be", "hls_brpk"], markers=True, line_shape=interpolation)
fig = px.line(dx[mask], x="dates", y=["DASH", "HLS"], color='channels', markers=True, line_shape=interpolation)
fig.show()

'''
fig = go.Figure()
fig.add_trace(go.Bar(x=dxv['dates'],
                y=dxv['DASH'],
                name='DASH codec',
                marker_color='rgb(55, 83, 109)'
                ))
fig.add_trace(go.Bar(x=dxv['dates'],
                y=dxv['HLS'],
                name='HLS codec',
                marker_color='rgb(26, 118, 255)'
                ))

fig.update_layout(
    title='Data for RTS 1 HD channel',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Time in ms',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()
'''
