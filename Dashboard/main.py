from tkinter import Label
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime

external_stylesheets = ['Assets/file.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Luxury Loan Dashboard'

#Overwrite your CSS setting by including style locally
colors = {
    'background': '#2D2D2D',
    'text': '#E1E2E5',
    'figure_text': '#ffffff',
    'number_of_loan':'#3CA4FF',
    'total_funded_amount':'#5A9E6F',
    'interest_rate':'#f44336',
    
}

#Creating custom style for local use
divBorderStyle = {
    'backgroundColor' : '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
}

#Creating custom style for local use
boxBorderStyle = {
    'borderColor' : '#393939',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth':2,
}


# Read Data
lp_df = pd.read_csv("../Data/LuxuryLoanPortfolio.csv")

# Feature Selector
lp_df = lp_df[["loan_id", "funded_amount", "funded_date", "duration years", "duration months", "10 yr treasury index date funded",
      "interest rate percent", "interest rate", "payments", "total past payments", "loan balance", "property value", "purpose",
      "employment length", "BUILDING CLASS CATEGORY","BUILDING CLASS AT PRESENT", "TAX CLASS AT PRESENT",
       "TAX CLASS AT TIME OF SALE", "TOTAL UNITS", "LAND SQUARE FEET", "GROSS SQUARE FEET"]]

# Pre-processing and Feature Engineering
lp_df['funded_date'] = pd.to_datetime(lp_df['funded_date'])
lp_df['year_month'] = lp_df['funded_date'].dt.strftime('%Y-%m')
lp_df['purpose'] = lp_df['purpose'].str.title()
lp_df['mortgage_constant'] = (lp_df['payments']*12)/lp_df['funded_amount']
lp_df['ltv'] = lp_df['funded_amount'] / lp_df['property value']

# Create Plot

## Demographic
def demographic(lp_df):
    temp = lp_df["purpose"].value_counts()

    df = pd.DataFrame({'labels': temp.index,
                    'values': temp.values
                    })

    fig = px.pie(df, values=df["values"], names=df["labels"], hole = 0.4)
    fig.update_traces(textposition='auto', textinfo='percent+label')
    fig.update_layout(paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),)
    return fig

## Interest Rate

# Change date index to datetimeindex and share x-axis with all the plot
def draw_interest_graph(lp_df):
    group = lp_df.groupby(['year_month'])['interest rate percent'].mean().round(decimals = 1).reset_index()
    group['purpose'] = "All"

    fig = px.line(group, x='year_month', y="interest rate percent", color = "purpose",)
    

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            x=0.02,
            y=1.25,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=9,
                color=colors['figure_text']
            ),
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, 
                    r=0, 
                    t=0, 
                    b=0
                    ),
        height=300,
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    # fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    return fig


# Interest Rate group by Purpose
def draw_interest_purpose_graph(lp_df):
    group = lp_df.groupby(['purpose', 'year_month'])['interest rate percent'].mean().round(decimals = 1).reset_index()

    fig = px.line(group, x='year_month', y="interest rate percent", color="purpose",
                color_discrete_sequence = px.colors.qualitative.Light24)
    

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            x=0.02,
            y=1.25,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=9,
                color=colors['figure_text']
            ),
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, 
                    r=0, 
                    t=0, 
                    b=0
                    ),
        height=300,
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    # fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    return fig

