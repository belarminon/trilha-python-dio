from abc import ABC, abstractmethod
from datetime import date, datetime

from narwhals import List


class Transacao(ABC):
    """Interface que define a estrutura de uma transação bancária."""
    
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @abstractmethod
    def registrar(self, conta: 'Conta') -> None:
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta') -> None:
        # Executa o depósito na conta e registra no histórico
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta') -> None:
        # Executa o saque na conta e registra no histórico
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


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


class Historico:
    def __init__(self):
        self._transacoes: List[Transacao] = []

    @property
    def transacoes(self) -> List[Transacao]:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append({
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
       

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


class ContaCorrente(Conta):
    def __init__(self, numero: int, agencia: str, cliente: 'Cliente', limite: float, limite_saques: int):
        super().__init__(numero, agency=agencia, cliente=cliente)
        self._limite: float = limite
        self._limite_saques: int = limite_saques

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    # Sobrecarga do método sacar para considerar o limite de crédito
    def sacar(self, valor: float) -> bool:
        # Exemplo simples considerando saldo + limite
        if valor > 0 and (self._saldo + self._limite) >= valor:
            self._saldo -= valor
            return True
        return False


class ContaPoupanca(Conta):
    def __init__(self, numero: int, agencia: str, cliente: 'Cliente', rendimento: float):
        super().__init__(numero, agency=agencia, cliente=cliente)
        self._rendimento: float = rendimento

    @property
    def rendimento(self) -> float:
        return self._rendimento