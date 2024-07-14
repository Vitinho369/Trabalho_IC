import random
populatin = [3, 5, 10]
rateCrossover = [0.9, 0.95, 1.0]
rateMutation = [0.01, 0.1, 0.5]
epochs = [10, 100, 1000]
acumulador = 0
medias = []
solveFinal = 0
for _ in range(2):  # questao 10
    for y in range(len(epochs)):
        for x in range(len(rateMutation)):
            for w in range(len(rateCrossover)):
                for z in range(len(populatin)):
                    acumulador = 0
                    print("populatin: ",populatin[z],"Crossover: ", rateCrossover[w], "Mutation: ", rateMutation[x], "Epochs: ", epochs[y])
                    for i in range(0, 30):
                        random.seed(i)
                        grafo = {
                            ("A","B"): 5,
                            ("A","F"): 2,
                            ("A","K"): 1,

                            ("B","A"): 5,
                            ("B","C"): 9,
                            ("B","F"): 2,
                            ("B","G"): 7,
                            
                            ("C","B"): 9,
                            ("C","D"): 5,
                            ("C","G"): 3,
                            ("C","H"): 7,
                            
                            ("D","E"): 2,    
                            ("D","C"): 5,    
                            ("D","H"): 3,    
                            ("D","I"): 5,

                            ("E","D"): 2,    
                            ("E","J"): 5,    
                            ("E","I"): 7,    

                            ("F","A"): 2,
                            ("F","B"): 2,    
                            ("F","K"): 2,    
                            ("F","L"): 5,    
                            ("F","G"): 9,   

                            ("G","F"): 9, 
                            ("G","H"): 5, 
                            ("G","M"): 5, 
                            ("G","L"): 3, 
                            ("G","B"): 7, 
                            ("G","C"): 3,

                            ("H","G"): 5, 
                            ("H","C"): 7, 
                            ("H","I"): 3, 
                            ("H","M"): 1, 
                            ("H","N"): 3, 
                            ("H","D"): 3,

                            ("I","H"): 3, 
                            ("I","J"): 9, 
                            ("I","N"): 2, 
                            ("I","O"): 1, 
                            ("I","E"): 7, 
                            ("I","D"): 5,

                            ("J","I"): 9, 
                            ("J","E"): 5, 
                            ("J","O"): 1,

                            ("K","A"): 1,
                            ("K","L"): 3,
                            ("K","F"): 2,

                            ("L","K"): 3,
                            ("L","F"): 5,
                            ("L","M"): 9,
                            ("L","G"): 3,

                            ("M","L"): 9,
                            ("M","N"): 5,
                            ("M","H"): 1,
                            ("M","G"): 5,

                            ("N","M"): 5,
                            ("N","I"): 2,
                            ("N","O"): 7,
                            ("N","H"): 3,

                            ("O","N"): 7,
                            ("O","I"): 1,
                            ("O","J"): 1,
                        }

                        size = 15
                        initRandom = 65                 
                        finalRandom = 79

                        class Solve:
                            def __init__(self):
                                self.encode:set[chr] = []
                                self.encode.append('A')
                                ascii_list = [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]
                                for _ in range(size-1):
                                    bit = random.choice(ascii_list)
                                    ascii_list.remove(bit)
                                    self.encode.append(chr(bit)) #geraa uma lista de caracteres aleatórios do A ao O
                            def copySolve(self, other:'Solve', start = 0, end = size) -> None:
                                for i in range(start, end):
                                    self.encode[i] = other.encode[i]
                            
                            def clone(self) -> 'Solve':
                                solve = Solve()
                                solve.copySolve(self)
                                return solve

                            def cost(self) -> int:
                                ## Deslocamento e limitações dos valores para evitar valores negativos na seleção por roleta
                                return 160 - self.func()

                            def func(self) -> float:
                                ## Exercício: modificar a função para -(x-2.2)**2/81 - (y-3.8)**2/49, nesse caso, as variáveis precisam ser reais
                                sumPath = 0
                                for i in range(0, size-1):
                                    caminho = (self.encode[i], self.encode[i+1])

                                    if(caminho in grafo):
                                        sumPath += grafo[caminho]
                                    else:
                                        sumPath += 10

                                return sumPath
                            
                            # Mutação e cruzamento
                            def decode(self) -> list[int]:
                                return self.encode
                            
                            def crossover(self, other:'Solve') -> None:
                                
                                positionInitList = random.randrange(0,size)
                                positionSecondList = random.randrange(0,size)
                                
                                if positionInitList > positionSecondList:
                                    troca = positionInitList
                                    positionInitList = positionSecondList
                                    positionSecondList = troca
                                
                                subEncodeFather1 = self.encode[positionInitList:positionSecondList+1]
                                subEncodeFather2 = other.encode[positionInitList:positionSecondList+1] 

                                child =  [' '] * 15
                                child[positionInitList:positionSecondList+1] = subEncodeFather1

                                # Crossover
                                for i in range(positionInitList, positionSecondList+1):
                                    # Se o valor do pai 1 for diferente do valor do pai 2 e o valor do pai 2 não estiver no filho
                                    if child[i] != other.encode[i]: 
                                        if other.encode[i] not in child:
                                            aux = other.encode[i]
                                            # Caso o gene do filho não esteja presente no subencode do pai 2
                                            if child[i] not in subEncodeFather2: 
                                                for j in range(0, size):
                                                        if other.encode[j] == child[i]:
                                                                child[j] = aux
                                                                break
                                            else: 
                                                # Caso o gene do filho esteja presente no subencode do pai 2
                                                left = positionInitList
                                                right = positionSecondList
                                                flag = True
                                                while left >= 0:
                                                    if child[left] == ' ':
                                                        child[left] = aux
                                                        flag = False
                                                        break
                                                    left -= 1
                                                if flag:
                                                    while right < size:
                                                        if child[right] == ' ':
                                                            child[right] = aux
                                                            break
                                                        right += 1
                                # Preenchendo os espaços vazios do filho
                                for j in range(0, size):
                                    if child[j] == ' ' and other.encode[j] not in child:
                                        child[j] = other.encode[j]
                                # Caso 3
                                for j in range(0, size):
                                    if child[j] == ' ':
                                        for k in range(0, size):
                                            if other.encode[k] not in child:
                                                child[j] = other.encode[k]
                                                break
                                self.encode = child

                            def mutate(self) -> None:
                                # Mutação por inversão
                                positionInitList = random.randrange(0,size)
                                positionSecondList = random.randrange(0,size)
                                if positionInitList < positionSecondList:
                                    reverse_encode =  self.encode[positionInitList:positionSecondList+1]
                                    self.encode[positionInitList:positionSecondList+1] = reverse_encode[::-1] 
                                elif positionInitList > positionSecondList:
                                    listaux1 = self.encode[positionInitList:size]
                                    listaux1 = listaux1[::-1]
                                    listaux2 = self.encode[0:positionSecondList+1]

                                    listaux = listaux2 + listaux1
                            
                                    sizeAux = len(listaux)
                                    for j in range(0, positionSecondList+1):
                                        self.encode[j] = listaux[sizeAux-j-1]

                                    cont = 0
                                    for i in range(positionInitList, size):
                                        self.encode[i] = listaux[cont]
                                        cont += 1

                            def __repr__(self) -> str:
                                c = str(self.cost())
                                v = str(self.func())
                                return str(self.decode()) + ' -> (' + v + ', ' + c + ')'


                        class GeneticAlgorihnm:
                            def __init__(self):
                                self.epochs:int = 100 ## Aumento da épocas para tratar os diferentes valores de cada variável
                                self.populationSize = 50
                                self.rateCrossover:float = 0.9
                                self.rateMutation:float = 0.01 ## Temos apenas duas variáveis, então a taxa de mutação deve ser maior
                            
                            def run(self) -> Solve:
                                population:list[Solve] = []
                                for _ in range(populatin[z]): # Gera as 100 soluções iniciais
                                    solve = Solve()
                                    population.append(solve)
                                bestSolve = population[0]
                                steps = 0
                                bestSolveGeneration = population[0]
                                # Gera as próximas gerações
                                while steps < epochs[y]:
                                    nextGeneration:list[Solve] = [] # reseta dee proximas geracoes 

                                    for _ in range(populatin[z]): # Gera mais 100 outras soluções
                                        first_parent = self.rouletteWheel(population)
                                        child = first_parent.clone()
                                        if random.random() < rateCrossover[w]:
                                            second_parent = self.rouletteWheel(population)
                                            child.crossover(second_parent)
                                        nextGeneration.append(child)

                                    # Mutação
                                    for child in nextGeneration:
                                        if random.random() < rateMutation[x]:
                                            child.mutate()

                                    population = nextGeneration
                                    steps += 1
                                    bestSolve = population[0]

                                    # Verifica a melhor solução da geração atual
                                    for solve in population:
                                        if solve.cost() >  bestSolve.cost():
                                            bestSolve = solve
                                    # Verifica se a melhor solução da geração atual é melhor que a melhor solução de todas as gerações
                                    if bestSolve.cost() > bestSolveGeneration.cost():
                                        bestSolveGeneration = bestSolve
                                # Retorna a melhor solução de todas as gerações``
                                global acumulador
                                acumulador = acumulador + bestSolveGeneration.func()
                                #print(bestSolveGeneration, i)
                                global solveFinal
                                if solveFinal != 0:
                                    if bestSolveGeneration.func() < solveFinal.func():
                                        solveFinal = bestSolveGeneration
                                else:
                                    solveFinal = bestSolveGeneration
                                return bestSolveGeneration


                            def rouletteWheel(self, population:list[Solve]) -> Solve:
                                sum = 0
                                for solve in population:
                                    sum += solve.cost()
                                r = random.random() * sum 
                                acc = 0
                                for solve in population:
                                    acc += solve.cost()
                                    if r <= acc:
                                        return solve
                                raise Exception("Wrong Values")


                        ga = GeneticAlgorihnm()
                        print(ga.run(), i)
                            
                    mediaFinal = acumulador/30
                    print("Media:", mediaFinal)
                    if z < 3 and w == 0 and x == 0 and y == 0:
                        medias.append([mediaFinal,populatin[z], rateCrossover[w], rateMutation[x], epochs[y]])
                        print("calculei a media")
                        if z == 2:
                            print("entrei no z == 2")
                            print("populatin")
                            # Pega a população com menor média
                            mediaFinal, theBestPopulatin, crossover, mutation, epoch = min(medias, key=lambda x: x[0])
                            # Reseta a população
                            populatin = []
                            # Adiciona a população com menor média
                            populatin.append(theBestPopulatin)
                            # Reseta a lista de médias
                            medias = []
                            # Adiciona a população com menor média
                            medias.append([mediaFinal, theBestPopulatin, crossover, mutation, epoch])
                            print(mediaFinal, theBestPopulatin, crossover, mutation, epoch)
                    
                    elif w >= 1 and x == 0 and y == 0:
                        medias.append([mediaFinal, populatin[0], rateCrossover[w], rateMutation[x], epochs[y]])
                        print("calculei a media")
                        if w == 2:
                            print("entrei no z == 2")
                            print("crossover")
                            print(medias)
                            mediaFinal, theBestPopulatin, crossover, mutation, epoch = min(medias, key=lambda x: x[0])
                            print(mediaFinal)
                            rateCrossover = []
                            rateCrossover.append(crossover)
                            medias = []
                            medias.append([mediaFinal, theBestPopulatin, crossover, mutation, epoch])
                            print(mediaFinal, theBestPopulatin, crossover, mutation, epoch)
                    elif x >= 1 and y == 0:
                        medias.append([mediaFinal, populatin[0], rateCrossover[0], rateMutation[x], epochs[y]])
                        print("calculei a media")
                        if x == 2:
                            print("entrei no z == 2")
                            print("mutation")
                            print(medias)
                            mediaFinal, theBestPopulatin, crossover, mutation, epoch = min(medias, key=lambda x: x[0])
                            print(mediaFinal)
                            rateMutation = []
                            rateMutation.append(mutation)
                            medias = []
                            medias.append([mediaFinal, theBestPopulatin, crossover, mutation, epoch])
                            print(mediaFinal, theBestPopulatin, crossover, mutation, epoch)
                    elif y >= 1:
                        medias.append([mediaFinal, populatin[0], rateCrossover[0], rateMutation[0], epochs[y]])
                        print("calculei a media")
                        if y == 2:
                            print("entrei no z == 2")
                            print("epochs")
                            print(medias)
                            mediaFinal, theBestPopulatin, crossover, mutation, epoch = min(medias, key=lambda x: x[0])
                            print(mediaFinal)
                            epochs = []
                            epochs.append(epoch)
                            medias = []
                            medias.append([mediaFinal, theBestPopulatin, crossover, mutation, epoch])
                            print(mediaFinal, theBestPopulatin, crossover, mutation, epoch)
    print(populatin, rateCrossover, rateMutation, epochs)
print("Solução final: ", solveFinal)