import pandas as pd

# Load the defects data from the provided CSV file
defects_file_path = 'defects.csv'
defects_data = pd.read_csv(defects_file_path)

# Displaying the first few rows of the defects data to understand its structure
defects_data.head()

# Defining the biscuit types as per the project description
biscuits = {
    'Biscuit_0': {'length': 4, 'value': 6, 'defect_thresholds': {'a': 4, 'b': 2, 'c': 3}},
    'Biscuit_1': {'length': 8, 'value': 12, 'defect_thresholds': {'a': 5, 'b': 4, 'c': 4}},
    'Biscuit_2': {'length': 2, 'value': 1, 'defect_thresholds': {'a': 1, 'b': 2, 'c': 1}},
    'Biscuit_3': {'length': 5, 'value': 8, 'defect_thresholds': {'a': 2, 'b': 3, 'c': 2}}
}

# Dough length
dough_length = 500


# Function to check if a biscuit can be placed at a given position considering defect thresholds
def can_place_biscuit(biscuit, position, defects):
    if position + biscuit['length'] > dough_length:
        return False  # Biscuit exceeds dough length

    # Filter defects that fall within the biscuit's range
    relevant_defects = defects[(defects['x'] >= position) & (defects['x'] < position + biscuit['length'])]

    # Check if the biscuit's defect thresholds are exceeded
    for defect_class in biscuit['defect_thresholds']:
        max_allowed = biscuit['defect_thresholds'][defect_class]
        defects_count = relevant_defects[relevant_defects['class'] == defect_class].shape[0]
        if defects_count > max_allowed:
            return False

    return True


import numpy as np


def optimize_biscuit_placement(biscuits, dough_length, defects):
    # Initialize an array to store the maximum value at each position
    max_values = np.zeros(dough_length + 1)

    # Iterate through each position on the dough roll
    for position in range(dough_length):
        # Update the maximum value for the current position
        max_values[position + 1] = max(max_values[position + 1], max_values[position])

        # Try placing each type of biscuit at the current position
        for biscuit_name, biscuit in biscuits.items():
            if can_place_biscuit(biscuit, position, defects):
                end_position = position + biscuit['length']
                if end_position <= dough_length:
                    # Calculate the new value if the biscuit is placed here
                    new_value = max_values[position] + biscuit['value']
                    # Update the maximum value at the end position of the biscuit
                    max_values[end_position] = max(max_values[end_position], new_value)

    return max_values[-1]


def get_biscuit_placement_details(biscuits, dough_length, defects):
    # Reusing the optimize_biscuit_placement logic with additional tracking
    max_values = np.zeros(dough_length + 1)
    placement_tracker = [None] * (dough_length + 1)  # Track biscuit placements

    for position in range(dough_length):
        max_values[position + 1] = max(max_values[position + 1], max_values[position])

        for biscuit_name, biscuit in biscuits.items():
            if can_place_biscuit(biscuit, position, defects):
                end_position = position + biscuit['length']
                if end_position <= dough_length:
                    new_value = max_values[position] + biscuit['value']
                    if new_value > max_values[end_position]:
                        max_values[end_position] = new_value
                        placement_tracker[end_position] = (biscuit_name, position)

    # Reconstruct the placement of biscuits
    biscuit_placement = []
    current_position = dough_length
    while current_position > 0:
        placement = placement_tracker[current_position]
        if placement:
            biscuit_name, position = placement
            biscuit_placement.append((biscuit_name, position))
            current_position = position
        else:
            current_position -= 1

    return list(reversed(biscuit_placement))


# Optimizing the biscuit placement
total_value = optimize_biscuit_placement(biscuits, dough_length, defects_data)
print(f"Total value of biscuits placed: {total_value}")

# Getting detailed placement of biscuits
biscuit_placement_details = get_biscuit_placement_details(biscuits, dough_length, defects_data)
biscuit_placement_details
