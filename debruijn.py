# -*- coding: utf-8 -*-

from MyGraph_Aula_10 import MyGraph

class DeBruijnGraph (MyGraph):
    
    def __init__(self, frags):
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o, d): #tem que mudar porque precisamos de poder ligar várias vezes os mesmos vértices um ao outro por ligações diferentes
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        self.graph[o].append(d)

    def in_degree(self, v):
        """Grau de entrada de um dado nó"""
        res = 0 #contador
        for k in self.graph.keys(): #por cada cada vértice do grafo
            if v in self.graph[k]: #se o v se encontrar nos valores da chave
                res += self.graph[k].count(v) #conta os v e adiciona ao contador quanto gruas tem
        return res

    def create_deBruijn_graph(self, frags): #nós são sufixos e prefixos dos reads e as reads as nossas ligações
        for seq in frags: #por cada seq in frags
            suf = suffix(seq) #vê o sufixo da seq
            self.add_vertex(suf) #aadiciona o sufixo com um vértice
            pre = prefix(seq) #vê o prefixo da seq
            self.add_vertex(pre) #adiciona o prefixo como um vértice
            self.add_edge(pre, suf) #adiciona o edge com origem no prefixo e destino no sufixo

    def seq_from_path(self, path): #recebe já uma seq com path
        seq = path[0] #as primeiras 2 letras da seq vão ser as 2 da 1ª read do path
        for i in range(1,len(path)): #por cada i no range do tamanho do path, iniciando em 1
            nxt = path[i] #a proxima seq vai ser a que se se encotra a seguir no path
            seq += nxt[-1] #vai adicionar à seq apenas a última letra que está na nxt seq, uma vez que as iniciais já estão na seq em si
        return seq
    
def suffix (seq): 
    return seq[1:]
    
def prefix(seq):
    return seq[:-1]

def composition(k, seq):
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res



def test1():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    
    
def test2():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    print (dbgr.check_nearly_balanced_graph())
    print(dbgr.eulerian_cycle())
    print (dbgr.eulerian_path())


def test3():
    orig_sequence = "ATGCAATGGTCTG"
    frags = composition(3, orig_sequence)
    # ... completar
    pass



# test1()
print()
test2()
#print()
#test3()
    
