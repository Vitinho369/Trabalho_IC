parameters = [
    [30, 50, 100],     # populationSize
    [0.9, 0.95, 1.0],  # rateCrossover
    [0.01, 0.1, 0.5],  # rateMutation
    [100, 1000, 10000] # epochs
]
CONT =0
# Iterando sobre todas as combinações possíveis
for pop_size in parameters[0]:
    for crossover_rate in parameters[1]:
        for mutation_rate in parameters[2]:
            for epoch in parameters[3]:
                print(pop_size)
                #print(f"populationSize: {pop_size}, rateCrossover: {crossover_rate}, rateMutation: {mutation_rate}, epochs: {epoch}")
                CONT +=1
print(CONT)


