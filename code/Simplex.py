import itertools
from shutil import ReadError
from ReadDocs import ReadDocs
import numpy as np

class Solution:

    def __init__(self, sol: list, val: int, resp: str, isG: bool):
        self.final_solution = sol
        self.value = val
        self.response = resp
        self.isGreat = isG
    

class Simplex:

    def __init__(self):
        self.n: int
        self.m: int
        self.c: np.array
        self.A: np.matrix
        self.b: np.array
        self.basic_solutions: dict = {}
        self.viables: int = 0
        self.not_viables: int = 0

    def CreateMatrices(self, name_file: str):
        rd = ReadDocs()
        
        rd.ReadDoc(name_file)
        
        rd.Tokenizer()
        list_aux = rd.DefineMatrices()

        self.n, self.m = list_aux[0:2]
        self.c = np.array(list_aux[2])
        self.A = np.matrix(list_aux[3])
        self.b = np.array(list_aux[-1]).reshape(-1,1)

    def PrintData(self):
        print("Numero de Variáveis: ", self.n)
        print("Numero de Restrições: ", self.m)
        print("Coeficientes da Função: ", self.c)
        print("Matriz mxn", self.A)
        print("Termos independentes: ", self.b)
        print("Soluções Básicas: ", self.basic_solutions)
    
    def FoundBasicSolutions(self):

        combinations = list(itertools.combinations(range(self.n), self.n - self.m))
        
        for comb in combinations:

            base_indexes = [i for i in range(self.n) if i not in comb]
            B = self.A[:, base_indexes]
            
            try:
                particular_result_xB = np.linalg.solve(B,self.b)

                self.basic_solutions[tuple(base_indexes)] = particular_result_xB
            except np.linalg.LinAlgError: # Quando aparece uma matriz singular
                continue
        # print(self.basic_solutions)
    
    def FormatSolutions(self):
        
        formatted_solutions = []

        for key, value in self.basic_solutions.items():
            final_solution_temp = np.zeros(self.n)
            index_aux = 0;
            for i in key:
                
                final_solution_temp[i] = value[index_aux].item()
                index_aux += 1 
            
            formatted_solutions.append(final_solution_temp)

        return np.array(formatted_solutions)    
    
    def ValidationSolutions(self, array_solutions: list) -> list[Solution]:

        solutions_validated_fomart: list = []
        response = ""
        menor = float('inf')
        z = 0
        
        # Auxiliares
        index = 0;
        cont = 0;
        for array in array_solutions:
            
            z = np.dot(self.c, array)

            if min(array) < 0:
                response = "inviável"
                self.not_viables = self.not_viables + 1   
            else:
                response = "viável"
                self.viables = self.viables + 1
                if z < menor:
                    menor = z
                    index = cont

            cont += 1;

            sol = Solution(array, z, response, False)
            solutions_validated_fomart.append(sol);

        solutions_validated_fomart[index].isGreat = True;

        return solutions_validated_fomart;

    def PrintSolution(self, solutions: list):
        for sol in solutions:
            if(sol.isGreat):
                print(f"Solução: x={tuple(sol.final_solution)},\tz = {sol.value},\t{sol.response} ==> Ótima")
            else:
                print(f"Solução: x={tuple(sol.final_solution)},\tz = {sol.value},\t{sol.response}")
        
        print("\n\n")
        print(f"Soluções básicas viáveis:   {self.viables}")
        print(f"Soluções básicas inviáveis:  {self.not_viables}")


if __name__ == "__main__":

    sp = Simplex()

    name_file = input("Digite o Nome do arquivo com o formato: ")

    try:
        sp.CreateMatrices(name_file)

        sp.FoundBasicSolutions()

        formatadas = sp.FormatSolutions()

        final = sp.ValidationSolutions(formatadas)

        sp.PrintSolution(final)
    except:
        print("Erro!")