## Average funding and duration - purpose
def avg_funding_duration(lp_df):
    
    avg_funding = lp_df.groupby('purpose')['funded_amount'].mean().reset_index()
    avg_duration = lp_df.groupby(['purpose'])['duration years'].mean().reset_index()
    
    y_duration = avg_duration['duration years'].unique().tolist()

    y_funded = avg_funding['funded_amount'].unique().tolist()

    x = avg_funding['purpose'].unique().tolist()

    # Creating two subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                        shared_yaxes=False, vertical_spacing=0.001)


    fig.append_trace(go.Bar(
        x=y_funded,
        y=x,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Average Funding',
        orientation='h',
    ), 1, 1)


    fig.append_trace(go.Bar(
        x=y_duration, 
        y=x,
        marker=dict(
            color='rgb(128, 0, 128)',
            line=dict(
                color='rgba(50, 171, 96, 0.6)',
                width=1),
        ),
        name='Average Duration',
        orientation='h',
    ), 1, 2)


    fig.update_layout(
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        yaxis2=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=False,
            domain=[0, 0.49],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=False,
            domain=[0.51, 1],
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
    )

    annotations = []
    new_yfunded = [ x / 1000000 for x in y_funded]
    y_funded = np.round(new_yfunded, decimals=2)
    y_duration = np.round(y_duration, decimals=1)

    # Adding labels
    for ydn, yd, xd in zip(y_duration, y_funded, x):
        # labeling the bar funding
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn + 4,
                                text=str(ydn) + ' year',
                                font=dict(family='Arial', size=12,
                                          color='rgb(128, 0, 128)'),
                                showarrow=False))
        # labeling the bar Duration
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 1000000,
                                text='{:,}'.format(yd) + 'M',
                                font=dict(family='Arial', size=12,
                                          color='rgb(50, 171, 96)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper',
                            x=-0.2, y=-0.109,
                            text='OECD "',
                            font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_xaxes(autorange="reversed", row=1, col=1)

    fig.update_layout(annotations=annotations,
                     paper_bgcolor=colors['background'],
                     plot_bgcolor=colors['background'],
                     font=dict(
                        family="sans-serif",
                        size=12,
                        color=colors['figure_text']
                    ),)
    
    return fig

## Create Loan Constant Graph
def loan_constant(lp_df, purpose='All'):
    if purpose=='All':
        df_mortgage_constant = lp_df.groupby('year_month')['mortgage_constant'].mean().round(decimals = 3).reset_index()
        df_mortgage_constant['purpose'] = "All"
        fig = px.line(df_mortgage_constant, x='year_month', y="mortgage_constant", title='Mortgage Ratio', color='purpose')

    else:
        df_mortgage_constant_year = lp_df.groupby(['purpose', 'year_month'])['mortgage_constant'].mean().round(decimals = 3).reset_index()
        df_mortgage_constant_year = df_mortgage_constant_year[df_mortgage_constant_year['purpose'] == purpose]
        fig = px.line(df_mortgage_constant_year, x='year_month', y="mortgage_constant", color="purpose", title='Mortgage Ratio')
    
    fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            font=dict(
                family="Courier New, monospace",
                size=14,
                color=colors['figure_text'],
            ),
            legend=dict(
                x=1.02,
                y=1.25,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=9,
                    color=colors['figure_text']
                ),
            ),
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background'],
            margin=dict(l=0, 
                        r=0, 
                        t=0, 
                        b=0
                        ),
            height=300,
        )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    # fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    return fig

## Loan to Value Ratio
def loan_value(lp_df, purpose='All'):
    if purpose=='All':
        df_ltv_avg = lp_df.groupby('year_month')['ltv'].mean().round(decimals = 2).reset_index()
        df_ltv_avg['purpose'] = "All"
        fig = px.line(df_ltv_avg, x='year_month', y="ltv", title='Loan to Value Ratio', color='purpose')

    else:
        df_ltv_avg_year = lp_df.groupby(['purpose', 'year_month'])['ltv'].mean().round(decimals = 2).reset_index()
        df_ltv_avg_year = df_ltv_avg_year[df_ltv_avg_year['purpose'] == purpose]
        fig = px.line(df_ltv_avg_year, x='year_month', y="ltv", color="purpose", title='Loan to Value Ratio')
    
    fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            font=dict(
                family="Courier New, monospace",
                size=14,
                color=colors['figure_text'],
            ),
            legend=dict(
                x=1.02,
                y=1.25,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=9,
                    color=colors['figure_text']
                ),
            ),
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background'],
            margin=dict(l=0, 
                        r=0, 
                        t=0, 
                        b=0
                        ),
            height=300,
        )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    # fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    return fig
    

# Create App Dash

