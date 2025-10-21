import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import os

# Load data
df = pd.read_csv("data/formatted_data.csv")

print("Current working directory:", os.getcwd())
print("CSV exists:", os.path.exists("data/formatted_data.csv"))

df.columns = df.columns.str.strip().str.lower()
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Create line chart
fig = px.line(df, x='date', y='sales',
              title='Sales Over Time',
              labels={'date': 'Date', 'sales': 'Sales Amount'})

# Add these new customizations here
# Customize the layout
fig.update_layout(
    plot_bgcolor='white',  # White background
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
    )
)

# Make the line thicker
fig.update_traces(line=dict(width=2))

# Get y-axis range for the vertical line
y_range = [df['sales'].min(), df['sales'].max()]

# Add vertical line as a shape
fig.add_shape(
    type='line',
    x0='2021-01-15',
    x1='2021-01-15',
    y0=y_range[0],
    y1=y_range[1],
    line=dict(
        color='red',
        dash='dash',
        width=2
    )
)

# Add annotation
fig.add_annotation(
    x='2021-01-15',
    y=y_range[1],
    text='Price Increase (Jan 15, 2021)',
    showarrow=False,
    yshift=10
)

# Build Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Soul Foods Sales Visualiser", style={'textAlign': 'center'}),
    html.P("Sales before and after Pink Morsel price increase (Jan 15, 2021)",
           style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

