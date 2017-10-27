import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.tools as tls

import pandas as pd
import numpy as np

import sqlite3

conn = sqlite3.connect("D:\multiagent projects\phdjango\phdjango\db.sqlite3")
c = conn.cursor()

app = dash.Dash()

app.layout = html.Div(
    id = 'main', children = [
    html.Div(

        html.Fieldset([
            html.Button(id = 'reset-button', n_clicks = 0, children = 'Очистити'),
            html.Label('Виберіть таблицю:'),
            dcc.Dropdown(
                id='table',
                options=[
                    {'label': 'Світ', 'value': 'models_worldresult'},
                    {'label': 'Фірми', 'value': 'models_firmresult'},
                    {'label': 'Ринок товарів', 'value': 'models_goodmarketresult'},
                    {'label': 'Ринок праці', 'value': 'models_labormarketresult'},
                ],
                value='models_worldresult'
            ),

            html.Label('Виберіть X:'),
            dcc.Dropdown(
                id='xaxis-field'
            ),

            html.Label('Виберіть Y:'),
            dcc.Dropdown(
                id='yaxis-fields',
                multi=True
            ),

            html.Label('Виберіть фільтри:'),

            html.Br(),

            html.Label('Змінна фільтрування 1:'),
            dcc.Dropdown(
                id='filter-variable1'
            ),
            html.Label('Значення фільтрування 1:'),
            dcc.Dropdown(
                id='filter-values1',
                multi = True,
                clearable = False
            ),

            html.Label('Зміна фільтрування 2:'),
            dcc.Dropdown(
                id='filter-variable2'
            ),
            html.Label('Значення фільтрування 2:'),
            dcc.Dropdown(
                id='filter-values2',
                multi=True,
                clearable = False
            ),

            html.Label('Зміна фільтрування 3:'),
            dcc.Dropdown(
                id='filter-variable3'
            ),
            html.Label('Значення фільтрування 3:'),
            dcc.Dropdown(
                id='filter-values3',
                multi=True,
                clearable = False
            ),

            html.Label('Виберіть змінні розбиття:'),
            dcc.Dropdown(
                id='split',
                multi=True
            ),

            html.Label('Виберіть спосіб розбиття:'),
            dcc.RadioItems(
                id='split-type',
                options=[
                    {'label': 'Фасет', 'value': 'facet'},
                    {'label': 'Колір', 'value': 'color'},
                ],
                value='facet',
                labelStyle = {'display': 'block'}
            ),

            html.Label('Виберіть стиль графіку:', ),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': 'Лінійний графік', 'value': 'lines'},
                    {'label': 'Точкова діаграма', 'value': 'markers'},
                    {'label': 'Стовпчикова діаграма', 'value': 'bar'},
                    {'label': 'Гістограма', 'value': 'histogram'},
                    {'label': 'Ящик з вусами', 'value': 'box'},
                ],
                value='lines',
                labelStyle = {'display': 'block'}
            ),

            html.Label('Виберіть спосіб агрегування:', ),
            dcc.RadioItems(
                id='aggregation-type',
                options=[
                    {'label': 'Мінімум', 'value': 'min'},
                    {'label': 'Максимум', 'value': 'max'},
                    {'label': 'Середнє', 'value': 'avg'},
                    {'label': 'Медіана', 'value': 'median'},
                    {'label': 'Кількість', 'value': 'count'},
                    {'label': 'Без агрегування', 'value': 'none'},
                ],
                value='none',
                labelStyle = {'display': 'block'}
            )
        ]
        ),
        className = 'column',
        style = {'float': 'left', 'width': '20%'}
    ),

    html.Div(
        [dcc.Graph(id='indicator-graphic')],
        className = 'column',
        style = {'float': 'right', 'width': '80%'}
    )

],
className = 'row')

app.config['suppress_callback_exceptions']=True


@app.callback(
    dash.dependencies.Output('xaxis-field', 'options'),
    [dash.dependencies.Input('table', 'value')]
)

def set_xaxis_field_options(selected_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_table + "'").fetchall()]


@app.callback(
    dash.dependencies.Output('yaxis-fields', 'options'),
    [dash.dependencies.Input('table', 'value')]
)
def set_yaxis_field_options(selected_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_table + "'").fetchall()]

@app.callback(
    dash.dependencies.Output('split', 'options'),
    [dash.dependencies.Input('table', 'value')]
)

def set_split_options(selected_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_table + "'").fetchall()]

