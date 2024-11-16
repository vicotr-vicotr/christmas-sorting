import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import os
import dash
from dash import dash_table, html, dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd

def create_plot(santa_df, gift_counts_df, opposite_df, total_participants, num_presents):
    # Update the opposite_df to set "Givers" to empty if the number of gifts is 0
    opposite_df['Givers'] = opposite_df.apply(lambda row: "" if gift_counts_df.loc[gift_counts_df['Recipient'] == row['Recipient'], 'Number of Gifts'].values[0] == 0 else row['Givers'], axis=1)
    #print(santa_df)
    # Create a new column in santa_df for the number of gifts each giver is giving
    santa_df['Number of Gifts'] = santa_df['Recipients'].apply(lambda x: len(x.split(', ')) if x else 0)


    # Create a new column in opposite_df to count the number of givers for each recipient
    opposite_df['Number of Givers'] = opposite_df['Givers'].apply(lambda x: len(x.split(', ')) if x else 0)
    opposite_df['Giftee'] = opposite_df['Recipient']

    opposite_df= opposite_df.sort_values(by='Giftee')
    # Create Plotly subplots (Two Tables)
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.5, 0.5],  # Adjust column widths to fit both tables compactly
        subplot_titles=["<b>Secret Santa Pairings</b>", "<b>Number of Gifts Each Recipient Receives</b>"],
        specs=[[{"type": "table"}, {"type": "table"}]]
    )

    #rename recipients wiht giftee
    santa_df['Giftees'] = santa_df['Recipients']
    gift_counts_df['Giftee'] = gift_counts_df['Recipient']

    # 1. Secret Santa Pairings Table with Christmas spirit
    fig.add_trace(go.Table(
        header=dict(values=["Giver", "Number of Gifts", "Giftees"],
                    fill_color='gold',  # Gold for header (Christmas color)
                    font=dict(color='red', size=14, family="Arial, sans-serif"),  # Red text for header
                    align='center'),
        cells=dict(values=[santa_df['Giver'],santa_df['Number of Gifts'], santa_df['Giftees']],
                   fill_color=['rgb(204, 255, 204)', 'rgb(204, 255, 204)', 'rgb(204, 255, 204)'],  # Light green for cells
                   font=dict(color='green', size=12, family="Arial, sans-serif"),  # Green text for cells
                   align='left',
                   height=30)  # Adjust the height of the cells to fit within the allocated space
    ), row=1, col=1)

    # 2. Gift Counts Table with Christmas spirit
    fig.add_trace(go.Table(
        header=dict(values=["Giftee", "Number of Givers", "Givers"],
                    fill_color='gold',  # Gold for header (Christmas color)
                    font=dict(color='red', size=14, family="Arial, sans-serif"),  # Red text for header
                    align='center'),
        cells=dict(values=[opposite_df['Giftee'], opposite_df['Number of Givers'], opposite_df['Givers'] ],
                   fill_color=['rgb(204, 255, 204)', 'rgb(204, 255, 204)', 'rgb(204, 255, 204)', 'rgb(204, 255, 204)'],  # Light green for cells
                   font=dict(color='green', size=12, family="Arial, sans-serif"),  # Green text for cells
                   align='left',
                   height=30)  # Adjust the height of the cells to fit within the allocated space
    ), row=1, col=2)

    # Add a description explaining what a "Recipient" and "Giver" are
    fig.add_annotation(
        text="""<b>Recipient:</b> A person who receives gifts in the Secret Santa exchange.<br>
                <b>Giver:</b> A person who makes gifts in the Secret Santa exchange.""",
        xref="paper", yref="paper",
        x=0.5, y=-0.0001,  # Position the annotation above the tables
        showarrow=False,
        font=dict(color='black', size=14, family="Arial, sans-serif"),
        align="center"
    )

    # Update layout for a refined Christmas look
    fig.update_layout(
        title={
            'text': f"<b>Blanchier Santa and Gift Distribution </b>",
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        title_font=dict(size=22, family="Arial, sans-serif", color='rgb(0, 128, 0)'),
        height=1200,  # Adjust the overall height to fit both tables compactly
        showlegend=False,
        plot_bgcolor='rgb(204, 255, 204)',  # Light green background for the plot area (Christmas tree-like)
        paper_bgcolor='rgb(240, 240, 240)',  # Subtle gray paper background
        font=dict(family="Arial, sans-serif", color="black"),

        # Show grid and adjust background
        xaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=False),
        margin=dict(t=70, b=50, l=50, r=50)  # Adjust margins to reduce space between tables
    )

    # Ensure the 'results' directory exists
    if not os.path.exists("results"):
        os.makedirs("results")

    # Save the results to CSV files in the 'results' folder
    santa_df.to_csv("results/secret_santa_pairings.csv", index=False)
    gift_counts_df.to_csv("results/gift_counts.csv", index=False)
    opposite_df.to_csv("results/reverse_givers.csv", index=False)
    # Save the figure as an HTML file in the 'results' folder
    fig.write_image("results/secret_santa_plot.png")

    # Additionally save the number of participants to a separate CSV
    num_participants_df = pd.DataFrame({"Total Participants": [total_participants]})
    num_participants_df.to_csv("results/total_participants.csv", index=False)

    # Show a success message
    print("Results have been saved in the 'results' folder.")

    return fig


