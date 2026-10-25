import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDShape(self):
        try:
            shape = self._model.getAllShape()
            for y in shape:
                self._view.ddshape.options.append(ft.dropdown.Option(y))
               # self._view._ddYear2.options.append(ft.dropdown.Option(y))
                # key=y.id,
                # text=y.name))
            self._view.update_page()

        except Exception as ex:
            self._view.txt_result1.controls.append(ft.Text(f"Errore nel recupero delle shape: {ex}", color="red"))
            self._view.update_page()


    def handle_graph(self, e):
        lat = self._view.txt_latitude.value
        lng = self._view.txt_longitude.value
        shape = self._view.ddshape.value
        minLat, minLng, maxLat, maxLng = self._model.getMaxMin()[0]

        if not lat:
            self._view.create_alert("Inserire la LATITUDINE prima di creare il grafo.")
            return
        if not lng :
            self._view.create_alert("Inserire la LONGITUDINE data prima di creare il grafo.")
            return
        if not shape:
          self._view.create_alert("Selezionare la SHAPE prima di creare il grafo.")
          return

        try:
            latFloat = float (lat)
        except Exception as ex:
            self._view.txt_result1.controls.append(
                ft.Text(f"Errore ! devi inserire un NUMERO per procedere: {ex}", color="red"))
            self._view.update_page()
            return

        try:
            lngFloat = float (lng)
        except Exception as ex:
            self._view.txt_result1.controls.append(ft.Text(f"Errore ! devi inserire un NUMERO per procedere: {ex}", color="red"))
            self._view.update_page()
            return

        if latFloat > maxLat or latFloat < minLat:
            self._view.create_alert(f"La latitudine deve essere un valore numerico come preso tra {minLat} e {maxLat}.")
            return

        if latFloat > maxLng or latFloat < minLng:
            self._view.create_alert(
                f"La longitudine deve essere un valore numerico come preso tra {minLng} e {maxLng}.")
            return

        try:
            self._model.creaGrafo(latFloat, lngFloat, shape)
           # self._view.txt_result.controls.append(ft.Text(f"Data selezionata: {anno1}", color="green"))
            #self._view.txt_result.controls.append(ft.Text(f"Data selezionata: {anno2}\n", color="green"))
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view.txt_result1.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
        # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
        # self.fillDDNodoStart(categoria)
        # self.fillDDNodoEnd(categoria)

        except Exception as ex:
            self._view.txt_result1.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
    #self._view.update_page()
        # C) 5 NODI CON PESO MAGGIORE
        top5N = self._model.getTop5Nodi()
        # self._view._txt_result.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f" 5 Nodi di GRADO maggiore ", color="green"))

        # self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        for i, (nodo, grado) in enumerate(top5N, start=1):
            self._view.txt_result1.controls.append(
                ft.Text(f"{i}) Nodo: {nodo.Name} - Grado: {grado}")
            )

        # C) 5 ARCHI CON PESO MAGGIORE
        top5 = self._model.getTop5Archi()
        # self._view._txt_result.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f" 5 Archi di peso maggiore ", color="green"))

        # self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        for i, arco in enumerate(top5, start=1):
            a1, a2, dati = arco
            self._view.txt_result1.controls.append(ft.Text(
                f"{i})  Arco: {a1.Name}   <--> {a2.Name}   )"
                f" - peso: {dati['weight']}")
            )
        self._view.update_page()

    def handle_path(self, e):
        n_nodes, _ = self._model.getGraphDetails()
        if n_nodes == 0:
            self._view.txt_result2.controls.append(
                ft.Text("Prima di cercare il percorso, devi creare il grafo!", color="red"))
            self._view.update_page()
            return

        percorso, punteggio = self._model.getPercorsoMigliore()

        if not percorso:
            self._view.create_alert("Nessun percorso trovato.")
            return

        self._view.txt_result2.controls.append(
            ft.Text(f"Punteggio migliore: {punteggio:.4f}", color="green")
        )

        for i, stato in enumerate(percorso, start=1):
            densita = self._model.calcolaDensita(stato)

            self._view.txt_result2.controls.append(
                ft.Text(f"{i}) {stato.Name} - Densità: {densita:.2f}")
            )

        self._view.update_page()


