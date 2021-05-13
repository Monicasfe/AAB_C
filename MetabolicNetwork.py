# -*- coding: utf-8 -*-

from MyGraph_MetabolicNetwork import MyGraph

class MetabolicNetwork (MyGraph):
    
    def __init__(self, network_type = "metabolite-reaction", split_rev = False): #default do tipo de reação e a flag de split_rev é para dar ou não split às reações
        MyGraph.__init__(self, {})
        self.net_type = network_type #tipo de rede é o que passamos na função como nt_type
        self.node_types = {} #os nós vao ser um dicionário na mesma
        if network_type == "metabolite-reaction": #neste tipo vai haver 2 tipos de vértices
            self.node_types["metabolite"] = [] #tem um a lista vazia
            self.node_types["reaction"] = []
        self.split_rev =  split_rev
    
    def add_vertex_type(self, v, nodetype):
        self.add_vertex(v) #chama o add_vertex da classe mãe
        self.node_types[nodetype].append(v) #vai adicionar ao type devido de acordo como type dado
    
    def get_nodes_type(self, node_type): #obtem o tipo de nós
        if node_type in self.node_types: #ve todos os nós no dicionario
            return self.node_types[node_type] #dar todos os values do nó, ou seja, todos os arcos/ligações entre aquele nó e outros nós
        else: return None
    
    def load_from_file(self, filename):
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction")
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: raise Exception("Invalid line:")    

        
        if self.net_type == "metabolite-reaction": 
            self.graph = gmr.graph
            self.node_types = gmr.node_types #o que fica guradado no grafo
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr) #reações só de matabolitos
        elif self.net_type == "reaction-reaction": 
            self.convert_reaction_graph(gmr) #reações só de reações
        else: self.graph = {}
        
        
    def convert_metabolite_net(self, gmr):
        for m in gmr.node_types["metabolite"]: #o mesmo que as reações mas para os metaboitos
            self.add_vertex(m)
            suce = gmr.get_successors(m)
            for r in suce:
                suce_reac = gmr.get_successors(r)
                for mm in suce_reac:
                    if m != mm:
                        self.add_edge(m, mm)

        
    def convert_reaction_graph(self, gmr): 
        for r in gmr.node_types["reaction"]:
            self.add_vertex(r) #por cada reação
            suce_reac = gmr.get_successors(r) #ir busacar os sucessores, ou seja, os metabolitos
            for m in suce_reac: #por cada metabolito
                suce_meta = gmr.get_successors(m) #ir busacar os sucessores, ou seja, as 2ªas reações
                for rr in suce_meta: #por cada 2ª reação
                    if r != rr: #se ela for != da reação inicial
                        self.add_edge(r, rr) #adicionar o edge reação e reação sucessora


def test1():
    m = MetabolicNetwork("metabolite-reaction")
    m.add_vertex_type("R1","reaction")
    m.add_vertex_type("R2","reaction")
    m.add_vertex_type("R3","reaction")
    m.add_vertex_type("M1","metabolite")
    m.add_vertex_type("M2","metabolite")
    m.add_vertex_type("M3","metabolite")
    m.add_vertex_type("M4","metabolite")
    m.add_vertex_type("M5","metabolite")
    m.add_vertex_type("M6","metabolite")
    m.add_edge("M1","R1")
    m.add_edge("M2","R1")
    m.add_edge("R1","M3")
    m.add_edge("R1","M4")
    m.add_edge("M4","R2")
    m.add_edge("M6","R2")
    m.add_edge("R2","M3")
    m.add_edge("M4","R3")
    m.add_edge("M5","R3")
    m.add_edge("R3","M6")
    m.add_edge("R3","M4")
    m.add_edge("R3","M5")
    m.add_edge("M6","R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction") )
    print("Metabolites: ", m.get_nodes_type("metabolite") )

        
def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("example-net.txt")
    mmn.print_graph()
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("example-net.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("example-net.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("example-net.txt")
    rrsn.print_graph()
    print()

def test3():

    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("ecoli.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction"))
    print("Metabolites: ", mrn.get_nodes_type("metabolite"))
    print()
    mrn.size()

    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("ecoli.txt")
    mmn.print_graph()
    print()

    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("ecoli.txt")
    rrn.print_graph()
    print()

    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("ecoli.txt")
    mrsn.print_graph()
    print()

    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("ecoli.txt")
    rrsn.print_graph()
    print()
    print(mrn.size())
    print("-" * 50)
    print(mrn.mean_degree("out"))
    d = mrn.prob_degree("out")
    for x in sorted(d.keys()):
        print(x, "\t", d[x])

    print("-" * 50,"\n", "Mean distance")
    print(mrn.mean_distances())

#test1()
print()
#test2()
print()
test3()
