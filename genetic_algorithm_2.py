import random

import pandas as pd
from deap import creator, base, tools, algorithms

# Define the individual (solution representation) and fitness function
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Biscuits and dough length
biscuits = {
    'Biscuit_0': {'length': 4, 'value': 6, 'defect_thresholds': {'a': 4, 'b': 2, 'c': 3}},
    'Biscuit_1': {'length': 8, 'value': 12, 'defect_thresholds': {'a': 5, 'b': 4, 'c': 4}},
    'Biscuit_2': {'length': 2, 'value': 1, 'defect_thresholds': {'a': 1, 'b': 2, 'c': 1}},
    'Biscuit_3': {'length': 5, 'value': 8, 'defect_thresholds': {'a': 2, 'b': 3, 'c': 2}}
}
dough_length = 500

# Initialize necessary components for the genetic algorithm
toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 0, len(biscuits) - 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, dough_length)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Load the defects data from the provided CSV file
defects_file_path = 'defects.csv'
defects_data = pd.read_csv(defects_file_path)


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


# Fitness function to evaluate each individual
def evaluate(individual):
    total_value = 0
    position = 0
    while position < dough_length:
        biscuit_idx = individual[position]
        biscuit_name = f'Biscuit_{biscuit_idx}'
        biscuit = biscuits[biscuit_name]
        if can_place_biscuit(biscuit, position, defects_data):
            total_value += biscuit['value']
            position += biscuit['length']
        else:
            position += 1
    return total_value,


# Genetic operators
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(biscuits) - 1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

# Create initial population
population = toolbox.population(n=100)

# Run the genetic algorithm
ngen = 50  # Number of generations
result = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen, verbose=False)

# Best solution
best_individual = tools.selBest(population, 1)[0]
best_fitness = evaluate(best_individual)[0]

print(f'Best individual: {best_individual}')
print(f'Best fitness: {best_fitness}')