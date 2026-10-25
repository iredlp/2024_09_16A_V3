
from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapR = {}

    def get_Lat(self):
        return DAO.get_Lat()

    def get_Lng(self):
        return DAO.get_Long()

    def getAllShape(self):
        return DAO.getAllShape()

    def getMaxMin(self):
        return DAO.getMaxMin()

    def creaGrafo(self, Lat, Lng, shape):
        self._grafo.clear()
        self._idMapR.clear()

        state = DAO.getAllNodes( Lat, Lng, shape)
        for a in state:
            self._idMapR[a.id] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        # Recupero geni e interazioni
        avvistamenti = DAO.get_all_sightings()
        vicini = DAO.getAllVicini()
        print("3 - Informazioni recuperate")


        # Aggiungo gli archi
        for i in range(len(state)):
            a1 = state[i]
            for j in range(i + 1, len(state)):
                a2 = state[j]

                # Controllo se esiste l'interazione
                for inter in vicini:
                    if (inter. state1 == a1.id and inter.state2 == a2.id) or \
                            (inter. state1 == a2.id and inter.state2 == a1.id):

                        # Recupero i tempi
                        durata1 = 0
                        durata2 = 0

                        for g in avvistamenti:
                            if g.state.upper() == a1.id and g.shape == shape:
                                durata1 += g.duration
                            if g.state.upper() == a2.id and g.shape == shape:
                                durata2 += g.duration

                                peso = durata1 + durata2
                                if peso>0:
                                    self._grafo.add_edge(a1, a2, weight=peso)
        print("4 - Archi aggiunti")


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getTop5Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(
            archi,
            key=lambda x: x[2]["weight"],
            reverse=True
        )[:5]

    def getTop5Nodi(self):
        nodi = self._grafo.nodes() #(data=True) SE METTO QUESTO RESTITUISCE UN DIZIONARIO CON I DATI PER OGNI NODO
        top5=sorted( nodi, key=lambda x: self._grafo.degree(x),  reverse=True )[:5]
        return [(nodo, self._grafo.degree(nodo)) for nodo in top5]

    def calcolaDensita(self, stato):
        return stato.Population / stato.Area

    def getPercorsoMigliore(self):
        self.bestPath = []
        self.bestScore = 0

        for nodo in self._grafo.nodes():
            self.ricorsionePercorso(nodo, [nodo], 0, 0)

        return self.bestPath, self.bestScore

    def ricorsionePercorso(self, nodo, percorso, sommaPesi, distanzaTotale):
        if distanzaTotale > 0:
            punteggio = sommaPesi / distanzaTotale

            if punteggio > self.bestScore:
                self.bestScore = punteggio
                self.bestPath = percorso.copy()

        for vicino in self._grafo.neighbors(nodo):
            if self.calcolaDensita(vicino) > self.calcolaDensita(nodo):
                if vicino not in percorso:
                    peso = self._grafo[nodo][vicino]["weight"]
                    distanza = nodo.distance_HV(vicino)

                    self.ricorsionePercorso(vicino, percorso + [vicino],sommaPesi + peso, distanzaTotale + distanza  )