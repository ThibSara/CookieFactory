import random
from classes import Biscuit, Defect, DoughRoll
import pandas as pd
import matplotlib.pyplot as plt

# Load the defects data
defects_data = pd.read_csv('defects.csv')
defects = [Defect(row['x'], row['class']) for _, row in defects_data.iterrows()]

# Create the biscuits
biscuits = [
    Biscuit("0", 4, 6, {'a': 4, 'b': 2, 'c': 3}),
    Biscuit("1", 8, 12, {'a': 5, 'b': 4, 'c': 4}),
    Biscuit("2", 2, 1, {'a': 1, 'b': 2, 'c': 1}),
    Biscuit("3", 5, 8, {'a': 2, 'b': 3, 'c': 2})
]

class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.dough_roll = DoughRoll(500, defects)
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        position = 0
        total_value = 0
        for gene in self.genes:
            biscuit = biscuits[gene]
            if self.dough_roll.is_legal_cut(position, biscuit):
                self.dough_roll.place_biscuit(position, biscuit)
                position += biscuit.size
                total_value += biscuit.value
            else:
                position += 1  # Move to the next position if the cut is not legal
        return total_value

    def get_best_placement(self):
        return self.dough_roll.biscuit_placements


class Population:
    def __init__(self, size):
        self.chromosomes = [Chromosome([random.randint(0, 3) for _ in range(500)]) for _ in range(size)]

    def get_best(self):
        return max(self.chromosomes, key=lambda chromosome: chromosome.fitness)


def selection(population):
    return random.choices(
        population.chromosomes,
        weights=[chromosome.fitness ** 2 for chromosome in population.chromosomes],
        k=2
    )


def crossover(parent1, parent2):
    crossover_index = random.randint(0, len(parent1.genes))
    child1_genes = parent1.genes[:crossover_index] + parent2.genes[crossover_index:]
    child2_genes = parent2.genes[:crossover_index] + parent1.genes[crossover_index:]
    return Chromosome(child1_genes), Chromosome(child2_genes)


def mutate(chromosome):
    mutation_index = random.randint(0, len(chromosome.genes) - 1)
    chromosome.genes[mutation_index] = random.randint(0, 3)

fitness_over_generations = []

# Genetic Algorithm
population = Population(100)
for _ in range(100):  # 100 generations
    new_population = Population(0)
    best_fitness = max(chromosome.fitness for chromosome in population.chromosomes)
    fitness_over_generations.append(best_fitness)
    while len(new_population.chromosomes) < len(population.chromosomes):
        parent1, parent2 = selection(population)
        child1, child2 = crossover(parent1, parent2)
        if random.random() < 0.1:  # 10% mutation rate
            mutate(child1)
            mutate(child2)
        new_population.chromosomes.append(child1)
        new_population.chromosomes.append(child2)
    population = new_population

best_chromosome = population.get_best()
print(f"Best total value: {best_chromosome.fitness}")
print(f"Best genes: {best_chromosome.genes}")
print(f"Best placement: {best_chromosome.get_best_placement()}")

plt.plot(fitness_over_generations)
plt.title("Fitness Evolution Over Generations")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.show()

print(len(best_chromosome.get_best_placement()))