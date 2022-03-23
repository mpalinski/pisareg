import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats

# external JavaScript files
external_scripts = [
    'https://cdn.jsdelivr.net/gh/mpalinski/etec_corr@main/assets/resizing.js'
]

df=pd.read_csv('./pisareg.csv')
df_math=pd.read_csv('./pisareg_math.csv')
df_science=pd.read_csv('./pisareg_science.csv')

df_def=pd.read_csv('./oecd_definitions.csv',sep='\t')

req_sel=['Variable','r2']

# list of predictors
to_sel=set(df.columns)-set(req_sel)
to_sel_math=set(df_math.columns)-set(req_sel)
to_sel_science=set(df_science.columns)-set(req_sel)


# .1 == S.E. columns
to_sel=[ x for x in list(to_sel) if ".1" not in x ]
to_sel_math=[ x for x in list(to_sel_math) if ".1" not in x ]
to_sel_science=[ x for x in list(to_sel_science) if ".1" not in x ]


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],external_scripts=external_scripts)

server = app.server

Options=[{'label': i, 'value': i} for i in to_sel]
Options_math=[{'label': i, 'value': i} for i in to_sel_math]
Options_science=[{'label': i, 'value': i} for i in to_sel_science]


tab1_content = dbc.Card(
    dbc.CardBody(
        [
 html.Div([

 html.Div([
    html.H4(
    [
    'Select ',
    html.Span(
                    "predictors",
                    id="tooltip-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                )],className="card-text"),
    html.Br(),
    dbc.Tooltip(
                    "You can select up to four predictors"
            ,
            target="tooltip-target",
        ),

    dcc.Dropdown(
    id='dropdown',
    # options=[{'label': i, 'value': i} for i in to_sel],
    value=['ESCS','Teacher support'],
    multi=True
),
]),
    html.Div(id='dropdown-limit'),
                dcc.Loading(
 html.Div([

    dcc.Graph(id="bar-chart"),
]),
),

 html.Div([
    dash_table.DataTable(
    id='stats',
    columns=([{'name': 'Predictor', 'id': 'Predictor'},
  {'name': 'Coefficient', 'id': 'Coefficient'},
  {'name': 'S.E.', 'id': 'S.E.'},
  {'name': 't-statistic', 'id': 't-statistic'},
  {'name': 'p-value', 'id': 'p-value'}
  ]),
# tooltip_data=tooltip
css=[{
        'selector': '.dash-table-tooltip',
        'rule': 'background-color: #00cdcd; font-family: monospace; color: white; min-width: 1000px; position: fixed; top: 0; right: 0; text-align: justify'
    }],
tooltip_duration=None,
      style_cell={'textAlign': 'left'},
)
],
style={
        # 'textAlign': 'center',
        # 'borderBottom': 'thin lightgrey solid',
        # 'backgroundColor': '#FFFF',
        # 'padding': '10px 5px'
        'width':'49%',
        # 'marginLeft': 'auto',
        # 'marginRight': 'auto'
        'padding': '0px 0px 0px 0px'

    }
),

],
style={
        # 'textAlign': 'center',
        # 'borderBottom': 'thin lightgrey solid',
        # 'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '0px 0px 0px 0px'
    }

)
        ]
    ),
    className="mt-3",
),

tab2_content = dbc.Card(
    dbc.CardBody(
        [
 html.Div([

 html.Div([
    html.H4(
    [
    'Select ',
    html.Span(
                    "predictors",
                    id="tooltip-target-math",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                )],className="card-text"),
    html.Br(),
    dbc.Tooltip(
                    "You can select up to four predictors"
            ,
            target="tooltip-target-math",
        ),

    dcc.Dropdown(
    id='dropdown-math',
    # options=[{'label': i, 'value': i} for i in to_sel],
    value=['ESCS','Teacher support'],
    multi=True
),
]),
    html.Div(id='dropdown-limit-math'),
                dcc.Loading(
 html.Div([

    dcc.Graph(id="bar-chart-math"),
]),
),

 html.Div([
    dash_table.DataTable(
    id='stats-math',
    columns=([{'name': 'Predictor', 'id': 'Predictor'},
  {'name': 'Coefficient', 'id': 'Coefficient'},
  {'name': 'S.E.', 'id': 'S.E.'},
  {'name': 't-statistic', 'id': 't-statistic'},
  {'name': 'p-value', 'id': 'p-value'}
  ]),
# tooltip_data=tooltip
css=[{
        'selector': '.dash-table-tooltip',
        'rule': 'background-color: #00cdcd; font-family: monospace; color: white; min-width: 1000px; position: fixed; top: 0; right: 0; text-align: justify'
    }],
tooltip_duration=None,
      style_cell={'textAlign': 'left'},
)
],
style={
        # 'textAlign': 'center',
        # 'borderBottom': 'thin lightgrey solid',
        # 'backgroundColor': '#FFFF',
        # 'padding': '10px 5px'
        'width':'49%',
        # 'marginLeft': 'auto',
        # 'marginRight': 'auto'
        'padding': '0px 0px 0px 0px'

    }
),

],
style={
        # 'textAlign': 'center',
        # 'borderBottom': 'thin lightgrey solid',
        # 'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '0px 0px 0px 0px'
    }

)
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
 html.Div([

 html.Div([
    html.H4(
    [
    'Select ',
    html.Span(
                    "predictors",
                    id="tooltip-target-science",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                )],className="card-text"),
    html.Br(),
    dbc.Tooltip(
                    "You can select up to four predictors"
            ,
            target="tooltip-target-science",
        ),

    dcc.Dropdown(
    id='dropdown-science',
    # options=[{'label': i, 'value': i} for i in to_sel],
    value=['ESCS','Teacher support'],
    multi=True
),
]),
    html.Div(id='dropdown-limit-science'),
                dcc.Loading(
 html.Div([

    dcc.Graph(id="bar-chart-science"),
]),
),

 html.Div([
    dash_table.DataTable(
    id='stats-science',
    columns=([{'name': 'Predictor', 'id': 'Predictor'},
  {'name': 'Coefficient', 'id': 'Coefficient'},
  {'name': 'S.E.', 'id': 'S.E.'},
  {'name': 't-statistic', 'id': 't-statistic'},
  {'name': 'p-value', 'id': 'p-value'}
  ]),
# tooltip_data=tooltip
css=[{
        'selector': '.dash-table-tooltip',
        'rule': 'background-color: #00cdcd; font-family: monospace; color: white; min-width: 1000px; position: fixed; top: 0; right: 0; text-align: justify'
    }],
tooltip_duration=None,
      style_cell={'textAlign': 'left'},
)
],
style={
        # 'textAlign': 'center',
        # 'borderBottom': 'thin lightgrey solid',
        # 'backgroundColor': '#FFFF',
        # 'padding': '10px 5px'
        'width':'49%',
        # 'marginLeft': 'auto',
        # 'marginRight': 'auto'
        'padding': '0px 0px 0px 0px'

    }
),

],
style={
        # 'textAlign': 'center',
        # 'borderBottom': 'thin lightgrey solid',
        # 'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '0px 0px 0px 0px'
    }

)
        ]
    ),
    className="mt-3",
)

app.title = 'PISA 2018 | OLS Regressions'

app.layout = html.Div([

    html.H1('PISA 2018 | OLS Regressions'),
    dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Reading"),
        dbc.Tab(tab2_content, label="Math"),
        dbc.Tab(tab3_content, label="Science"),
    ]
),
],
style={
        # 'textAlign': 'center',
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 20px 0px 20px'
    }
)


@app.callback(
    Output(component_id='dropdown-limit', component_property='children'),
    [Input("dropdown", "value")]
)
def update_output_div(value):
    if len(value) > 3:
        return "Select up to 4 variables"


@app.callback(
    Output(component_id="dropdown", component_property="options"),
    [
        Input(component_id="dropdown", component_property="value"),
    ],
)
def update_dropdown_options(values):
    if len(values)>3:
        options=[{'label': i, 'value': i, "disabled":True} for i in to_sel]
        return options
    else:
        options=Options
        return options



@app.callback(
    [Output("bar-chart", "figure"), Output("stats","data")],
    [Input("dropdown", "value")])

def update_bar_chart(value):
    user_sel=value
    se_sel=[]
    for _ in user_sel:
        se_sel.append(_+'.1')
    sel=user_sel+se_sel+req_sel
    nosel=list(set(df.columns)-set(sel))
    temp=df[(~df[sel].isna().any(axis=1))&(df[nosel].isna().all(axis=1))]
    coefs=temp[user_sel].values
    coefs=coefs.astype(float)
    coefs=coefs[0]
    se=temp[se_sel].values
    se=se.astype(float)
    se=se[0]
    stat=np.round(coefs/se,2)

    pval=np.round(stats.t.sf(abs(stat), 6136),5)
    dfstats=pd.DataFrame(list(zip(user_sel,coefs,se,stat,pval)),columns=['Predictor','Coefficient','S.E.','t-statistic','p-value'])
    data=dfstats.to_dict('records')
    colors = ['Positive' if c > 0 else 'Negative' for c in coefs]
    fig = px.bar(
    x=user_sel, y=coefs, color=colors,
    color_discrete_sequence=['#00cdcd', '#ff6a6a'],
    labels=dict(x='', y='Linear coefficient'),
    title='Weight of each coefficient for predicting ' + '<b>'+ temp['Variable'].values[0]+ ' score'+ '</b>' + '. R' + '<sup>'+'2'+'</sup>: '+ str(temp['r2'].values[0]),
    error_y=temp[se_sel].values[0],
    template="simple_white"
    )

    return fig, data

@app.callback(
    Output("stats","tooltip_data"),
    [Input("dropdown", "value")])

def update_tooltip(value):
    df_sel=df_def[df_def['Predictor'].isin(value)]
    df_sel['Predictor'] = pd.Categorical(
    df_sel['Predictor'],
    categories=value,
    ordered=True
)
    df_sel=df_sel.sort_values('Predictor')
    tooltip_data=[{
        'Predictor': {'value': row['Definition'], 'type': 'markdown'}
        } for row in df_sel.to_dict('records')],
    return tooltip_data[0]

###

@app.callback(
    Output(component_id='dropdown-limit-math', component_property='children'),
    [Input("dropdown-math", "value")]
)
def update_output_div(value):
    if len(value) > 3:
        return "Select up to 4 variables"


@app.callback(
    Output(component_id="dropdown-math", component_property="options"),
    [
        Input(component_id="dropdown-math", component_property="value"),
    ],
)
def update_dropdown_options(values):
    if len(values)>3:
        options=[{'label': i, 'value': i, "disabled":True} for i in to_sel_math]
        return options
    else:
        options=Options_math
        return options

@app.callback(
    [Output("bar-chart-math", "figure"), Output("stats-math","data")],
    [Input("dropdown-math", "value")])

def update_bar_chart(value):
    user_sel=value
    se_sel=[]
    for _ in user_sel:
        se_sel.append(_+'.1')
    sel=user_sel+se_sel+req_sel
    nosel=list(set(df_math.columns)-set(sel))
    temp=df_math[(~df_math[sel].isna().any(axis=1))&(df_math[nosel].isna().all(axis=1))]
    coefs=temp[user_sel].values
    coefs=coefs.astype(float)
    coefs=coefs[0]
    se=temp[se_sel].values
    se=se.astype(float)
    se=se[0]
    stat=np.round(coefs/se,2)

    pval=np.round(stats.t.sf(abs(stat), 6136),5)
    dfstats=pd.DataFrame(list(zip(user_sel,coefs,se,stat,pval)),columns=['Predictor','Coefficient','S.E.','t-statistic','p-value'])
    data=dfstats.to_dict('records')
    colors = ['Positive' if c > 0 else 'Negative' for c in coefs]
    fig = px.bar(
    x=user_sel, y=coefs, color=colors,
    color_discrete_sequence=['#00cdcd', '#ff6a6a'],
    labels=dict(x='', y='Linear coefficient'),
    title='Weight of each coefficient for predicting ' + '<b>'+ temp['Variable'].values[0]+ ' score'+ '</b>' + '. R' + '<sup>'+'2'+'</sup>: '+ str(temp['r2'].values[0]),
    error_y=temp[se_sel].values[0],
    template="simple_white",
    # width=100%,
    height=450
    )

    return fig, data

@app.callback(
    Output("stats-math","tooltip_data"),
    [Input("dropdown-math", "value")])

def update_tooltip(value):
    df_sel=df_def[df_def['Predictor'].isin(value)]
    df_sel['Predictor'] = pd.Categorical(
    df_sel['Predictor'],
    categories=value,
    ordered=True
)
    df_sel=df_sel.sort_values('Predictor')
    tooltip_data=[{
        'Predictor': {'value': row['Definition'], 'type': 'markdown'}
        } for row in df_sel.to_dict('records')],
    return tooltip_data[0]

### science

@app.callback(
    Output(component_id='dropdown-limit-science', component_property='children'),
    [Input("dropdown-science", "value")]
)
def update_output_div(value):
    if len(value) > 3:
        return "Select up to 4 variables"


@app.callback(
    Output(component_id="dropdown-science", component_property="options"),
    [
        Input(component_id="dropdown-science", component_property="value"),
    ],
)
def update_dropdown_options(values):
    if len(values)>3:
        options=[{'label': i, 'value': i, "disabled":True} for i in to_sel_science]
        return options
    else:
        options=Options_science
        return options

@app.callback(
    [Output("bar-chart-science", "figure"), Output("stats-science","data")],
    [Input("dropdown-science", "value")])

def update_bar_chart(value):
    user_sel=value
    se_sel=[]
    for _ in user_sel:
        se_sel.append(_+'.1')
    sel=user_sel+se_sel+req_sel
    nosel=list(set(df_math.columns)-set(sel))
    temp=df_science[(~df_science[sel].isna().any(axis=1))&(df_science[nosel].isna().all(axis=1))]
    coefs=temp[user_sel].values
    coefs=coefs.astype(float)
    coefs=coefs[0]
    se=temp[se_sel].values
    se=se.astype(float)
    se=se[0]
    stat=np.round(coefs/se,2)

    pval=np.round(stats.t.sf(abs(stat), 6136),5)
    dfstats=pd.DataFrame(list(zip(user_sel,coefs,se,stat,pval)),columns=['Predictor','Coefficient','S.E.','t-statistic','p-value'])
    data=dfstats.to_dict('records')
    colors = ['Positive' if c > 0 else 'Negative' for c in coefs]
    fig = px.bar(
    x=user_sel, y=coefs, color=colors,
    color_discrete_sequence=['#00cdcd', '#ff6a6a'],
    labels=dict(x='', y='Linear coefficient'),
    title='Weight of each coefficient for predicting ' + '<b>'+ temp['Variable'].values[0]+ ' score'+ '</b>' + '. R' + '<sup>'+'2'+'</sup>: '+ str(temp['r2'].values[0]),
    error_y=temp[se_sel].values[0],
    template="simple_white",
    # width=100%,
    height=450
    )

    return fig, data

@app.callback(
    Output("stats-science","tooltip_data"),
    [Input("dropdown-science", "value")])

def update_tooltip(value):
    df_sel=df_def[df_def['Predictor'].isin(value)]
    df_sel['Predictor'] = pd.Categorical(
    df_sel['Predictor'],
    categories=value,
    ordered=True
)
    df_sel=df_sel.sort_values('Predictor')
    tooltip_data=[{
        'Predictor': {'value': row['Definition'], 'type': 'markdown'}
        } for row in df_sel.to_dict('records')],
    return tooltip_data[0]


if __name__ == '__main__':
    app.run_server(debug=True)