app.layout = html.Div(
    html.Div([
        # Header display
        html.Div(
            [
                html.H1(children='Luxury Loan Dashboard',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],
                        },
                        className='title',
                        ),

                html.Div([html.Span('Dashboard by: Rheco Paradhika Kusuma',
                             style={'color': colors['text'],
                             }),

                         ],
                         className='sub-title'
                         ),

                html.Div([html.Span('Created: 18-06-2022',
                             style={'color': colors['text'],
                             }),

                         ],
                         className='sub-title'
                         ),

            ], className="header"
        ),

        # Top column display of confirmed, death and recovered total numbers
        html.Div([
            html.Div([
                html.H4(children='Number of Loan Given: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['number_of_loan'],
                       }
                       ),
                html.P(f"{lp_df['loan_id'].nunique()}",
                       style={
                    'textAlign': 'center',
                    'color': colors['number_of_loan'],
                    'fontSize': 30,
                }
                ),
            ],
                style=divBorderStyle,
                className='loan descriptive columns',
            ),
            html.Div([
                html.H4(children='Total Funded Amount: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['total_funded_amount'],
                       }
                       ),
                html.P(f"{np.round(lp_df['funded_amount'].sum() / 1000000, 2)}" + "M",
                       style={
                    'textAlign': 'center',
                    'color': colors['total_funded_amount'],
                    'fontSize': 30,
                }
                ),
            ],
                style=divBorderStyle,
                className='loan descriptive columns'),
            html.Div([
                html.H4(children='Average Interest Rate: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['interest_rate'],
                       }
                       ),
                html.P(f"{np.round(lp_df['interest rate percent'].mean(), 2)}" + "%",
                       style={
                    'textAlign': 'center',
                    'color': colors['interest_rate'],
                    'fontSize': 30,
                }
                ),
            ],
                style=divBorderStyle,
                className='loan descriptive columns'),

            # Graph of Demographic
            html.Div(
                [
                    html.H4(children='Purpose Demographic',
                            style={
                                'textAlign': 'center',
                                'color': colors['text'],
                                'backgroundColor': colors['background'],

                            },
                            className='title demographic columns'
                            ),
                    html.Div([
                        dcc.Graph(
                            id='demographic-graph',
                            figure=demographic(lp_df)
                        )
                    ], className='graph demographic columns',
                    ),

                ], className="demographic",
                
            ),

            # Graph of Interest Rate
            html.Div(
                [
                    html.H4(children='Interest Rate',
                            style={
                                'textAlign': 'center',
                                'color': colors['text'],
                                'backgroundColor': colors['background'],

                            },
                            className='twelve columns'
                            ),
                    html.Div([
                        dcc.Graph(
                            id='interest-purpose-graph',
                            figure=draw_interest_purpose_graph(lp_df)

                        )
                    ], className='interest columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            id='interest-graph',
                            figure=draw_interest_graph(lp_df)

                        )
                    ], className='interest columns'
                    ),

                ], className="row",
                style={
                    'textAlign': 'left',
                    'color': colors['text'],
                    'backgroundColor': colors['background'],
                },
            ),

            # Graph of Average Funding and Duration
            html.Div(
                [
                    html.H4(children='Average Funding and Duration',
                            style={
                                'textAlign': 'center',
                                'color': colors['text'],
                                'backgroundColor': colors['background'],

                            },
                            className='twelve columns'
                            ),
                    html.Div([
                        dcc.Graph(
                            id='funding-duration-graph',
                            figure=avg_funding_duration(lp_df)
                        )
                    ], className='graph average funding duration columns',
                    style={'padding-right': '130px'}
                    ),

                ], className="average funding duration columns",
                
            ),

            # Graph of LTV and Loan Constant
            html.Div(
                [
                    html.H4(children='Mortgage Constant and Loan to Value Ratio',
                            style={
                                'textAlign': 'center',
                                'color': colors['text'],
                                'backgroundColor': colors['background'],

                            },
                            className='twelve columns'
                            ),
                    html.Div([
                            dcc.Dropdown(['All', 'Boat', 'Commerical Property', 
                            'Home', 'Investment Property', 'Plane'], 'All', id='demo-dropdown',
                            style=dict(
                                width='50%',
                                left='25%',
                                textAlign= 'center',
                                right='auto',
                                display='block',
                                verticalAlign="middle",
                                color= "#000000"
                            ))
                    ], style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

                    html.Div([
                        dcc.Graph(
                            id='loan-constant-graph',

                        )
                    ], className='lc ltv columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            id='ltv-graph',

                        )
                    ], className='lc ltv columns'
                    )
                ]
            ),

            html.Div(
                [
                        html.Hr(),
                        html.P('Social Media:  ',
                               style={'display': 'block'}),
                        html.A([html.Img(src=app.get_asset_url('Linkedin.png'), style={'height':'1%', 'width':'2%'})],
                               href='https://www.linkedin.com/in/rheco-paradhika-kusuma/?originalSubdomain=id'),
                        html.A([html.Img(src=app.get_asset_url('Gmail.png'), style={'height':'8%', 'width':'2.6%'})],
                               href='mailto:rhecopk@gmail.com'),
                        html.Hr(),
                    ], className="twelve columns",
                    style={'fontSize': 18, 'padding-top': 20}
                ),


        ], className='row'),]),
        style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background'],
        "display": "block"
    },)

@app.callback(
    [Output('loan-constant-graph', 'figure'), Output('ltv-graph', 'figure')],
    [Input('demo-dropdown', 'value')]
)
def purpose_selection(value):
    fig1 = loan_constant(lp_df, value)
    fig2 = loan_value(lp_df, value)
    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug= True)