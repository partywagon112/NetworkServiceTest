import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import time
import signal
import datetime
import yaml

from PingTools import Ping

with open('config.yml', 'r') as file:
    configuration = yaml.safe_load(file)

ping = Ping(configuration["ip_address"], configuration["interval"] )

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval-component',
                 interval=configuration["interval"]*1000, # in milliseconds
                 n_intervals=0)
])

@app.callback(Output('graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    data = ping.log
    # x = [i[0] for i in data[1:]]
    x = [datetime.datetime.fromtimestamp(i[0]).strftime('%Y-%m-%d %H:%M:%S') for i in data[1:]]
    ping_time = [i[2] for i in data[1:]]
    figure = {
        'data': [go.Scatter(x=x, y=ping_time, mode='lines+markers', name=data[0][2])],
        'layout': go.Layout(
            title=f"Ping Test to {ping.ip_address}", 
            yaxis=dict(title="Ping (ms)"), 
            xaxis=dict(
                title="Time", 
                range=[
                    datetime.datetime.fromtimestamp(time.time() - configuration["intertested_period"]).strftime('%Y-%m-%d %H:%M:%S'), 
                    datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                ]
            )
        )
    }
    return figure


def handler(signum, frame):
    global ping
    ping.stop()
    print("Ping stopped by user.")
    exit(0)

if __name__ == '__main__':
    ping.start()

    signal.signal(signal.SIGINT, handler)

    app.run_server(debug=True, port=configuration["port"])