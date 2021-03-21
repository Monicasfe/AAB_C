class SuffixTreeMul:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0
        self.seq1 = ""
        self.seq2 = ""

    def descompacta(self, node):
        """Separa o tuplo das folhas em 2 variáveis m, n"""
        if self.nodes[node][0] == -1:
            m = self.nodes[node][0]
            n = ''
        else:
            m, n = self.nodes[node][0]
        return m , n

    def print_tree(self):
        for k in self.nodes.keys():
            m , n = self.descompacta(k)
            if m < 0:
                print(k, "->",self.nodes[k][1])
            else:
                print(k, ":", m , n)

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num  # [1] vai buscar o {} dentro do tuplo, define onde ir buscar
        self.nodes[self.num] = (leafnum, {})  # constroi o tuplo para o no seuinte,já estamos dentro do no para onde vamos
        # quando leafnum != -1 é folha, o nº que está na folha é de onde ele veio

    def add_suffix(self, p, sufnum):
        pos = 0
        node = 0
        while pos < len(p):  # equanto a pos < tamanho do padrão
            if p[pos] not in self.nodes[node][1].keys():  # se a letra da pos da seq p não existir:
                if pos == len(p) - 1:  # se ultimo caracter que vai ser o $
                    self.add_node(node, p[pos], sufnum)  # adiciona folha, não dá o sufnum, que é o nº da folha e continua com -1
                else:  # se não $ add node
                    self.add_node(node, p[pos])  # add ao node a letra p[pos]
            node = self.nodes[node][1][p[pos]]  # muda de no, e o output é 1 nº
            # p[pos] o p é a letra a pos é o no para onde o p vai
            pos += 1  # add 1 ao pos e recomeça o ciclo

    def suffix_tree_from_seq(self, text1, text2):
        t1 = text1 + "$"  # adiciona o $ à seq1 no fim
        t2 = text2 + "#" #adiciona o # à seq2 no fim
        self.seq1 = t1
        self.seq2 = t2
        for i in range(len(t1)):
            self.add_suffix(t1[i:], (0 , i))  # comeca na posicao i e vai ate ao fim, a partir pa posição que foi passada
            # passa o texto na po inicial i e vai até ao fim, o segundo i é a posiçao onde começou na seq original
        for j in range(len(t2)):
            self.add_suffix(t2[j:], (1 , j))


    def find_pattern(self, pattern):
        node = 0
        for pos in range(len(pattern)):  #
            if pattern[pos] in self.nodes[node][1].keys():  # se eltras estive no self. nodes na pos 0 nas keys do {}
                node = self.nodes[node][1][pattern[pos]]  # troca de no
                pos += 1
            else:
                return None
        return self.get_leafes_below(node)

    def get_leafes_below(self, node):
        """"""
        res = []
        res1 = []
        m , n = self.descompacta(node)
        if m >= 0:  # se o nó 0 nao é -1 entao e uma folha
            if m == 1:
                res.append(n)# dar append à pos do nó
            else:
                res1.append(n)
        else:
            for k in self.nodes[node][1].keys():  # itera as chaves do {}, letras
                newnode = self.nodes[node][1][k]  # por cada letras no {}, vai daqui um nº que vai ser o no para ionde vai qeu correpsonde ao k
                l_1 , l_2 = self.get_leafes_below(newnode)  # recursividade para seguir os ramos até folha, faz a recursividade no ramo
                res.extend(l_1)  # adiciona tudo no mesmo grupo, concatena listas
                res1.extend(l_2)
        return (res, res1)  # pos iniciais do padrao

    def largestCommonSubstring(self):
        """
        Retorna uma string com a maior sequencia comum as 2 sequencias
        """
        res = "" #string para formar a seq
        s1 = self.seq1
        s2 = self.seq2
        for i in range(0, len(s1)):#para cada posicao do tamanho da s1
            for j in range(0, len(s2)):#para cada posicao do tamanho da s2
                k = 1 # para somar às posições
                while i + k <= len(s1) and j + k <= len(s2) and s1[i:i+k] == s2[j:j+k]: #equanto que a posição + k <= tanto para s1 com para s2 e se os caracterres desde i a i+k e de j a j+k forem =
                    if len(res) <= len(s1[i:i+k]):# se o tamanho da string for <= ao tamanho da s1 desde a posição i até i+k
                        res = s1[i:i+k]#res passa a ser a seq s1 desde a pos i até à i+k
                    k += 1 #acrescenta 1 ao k que vai para o inicio do ciclo outra vez e aumenta a posição
        return res

def test():
    seq1 = "AATACTA"
    seq2 = "TATACTAT"
    st = SuffixTreeMul()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print(st.find_pattern("TA"))
    #print (st.find_pattern("ACG"))
    print(st.largestCommonSubstring())

test()

