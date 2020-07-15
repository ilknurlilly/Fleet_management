import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
# TODO are imports unused or there on purpose?
import calendar
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc

from database_connection import connect, return_engine

# connect to database and add files to
conn = connect()
sql = "select * from vehicle_data;"
vehicle_data = pd.read_sql_query(sql, conn)
sql = "select * from cleaned_data_fleet_dna;"
fleet_data = pd.read_sql_query(sql, conn)
conn = None

# Data
# fleet_data = pd.read_csv('cleaned-data-for-fleet-dna.csv')
# fleet_data = fleet_data.head(10)  # limits the displayed rows to 10
# fleet_data.iloc[:,1:3]


# Calender

# calenderview = open('calendar.html', 'wb')

# PieCharts

# Downtimes Overview graph
# dt = fleet_data[["maintenance"]]
# for i in dt
# labels = vehicle_data.vehicle_status
labels = ['Accidents', 'Traffic Jams', 'Maintenance', 'Unused']
# values = [20, 30, 10, 40]
values = vehicle_data.vehicle_status.value_counts()
# values = fleet_data[["vehicle_status"]].groupby('vehicle_status').count()


pie1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Need for Maintenance graph

labels = ['Need', 'Soon', 'No need']
values = [2, 5, 10]

pie2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Accident Probability graph

labels = ['Category 1', 'Category 2', 'Category 3']
values = [20, 30, 10, 40]

pie3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, )])

####################### Mapbox ###########################
# mapbox_access_token = open(".mapbox_token").read()

####### Vehicle  position data extraction ###################
fleet_lat = vehicle_data.position_latitude
fleet_lon = vehicle_data.position_longitude
fleet_vid = vehicle_data.vid

fig = go.Figure(go.Scattermapbox(

    lat=fleet_lat,
    lon=fleet_lon,
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text=fleet_vid,
))

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken='pk.eyJ1IjoiamFrb2JzY2hhYWwiLCJhIjoiY2tiMWVqYnYwMDEyNDJ5bWF3YWhnMTFnNCJ9.KitYnq2a645C15FwvFdqAw',
        bearing=0,
        center=dict(
            lat=38.92,
            lon=-77.07
        ),
        pitch=0,
        zoom=10,
        style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
    ),
)

