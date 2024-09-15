import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_anni = []
        self._grafo = nx.Graph()

    def get_all_anni(self):
        self._all_anni = DAO.get_all_anni()
        return self._all_anni

    def get_forme_anno(self, anno):
        forme_anno = DAO.get_forme_anno(anno)
        return forme_anno


    def crea_grafo(self, anno, forma):
        self._grafo.clear()
        #print("crea_grafo() called")
        self._nodi = DAO.get_nodi()
        print(len(self._nodi))

        #print("getNodi()")
        self._grafo.add_nodes_from(self._nodi)
        print(self._grafo.number_of_nodes())

        #print("addNodi()")
        self._idMap_nodi = {}
        for n in self._nodi:
            self._idMap_nodi[n.id] = n

        self._archi = DAO.get_archi(anno, forma, self._idMap_nodi)
        for t in self._archi:
            self._grafo.add_edge(t[0], t[1], weight=t[2])


    def get_dettagli_grafo(self):
        print("num nodi dett", self._grafo.number_of_nodes())
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def get_nodi(self):
        return list(self._nodi)

    def get_peso_incidenti(self, nodo):
        peso_tot = 0
        archi_incidenti = self._grafo.edges(nodo, data=True)
        #print(archi_incidenti)
        for tupla in archi_incidenti:
            peso_tot += self._grafo[tupla[0]][tupla[1]]["weight"]

        return peso_tot





