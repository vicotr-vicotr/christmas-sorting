import random
from collections import defaultdict
import pandas as pd
import os
import dash
from dash import dash_table, html
from dash.dependencies import Input, Output

# Secret Santa function
def secret_santa_with_forced_constraints(participants, num_presents, constraints, couples, godparents, no_presents):
    santa_pairs = {person: [] for person in participants}
    gift_counts = defaultdict(int)

    for person in participants:
        if person in no_presents:
            continue
        forced_recipients = constraints.get(person, [])
        santa_pairs[person].extend(forced_recipients)
        for recipient in forced_recipients:
            gift_counts[recipient] += 1

        remaining_gifts = max(0, num_presents - len(forced_recipients))
        possible_recipients = [
            p for p in participants if p != person and p not in santa_pairs[person] and gift_counts[p] < 4
        ]

        if len(possible_recipients) < remaining_gifts:
            return f"Not enough possible recipients for {person} due to constraints."

        selected_recipients = random.sample(possible_recipients, remaining_gifts)
        santa_pairs[person].extend(selected_recipients)
        for recipient in selected_recipients:
            gift_counts[recipient] += 1

    for person, partner in couples.items():
        if partner not in santa_pairs[person] and gift_counts[partner] < 4:
            santa_pairs[person].append(partner)
            santa_pairs[partner].append(person)
            gift_counts[person] += 1
            gift_counts[partner] += 1

    for godparent, godchildren in godparents.items():
        for godchild in godchildren:
            if godchild not in santa_pairs[godparent] and gift_counts[godchild] < 4:
                santa_pairs[godparent].append(godchild)
                gift_counts[godchild] += 1
            if godparent not in santa_pairs[godchild] and gift_counts[godparent] < 4:
                santa_pairs[godchild].append(godparent)
                gift_counts[godparent] += 1

    for person in participants:
        while gift_counts[person] < num_presents:
            possible_givers = [
                p for p in participants
                if p != person and gift_counts[p] < num_presents and p not in santa_pairs[person] and gift_counts[person] < 4
            ]
            if not possible_givers:
                break
            giver = random.choice(possible_givers)
            santa_pairs[giver].append(person)
            gift_counts[person] += 1
            gift_counts[giver] += 1

    santa_df = pd.DataFrame([(person, ", ".join(recipients)) for person, recipients in santa_pairs.items()],
                            columns=["Giver", "Recipients"]).sort_values(by="Giver").reset_index(drop=True)

    gift_counts_df = pd.DataFrame(list(gift_counts.items()), columns=["Recipient", "Number of Gifts"]).sort_values(by="Recipient").reset_index(drop=True)

    reverse_df = pd.DataFrame([(recipient, ", ".join([giver for giver, recs in santa_pairs.items() if recipient in recs]))
                               for recipient in participants], columns=["Recipient", "Givers"])

    total_participants = len(participants)
    total_presents = total_participants * num_presents

    return santa_df, gift_counts_df, reverse_df, total_participants, total_presents