@app.callback(
    dash.dependencies.Output('filter-variable1', 'options'),
    [dash.dependencies.Input('table', 'value')]
)

def set_filter_variable1_options(selected_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_table + "'").fetchall()]

@app.callback(
    dash.dependencies.Output('filter-values1', 'options'),
    [dash.dependencies.Input('filter-variable1', 'value'),
     dash.dependencies.Input('table', 'value')]
)

def set_filter_values1_options(filter_variable, selected_table):
    return [{'label': value[0], 'value': value[0]} for value in c.execute("SELECT DISTINCT " + filter_variable +
                                                                             " FROM " + selected_table).fetchall()]

@app.callback(
    dash.dependencies.Output('filter-variable2', 'options'),
    [dash.dependencies.Input('table', 'value')]
)

def set_filter_variable2_options(selected_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_table + "'").fetchall()]

@app.callback(
    dash.dependencies.Output('filter-values2', 'options'),
    [dash.dependencies.Input('filter-variable2', 'value'),
     dash.dependencies.Input('table', 'value')]
)

def set_filter_values2_options(filter_variable_2, selected_table_2):
    return [{'label': value[0], 'value': value[0]} for value in c.execute("SELECT DISTINCT " + filter_variable_2 +
                                                                             " FROM " + selected_table_2).fetchall()]

@app.callback(
    dash.dependencies.Output('filter-variable3', 'options'),
    [dash.dependencies.Input('table', 'value')]
)
def set_filter_variable3_options(selected_table):
    return [{'label': record[1], 'value': record[0]} for record in c.execute("SELECT field_name, field_human "
                                                                             "FROM models_modelverbosenames "
                                                                             "WHERE [table] = '" + selected_table + "'").fetchall()]

@app.callback(
    dash.dependencies.Output('filter-values3', 'options'),
    [dash.dependencies.Input('filter-variable3', 'value'),
     dash.dependencies.Input('table', 'value')]
)

def set_filter_values3_options(filter_variable, selected_table):
    return [{'label': value[0], 'value': value[0]} for value in c.execute("SELECT DISTINCT " + filter_variable +
                                                                             " FROM " + selected_table).fetchall()]

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('table', 'value'),
     dash.dependencies.Input('xaxis-field', 'value'),
     dash.dependencies.Input('yaxis-fields', 'value'),
     dash.dependencies.Input('split', 'value'),
     dash.dependencies.Input('chart-type', 'value'),
     dash.dependencies.Input('aggregation-type', 'value'),
     dash.dependencies.Input('split-type', 'value'),
     dash.dependencies.Input('filter-variable1', 'value'),
     dash.dependencies.Input('filter-values1', 'value'),
     dash.dependencies.Input('filter-variable2', 'value'),
     dash.dependencies.Input('filter-values2', 'value'),
     dash.dependencies.Input('filter-variable3', 'value'),
     dash.dependencies.Input('filter-values3', 'value'),
     ])


