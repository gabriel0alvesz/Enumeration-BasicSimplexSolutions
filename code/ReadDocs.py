class ReadDocs:

    def __init__(self):
        self.lines: list
    
    def ReadDoc(self, name_doc: str):
        with open(name_doc,'r') as f:
            self.lines = f.readlines()
    
    def Tokenizer(self):
        self.lines = [line.strip().split() for line in self.lines]

    def DefineMatrices(self) -> list:
        n, m = map(int, self.lines[0][0:2])
        c = list(map(float, self.lines[1]))
        A = [[float(self.lines[i][j]) for j in range(0,5)] for i in range(2,5)]
        b = list(map(float, self.lines[-1]))
        return [n, m, c, A, b]
