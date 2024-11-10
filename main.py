import os
from secret_santa import secret_santa_with_forced_constraints
from utils import read_participants, read_constraints, read_couples, read_godparents, read_no_presents
from plot import create_plot

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

# Number of presents each person will give
num_presents = 3

# Generate the Secret Santa results
santa_df, gift_counts_df, reverse_df, total_participants, total_presents = secret_santa_with_forced_constraints(
    participants, num_presents, constraints, couples, godparents, no_presents
)

# Create and show the plot
fig = create_plot(santa_df, gift_counts_df, reverse_df, total_participants, num_presents)
fig.show()

# Display total summary
print(f"Total Participants: {total_participants}")
print(f"Total Presents Given: {total_presents}")