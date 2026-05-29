from abc import ABC, abstractmethod
from datetime import date

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: date, endereco: str):
        super().__init__(endereco=endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero: int, agencia: str, cliente: 'Cliente'):
        self._saldo: float = 0.0
        self._numero: int = numero
        self._agencia: str = agencia
        self._cliente: 'Cliente' = cliente
        self._historico: Historico = Historico()

    # Getters usando property
    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> 'Cliente':
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    # Métodos de negócio
    def saldo_atual(self) -> float:
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int, agencia: str = "0001") -> 'Conta':
        return cls(numero, agencia, cliente)

    def sacar(self, valor: float) -> bool:
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        return False

