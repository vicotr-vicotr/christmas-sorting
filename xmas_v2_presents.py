import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Sample data
data = {
    'Day': ['Dec 1', 'Dec 2', 'Dec 3', 'Dec 4', 'Dec 5', 'Dec 6', 'Dec 7', 'Dec 8', 'Dec 9', 'Dec 10',
             'Dec 11', 'Dec 12', 'Dec 13', 'Dec 14', 'Dec 15', 'Dec 16', 'Dec 17', 'Dec 18', 'Dec 19', 'Dec 20',
             'Dec 21', 'Dec 22', 'Dec 23', 'Dec 24', 'Dec 25'],
    'Gifts': [5, 7, 6, 8, 9, 10, 12, 11, 13, 14,
              15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 30],
    'Holiday Spirit': [10, 12, 11, 13, 14, 15, 16, 17, 18, 19,
                       20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                       30, 31, 32, 33, 35]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a scatter plot
fig = px.scatter(df, x='Day', y='Gifts', color='Holiday Spirit',
                 title='Christmas Gifts and Holiday Spirit',
                 labels={'Gifts': 'Number of Gifts', 'Holiday Spirit': 'Holiday Spirit Level'},
                 color_continuous_scale='RdYlGn')

# Customize the plot
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='lightgrey',
    font=dict(color='darkred'),
    title_font=dict(size=24, color='darkred'),
    xaxis=dict(title='Day', titlefont=dict(size=18, color='darkred')),
    yaxis=dict(title='Number of Gifts', titlefont=dict(size=18, color='darkred')),
    coloraxis_colorbar=dict(title='Holiday Spirit Level', titlefont=dict(size=18, color='darkred'))
)

# Create a Christmas tree shape
tree_shape = go.Scatter(
    x=[15, 15, 15, 15, 15, 15],
    y=[5, 10, 15, 20, 25, 30],
    mode='markers+text',
    text=['*', '***', '*****', '*******', '*********', '*'],
    marker=dict(size=20, color='green'),
    textfont=dict(size=20, color='green')
)

# Add the Christmas tree shape to the figure
fig.add_trace(tree_shape)

# Add a star on top of the tree
star_shape = go.Scatter(
    x=[15],
    y=[35],
    mode='markers+text',
    text=['★'],
    marker=dict(size=30, color='gold'),
    textfont=dict(size=30, color='gold')
)

# Add the star shape to the figure
fig.add_trace(star_shape)

# Update layout to include the Christmas tree in a subplot
fig.update_layout(
    shapes=[
        dict(
            type="rect",
            xref="x", yref="y",
            x0=14, y0=4,
            x1=16, y1=36,
            fillcolor="rgba(0, 0, 0, 0)",
            line_width=0,
        )
    ]
)

# Show the plot
fig.show()
