class Pessoa:
    def __init__(self, nome, idade):
        self.__nome = nome
        self.__idade = idade

    @property
    def nome(self):
        return self.__nome

    @property
    def idade(self):
        return self.__idade

    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome

    @idade.setter
    def idade(self, nova_idade):
        self.__idade = nova_idade