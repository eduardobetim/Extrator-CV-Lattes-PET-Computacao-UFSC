class Aparicao:
    def __init__(self, docId, frequencia, frequencia_geral):
        self.docId = docId
        self.frequencia = frequencia
        self.frequencia_geral = frequencia_geral

    def __repr__(self):
        return str(self.__dict__)
