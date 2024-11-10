import random
from collections import defaultdict
import pandas as pd

def secret_santa_with_forced_constraints(participants, num_presents, constraints, couples, godparents, no_presents):
    """
    Secret Santa logic with forced constraints for couples, godparents, and exclusions.
    """
    santa_pairs = {person: [] for person in participants}
    gift_counts = defaultdict(int)

    for person in participants:
        if person in no_presents:
            continue

        # Add forced recipients from constraints
        forced_recipients = constraints.get(person, [])
        if len(forced_recipients) > num_presents:
            return f"{person} has more forced recipients than allowed presents."
        santa_pairs[person].extend(forced_recipients)
        for recipient in forced_recipients:
            gift_counts[recipient] += 1

        # Remaining gifts to assign
        remaining_gifts = num_presents - len(forced_recipients)
        possible_recipients = [p for p in participants if p != person and p not in santa_pairs[person]]

        if len(possible_recipients) < remaining_gifts:
            return f"Not enough possible recipients for {person} due to constraints."

        selected_recipients = random.sample(possible_recipients, remaining_gifts)
        santa_pairs[person].extend(selected_recipients)
        for recipient in selected_recipients:
            gift_counts[recipient] += 1

    # Handling couples constraints
    for person, partner in couples.items():
        if partner not in santa_pairs[person]:
            santa_pairs[person].append(partner)
            santa_pairs[partner].append(person)
            gift_counts[person] += 1
            gift_counts[partner] += 1

    # Handling godparents and godchildren constraints
    for godparent, godchildren in godparents.items():
        for godchild in godchildren:
            if godchild not in santa_pairs[godparent]:
                santa_pairs[godparent].append(godchild)
                gift_counts[godchild] += 1
            if godparent not in santa_pairs[godchild]:
                santa_pairs[godchild].append(godparent)
                gift_counts[godparent] += 1

    # Handling people with no presents
    for person in no_presents:
        santa_pairs[person] = []
        gift_counts[person] = 0

    # Ensure everyone gets the minimum number of presents
    for person in participants:
        if person in no_presents:
            continue
        while gift_counts[person] < num_presents:
            possible_givers = [p for p in participants if p != person and p not in no_presents and gift_counts[p] < num_presents]
            if not possible_givers:
                break
            giver = random.choice(possible_givers)
            santa_pairs[giver].append(person)
            gift_counts[person] += 1
            gift_counts[giver] += 1

    # Ensure people in no_presents receive presents
    for person in no_presents:
        while gift_counts[person] < num_presents:
            possible_givers = [p for p in participants if p not in no_presents and gift_counts[p] < num_presents]
            if not possible_givers:
                break
            giver = random.choice(possible_givers)
            santa_pairs[giver].append(person)
            gift_counts[person] += 1
            gift_counts[giver] += 1

    # Create the results DataFrame
    santa_df = pd.DataFrame([(person, ", ".join(recipients)) for person, recipients in santa_pairs.items()],
                            columns=["Giver", "Recipients"])
    santa_df = santa_df.sort_values(by="Giver").reset_index(drop=True)

    gift_counts_df = pd.DataFrame(list(gift_counts.items()), columns=["Recipient", "Number of Gifts"])
    gift_counts_df = gift_counts_df.sort_values(by="Recipient").reset_index(drop=True)

    reverse_df = pd.DataFrame([(recipient, ", ".join([giver for giver, recs in santa_pairs.items() if recipient in recs]))
                               for recipient in participants], columns=["Recipient", "Givers"])

    total_participants = len(participants)
    total_presents = total_participants * num_presents - len(no_presents) * num_presents

    return santa_df, gift_counts_df, reverse_df, total_participants, total_presents
