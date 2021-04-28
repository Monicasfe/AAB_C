class MyGraphD:

    def __init__(self, g={}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())

    def get_edges(self):
        ''' Returns edges in the graph as a list of tuples (origin, destination, peso) '''
        edges = []
        for v in self.graph.keys(): #o v é a origem e de é o destino
            for des in self.graph[v]: #vai buscar o valor da chave v, ou seja o destinom dai o des
                d, p = des
                edges.append((v, d, p))
        return edges

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())

    ## add nodes and edges

    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys(): #se a chave não existe vai adicionar o vértice ao grafo/dicionario
            self.graph[v] = []

    def add_edge(self, o, d, wg):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys():  # verifica se ha o vertice o senao adiciona ao dicionario
            self.add_vertex(o)
        if d not in self.graph.keys():  # verifica se ha d vertice o senao adiciona ao dicionario
            self.add_vertex(d)
        des = []
        for j in self.graph[o]:
            vertice, peso = j
            des.append(vertice)
        if d not in des:
            # verifica se ha ligação entre os dois vertices, caso contrario adiciona o vertice d à lista do vertice o
            self.graph[o].append((d, wg))

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v):
        res = []
        for i in self.graph[v]:
            vertice, peso = i
            res.append(vertice)
        return res  # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v):
        res = []
        for i in self.graph.keys(): #por cada vertice no grafo, ou seja, a chave no dicionario
            for tuplo in self.graph[i]: #por cad tuplo, ou seja, os valores associados à chave
                d, wg = tuplo #descompata o tuplo em d e wg, sendo o d o vertice ewg o custo do arco
                if d == v: #se o destino do i, ou seja o d for = ao nosso v damos append ao i qeu vai ser o antecessor do v
                    res.append(i) #i é a chave e d o valor da chave que tem que ser = ao nosso v
        return res #lista com os antecessores

    def get_adjacents(self, v):
        suce = self.get_successors(v)  #vai buscar os sucessores e guarda na variável
        pred = self.get_predecessors(v)  #vai buscar os predecessores e guarda na variável
        res = pred
        for p in suce:  # adcionar os sucessores não presentes na lista vai evitar os duplicados
            if p not in res:
                res.append(p)
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
        l = [v]  #guardamos o nó de origem na nossa lista, lista de nós a ser processados
        res = []  # nós já processados com o resultado de nos atingiveis
        while len(l) > 0:  # enquanto ha elementos na lista l (lista de queue)
            node = l.pop(0)  # isolar o 1º no na queue
            if node != v:
                res.append(node)
            for elem in self.graph[node]:  #buscar os sucessores do nó que estamos a ver
                vertice, peso = elem #vai descompactar o tuplo para conseguir chegar ao vertice
                if veritce not in res and vertice not in l and vertice != node:  #adicionar á queue
                    l.append(vertice) #vai dar append à lista de espera à queue
        return res

    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v:  # se o v não entra na lista de nos acessiveis e for diferente é adiciona a lista
                res.append(node)  # controi o resultado sempre a colocar no fim, ou seja os primeiros ficam para ultimo
            s = 0  # posição onde vamos inserir o nó
            for elem in self.graph[node]:
                vertice, peso = elem
                if vertice not in res and vertice not in l:
                    l.insert(s, vertice) #vai juntar na posição certa por ordem (s) o elemento (elem)
                    s += 1 #incrementa +1 ao s para dar a posição e ordem de como correr a lista para ver em profundidade
        return res

    def distance(self, s, d):
        if s == d:
            return 0
        else:
            l = [(s, 0)]  # sitio onde tou a começar, lista de coisas a começar, ou seja começa pelo no de origem
            visitado = [s]  # nós processados a lista do resultado de nos atingiveis
            while len(l) > 0:  # enquanto ha elementos na lista l (lista de queue)
                node, dista = l.pop(0)  #isolar o 1º no na queue com a distancia somada (soma dos pesos do caminho percorrido)
                for elem in self.graph[node]: #iterar os sucessores do vertice s
                    vertice, peso = elem
                    if vertice == d:
                        return dista + peso
                    if vertice not in visitado and vertice not in l and vertice != node:  # adicionar á queue
                        l.append((vertice, dista + peso))
                        visitado.append(visitado)
            return None

    def shortest_path(self, s, d): #algoritmo de Dijkstra
        if s == d:
            return [s, d]
        else:
            l = [(s, [], 0)] #fila de espera com s a lista com caminho até o vertice + custo total até ao vertice
            visitado = [s]  # lista visitados
            while len(l) > 0:  # enquanto ha elementos na lista l (lista de queue)
                node, cami, dista = l.pop(0)  # isolar o 1º no na queue
                custo_minimo = 9999999999 #infinito basicamente
                for elem in self.graph[node]: #sucessores do nó 1 da lista l
                    vertice, peso = elem #separar o tuplo
                    if vertice == d: #quando vemos que é destino pomos logo o dist+peso e damos return. Esta é a consição desejada para o nosso return
                        return cami + [(node, vertice)] , dista + peso
                    if peso < custo_minimo:
                        custo_minimo = peso #caso haja 2 caminhos para o mesmo vertice o 1º custo que ficou vai ser o custo minimo a comparar com o seguinte
                        vertice_minimo = vertice
                if vertice_minimo not in visitado:  # adicionar á queue
                    l.append((vertice_minimo, cami + [(node, vertice_minimo)], dista + custo_minimo)) #adiciona o vertice_minimo à espera, junatemnte com o caminho associado e o custo total
                    visitado.append(vertice_minimo) #adiciona ao visitados
            return None

    def reachable_with_dist(self,s): #travessia total do grafo mas com as distancias associadas, faz a travessia sobre todos os pontos
        res = []
        l = [(s, 0)]
        while len(l) > 0:
            node, dista = l.pop(0)
            if node != s:
                res.append((node, dista))
            for elem in self.graph[node]:
                vertice, peso = elem #separar o tuplo em vertice e peso
                if not is_in_tuple_list(l, vertice) and not is_in_tuple_list(res, vertice): #juntar sempre a distancia ao registo dos elementos nos grafos
                    l.append((vertice, dista + peso)) #vertice e a distancia somada dos pesos
        return res

    ## cycles
    def node_has_cycle(self, v):
        l = [v]
        False
        visitado = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                vertice, peso = elem
                if vertice == v:
                    return True #chegou à partida e tem ciclo dai o true
                elif vertice not in visitado:
                    l.append(vertice)
                    visitado.append(vertice)
        return False #se o 1ª if nunca ocorrer para dar o true vai dar o false

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v):
                return True
        return res


