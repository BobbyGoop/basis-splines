from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go

from SinusSpline import SinusSpline

app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])

app.layout = html.Div([
	dbc.Row([
		dcc.Graph(id='graph', style={'width': '100%', 'height': '85vh'})
	]),
	dbc.Row([
		dbc.Col([
			html.Div("Number of tick points: "),
			dbc.Input(id="input-ticks", type='number', value=200),
		], width={"size": 2}),
		dbc.Col([
			html.Div("Number of control points: "),
			dbc.Input(id="input-control", type='number', value=10)
			], width={"size": 2}
		),
		dbc.Col([
			html.Div("Spline degree: "),
			dbc.Select(id="input-degree", options=[
				{'label': 'Degree 1', 'value': 1},
				{'label': 'Degree 2', 'value': 2},
				{'label': 'Degree 3', 'value': 3},
				{'label': 'Degree 4', 'value': 4},
				{'label': 'Degree 5', 'value': 5},
			], value=2)
			], width={"size": 2}, align="end"
		),
		dbc.Col(
			dbc.Button('Apply', id="button-apply", type="submit"),
			width={"size": 1},
			align="end"
		)
	])
], style={"margin-left": "2em", "margin-right": "2em"})


@app.callback(Output("graph", "figure"),
			  [Input("button-apply", "n_clicks")],
			  [State("input-ticks", "value"),
			   State("input-control", "value"),
			   State("input-degree", "value")],
			  prevent_initial_calls=True,
)
def update_graph(_, tick_value, control_value, degree):
	spline = SinusSpline(ticks=tick_value, knots=control_value, degree=int(degree))
	df = pd.DataFrame({
		'fx': {
			'x': spline.get_base_data()[0],
			'y': spline.get_base_data()[1],
		},
		'sn': {
			'x': spline.get_spline_native()[0],
			'y': spline.get_spline_native()[1],
		},
		'sa': {
			'x': spline.get_spline_auto()[0],
			'y': spline.get_spline_auto()[1], },
		'cp': {
			'x': spline.get_original_points()[0],
			'y': spline.get_original_points()[1],
		},
	})

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df.fx.x, y=df.fx.y, mode='lines', name='y = f(fx)', line={'dash': 'dash'}))
	fig.add_trace(go.Scatter(x=df.sn.x, y=df.sn.y, mode='lines', name='Spline'))

	# fig.add_trace(go.Scatter(x=df.ak.x, y=df.ak.y, mode='markers', name='Additional knots', marker={'size':16}))
	fig.add_trace(go.Scatter(x=df.cp.x, y=df.cp.y, mode='lines', name='Linear interpolation'))
	fig.add_trace(go.Scatter(x=df.cp.x, y=df.cp.y, mode='markers', name='Control points', marker={'size': 10}))

	# for x in df.ak.x:
	# 	fig.add_trace(go.Scatter(x = [x, x], y = [-1, 1], mode='lines'))

	fig.update_layout(
		title = "Drawing B-Spline on trigonometric function",
		xaxis_title="X",
		yaxis_title="Y",
		legend_title="Legend",
	)
	return fig


if __name__ == "__main__":
	app.run_server(debug=True)