layout = html.Div(
    className='downtimes-content',
    children=[

        ###### Tab-Layout ############

        dcc.Tabs([

            # Downtimes Home

            dcc.Tab(label='Downtimes', children=[

                ################# Row 1 ###########################

                dbc.Row([

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H1('Vehicle Downtimes'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=pie1, config={'responsive': True}), className='piechart'),
                            dbc.Col([

                                ##################Radiobuttons Downtimes###################

                                dcc.Checklist(
                                    id='page-downtimes-radios-1',
                                    options=[{'label': i, 'value': i}
                                             for i in ['unused', 'traffic jams', 'accident', 'maintenance']],
                                    value=['unused', 'traffic jams', 'accident', 'maintenance']),

                                ##################Searchbox Downtimes###################

                                # dcc.Dropdown(
                                #     id='searchbox_downtime_table',
                                #     options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                #     value='',
                                #     placeholder='Search for vehicle...'
                                # ),

                                ##################Table Downtimes#########################

                                dash_table.DataTable(
                                    id="downtime_table",
                                    filter_action='native',
                                    sort_action='native',
                                    style_table={
                                        'maxHeight': '',
                                        'maxWidth': '',
                                        'overflowY': ''
                                    },
                                    data=[{}],

                                    columns=[{'name': i, 'id': i} for i in
                                             vehicle_data.loc[:, ['licence_plate', 'vehicle_status']]],
                                    page_size=10,
                                    style_header={
                                        'backgroundColor': '#f1f1f1',
                                        'fontWeight': 'bold',
                                        'fontSize': 12,
                                        'fontFamily': 'Open Sans'
                                    },
                                    style_cell={
                                        'padding': '5px',
                                        'fontSize': 13,
                                        'fontFamily': 'sans-serif'
                                    },
                                    style_cell_conditional=[

                                    ]),
                            ]),
                        ]),
                    ], className='card-tab card', width=True),

                    ##################Map Accidents#########################

                    dbc.Col(html.Div([
                        html.Div([
                            html.Div(
                                html.H1('Accidents'), className='map-margin'
                            ),
                            html.Div(
                                dcc.Graph(figure=fig, config={'responsive': True}, className='accidentsmap'),
                            ),
                        ]),

                    ]), className='card-tab card', width=True),

                ]),

                ################# Row 2 ###########################

                dbc.Row([

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H1('Need for Maintenance'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=pie2)),
                            dbc.Col([

                                ################## Radio-Buttons Maintenance ################

                                dcc.Checklist(
                                    id='page-downtimes-radios-2',
                                    options=[{'label': i, 'value': i}
                                             for i in ['Need', 'Soon', 'No need']],
                                    value=['Need', 'Soon', 'No need']),

                                ################## Searchbox Maintenance ###################

                                # dcc.Dropdown(
                                #     id='maintenance_filter_x',
                                #     options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                #     value='',
                                #     placeholder='Search for vehicle...'
                                # ),

                                dash_table.DataTable(
                                    data=vehicle_data.to_dict('records'),
                                    filter_action='native',
                                    sort_action='native',
                                    columns=[{'name': i, 'id': i} for i in
                                             vehicle_data.loc[:, ['licence_plate', 'maintenance']]],
                                    page_size=10,
                                    style_header={
                                        'backgroundColor': '#f1f1f1',
                                        'fontWeight': 'bold',
                                        'fontSize': 12,
                                        'fontFamily': 'Open Sans'
                                    },
                                    style_cell={
                                        'padding': '5px',
                                        'fontSize': 13,
                                        'fontFamily': 'sans-serif'
                                    },
                                    style_cell_conditional=[

                                    ]),
                            ]),
                        ]),
                    ], className='card-tab card', width=True),

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H1('Accident Probability'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=pie3)),
                            dbc.Col([
                                ################## Searchbox Accidents ###################

                                dcc.Checklist(
                                    id='page-downtimes-radios-3',
                                    options=[{'label': i, 'value': i}
                                             for i in ['Category 1', 'Category 2', 'Category 3']],
                                    value=['Category 1', 'Category 2', 'Category 3']),

                                ################## Searchbox Accidents ###################

                                # dcc.Dropdown(
                                #     id='accident_filter_x',
                                #     options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                #     value='',
                                #     placeholder='Search for vehicle...'
                                # ),

                                dash_table.DataTable(
                                    data=vehicle_data.to_dict('records'),
                                    filter_action='native',
                                    sort_action='native',
                                    # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                    columns=[{'name': i, 'id': i} for i in
                                             vehicle_data.loc[:, ['licence_plate', 'maintenance']]],
                                    page_size=10,
                                    style_header={
                                        'backgroundColor': '#f1f1f1',
                                        'fontWeight': 'bold',
                                        'fontSize': 12,
                                        'fontFamily': 'Open Sans'
                                    },
                                    style_cell={
                                        'padding': '5px',
                                        'fontSize': 13,
                                        'fontFamily': 'sans-serif'
                                    },
                                    style_cell_conditional=[
                                    ]),
                            ]),
                        ]),
                    ], className='card-tab card', width=True),

                ]),

                ############# Row 3 #############

                dbc.Row([

                    # Overstepping speed limit table

                    # dbc.Col([
                    #     dbc.Row(
                    #         dbc.Col(
                    #             html.Div(
                    #                 html.H3('Overstepping Speed Limit'),
                    #                 style={'textAlign': 'center'}
                    #             ),
                    #         ),
                    #     ),
                    #     dbc.Row([
                    #         dbc.Col(dash_table.DataTable(
                    #             data=vehicle_data.to_dict('records'),
                    #             # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                    #             columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                    #             page_size=5,
                    #             style_cell={'textAlign': 'left'},
                    #             style_cell_conditional=[
                    #
                    #             ]), ),
                    #     ]),
                    # ], className='card', width=True),

                    # Oldest Vehicles table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Oldest Vehicles'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                                columns=[{'name': i, 'id': i} for i in
                                         vehicle_data.loc[:, ['licence_plate', 'vehicle_construction_year']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                    ], className='card-tab card', width=True),

                    # Excessive speeding table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Excessive Speeding'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in
                                         vehicle_data.loc[:, ['licence_plate', 'maintenance']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                    ], className='card-tab card', width=True),

                    # Excessive acceleration table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Excessive Acceleration'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in
                                         vehicle_data.loc[:, ['licence_plate', 'maintenance']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                    ], className='card-tab card', width=True),

                    # Excessive breaking table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Excessive Breaking'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                    ], className='card-tab card', width=True),
                ]),

            ]),

            # Maintenance Calendar
            dcc.Tab(label='Maintenance Calendar', children=[

                # dcc.Graph(figure=calenderview),

                html.Div([
                    html.Embed(src='assets/calendar.html', className="cal-container")
                ])
            ]),

            # Fleet Location Map
            dcc.Tab(label='Realtime Map', children=[

                dcc.Graph(figure=fig),

                html.H3('Vehicle Details'),

                dash_table.DataTable(
                    data=vehicle_data.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                    style_header={
                        'backgroundColor': 'lightgrey',
                        'fontWeight': 'bold',
                        'fontSize': 12,
                        'fontFamily': 'Open Sans'
                    },
                    style_cell={
                        'padding': '5px',
                        'fontSize': 13,
                        'fontFamily': 'sans-serif'
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'Region'},
                            'textAlign': 'left'
                        }
                    ])
            ]),
        ])
    ])