def is_in_tuple_list(tl, val):
    res = False
    for (x, y) in tl:
        if val == x:
            return True
    return res


def test1():
    gr = MyGraphD({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})  #criar o grafo
    gr.print_graph()
    print(gr.get_nodes())
    print(gr.get_edges())


def test2():
    gr2 = MyGraphD()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)

    gr2.add_edge(1, 2, 2)
    gr2.add_edge(2, 3, 4)
    gr2.add_edge(3, 2, 3)
    gr2.add_edge(3, 4, 2)
    gr2.add_edge(4, 2, 5)

    gr2.print_graph()


def test3():
    gr = MyGraphD({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    gr.print_graph()
    print()
    print("Sucessores")
    print(gr.get_successors(2))
    print()
    print("Antecessores")
    print(gr.get_predecessors(2))
    print()
    print("Adjacentes")
    print(gr.get_adjacents(2))
    print()
    print("Grau entrada")
    print(gr.in_degree(2))
    print()
    print("Grau saida")
    print(gr.out_degree(2))
    print()
    print("Grau total")
    print(gr.degree(2))


def test4():
    gr = MyGraphD({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print("Distance 1-4 gr")
    print(gr.distance(1, 4))
    print()
    print("Distance 4-3 gr")
    print(gr.distance(4, 3))

    print()
    print("Shortest path 1-4 gr")
    print(gr.shortest_path(1, 4))
    print()
    print("Shortest path 4-3 gr")
    print(gr.shortest_path(4, 3))

    print()
    print("Reachable dist 1 gr")
    print(gr.reachable_with_dist(1))
    print()
    print("Reachable dist 3 gr")
    print(gr.reachable_with_dist(3))

    gr2 = MyGraphD({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print()
    print("Distance 2-1 gr2")
    print(gr2.distance(2, 1))
    print()
    print("Distance 1-5 gr2")
    print(gr2.distance(1, 5))

    print()
    print("Shortest path 1-5 gr2")
    print(gr2.shortest_path(1, 5))
    print()
    print("Shortest path 2-1 gr2")
    print(gr2.shortest_path(2, 1))

    print()
    print("Reachable dist 4 gr2")
    print(gr2.reachable_with_dist(1))
    print()
    print("Reachable dist 4 gr2")
    print(gr2.reachable_with_dist(4))


def test5():
    gr = MyGraphD({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    print("Node cycle 2 gr")
    print(gr.node_has_cycle(2))
    print()
    print("Node cycle 1 gr")
    print(gr.node_has_cycle(1))
    print()
    print("Total cycle gr")
    print(gr.has_cycle())

    gr2 = MyGraphD({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    print()
    print("Node cycle 1 gr2")
    print(gr2.node_has_cycle(1))
    print()
    print("Total cycle gr2")
    print(gr2.has_cycle())


if __name__ == "__main__":
    #test1()
    #test2()
    test3()
    #test4()
    #test5()