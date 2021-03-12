# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        self.num += 1
        self.nodes[origin][symbol] = self.num #buscar o valor associado ao simbolo e vai buscar o no
        self.nodes[self.num] = {}
    
    def add_pattern(self, p):
        posi = 0 #posicao na seq
        no = 0 #dicionario
        while posi < len(p): #pode ser feito com um for tambem
            if p[posi] not in self.nodes[no].keys(): #o p[posi] é o caracter, se não existir criar um no novo
                self.add_node(no, p[posi])  #cira o no novo
            no = self.nodes[no][p[posi]] #o novo no corrente e ir buscar ao dicionario o caracter e o valor
            posi += 1
            
    def trie_from_patterns(self, pats):
        for p in pats:
            self.add_pattern(p)
            
    def prefix_trie_match(self, text):
        pos = 0
        match = ""
        node = 0
        while pos < len(text):
            if text[pos] in self.nodes[node].keys():
                node = self.nodes[node][text[pos]]
                match += text[pos]
                if self.nodes[node] == {}:# se ainda não for folha ({} indica folha pq não há descendencia )
                    return match
                else:
                    pos +=1 #adicionar 1 ao padrao
            else:
                return None
        return None

        
    def trie_matches(self, text):
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])
            if m is not None: # is not faz o mesmo efeito que !=
                res.append((i, m))
        return res
          
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
