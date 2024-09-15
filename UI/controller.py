import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        lista_anni = self._model.get_all_anni()

        for a in lista_anni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))
            self._listYear.append(a)

        self._view.update_page()

    def fillDDShape(self, e):
        anno = self._view.ddyear.value

        lista_forme = self._model.get_forme_anno(anno)

        for f in lista_forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))
            self._listShape.append(f)

        self._view.update_page()


    def handle_graph(self, e):
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value

        if anno is None or forma is None:
            self._view.create_alert("Per favore seleziona i campi mancanti")
            return

        self._view.txt_result.controls.clear()

        self._model.crea_grafo(anno, forma)

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))

        num_nodi, num_archi = self._model.get_dettagli_grafo()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {num_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {num_archi}"))


        self._view.update_page()

        for n in self._model.get_nodi():
            self._view.txt_result.controls.append(ft.Text(f"Nodo {n} somma pesi su archi = {self._model.get_peso_incidenti(n)}"))

        self._view.update_page()



    def handle_path(self, e):
        cammino, archi_cammino, peso = self._model.get_cammino()

        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo: {peso}"))

        for arco in archi_cammino:
            n0 = arco[0]
            n1 = arco[1]
            peso = self._model.get_peso_arco((n0, n1))
            distanza = self._model.get_distanza_arco((n0, n1))
            self._view.txtOut2.controls.append(ft.Text(f"{n0} --> {n1}: peso {peso}, distanza {distanza} "))


        self._view.update_page()