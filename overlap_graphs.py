# -*- coding: utf-8 -*-

from MyGraph_Aula_10 import MyGraph

class OverlapGraph(MyGraph):
    
    def __init__(self, frags, reps = False):
        MyGraph.__init__(self, {})
        # self.create_overlap_graph(frags)
        if reps:
            self.create_overlap_graph_with_reps(frags)
        else:
            self.create_overlap_graph(frags)
        self.reps = reps
        
    
    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags):
        self.graph
        for i in frags: #por cada seq em frags
            self.add_vertex(i) #vai criar um vértice no grafo
        for seq in frags: # por cada seq em frags
            suf = suffix(seq) #ber qual o sufixo da seq, ou seja todas as leras menos a primeira da seq
            for seq2 in frags: #por cada seq in frags
                if prefix(seq2) == suf: #se o prefixo, ou seja, tudo menos a ultima letra, for = ao sufixo
                    self.add_edge(seq, seq2) #adicionar edge como tuplo seq, seq2 (sufixo, prefixo)


    def create_overlap_graph_with_reps(self, frags):  # caso de replicas de fragmentos
        idnum = 1 #por o id ocm o1 para adicionar os vértices
        for seq in frags: #por cada seq no frags
            self.add_vertex(seq + "-" + str(idnum)) # vai adicionar o vertice com a seq mais um identificador associado que começa em 1
            idnum = idnum + 1 #o proximo id da seq vai ser igual ao anterior +1
        idnum = 1 #por o id com 1 para adicionar os edges
        for seq in frags: #por cada seq in frags
            suf = suffix(seq) #ver o sufixo da seq
            for seq2 in frags: #por cada seq in frags
                if prefix(seq2) == suf: #ver o prefixo e se for igual ao sufixo
                    for x in self.get_instances(seq2): # por cada x vindo da função get_instance
                        self.add_edge(seq + "-" + str(idnum), x) #adicionar edges ao vérice, primeiro damos o vértice de origem (seq + "-" + str(idnum)) e depois o de destino que vai ser o x que é cada elemento vindo da lista da função get_instances
            idnum = idnum + 1 #vai para o p´roximo vértice

    def get_instances(self, seq):
        res = []
        for k in self.graph.keys(): #k vai ser o nó do grafo por isso
            if seq in k: #se a seq dada estiver no k, sendo que a seq vai ser uma read, ou seja, uma seq pequena
                res.append(k) #dar append do k à lista
        return res #resulta numa lista com todos os vertices que contêm a seq dada, juntamente como id associado
    
    def get_seq(self, node):
        if node not in self.graph.keys(): #se o nó não estiver na keys, pou seja se a seq ou seq+id não estiver nas keys
            return None # devolve none
        if self.reps: #se houver repetições
            return node.split("-")[0] #vai ao nó dá split, e fica apenas com a seq sem o numero
        else: #se não houver reps
            return node #dá o nó, apenas a seq portanto
    
    def seq_from_path(self, path): #recebe já uma seq com path
        if not self.check_if_hamiltonian_path(path): #verifica se o caminho é hamiltoniano
            return None #se não for return None
        seq = self.get_seq(path[0]) #as primeiras 3 letras da seq vão ser as 3 da 1ª read do path
        for i in range(1, len(path)): #por cada i no range do tamanho do path, iniciando em 1
            nxt = self.get_seq(path[i]) #a proxima seq vai ser a que se se encotra a seguir no path, mas tem que ir buscar apenas a seq sem o id à função get seq
            seq += nxt[-1] #vai adicionar à seq apenas a última letra que está na nxt seq, uma vez que as iniciais já estão na seq em si, porque são os prefixos dela
        return seq    #dá return da seq
   
                    
# auxiliary
def composition(k, seq): #segmentar em conjuntos de tamanho k
    res = []
    for i in range(len(seq)-k+1): #por cada i no range do tamanho da seq menos k+1
        res.append(seq[i:i+k]) #dar append à lista res as subseqs de tamanho k, desde a posição i até i+k
    #res.sort()
    return res
    
def suffix (seq): #dá tudo menos a a primeira posição
    return seq[1:]
#ambas ajudam a ver se um read vem a seguir ao outro ou não
def prefix(seq): #dá tudo menos a ultima posição
    return seq[:-1]

  
# testing / mains
def test1():
    seq = "CAATCATGATG"
    k = 3
    print (composition(k, seq))
   
def test2():
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags, False)
    ovgr.print_graph()

def test3():
     frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
     ovgr = OverlapGraph(frags, True)
     ovgr.print_graph()

def test4():
    frags = ["ATA",  "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    path = ["ACC-2", "CAA-8", "CAT-5", "ATG-3"]
    ovgr.print_graph()
    print (ovgr.check_if_valid_path(path))
    print (ovgr.check_if_hamiltonian_path(path))
    path2 = ["ACC-2", "CCA-8", "CAT-5", "ATG-3", "TGG-13", "GGC-10", "GCA-9", "CAT-6", "ATT-4", "TTT-15", "TTC-14", "TCA-12", "CAT-7", "ATA-1", "TAA-11"]
    print (ovgr.check_if_valid_path(path2))
    print (ovgr.check_if_hamiltonian_path(path2))
    print (ovgr.seq_from_path(path2))

def test5():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)

    path = ovgr.search_hamiltonian_path()
    print(path)
    print (ovgr.check_if_hamiltonian_path(path))
    print (ovgr.seq_from_path(path))

def test6():
    orig_sequence = "CAATCATGATGATGATC"
    frags = composition(3, orig_sequence)
    print (frags)
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    print (path)
    print (ovgr.seq_from_path(path))
   
#test1()
print()
# test2()
print()
# test3()
#print()
test4()
#print()
#test5()
#print()
#test6()
