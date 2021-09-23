import PySimpleGUI as sg

sg.theme("SystemDefault1")


class Interface:
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__container = []
        self.__window = sg.Window("Extrator CV Lattes",
                                  self.__container,
                                  font=("Helvetica", 14))

    @property
    def window(self):
        return self.__window

    @property
    def container(self):
        return self.__container

    def criar_tela(self):
        linha0 = [sg.Text("Pesquisa:")]
        linha1 = [sg.Text("Digite:"), sg.InputText("", key="nome")]
        linha2 = [sg.Button("Buscar por nome"),
                  sg.Button("Buscar por local de publicação"),
                  sg.Text('Nº de resultados:'),
                  sg.Spin([i for i in range(1,10)],initial_value=3, key="num"),
                  sg.Button("Limpar")]
        linha3 = [sg.Output(size=(107, 25), key="output")]

        self.__container = [linha0, linha1, linha2, linha3]
        self.__window = sg.Window("Extrator CV Lattes",
                                  self.__container,
                                  font=("Helvetica", 14))

    def limpa_resultado(self):
        self.__window.FindElement("output").Update("")

    def le_eventos(self):
        return self.__window.read()

    def fim(self):
        self.__window.close()
