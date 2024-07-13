

import random
random.seed(1)

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
        self.dados = [
                [30, 50, 100],
                [0.9, 0.95, 1.0],
                [0.01, 0.1, 0.5],
                [100, 1000, 10000]]
    
    def run(self) -> Solve:
        populationSize = self.dados[0][0]
        rateCrossover = self.dados[1][0]
        rateMutation = self.dados[2][0]
        epochs = self.dados[3][0]
        cache = {}
        theBestSolves = []
        flagTwo = True
        saida = []
        for i in range(4):
            flagTwo = True
            for j in range(3):
                # Fixar as variáveis de acordo com o melhor custo
                if i == 0: 
                    populationSize = self.dados[0][j]
                elif i == 1: 
                    # Seleciona as 3 primeiras melhores soluções
                    if flagTwo: 
                        solves =  theBestSolves
                        menorCusto = solves[0]['custo']
                        for solve in solves:
                            if solve['custo'] < menorCusto:
                                populationSize = solve['populacao']
                                flagTwo = False
                            elif solve['custo'] > menorCusto:
                                theBestSolves.remove(solve)
                        if flagTwo:
                            populationSize = solves[0]['populacao']
                            flagTwo = False
                        print("Population Size: ", populationSize)
                    rateCrossover = self.dados[1][j]
                elif i == 2:
                    if flagTwo: 
                        solves =  theBestSolves
                        menorCusto = solves[0]['custo']
                        for solve in solves:
                                if solve['custo'] < menorCusto:
                                    rateCrossover = solve['crossover']
                                    flagTwo = False
                                elif solve['custo'] > menorCusto:
                                    theBestSolves.remove(solve)
                        if flagTwo:
                            rateCrossover = solves[0]['crossover']
                            flagTwo = False
                        print("Rate Crossover: ", rateCrossover)
                    rateMutation = self.dados[2][j]
                elif 3:
                    if flagTwo: 
                        solves =  theBestSolves
                        menorCusto = solves[0]['custo']
                        for solve in solves:
                            if solve['custo'] < menorCusto:
                                rateMutation = solve['mutacao']
                                flagTwo = False
                            elif solve['custo'] > menorCusto:
                                theBestSolves.remove(solve)
                        if flagTwo:
                            rateMutation = solves[0]['mutacao']
                            flagTwo = False 
                        print("Rate Mutation: ", rateMutation)
                    epochs = self.dados[3][j]
                # Verifica se a combinação de parâmetros já foi calculada
                if (populationSize, rateCrossover, rateMutation, epochs) not in cache:
                    population:list[Solve] = []
                    for _ in range(populationSize):
                        solve = Solve()
                        population.append(solve)
                    bestSolve = population[0]
                    steps = 0
                    bestSolveGeneration = population[0]
                    # Gera as próximas gerações
                    while steps < epochs:
                        nextGeneration:list[Solve] = [] # reseta dee proximas geracoes 

                        for _ in range(populationSize): # Gera mais 100 outras soluções
                            first_parent = self.rouletteWheel(population)
                            child = first_parent.clone()
                            if random.random() <  rateCrossover:
                                second_parent = self.rouletteWheel(population)
                                child.crossover(second_parent)
                            nextGeneration.append(child)

                        # Mutação
                        for child in nextGeneration:
                            if random.random() < rateMutation:
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
                        
                    saida.append([bestSolveGeneration.func(), bestSolveGeneration])
                    # Adiciona a melhor solução de cada combinação de parâmetros
                    cache[(populationSize, rateCrossover, rateMutation, epochs)] = bestSolveGeneration.func()
                    # Retorna a melhor solução de todas as gerações
                    theBestSolves.append({"indice i": i, "indice j" : j,"custo": bestSolveGeneration.func(), "populacao": populationSize, "crossover": rateCrossover, "mutacao": rateMutation, "epocas": epochs})
        print("-----------------")
        print("Cache: ", cache)
        _, melhor_solucao = min(saida, key=lambda x: x[0])
        return melhor_solucao

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
print(ga.run())