def create_app_dash():
    # Load data
    santa_df = pd.read_csv("results/secret_santa_pairings.csv")
    opposite_df= pd.read_csv("results/reverse_givers.csv")
    gift_counts_df = pd.read_csv("results/gift_counts.csv")

    # Prepare data for the Dash tables
    #santa_df["Number of Gifts"] = santa_df['Recipients'].apply(lambda x: len(x.split(', ')) if x else 0)
    #santa_df.rename(columns={"Recipients": "Giftees"}, inplace=True)
    #gift_counts_df.rename(columns={"Recipient": "Giftee"}, inplace=True)

    # Create Dash app
    app = dash.Dash(__name__)
    app.title = "Blanchier Secret Santa Gift Distribution"

    app.layout = html.Div([
        # Header
        html.H1("Blanchier Santa and Gift Distribution", style={"text-align": "center", "color": "green"}),

        # Create a 2-column layout using Grid
        dbc.Row(
            [
                # Column for the Secret Santa Pairings table
                dbc.Col(
                    [
                        html.H3("Secret Santa Pairings", style={"color": "red", "text-align": "center"}),
                        dash_table.DataTable(
                            id="santa-table",
                            columns=[
                                {"name": "Giver", "id": "Giver"},
                                {"name": "Number of Gifts", "id": "Number of Gifts"},
                                {"name": "Giftees", "id": "Giftees"},
                            ],
                            data=santa_df.to_dict("records"),
                            editable=True,
                            style_header={
                                'backgroundColor': 'gold',
                                'color': 'red',
                                'fontWeight': 'bold',
                                'textAlign': 'center',
                            },
                            style_cell={
                                'backgroundColor': 'rgb(204, 255, 204)',
                                'color': 'green',
                                'textAlign': 'left',
                                'whiteSpace': 'normal',  # Allow text to wrap
                                'height': 'auto',
                            },
                            style_data={'height': '30px'},
                            style_table={'width': '100%'}
                        ),
                    ], width=6  # 50% of the row width
                ),

                # Column for the Gift Counts table
                dbc.Col(
                    [
                        html.H3("Number of Gifts Each Recipient Receives",
                                style={"color": "red", "text-align": "center"}),
                        dash_table.DataTable(
                            id="gift-counts-table",
                            columns=[
                                {"name": "Giftee", "id": "Giftee"},
                                {"name": "Number of Givers", "id": "Number of Givers"},
                                {"name": "Givers", "id": "Givers"},
                            ],
                            data=opposite_df.to_dict("records"),
                            editable=True,
                            style_header={
                                'backgroundColor': 'gold',
                                'color': 'red',
                                'fontWeight': 'bold',
                                'textAlign': 'center',
                            },
                            style_cell={
                                'backgroundColor': 'rgb(204, 255, 204)',
                                'color': 'green',
                                'textAlign': 'left',
                                'whiteSpace': 'normal',  # Allow text to wrap
                                'height': 'auto',
                            },
                            style_data={'height': '30px'},
                            style_table={'width': '100%'}
                        ),
                    ], width=6  # 50% of the row width
                )
            ]
        ),

        # Description
        html.Div([
            html.P(
                """<b>Recipient:</b> A person who receives gifts in the Secret Santa exchange.<br>
                <b>Giver:</b> A person who makes gifts in the Secret Santa exchange.""",
                style={"text-align": "center", "color": "black"}
            )
        ], style={"width": "90%", "margin": "0 auto", "padding": "20px"})
    ])

    return app