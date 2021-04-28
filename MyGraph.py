# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys(): #o v é a origem e de é o destino
            for d in self.graph[v]: #vai buscar o valor da chave v
                edges.append((v,d))
        return edges
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    

    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys(): #se a chave não existe vai adicionar o vértice ao grafo
            self.graph[v] = []

    def add_edge(self, o, d):  # Adiciona o arco ao grafo
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys():
            self.add_vertex(o)  # Adiciona o nó de origem ao grafo
        if d not in self.graph.keys():
            self.add_vertex(d) #Adiciona o nó de destino ao grafo
        if d not in self.graph[o]: #se o d não estiver associado à chave da origem vai adicionar o d aos valores de o
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used
             
    def get_predecessors(self, v):
        """Vai buscar os antecessores e vai adicionar à lisa res"""
        res = []
        for i in self.graph.keys(): #por cada i, ou seja no dicionário/grafo
            if v in self.graph[i]: #se o valor que demos estiver nos sucessores do nosso i, ou seja na lista de valores da chave
                res.append(i) #juntamos o i à lista
        return res

    def get_adjacents(self, v):
        res = [] #tentar com sets um dia destes
        for j in self.graph.keys():
            if v in self.graph.keys() and j!=v:
                res.append(j)
        return res
    ## degrees    
    
    def out_degree(self, v): #saem
        return len(self.graph[v])

    def in_degree(self, v): #entram
        return len(self.get_predecessors(v))

    def degree(self, v): #todos
        return len(self.get_adjacents(v))
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        """Em larguram dá todos os nós que podem ser atingiveis a partir de 1"""
        l = [v] #guardamos o nó de origem na nossa lista, lista de nós a ser processaos
        res = [] #nós já processados
        while len(l) > 0: #verifica se a lista ainda tem alguma coisa na lista do snós a verificar
            node = l.pop(0) #guardar na variável node o elemento na posição 0 na lista l, o pop remove mesmo da lista
            if node != v: res.append(node) #se o nó é != do v então vai juntar à lita dos processados, depende se contamos o proprio nó ou não
            for elem in self.graph[node]: #para todos os sucessores do nó qu estamos neste momento, vamos ver se esão na lista dos processados e se é != do v
                if elem not in res and elem not in l and elem != node: #caso não esteja vamos adcicionar à lista dos a processar
                    l.append(elem) #vai juntar ao fim
        return res
        
    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v:
                res.append(node)#quando o nó de origem é != do nó atual
            s = 0 #posição onde vamos inserir o nó
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem) #vai juntar na posição certa por ordem (s) o elemento (elem)
                    s += 1 #incrementa +1 ao s para dar a posição e ordem de como correr a lista para ver em profundidade
        return res

    ##Exemplo: no grafo 2 temos que vai para o 5 e 6, como o 5 vem 1º vai para a posição 0 e o 6 para a 1, por isso vai
    #vai ser qual vem depois do 5 e vai ser o 7, como depois não vem nada vamos "voltar para trás" e como o pop remove a posição
    #0 o que era antes a posição 1, ou seja, o vértice 6, vamos ver esse vértice e ver se tem seguimento, como não tem vamos
    #para o ponto anterior que será o 2 e como já não tem nada vai para o 3.
    #Vai tudo para a mesma lista mas o mais recente fica em 1º ou sej ana posição 0 da lista l e aempre assim até a
    #lista estar vazia
    
    def distance(self, s, d):
        if s == d:
            return 0
        res = [(s, 0)] #cria a lista de tuplos entre o nó e a distancia
        visitado  = [s] #são os nós que já foram visitados
        while len(res)>0: #o while chegaro ao fim significa que que não parou no 1º return, significa que o nó não é atingivel e vai retornar o none
            no, dist = res.pop(0)
            for el in self.graph[no]: #vamos buscar os sucessores do no
                if el == d: #quando vemos que é destino pomos logo o dist+1 e damos return. Esta é a consição desejada para o nosso return
                    return dist+1
                elif el not in visitado: #se não estiver nos visitados adicionamos à lista dos tuplos o tuplo do el , dist
                    res.append((el, dist + 1)) #isto vai ser uma queue
                    visitado.append(el) #para garantir que não vai usar outra vez um vértice já utilizado
        return None #ocorre se não houver caminho
        
    def shortest_path(self, s, d):
        if s == d:
            return [s,d]
        #else
        lista = [(s, [])] #em vez de termos aqui a lista como caminho completo guardamos apenas o antecessor do nó e refazer depoiis o caminho completo
        visitado = [s] #lista com os nós já visitados
        while len(lista)>0:
            no, cami = lista.pop(0) #dá pop do nó e do caminho /ficamos com o nó e uma lista vazia que é o cami
            for el in self.graph[no]: #vai dar os sucessores do nosso nó (chave)
                if el == d: #se o nosso elemento sucessor ao nó for = ao nosso destino
                    return cami + [no, el] #se o nosso el que é o sucessor for = ao nosso destino vamso adcionar ao caminho nosso no e o el qeu vai ser = ao d, ou seja, acabou
                elif el not in visitado: #se não estiver na lista dos visitados
                    lista.append((el, cami+[no])) #adicionar à queue #em vez de somar vamos somar o caminho ao anterior ao nó#vamos adicionar à lista o elementos (el) e o nó
                    visitado.append(el)# aos visitados vamos adicionar o elemeneto que acabamos de ver
        return None
        
    def reachable_with_dist(self, s):
        """Fazer a travessia toda do grafo mas com a distância associada (neste caso naão está implementado
        mas podemos guardar também o predecessor para além da distância)"""
        res = []
        l = [(s,0)] #começamos com o 0 na mesma
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: #na 1ª iteração não se verifica porque o s é = ao nó, serve para ignorar a origem
                res.append((node,dist))
            #Serve para incrementar a posição
            for elem in self.graph[node]: #ver os sucessores do no
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))#mas aqui em vez de pormos apenas o nó pomos o nó com a dist associa num tuplo
                    #vai adicionar 1 à dist que já vem do antecessor, no caso de querermos ir do 1 para o dois vamos dar
                    #append de (2, 0+1) = (2, 1)
        return res

## cycles
    def node_has_cycle (self, v):
        """
        VEMOS SE O NÓ DENTRO DOS SEUS SUCESSORES É CICLICO OU NÃO. TIPO SE UM DOS SEUS SUCESSORES VAI SER SEU ANTECESSOR
        Iniciamos a travessia por todos os nó e vemos se conseguimos chegar ao mesmo nó.
        Se no fim não houver é porque o grafo não é ciclico. Podemos usar o lateral ou vertical"""
        l = [v]
        visitado = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v:
                    return True #chegou à partida e tem ciclo dai o true
                elif elem not in visitado:
                    l.append(elem)
                    visitado.append(elem)
        return False #se o 1ª if nunca ocorrer para dar o true vai dar o false

    def has_cycle(self):
        for v in self.graph.keys():
            if self.node_has_cycle(v):
                return True
        return False


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x:
            return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    print (gr.distance(1,4))
    print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())


if __name__ == "__main__":
    #test1()
    test2()
    #test3()
    #test4()
    #test5()
