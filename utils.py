# utils.py

import os
from collections import defaultdict

# Function to read participants from a file
def read_participants(file_path):
    with open(file_path, 'r') as file:
        participants = [line.strip() for line in file.readlines() if line.strip()]
    return participants

# Function to read constraints from a file
def read_constraints(file_path):
    constraints = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                parts = line.split(":")
                if len(parts) == 2:
                    participant, forced = parts
                    constraints[participant.strip()] = [x.strip() for x in forced.split(",")]
    return constraints

# Function to read couples from a file
def read_couples(file_path):
    couples = {}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                parts = line.split(":")
                if len(parts) == 2:
                    person1, person2 = parts
                    couples[person1.strip()] = person2.strip()
                    couples[person2.strip()] = person1.strip()
    return couples

# Function to read godparents from a file
def read_godparents(file_path):
    godparents = defaultdict(list)
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                parts = line.split(":")
                if len(parts) == 2:
                    godparent, godchildren = parts
                    godparents[godparent.strip()] = [x.strip() for x in godchildren.split(",")]
    return godparents

# Function to read no_presents from a file
def read_no_presents(file_path):
    with open(file_path, 'r') as file:
        no_presents = [line.strip() for line in file.readlines() if line.strip()]
    return no_presents