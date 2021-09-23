class Registro:
    def __init__(self):
        self.reg = dict()

    def __repr__(self):
        return str(self.__dict__)

    def get(self, id):
        return self.reg.get(id, None)

    def add(self, document):
        return self.reg.update({document['id']: document})

    def remove(self, document):
        return self.reg.pop(document['id'], None)
