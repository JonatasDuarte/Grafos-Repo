# -*- coding: utf-8 -*-

import copy

class VerticeInvalidoException(Exception):
    pass

class ArestaInvalidaException(Exception):
    pass

class MatrizInvalidaException(Exception):
    pass

class Grafo:

    QTDE_MAX_SEPARADOR = 1
    SEPARADOR_ARESTA = '-'
    __maior_vertice = 0

    def __init__(self, V=None, M=None):
        '''
        Constrói um objeto do tipo Grafo. Se nenhum parâmetro for passado, cria um Grafo vazio.
        Se houver alguma aresta ou algum vértice inválido, uma exceção é lançada.
        :param V: Uma lista dos vértices (ou nodos) do grafo.
        :param V: Uma matriz de adjacência que guarda as arestas do grafo. Cada entrada da matriz tem um inteiro que indica a quantidade de arestas que ligam aqueles vértices
        '''

        if V == None:
            V = list()
        if M == None:
            M = list()

        for v in V:
            if not(Grafo.verticeValido(v)):
                raise VerticeInvalidoException('O vértice ' + v + ' é inválido')
            if len(v) > self.__maior_vertice:
                self.__maior_vertice = len(v)

        self.N = list(V)

        if M == []:
            for k in range(len(V)):
                M.append(list())
                for l in range(len(V)):
                    if k>l:
                        M[k].append('-')
                    else:
                        M[k].append(0)


        if len(M) != len(V):
            raise MatrizInvalidaException('A matriz passada como parâmetro não tem o tamanho correto')

        for c in M:
            if len(c) != len(V):
                raise MatrizInvalidaException('A matriz passada como parâmetro não tem o tamanho correto')

        for i in range(len(V)):
            for j in range(len(V)):
                '''
                Verifica se os índices passados como parâmetro representam um elemento da matriz abaixo da diagonal principal.
                Além disso, verifica se o referido elemento é um traço "-". Isso indica que a matriz é não direcionada e foi construída corretamente.
                '''
                if i>j and not(M[i][j] == '-'):
                    raise MatrizInvalidaException('A matriz não representa uma matriz não direcionada')


                aresta = V[i] + Grafo.SEPARADOR_ARESTA + V[j]
                if not(self.arestaValida(aresta)):
                    raise ArestaInvalidaException('A aresta ' + aresta + ' é inválida')

        self.M = list(M)

    def arestaValida(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro está dentro do padrão estabelecido.
        Uma aresta é representada por um string com o formato a-b, onde:
        a é um substring de aresta que é o nome de um vértice adjacente à aresta.
        - é um caractere separador. Uma aresta só pode ter um único caractere como esse.
        b é um substring de aresta que é o nome do outro vértice adjacente à aresta.
        Além disso, uma aresta só é válida se conectar dois vértices existentes no grafo.
        :param aresta: A aresta que se quer verificar se está no formato correto.
        :return: Um valor booleano que indica se a aresta está no formato correto.
        '''

        # Não pode haver mais de um caractere separador
        if aresta.count(Grafo.SEPARADOR_ARESTA) != Grafo.QTDE_MAX_SEPARADOR:
            return False

        # Índice do elemento separador
        i_traco = aresta.index(Grafo.SEPARADOR_ARESTA)

        # O caractere separador não pode ser o primeiro ou o último caractere da aresta
        if i_traco == 0 or aresta[-1] == Grafo.SEPARADOR_ARESTA:
            return False

        if not(self.existeVertice(aresta[:i_traco])) or not(self.existeVertice(aresta[i_traco+1:])):
            return False

        return True

    @classmethod
    def verticeValido(self, vertice: str):
        '''
        Verifica se um vértice passado como parâmetro está dentro do padrão estabelecido.
        Um vértice é um string qualquer que não pode ser vazio e nem conter o caractere separador.
        :param vertice: Um string que representa o vértice a ser analisado.
        :return: Um valor booleano que indica se o vértice está no formato correto.
        '''
        return vertice != '' and vertice.count(Grafo.SEPARADOR_ARESTA) == 0

    def existeVertice(self, vertice: str):
        '''
        Verifica se um vértice passado como parâmetro pertence ao grafo.
        :param vertice: O vértice que deve ser verificado.
        :return: Um valor booleano que indica se o vértice existe no grafo.
        '''
        return Grafo.verticeValido(vertice) and self.N.count(vertice) > 0

    def __primeiro_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o vértice X
        :param a: a aresta a ser analisada
        :return: O primeiro vértice da aresta
        '''
        return a[0:a.index(Grafo.SEPARADOR_ARESTA)]

    def __segundo_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o vértice Y
        :param a: A aresta a ser analisada
        :return: O segundo vértice da aresta
        '''
        return a[a.index(Grafo.SEPARADOR_ARESTA)+1:]

    def __indice_primeiro_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o índice do vértice X na lista de vértices
        :param a: A aresta a ser analisada
        :return: O índice do primeiro vértice da aresta na lista de vértices
        '''
        return self.N.index(self.__primeiro_vertice_aresta(a))

    def __indice_segundo_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o índice do vértice Y na lista de vértices
        :param a: A aresta a ser analisada
        :return: O índice do segundo vértice da aresta na lista de vértices
        '''
        return self.N.index(self.__segundo_vertice_aresta(a))

    def existeAresta(self, a: str):
        '''
        Verifica se uma aresta passada como parâmetro pertence ao grafo.
        :param aresta: A aresta a ser verificada
        :return: Um valor booleano que indica se a aresta existe no grafo.
        '''
        existe = False
        if Grafo.arestaValida(self, a):
            for i in range(len(self.M)):
                for j in range(len(self.M)):
                    if self.M[self.__indice_primeiro_vertice_aresta(a)][self.__indice_segundo_vertice_aresta(a)]:
                        existe = True

        return existe

    def adicionaVertice(self, v):
        '''
        Inclui um vértice no grafo se ele estiver no formato correto.
        :param v: O vértice a ser incluído no grafo.
        :raises VerticeInvalidoException se o vértice já existe ou se ele não estiver no formato válido.
        '''
        if v in self.N:
            raise VerticeInvalidoException('O vértice {} já existe'.format(v))

        if self.verticeValido(v):
            if len(v) > self.__maior_vertice:
                self.__maior_vertice = len(v)

            self.N.append(v) # Adiciona vértice na lista de vértices
            self.M.append([]) # Adiciona a linha

            for k in range(len(self.N)):
                if k != len(self.N) -1:
                    self.M[k].append(0) # adiciona os elementos da coluna do vértice
                    self.M[self.N.index(v)].append('-') # adiciona os elementos da linha do vértice
                else:
                    self.M[self.N.index(v)].append(0)  # adiciona um zero no último elemento da linha
        else:
            raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

    def adicionaAresta(self, a):
        '''
        Adiciona uma aresta ao grafo no formato X-Y, onde X é o primeiro vértice e Y é o segundo vértice
        :param a: a aresta no formato correto
        :raise: lança uma exceção caso a aresta não estiver em um formato válido
        '''
        if self.arestaValida(a):
            i_a1 = self.__indice_primeiro_vertice_aresta(a)
            i_a2 = self.__indice_segundo_vertice_aresta(a)
            if i_a1 < i_a2:
                self.M[i_a1][i_a2] += 1
            else:
                self.M[i_a2][i_a1] += 1
        else:
            raise ArestaInvalidaException('A aresta {} é inválida'.format(a))

    def remove_aresta(self, a):
        '''
        Remove uma aresta ao grafo no formato X-Y, onde X é o primeiro vértice e Y é o segundo vértice
        :param a: a aresta no formato correto
        :raise: lança uma exceção caso a aresta não estiver em um formato válido
        '''
        if self.arestaValida(a):
            if self.existeAresta(a):
                i_a1 = self.__indice_primeiro_vertice_aresta(a)
                i_a2 = self.__indice_segundo_vertice_aresta(a)
                if i_a1 < i_a2:
                    self.M[i_a1][i_a2] -= 1
                else:
                    self.M[i_a2][i_a1] -= 1
        else:
            raise ArestaInvalidaException('A aresta {} é inválida'.format(a))

    def ha_paralelas(self):
        ind = len(self.M)
        for i in range(len(self.M)):
            for j in range(ind):
                if(self.M[i][j]==2):
                    return True
        return False
    
    def grau(self, V):
        if(self.verticeValido(V)):
            ind = self.N.index(V)
            count = 0

            for j in range(len(self.M)):
                if(self.M[ind][j] !='-'):
                    count+=self.M[ind][j]


            # COLUNA
            for i in range(len(self.M)):
                if(self.M[i][ind]!='-' and i != ind):
                    count+=self.M[i][ind]
            return count
            

    def vertices_nao_adjacentes(self):
        ind = len(self.M)
        res = []
        for i in range(ind):
            for j in range(ind):
                if(self.M[i][j]==0):
                    item = self.N[i]+'-'+self.N[j]
                    res.append(item)
        return res
        
            
    def arestas_sobre_vertice(self, V):
        if(self.verticeValido(V)):
            arestas = []
            ind = self.N.index(V)
            for i in range(len(self.M)):
                if(self.M[i][ind]!='-' and self.M[i][ind]>0):
                    item = self.N[i]+'-'+self.N[ind]
                    arestas.extend([item for i in range(self.M[i][ind])])
                if(i != ind):
                    if(self.M[ind][i] !='-' and self.M[ind][i]>0):
                        item = self.N[ind]+'-'+self.N[i]
                        arestas.extend([item for i in range(self.M[ind][i])])
            return arestas


    def eh_completo(self):
        if(self.ha_laco()):
            return False
        if(self.ha_paralelas()):
            return False
    


        ind = len(self.M)
        res = []
        for i in range(ind):
            for j in range(ind):
                if(self.M[i][j]==0 and i!=j):
                    item = self.N[i]+'-'+self.N[j]
                    res.append(item)
        

        return res == []
        

    def ha_laco(self):
        ind = len(self.M)
        for i in range(ind):
            if(self.M[i][i] > 0):
                return True
        return False

    def quantidadeDeArestas(self):
        count = 0
        for i in self.M:
            for j in i:
                if(j == 1):
                    count+=1
        return count

    def caminhoEuleriano(self):
        qntVerticesImpares = sum([self.grau(vertice) % 2 for vertice in self.N])
        # Verificamos se é possível formar um caminho euleriano
        if(qntVerticesImpares != 0 and qntVerticesImpares != 2):
            return None
        else:
            # Criamos uma cópia identica do grafo original para percorremos o caminho
            # e remover as arestas percorridas
            grafoCopia = Grafo(self.N, self.M)
            caminho = []
            raiz = None
            if(qntVerticesImpares == 0):
                # Se não gouver vértice de grau impar podemos começar de qualquer vértice
                raiz = self.N[0]
            else:
                # Senão, temos que começar de algum vértice de grau impar
                verticesImpares = list(filter(lambda vertice: self.grau(vertice) % 2 != 0, self.N))
                raiz = verticesImpares[0]


            while(grafoCopia.quantidadeDeArestas() > 0):
                # Enquanto houverem arestas para percorrer o caminho continuará a ser formado
                arestasSobVertice = self.arestas_sobre_vertice(raiz)
                for aresta in (arestasSobVertice):
                    vertices = aresta.split(self.SEPARADOR_ARESTA)
                    vertices.remove(raiz)
                    verticeCorrente = vertices[0]
                    if(grafoCopia.grau(verticeCorrente) > 1 or grafoCopia.quantidadeDeArestas() == 1):
                        # Verificamos se o vértice não é uma ponte
                        # NOTA: achamos a definição de ponte um pouco abstrata e percebemos
                        # que também pode ser uma aresta de A para B que, se removido do
                        # grafo não haverá mais caminho de A para B.
                        raiz = verticeCorrente
                        caminho.append(aresta)
                        grafoCopia.remove_aresta(aresta)
                        break
            return caminho

    def __str__(self):
        '''
        Fornece uma representação do tipo String do grafo.
        O String contém um sequência dos vértices separados por vírgula, seguido de uma sequência das arestas no formato padrão.
        :return: Uma string que representa o grafo
        '''

        # Dá o espaçamento correto de acordo com o tamanho do string do maior vértice
        espaco = ' '*(self.__maior_vertice)

        grafo_str = espaco + ' '

        for v in range(len(self.N)):
            grafo_str += self.N[v]
            if v < (len(self.N) - 1):  # Só coloca o espaço se não for o último vértice
                grafo_str += ' '

        grafo_str += '\n'

        for l in range(len(self.M)):
            grafo_str += self.N[l] + ' '
            for c in range(len(self.M)):
                grafo_str += str(self.M[l][c]) + ' '
            grafo_str += '\n'

        return grafo_str
    
    # def ciclo_hamiltoniano(self):
    #     corrente = 0
    #     caminho = []
    #     grafoCopia = copy.deepcopy(self)
    #     while(len(caminho) < len(grafoCopia.N)):
    #         for index in range(len(grafoCopia.N)):
    #             if(
    #                 (
    #                     grafoCopia.M[corrente][index] == '-' and grafoCopia.M[index][corrente] == 1
    #                 ) or
    #                 (
    #                     grafoCopia.M[corrente][index] == 1)
    #                 ):
    #                 caminho.append(grafoCopia.N[corrente])
    #                 corrente = index
    #                 print(grafoCopia.N[corrente])
    #                 grafoCopia.remove_aresta()
    #                 break
    #     return corrente

    def vertices_adjacentes(self, vertice):
        arestas = self.arestas_sobre_vertice(vertice)
        vertices = []
        for aresta in arestas:
            verticeAdj = aresta.split('-')
            verticeAdj.remove(vertice)
            vertices.append(verticeAdj[0])
        
        return vertices

    def ciclo_hamiltoniano(self):
        aux = self.aux_ciclo_hamiltoniano(self.N[0], [])
        return None if(not len(aux)) else aux

    def aux_ciclo_hamiltoniano(self, vertice, path):
        if vertice not in set(path):
            path.append(vertice)
            if len(path) == len(self.N):
                return path
            # inicio do backtracking
            todos_candidatos = []
            for prox_ponto in self.vertices_adjacentes(vertice):
                res_path = [i for i in path]
                # print(res_path)
                candidatos = self.aux_ciclo_hamiltoniano(prox_ponto, res_path)
                if candidatos is not None:
                    todos_candidatos.extend(candidatos)
                    break
                else:
                    pass
            return todos_candidatos
        else:
            return None