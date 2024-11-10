import pandas as pd
import random
from collections import defaultdict


def secret_santa_with_forced_constraints(participants, num_presents, constraints):
    """
    Organizes Secret Santa with multiple presents per person, including forced gift constraints.

    Args:
    participants (list): List of participant names.
    num_presents (int): Number of presents each person gives.
    constraints (dict): A dictionary where keys are participant names and values are lists of names they must gift.

    Returns:
    DataFrame, dict, int, int:
        - santa_df: A DataFrame where each row represents a participant and their gift recipients.
        - gift_counts: A dictionary counting how many gifts each participant will receive.
        - total_participants: Total number of participants.
        - total_presents: Total number of presents given in total.
    """
    # Initialize the dictionary for pairing and counting gifts
    santa_pairs = {person: [] for person in participants}
    gift_counts = defaultdict(int)

    for person in participants:
        # Start with forced recipients if they exist
        forced_recipients = constraints.get(person, [])

        # Check if the forced recipients exceed or equal the number of presents
        if len(forced_recipients) > num_presents:
            return f"{person} has more forced recipients than allowed presents."

        # Add forced recipients to the participant's gift list
        santa_pairs[person].extend(forced_recipients)

        # Update gift counts for forced recipients
        for recipient in forced_recipients:
            gift_counts[recipient] += 1

        # Calculate how many more recipients are needed
        remaining_gifts = num_presents - len(forced_recipients)

        # Determine eligible random recipients, excluding self, forced, and already assigned recipients
        possible_recipients = [p for p in participants
                               if p != person and p not in santa_pairs[person]]

        # If not enough eligible recipients are available, return an error
        if len(possible_recipients) < remaining_gifts:
            return f"Not enough possible recipients for {person} due to constraints."

        # Randomly assign remaining recipients
        selected_recipients = random.sample(possible_recipients, remaining_gifts)
        santa_pairs[person].extend(selected_recipients)

        # Update gift count for additional recipients
        for recipient in selected_recipients:
            gift_counts[recipient] += 1

    # Convert santa_pairs dictionary to DataFrame
    santa_df = pd.DataFrame([(person, recipients) for person, recipients in santa_pairs.items()],
                            columns=["Giver", "Recipients"])

    # Count participants and total presents
    total_participants = len(participants)
    total_presents = total_participants * num_presents

    return santa_df, dict(gift_counts), total_participants, total_presents




participants = ["Oma", "Grand-mere", "Pierre", "Francois", "Marielle", 'Philippe',
                "Paul", "Isabelle", "Amaury", "Stanislas", "Victor", "Valentine",
                "Edouard", "Coline", "Eloi", "Clementine", "Theodore", "Henri",
                "Pauline", "Louis", "Salome", "Theophane", "Marie", "Felix",
                "Pierre-Eloi", "Augustin", "Esperance", "Charles", "Eugenie", "Domitille"]



num_presents = 3  # Each person gives 2 gifts
constraints = {
    "Clementine": ["Theodore", "Paul"],
    "Philippe": ["Victor", 'Henri'], # Philippe offers a present to Victor and Henri for example
    "Domitille": ["Edouard", "Oma", "Isabelle"],
    "Felix": ['Victor', 'Henri']
}
# Domitille —> Édouard Oma Isabelle
# Oma —> Marielle les petits enfants
# Grand mere —> Pierre les petits enfants
# Francois —> grand-mère
# Pierre —> enfants Blanchier Kdo commun
# Marielle —> enfants Blanchier Kdo commun
# Victor  —> Valentine pierre Eloi Charles
# Valentine —> Victor clémentine pierre+marielle
# Paul —> Isabelle Augustin
# Isabelle —> Paul pierre+marielle
# Amaury —> clementine grand mère
# Stanislas —> espérance grand mère
# Édouard —> Coline Victor
# Coline —> Édouard pierre+marielle
# Eloi —> Pauline grand mère
# Theodore —> Clementine pierre+marielle
# Henri —> Charles, Eugenie, Philippe
# Pauline —> Henri pierre+marielle
# Louis —> Salome, Pierre Eloi charles
# Salomé —> Louis pierre+marielle
# Théophane —> marie Espérance
# Marie —>theophane pierre+marielle
# Felix —> Victor, Henri
# Pierre eloi —> Félix
# Augustin —> Louis grand mère
# Espérance —> clementine grand mère
# Charles —> Victor clementine
# Eugenie —>paul grand mère


santa_df, gift_counts, total_participants, total_presents = secret_santa_with_forced_constraints(participants, num_presents,
                                                                                             constraints)
print("Santa Pairings DataFrame:")
print(santa_df)
print("\nGift Counts Dictionary:")
print(gift_counts)
print(f"\nTotal Participants: {total_participants}")
print(f"Total Presents: {total_presents}")

