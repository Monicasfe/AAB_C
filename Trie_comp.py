# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        """Recebe como parametros origin e symbol
        começa sempre com o 0 pq é o 1º nó e parte depois dai"""
        self.num += 1 #contador do nº de nos
        self.nodes[origin][symbol] = self.num #buscar o valor associado ao simbolo e vai buscar o no
        self.nodes[self.num] = {} #abre o dicionario de um key(no), od {} dento dos {} 1.
    
    def add_pattern(self, p):#este pe cem da funçaoa abaixo
        posi = 0 #posicao na seq
        no = 0 #dicionario
        while posi < len(p): #enaqunto a posição (iterador) < que que tamanho padrao
            if p[posi] not in self.nodes[no].keys(): #o p[posi] é o caracter se existir avança, se não existir criar um novo
                self.add_node(no, p[posi])  #cira o no novo, sendo no o nº e p[posi] o simbolo
            no = self.nodes[no][p[posi]] #o novo no corrente e ir buscar ao dicionario o caracter e o valor
            #define o novo no, sendo que o nº que era o 0 por exemplo passa a ser mais que o anterior
            posi += 1 #avaça na posicao
            
    def trie_from_patterns(self, pats):#pega num padrão da lista dos padroes
        for p in pats:
            self.add_pattern(p)#chama a função acima
            
    def prefix_trie_match(self, text):
        """
        Serve para ver se um padrão se encontra na árvore já
        """
        pos = 0
        match = ""
        node = 0
        while pos < len(text):
            if text[pos] in self.nodes[node].keys():#verifica se a base está na arvore
                node = self.nodes[node][text[pos]]#guarda o nó em que está a base (items do 2º {})
                match += text[pos]#adiciona a base correspondente ao match
                if self.nodes[node] == {}:#quando chega à folha retorna o match ({} indica folha pq não há descendencia )
                    return match
                else:
                    pos +=1 #add 1 à posição para continuar a pesquisa no texto
            else:
                return None #quando não há correspondencia nenhuma retorna none
        return None#caso de má argumentação

        
    def trie_matches(self, text):
        """Descobre se a aprtir de qualquer posição inicial se há match"""
        res = []
        for i in range(len(text)):#iteração para cada um dos caracteres da string text
            m = self.prefix_trie_match(text[i:])# guarada em m o resultado da prefix_trie_match desde a posi i até ao fim
            # começa em todas as posi iniciais possiveis
            if m is not None: # is not faz o mesmo efeito que !=
                res.append((i, m))# se houver padroes indexar a res um tuplo com a posi e o padrao
        return res #devolve a lista com os tuplos
          
def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
test()
print()
test2()
