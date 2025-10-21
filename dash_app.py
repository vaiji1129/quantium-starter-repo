import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import os

# Load data
df = pd.read_csv("data/formatted_data.csv")

print("Current working directory:", os.getcwd())
print("CSV exists:", os.path.exists("data/formatted_data.csv"))

df.columns = df.columns.str.strip().str.lower()
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Initialize the app
app = Dash(__name__)

# Define the layout with radio buttons and styling
app.layout = html.Div([
    # Main container
    html.Div([
        # Header
        html.H1("Soul Foods Sales Visualiser",
                style={'textAlign': 'center',
                       'color': '#2c3e50',
                       'font-family': 'Arial, sans-serif',
                       'margin-bottom': '20px'}),

        html.P("Sales before and after Pink Morsel price increase (Jan 15, 2021)",
               style={'textAlign': 'center',
                      'color': '#7f8c8d',
                      'font-size': '1.2em',
                      'margin-bottom': '30px'}),

        # Radio Button Container
        html.Div([
            html.Label('Select Region:',
                       style={'font-weight': 'bold',
                              'margin-right': '15px'}),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': ' All  ', 'value': 'all'},
                    {'label': ' North  ', 'value': 'north'},
                    {'label': ' South  ', 'value': 'south'},
                    {'label': ' East  ', 'value': 'east'},
                    {'label': ' West  ', 'value': 'west'},
                ],
                value='all',
                style={'display': 'inline-block'},
                className='radio-items'
            )
        ], style={'textAlign': 'center',
                  'padding': '20px',
                  'backgroundColor': '#f8f9fa',
                  'border-radius': '10px',
                  'margin-bottom': '20px'}),

        # Graph Container
        html.Div([
            dcc.Graph(id='sales-graph')
        ], style={'padding': '20px',
                  'backgroundColor': 'white',
                  'box-shadow': '0px 0px 10px rgba(0,0,0,0.1)',
                  'border-radius': '10px'})

    ], style={'max-width': '1200px',
              'margin': '0 auto',
              'padding': '20px'})
], style={'backgroundColor': '#f0f2f5',
          'min-height': '100vh',
          'padding': '20px'})


# Define callback to update graph based on radio button selection
@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    # Create line chart
    fig = px.line(filtered_df, x='date', y='sales',
                  title=f'Sales Over Time - {selected_region.title()} Region',
                  labels={'date': 'Date', 'sales': 'Sales Amount'})

    # Customize the layout
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            gridcolor='lightgrey',
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            showgrid=True
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16
        ),
        title_x=0.5,  # Center the title
        font=dict(family="Arial, sans-serif")
    )

    # Make the line thicker
    fig.update_traces(line=dict(width=2))

    # Add vertical line for price increase
    fig.add_shape(
        type='line',
        x0='2021-01-15',
        x1='2021-01-15',
        y0=0,
        y1=1,
        yref='paper',
        line=dict(
            color='red',
            dash='dash',
            width=2
        )
    )

    # Add annotation
    fig.add_annotation(
        x='2021-01-15',
        y=1,
        text='Price Increase (Jan 15, 2021)',
        showarrow=False,
        yshift=10
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)