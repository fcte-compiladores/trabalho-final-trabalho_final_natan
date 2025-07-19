from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union


class ASTNode(ABC):
    pass


class Expressao(ASTNode):
    pass


class Comando(ASTNode):
    pass


class Declaracao(ASTNode):
    pass


class Programa(ASTNode):
    def __init__(self, declaracoes: List[Declaracao]):
        self.declaracoes = declaracoes

class Tipo:
    def __init__(self, nome: str):
        self.nome = nome
    
    def __str__(self):
        return self.nome

class ExpressaoLiteral(Expressao):
    def __init__(self, valor: Any):
        self.valor = valor


class ExpressaoIdentificador(Expressao):
    def __init__(self, nome: str):
        self.nome = nome


class ExpressaoBinaria(Expressao):
    def __init__(self, esquerda: Expressao, operador: str, direita: Expressao):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita


class ExpressaoUnaria(Expressao):
    def __init__(self, operador: str, expressao: Expressao):
        self.operador = operador
        self.expressao = expressao


class ChamadaFuncao(Expressao):
    def __init__(self, nome: str, argumentos: List[Expressao]):
        self.nome = nome
        self.argumentos = argumentos


class ComandoAtribuicao(Comando):
    def __init__(self, identificador: str, expressao: Expressao):
        self.identificador = identificador
        self.expressao = expressao


class ComandoSe(Comando):
    def __init__(self, condicao: Expressao, comando_entao: Comando, comando_senao: Optional[Comando] = None):
        self.condicao = condicao
        self.comando_entao = comando_entao
        self.comando_senao = comando_senao


class ComandoEnquanto(Comando):
    def __init__(self, condicao: Expressao, comando: Comando):
        self.condicao = condicao
        self.comando = comando


class ComandoPara(Comando):
    def __init__(self, inicializacao: ComandoAtribuicao, condicao: Expressao, incremento: str, comando: Comando):
        self.inicializacao = inicializacao
        self.condicao = condicao
        self.incremento = incremento
        self.comando = comando


class ComandoEscreva(Comando):
    def __init__(self, expressoes: List[Expressao]):
        self.expressoes = expressoes


class ComandoLeia(Comando):
    def __init__(self, identificador: str):
        self.identificador = identificador


class ComandoRetorne(Comando):
    def __init__(self, expressao: Optional[Expressao] = None):
        self.expressao = expressao


class Bloco(Comando):
    def __init__(self, declaracoes: List[Union[Declaracao, Comando]]):
        self.declaracoes = declaracoes


class DeclaracaoVariavel(Declaracao):
    def __init__(self, tipo: Tipo, identificador: str, inicializador: Optional[Expressao] = None):
        self.tipo = tipo
        self.identificador = identificador
        self.inicializador = inicializador


class Parametro:
    def __init__(self, tipo: Tipo, identificador: str):
        self.tipo = tipo
        self.identificador = identificador


class DeclaracaoFuncao(Declaracao):
    def __init__(self, tipo: Tipo, nome: str, parametros: List[Parametro], corpo: Bloco):
        self.tipo = tipo
        self.nome = nome
        self.parametros = parametros
        self.corpo = corpo

