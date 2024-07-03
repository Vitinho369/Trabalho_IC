
import random
random.seed(1)
from collections import Counter

#Problema no crossover, não está gerando filhos válidos, pois está repetindo valores
#Alterar a função de geração da população inicial
# Fixar a primeira cidade como A (Feito)

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

size = 14
initRandom = 65                 
finalRandom = 79

class Solve:
    def __init__(self):
        self.encode:set[chr] = []
        self.encode.append('A')
        ascii_list = [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]
        for _ in range(size):
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

        child = other.encode.copy()
        child[positionInitList:positionSecondList+1] = subEncodeFather1
       
        cont = 0
        positions = []
        for i in range(positionInitList, positionSecondList+1):
            position = other.encode.index(child[i])  
            while position not in positions:
                possiblepositions = [index for index,element  in enumerate(child) if child[position] == element]
                for j in possiblepositions:
                    print(possiblepositions, positions)
                    print("Father 1: ",self.encode)
                    print("Father 2: ", other.encode)
                    print("Subencode 1: ", subEncodeFather1)
                    print("Subencode 2: ", subEncodeFather2)
                    print("Child: ", child, child[j], j)

                    if child[j] not in subEncodeFather2:
                        position = other.encode.index(child[j])
                        positions.append(position)
                    else:
                        positions.append(position)
            if subEncodeFather2[cont] not in subEncodeFather1:
                child[position] = subEncodeFather2[cont]
            cont+=1
            
        for l in child:
            if child.count(l) > 1:
                print(l)
                print(cont)
                raise Exception(child)
            
        self.encode = child

    def mutate(self) -> None:
        # Mutação por inversão
        positionInitList = random.randrange(0,size)
        positionSecondList = random.randrange(0,size)
        print("---------------------")
        print("antes")
        print( self.encode )
                # Usando Counter para contar as ocorrências de cada letra
        contagem_letras = Counter(self.encode)

        # Exibindo o resultado
        for letra, contagem in contagem_letras.items():
            print(f"A letra '{letra}' aparece {contagem} vezes.")
        print("---------------------")
        if positionInitList < positionSecondList and True == False:
            print("---------------------")
            print("antes")
            print( self.encode )
            print(str(positionInitList) + " - Inicio " + str(positionSecondList) + " - Fim")
            reverse_encode =  self.encode[positionInitList:positionSecondList+1]
            self.encode[positionInitList:positionSecondList+1] = reverse_encode[::-1] 
            print( self.encode)    
            print("depois")
            print("---------------------")
        elif positionInitList > positionSecondList and True == False:
            print("---------------------")
            print("antes")
            print( self.encode )
            print(str(positionInitList) + " - Inicio " + str(positionSecondList) + " - Fim")
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
            print( self.encode)    
            print("depois")
            print("---------------------")

    def __repr__(self) -> str:
        c = str(self.cost())
        v = str(self.func())
        return str(self.decode()) + ' -> (' + v + ', ' + c + ')'


class GeneticAlgorihnm:
    def __init__(self):
        self.epochs:int = 100 ## Aumento da épocas para tratar os diferentes valores de cada variável
        self.populationSize = 100
        self.rateCrossover:float = 0.95
        self.rateMutation:float = 0.05 ## Temos apenas duas variáveis, então a taxa de mutação deve ser maior
    
    def run(self) -> Solve:
        population:list[Solve] = []
        for _ in range(self.populationSize): # Gera as 100 soluções iniciais
            solve = Solve()
            population.append(solve)
        bestSolve = population[0]
        
        steps = 0
        bestSolveGeneration = population[0]
        # Gera as próximas gerações
        while steps < self.epochs:
            nextGeneration:list[Solve] = [] # reseta dee proximas geracoes 

            for _ in range(self.populationSize): # Gera mais 100 outras soluções
                first_parent = self.rouletteWheel(population)
                child = first_parent.clone()
                if random.random() < self.rateCrossover:
                    second_parent = self.rouletteWheel(population)
                    #child.crossover(second_parent)
                nextGeneration.append(child)

            # Mutação
            for child in nextGeneration:
                if random.random() < self.rateMutation:
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
        # Retorna a melhor solução de todas as gerações
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
print(ga.run())
