# trilha-python-dio
Repo da trilha de aprendizado da linguagem python administrado da DIO

# Desafio Sistema Banário O.O. (v1)
<img width="886" height="529" alt="image" src="https://github.com/user-attachments/assets/824b2756-7e1c-4fb7-bbfb-516bd4692fb8" />

Descrição da Entrega: Sistema Bancário O.O. (v1)
Esta entrega consiste na transição de um sistema bancário anteriormente estruturado em funções/procedimentos para uma arquitetura totalmente orientada a objetos, mapeando os requisitos de negócio em classes bem definidas de acordo com o modelo conceitual UML.

Principais componentes entregues:

Abstração e Modelagem de Entidades:

Cliente e PessoaFisica: Implementação do conceito de herança, onde PessoaFisica herda os dados base do cliente (como endereço) e adiciona atributos específicos como CPF e nome.

Conta e ContaCorrente: Estruturação da conta bancária padrão contendo atributos de saldo, número e agência, especializada através de herança na classe ContaCorrente para suportar regras de limite de crédito e teto de saques diários.

Registro e Rastreabilidade de Operações:

Historico e Transacao: Implementação do padrão onde as operações não apenas alteram o saldo, mas geram objetos do tipo Deposito ou Saque (que assinam uma interface comum) e são encapsulados cronologicamente dentro do histórico de cada conta.

Fluxo de Negócio:

O código entrega os métodos operacionais capazes de validar as regras de negócio tradicionais (como impedir saques se não houver saldo/limite disponível, validar valores negativos e limitar a quantidade de saques por dia) utilizando a interação direta entre esses objetos.

Em suma, o que está sendo entregue é uma fundação sólida de código Python estruturado, que aplica conceitos essenciais de POO (herança, encapsulamento, polimorfismo e classes abstratas) para resolver o problema clássico de gerenciamento de contas e transações bancárias.

