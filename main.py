import os
from secret_santa import secret_santa_with_forced_constraints
from utils import read_participants, read_constraints, read_couples, read_godparents, read_no_presents
from plot import create_plot, create_app_dash
import dash
from dash import dash_table, html
from dash.dependencies import Input, Output



# Number of presents each person will give
num_presents = 4



# Main function
def main():
    # Ensure data directory exists
    data_folder = "data"
    results_folder = "results"
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(results_folder, exist_ok=True)

    # Load participant data from data folder
    # Define the path to the data folder
    data_folder = 'data/'

    participants_file = os.path.join(data_folder, 'participants.txt')
    constraints_file = os.path.join(data_folder, 'constraints.txt')
    couples_file = os.path.join(data_folder, 'couples.txt')
    godparents_file = os.path.join(data_folder, 'godparents.txt')
    no_presents_file = os.path.join(data_folder, 'no_presents.txt')

    # Read the data
    participants = read_participants(participants_file)
    constraints = read_constraints(constraints_file)
    couples = read_couples(couples_file)
    godparents = read_godparents(godparents_file)
    no_presents = read_no_presents(no_presents_file)
    # Run Secret Santa logic
    num_presents = 3  # You can change the default number of presents per person here
    santa_df, gift_counts_df, reverse_df, total_participants, total_presents = secret_santa_with_forced_constraints(
        participants, num_presents, constraints, couples, godparents, no_presents
    )
    ##show
    fig = create_plot(santa_df, gift_counts_df, reverse_df, total_participants, num_presents)
    fig.show()

    # Save results to the results folder
    santa_df.to_csv(f"{results_folder}/secret_santa_pairings.csv", index=False)
    gift_counts_df.to_csv(f"{results_folder}/gift_counts.csv", index=False)
    reverse_df.to_csv(f"{results_folder}/reverse_givers.csv", index=False)

    app = create_app_dash()
    app.run_server(debug=True)

# Execute main function
if __name__ == "__main__":
    main()