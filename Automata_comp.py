# -*- coding: utf-8 -*-


class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern): #o pattern vem como argumento pq não foi guardado no init da classe
        for q in range(self.numstates):
            for a in self.alphabet:
                prefixo = pattern[:q] + a #aqui não precisamos de q-1 pq o q é exclusivo nº final da [] não conta
                self.transitionTable[(q,a)] = overlap(prefixo, pattern) #q é o estado onde estou, e a o estado para onde vou
       
    def printAutomata(self):
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table:")
        for k in self.transitionTable.keys():
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
        return self.transitionTable[(current, symbol)]
        #ou return self.transitionTable.get((current, symbol))
        #a diferença entre 1 e outro é que com o get se não houver a chave no dict posso retornar o valor por defeito
        #definido por nos tipo get((current, symbol), 5) relacionado com kwargs

    def applySeq(self, seq):
        q = 0 #iniciador do estado
        res = [q]
        for c in seq:
            q = self.nextState(q, c) #guardamos pq depois o estado terá que comecar neste
            res.append(q)
        return res
        
    def occurencesPattern(self, text):
        q = 0 
        res = []
        #applySeq(text).index(self.numstates) - len(self.pattern)
        for aa in range(len(text)):
            q = self.nextState(q, text[aa])
            if q == self.numstates - 1:
                res.append(aa - self.numstates + 2)
                #para ter o tamanho da seq pomos 1 e depois para dar a casa em branco pomos outro
        return res

def overlap(s1, s2):
    maxov = min(len(s1), len(s2))
    for i in range(maxov,0,-1):
        if s1[-i:] == s2[:i]: return i
    return 0
               
def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print (auto.applySeq("CACAACAA"))
    print (auto.occurencesPattern("CACAACAA"))

if __name__ == "__main__":
    test()

#States:  4
#Alphabet:  AC
#Transition table:
#0 , A  ->  1
#0 , C  ->  0
#1 , A  ->  1
#1 , C  ->  2
#2 , A  ->  3
#2 , C  ->  0
#3 , A  ->  1
#3 , C  ->  2
#[0, 0, 1, 2, 3, 1, 2, 3, 1]
#[1, 4]



