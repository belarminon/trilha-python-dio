class Foo:
    def __init__(self, valor=None):
        self._valor = valor

    @property
    def valor(self):
        return self._valor or 0

    @valor.setter
    def valor(self, novo_valor):
        if isinstance(novo_valor, int) and novo_valor >= 0:
            self._valor = novo_valor
        else:
            raise ValueError("O valor deve ser um inteiro não negativo.")
        
    @valor.deleter
    def valor(self):
        self._valor = None
        
foo = Foo()
print(foo.valor)  # Saída: 0
foo.valor = 20
print(foo.valor)  # Saída: 10
del foo.valor
print(foo.valor)  # Saída: 0