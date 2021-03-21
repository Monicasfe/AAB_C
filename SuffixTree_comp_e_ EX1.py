# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        #é um {} por compreensão, onde a key é
        self.num = 0
        self.seq = "" #vai permitir adicionar a seq inicial

    def print_tree(self):
        """
        Permite imprimir a árvore da sequência forncida

        :return: nós das arvores e respetívos valores
        """
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0: #se não é folha
                print (k, "->", self.nodes[k][1]) #imprime o {} com os nt e os nós
            else: #se folha
                print (k, ":", self.nodes[k][0]) #imprime o nó de incio da seq que originou a folha
                
    def add_node(self, origin, symbol, leafnum = -1):
        """
        Permite adicionar um nó caso ainda nã exista na árvore
        """
        self.num += 1
        self.nodes[origin][1][symbol] = self.num # [1] vai buscar o {} dentro do tuplo, define onde ir buscar
        self.nodes[self.num] = (leafnum,{}) # constroi o tuplo para o no seuinte,já estamos dentro do no para onde vamos
        #quando leafnum != -1 é folha, o nº que está na folha é de onde ele veio

    def add_suffix(self, p, sufnum):
        """
        Adiciona um sufixo à árvore, sempre até chegar às folhas de cada ramo

        :param p:padrao
        :param sufnum: é o i, ou seja, a posiçao do excerto do padrao
        """
        pos = 0
        node = 0
        while pos < len(p): #equanto a pos < tamanho do padrão
            if p[pos] not in self.nodes[node][1].keys(): #se a letra da pos da seq p não existir:
                if pos == len(p) - 1: #se ultimo caracter que vai ser o $
                    self.add_node(node, p[pos], sufnum)#adiciona folha, não dá o sufnum, que é o nº da folha e continua com -1
                else: #se não $ add node
                    self.add_node(node, p[pos])#add ao node a letra p[pos]
            node = self.nodes[node][1][p[pos]]# muda de no, e o output é 1 nº
            #p[pos] o p é a letra a pos é o no para onde o p vai
            pos += 1 #add 1 ao pos e recomeça o ciclo
    
    def suffix_tree_from_seq(self, text):
        """
        Cria a árvore de sufixos a partir da sequência inicial fornecida

        :param text: sequência a ser fonecida
        """
        t = text+"$"#adiciona o $ à seq no fim
        self.seq = t #torna a seq num objeto da classe
        for i in range(len(t)):
            self.add_suffix(t[i:], i)#comeca na posicao i e vai ate ao fim, a partir pa posição que foi passada
            #passa o texto na po inicial i e vai até ao fim, o segundo i é a posiçao onde começou na seq original
            
    def find_pattern(self, pattern):
        """
        Procura se um dado padrão exist ou não na seqência/árvore, retornando a su aposção caso se verifique a
        existência do padrão.

        :param pattern: padrão a pesquisar
        :return: uma lista com as posições iniciais do padrão na árvore
        """
        node = 0
        for pos in range(len(pattern)): #por cada posição no ao longo do tamanho do padrão
            if pattern[pos] in self.nodes[node][1].keys():# se as letras estiverem no self. nodes na pos 0 nas keys do {}
                node = self.nodes[node][1][pattern[pos]]#troca de no
            else:
                return None
        return self.get_leafes_below(node)


    def get_leafes_below(self, node):
        """
        Identifica as folhas que se ecnontram abaixo de um nó fornecido como parâmetro

        :param node: nó inicial de contagem a partir do qual queremos descobrir as folhas
        :return: uma lista com as posisões da folhas abaixo do nó indicado
        """
        res = []
        if self.nodes[node][0] >=0: # se o nó 0 nao é -1 entao e uma folha
            res.append(self.nodes[node][0])#dar append à pos do nó
        else:
            for k in self.nodes[node][1].keys(): #itera as chaves do {}, letras
                newnode = self.nodes[node][1][k]#por cada letras no {}, vai daqui um nº que vai ser o no para ionde vai qeu correpsonde ao k
                leafes = self.get_leafes_below(newnode)#recursividade para seguir os ramos até folha, faz a recursividade no ramo
                res.extend(leafes)#adiciona tudo no mesmo grupo, concatena listas
        return res #pos iniciais do padrao

    #EX 1a

    def nodes_below(self, node):
        """
        Permite identificar os nós subsequentes a um dado nó forncecido incialmente no parametro "node"

        :param node: nó inicial de contagem a partir do qual queremos descobrir os nós subsequentes
        :return: uma lista com todos os nós existentes abaixo do "node", por ordem de acontecimento
        """
        if node in self.nodes.keys():# verfifica se o nº do no existe
            res = list(self.nodes[node][1].values())#cria a lista com os valores dos nos depois do no que demos
            for no in res:#itera os nos que estao na lista res
                res.extend(list(self.nodes[no][1].values()))#acrescenta os valores obtidos na lista mae
            return res #devolve a lista
        else:
            return None

    #EX 1b

    def matches_prefix(self, prefix):
        """
        Dado um prefixo permite inferir a sua existencia na seqeuncia original. Caso se verifique a existencia do
        prefixo será fornecida todas as subsequencias possiveis na sequência, iniciadas com o prefixo.

        :param prefix: Prefixo a procurar
        :return: lista com todas as combinações possíveis inicadas no prefixo
        """
        res = [] #lista para receber as subsequencias
        s1 = self.seq.replace("$", "") #definir a sequencias inicial como s1 e retirar $ no fim
        match = self.find_pattern(prefix) #analisar se existe match do prefixo na sequencia
        if match == None: #se não houver match
            return "O prefixo não existe na sequência"
        else:
            for i in match:#por cada posição onde ocorre match
                ma = i
            #ma = int(match[0]) #definir a posição onde se encontra o match
                tam = len(s1) #tamanho da sequencia original
                while tam >= len(prefix): #enauqnto o o tamanho da sequencia origina >= ao tamanho do prefixo
                    s = s1[ma:tam] #subsequencia, iniciada na posição do match
                    if len(s) >= len(prefix):#apenas dar append à lista se o tamanho de s for > que o do prefixo
                        res.append(s)
                    else:
                        pass #se não for maior avançar
                    tam -= 1 #diminuir 1 ao tamnho da seq
                res = list(dict.fromkeys(res)) #remove os duplicados
                res.sort(key = len) #ordenar as lista por tamanho crescente
            return res

def test():
    seq = "TACTATATTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print(st.get_leafes_below(2))
    print(st.nodes_below(2))
    #print (st.find_pattern("ACG"))
    print(st.matches_prefix("TACT"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    #print (st.find_pattern("TA"))
    #print(st.repeats(2,2))
    #print(st.nodes_below(2))

test()
print()
test2()
        
            
    
    
