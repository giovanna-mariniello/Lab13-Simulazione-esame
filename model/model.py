import copy

import geopy
import networkx as nx

from database.DAO import DAO

from geopy import distance


class Model:
    def __init__(self):
        self._all_anni = []
        self._grafo = nx.Graph()
        self._bestPath = []
        self._bestScore = 0

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
        #print(len(self._nodi))

        #print("getNodi()")
        self._grafo.add_nodes_from(self._nodi)
        #print(self._grafo.number_of_nodes())

        #print("addNodi()")
        self._idMap_nodi = {}
        for n in self._nodi:
            self._idMap_nodi[n.id] = n

        self._archi = DAO.get_archi(anno, forma, self._idMap_nodi)
        for t in self._archi:
            self._grafo.add_edge(t[0], t[1], weight=t[2])


    def get_dettagli_grafo(self):
        #print("num nodi dett", self._grafo.number_of_nodes())
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def get_nodi(self):
        return list(self._nodi)

    def get_peso_incidenti(self, nodo):
        peso_tot = 0
        archi_incidenti = self._grafo.edges(nodo, data=True)
        #nodi_connessi = []
        #print(archi_incidenti)
        for tupla in archi_incidenti:
            peso_tot += self._grafo[tupla[0]][tupla[1]]["weight"]


        return peso_tot

    def get_cammino(self):
        self._bestPath = []
        self._archiPath = []
        self._bestScore = 0

        parziale = []

        for n in self._nodi:
            parziale.append(n)
            self._ricorsione(parziale, [])

        return self._bestPath, self._archiPath, self._bestScore

    def _ricorsione(self, parziale, archi_parziale):

        ultimo = parziale[-1]
        vicini = self.get_vicini_ammissibili(ultimo, archi_parziale)

        if len(vicini) == 0:
            peso_path = self.get_peso_cammino(archi_parziale)
            if peso_path > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._archiPath = copy.deepcopy(archi_parziale)
                self._bestScore = peso_path
            return

        for v in vicini:
            if((ultimo, v)) not in archi_parziale:
                archi_parziale.append((ultimo, v, self._grafo.get_edge_data(ultimo, v)["weight"]))
                parziale.append(v)
                self._ricorsione(parziale, archi_parziale)
                parziale.pop()
                archi_parziale.pop()

    def get_vicini_ammissibili(self, ultimo, archi_parziale):

        incidenti = self._grafo.edges(ultimo, data=True)
        result = []

        for i in incidenti:
            if len(archi_parziale) != 0:
                if i[2]["weight"] > archi_parziale[-1][2]:
                    result.append(i[1])
            else:
                result.append(i[1])

        return result

    def get_peso_cammino(self, lista_archi):
        peso_path = 0

        for arco in lista_archi:
            peso_path += distance.geodesic((arco[0].Lat, arco[0].Lng), (arco[1].Lat, arco[1].Lng)).km

        return peso_path

    def get_distanza_arco(self, arco):
        return distance.geodesic((arco[0].Lat, arco[0].Lng), (arco[1].Lat, arco[1].Lng)).km

    def get_peso_arco(self, arco):
        return self._grafo[arco[0]][arco[1]]["weight"]










