import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

import sqlite3

conn = sqlite3.connect("D:\multiagent projects\phdjango\phdjango\db.sqlite3")
c = conn.cursor()

table_name = 'models_worldresult'

print([record for record in c.execute(
    "SELECT field_name, field_human FROM models_modelverbosenames WHERE [table] = 'models_worldresult'").fetchall()])

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            html.Label('Виберіть Х:'),
            dcc.Dropdown(
                id='xaxis-table',
                options=[
                    {'label': 'Світ', 'value': 'models_worldresult'},
                    {'label': 'Фірми', 'value': 'models_firmresult'},
                    {'label': 'Ринок товарів', 'value': 'models_goodmarketresult'},
                    {'label': 'Ринок праці', 'value': 'models_labormarketresult'},
                ],
                value='models_worldresult'
            ),
            dcc.Dropdown(
                id='xaxis-field'
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Виберіть Y:'),
            dcc.Dropdown(
                id='yaxis-table',
                options=[
                    {'label': 'Світ', 'value': 'models_worldresult'},
                    {'label': 'Фірми', 'value': 'models_firmresult'},
                    {'label': 'Ринок товарів', 'value': 'models_goodmarketresult'},
                    {'label': 'Ринок праці', 'value': 'models_labormarketresult'},
                ],
                value='models_worldresult'
            ),
            dcc.Dropdown(
                id='yaxis-fields',
                multi=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Div([
        html.Label('Виберіть стиль графіку:', ),
        dcc.RadioItems(
            id='chart-type',
            options=[
                {'label': 'Лінійний графік', 'value': 'lines', 'style' : {'display': 'block'}},
                {'label': 'Точкова діаграма', 'value': 'markers', 'style' : {'display': 'block'}},
                {'label': 'Гістограма', 'value': 'bar', 'style' : {'display': 'block'}},
                {'label': 'Кругова діаграма', 'value': 'pie', 'style' : {'display': 'block'}},
            ],
            value='lines'
        )
    ],
        style={'width': '25%', 'float': 'left'}
    ),

    dcc.Graph(id='indicator-graphic', style={'width': '74%', 'float': 'right', 'display': 'inline-block'})
])


@app.callback(
    dash.dependencies.Output('xaxis-field', 'options'),
    [dash.dependencies.Input('xaxis-table', 'value')]
)
def set_xaxis_field_options(selected_x_axis_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_x_axis_table + "'").fetchall()]


@app.callback(
    dash.dependencies.Output('yaxis-fields', 'options'),
    [dash.dependencies.Input('yaxis-table', 'value')]
)
def set_yaxis_field_options(selected_y_axis_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_y_axis_table + "'").fetchall()]


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-table', 'value'),
     dash.dependencies.Input('xaxis-field', 'value'),
     dash.dependencies.Input('yaxis-table', 'value'),
     dash.dependencies.Input('yaxis-fields', 'value'),
     dash.dependencies.Input('chart-type', 'value')
     ])
def update_graph(xaxis_table, xaxis_field,
                 yaxis_table, yaxis_fields, chart_type):
    if xaxis_field is None:
        xaxis_field = 'step'
    if yaxis_fields is None:
        yaxis_fields = ['step']
    df_x = pd.read_sql('SELECT ' + xaxis_field + ' FROM ' + xaxis_table, conn)
    df_y = pd.read_sql('SELECT ' + ','.join(yaxis_fields) + ' FROM ' + yaxis_table, conn)

    plot = [go.Scatter(
        x=df_x[xaxis_field],
        y=df_y[yaxis_field],
        mode=chart_type,
        name=yaxis_field,
        marker={
            'size': 15,
            'opacity': 0.5,
            'line': {'width': 0.5, 'color': 'white'}
        }
    ) for yaxis_field in yaxis_fields]

    layout = dict(title='Styled Scatter',
                  yaxis=dict(zeroline=False),
                  xaxis=dict(zeroline=False)
                  )

    return {
        'data': plot,
        'layout': layout
    }


app.run_server()