def update_graph(table, xaxis_field, yaxis_fields, split, chart_type, aggregation_type, split_type,
                 filter_variable_1, filter_values_1, filter_variable_2, filter_values_2, filter_variable_3, filter_values_3):
    if xaxis_field is None or yaxis_fields is None:
        return {
            "layout": {'style': {'display': 'none'}}
        }

    filter_variables = [filter_variable_1, filter_variable_2, filter_variable_3]
    filter_values = [filter_values_1, filter_values_2, filter_values_3]

    filters = {}

    for i, filter_variable in enumerate(filter_variables):
        if filter_variable is not None and filter_values[i] is not None:
            filters[filter_variable] = filter_values[i]

    if split is None:
        columns = set(yaxis_fields + [xaxis_field] + list(filters.keys()))
        df = pd.read_sql('SELECT ' + ','.join(list(columns)) + ' FROM ' + table, conn)

        for variable, values in filters.items():
            df = df[df[variable].isin(values)]

        if aggregation_type == 'avg':
            df = df.groupby('step', as_index=False).aggregate(np.mean)
        elif aggregation_type == 'min':
            df = df.groupby('step', as_index=False).aggregate(min)
        elif aggregation_type == 'max':
            df = df.groupby('step', as_index=False).aggregate(max)
        elif aggregation_type == 'median':
            df = df.groupby('step', as_index=False).aggregate(np.median)
        elif aggregation_type == 'count':
            df = df.groupby('step', as_index=False).aggregate(len)


        if chart_type == 'bar':
            plot = [go.Bar(
                x=df[xaxis_field],
                y=df[yaxis_field],
                name=yaxis_field
            ) for yaxis_field in yaxis_fields]
        elif chart_type == 'box':
            plot = [go.Box(
                x=df[xaxis_field],
                y=df[yaxis_field],
                name=yaxis_field
            ) for yaxis_field in yaxis_fields]
        elif chart_type == 'histogram':
            plot = [go.Histogram(
                y=df[yaxis_field],
                name=yaxis_field,
                histnorm = 'probability'
            ) for yaxis_field in yaxis_fields]
        else:
            plot = [go.Scatter(
                x=df[xaxis_field],
                y=df[yaxis_field],
                mode=chart_type,
                name=yaxis_field,
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            ) for yaxis_field in yaxis_fields]
    else:
        columns = set(yaxis_fields + [xaxis_field] + split + list(filters.keys()))
        df = pd.read_sql('SELECT ' + ','.join(list(columns)) + ' FROM ' + table, conn)

        for variable, values in filters.items():
            df = df[df[variable].isin(values)]


        if aggregation_type == 'avg':
            df = df.groupby(split + ['step'], as_index=False).aggregate(np.mean)
        elif aggregation_type == 'min':
            df = df.groupby(split + ['step'], as_index=False).aggregate(min)
        elif aggregation_type == 'max':
            df = df.groupby(split + ['step'], as_index=False).aggregate(max)
        elif aggregation_type == 'median':
            df = df.groupby(split + ['step'], as_index=False).aggregate(np.median)
        elif aggregation_type == 'count':
            df = df.groupby(split + ['step'], as_index=False).aggregate(len)

        if split_type == 'facet':
            trace = 'scatter' if chart_type == 'markers' or chart_type == 'lines' else chart_type

            if len(split) == 1:
                plot = ff.create_facet_grid(
                    df,
                    x=xaxis_field,
                    y=yaxis_fields[0],
                    facet_col=split[0],
                    trace_type=trace,
                )
            elif len(split) == 2:
                plot = ff.create_facet_grid(
                    df,
                    x=xaxis_field,
                    y=yaxis_fields[0],
                    facet_col=split[0],
                    facet_row= split[1],
                    trace_type=trace,
                )
            else:
                plot = ff.create_facet_grid(
                    df,
                    x=xaxis_field,
                    y=yaxis_fields[0],
                    facet_col=split[0],
                    facet_row = split[1],
                    color_name= split[2],
                    color_is_cat=True,
                    trace_type=trace,
                )
        else:
            levels = df[split[0]].unique()
            if chart_type == 'bar':
                plot = [go.Bar(
                    x=df[df[split[0]] == level][xaxis_field],
                    y=df[df[split[0]] == level][yaxis_fields[0]],
                    name=level
                ) for level in levels]
            elif chart_type == 'box':
                plot = [go.Box(
                    x=df[df[split[0]] == level][xaxis_field],
                    y=df[df[split[0]] == level][yaxis_fields[0]],
                    name=level
                ) for level in levels]
            elif chart_type == 'histogram':
                plot = [go.Histogram(
                    y=df[df[split[0]] == level][yaxis_fields[0]],
                    name=level,
                    histnorm='probability'
                ) for level in levels]
            else:
                plot = [go.Scatter(
                    x=df[df[split[0]] == level][xaxis_field],
                    y=df[df[split[0]] == level][yaxis_fields[0]],
                    mode=chart_type,
                    name=level,
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                ) for level in levels]


    layout = {
        'style' : {'display': 'block'}
    }

    return {
        'data': plot,
        'layout': layout
    }

@app.callback(
    dash.dependencies.Output('xaxis-field', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_xaxis():
    return None

@app.callback(
    dash.dependencies.Output('yaxis-fields', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_yaxis():
    return None

@app.callback(
    dash.dependencies.Output('filter-variable1', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_filter_variable_1():
    return None

@app.callback(
    dash.dependencies.Output('filter-values1', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_filter_values_1():
    return None

@app.callback(
    dash.dependencies.Output('filter-variable2', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_filter_variable_2():
    return None

@app.callback(
    dash.dependencies.Output('filter-values2', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_filter_values_2():
    return None

@app.callback(
    dash.dependencies.Output('filter-variable3', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_filter_variable_3():
    return None

@app.callback(
    dash.dependencies.Output('filter-values3', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_values_3():
    return None

@app.callback(
    dash.dependencies.Output('split', 'value'),
    events = [dash.dependencies.Event('reset-button', 'click')]
)
def reset_split():
    return None



app.run_server()
