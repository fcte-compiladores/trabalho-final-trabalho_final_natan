
"""
Interpretador para a linguagem Portugol.
"""

from typing import Any, Dict, Optional
from .ast import (
    Programa, Bloco, DeclaracaoVariavel, DeclaracaoFuncao,
    ComandoAtribuicao, ComandoSe, ComandoEnquanto, ComandoPara,
    ComandoEscreva, ComandoLeia, ComandoRetorne, ChamadaFuncao,
    ExpressaoLiteral, ExpressaoIdentificador, ExpressaoBinaria, ExpressaoUnaria
)


class ErroExecucao(Exception):
    pass


class RetornoFuncao(Exception):
    def __init__(self, valor: Any = None):
        self.valor = valor


class Ambiente:
    def __init__(self, pai: Optional["Ambiente"] = None):
        self.valores: Dict[str, Any] = {}
        self.pai = pai

    def definir(self, nome: str, valor: Any):
        self.valores[nome] = valor

    def obter(self, nome: str):
        if nome in self.valores:
            return self.valores[nome]
        if self.pai:
            return self.pai.obter(nome)
        raise ErroExecucao(f"Variável '{nome}' não definida.")

    def atribuir(self, nome: str, valor: Any):
        if nome in self.valores:
            self.valores[nome] = valor
            return
        if self.pai:
            self.pai.atribuir(nome, valor)
            return
        raise ErroExecucao(f"Variável '{nome}' não definida para atribuição.")

# Classe para representar uma função em tempo de execução (closure)
class Funcao:
    def __init__(self, declaracao: DeclaracaoFuncao, ambiente_definicao: Ambiente):
        self.declaracao = declaracao
        self.ambiente_definicao = ambiente_definicao


class Interpretador:
    def __init__(self):
        self.ambiente_global = Ambiente()
        self.ambiente_atual = self.ambiente_global

    def interpretar(self, programa: Programa):
        try:
            self.executar(programa)
        except ErroExecucao as e:
            print(f"Erro de execução: {e}")

    def executar(self, no):
        metodo_nome = 'visitar_' + type(no).__name__
        metodo = getattr(self, metodo_nome, self.visitar_no_desconhecido)
        return metodo(no)

    def visitar_no_desconhecido(self, no):
        raise ErroExecucao(f"Tipo de nó AST desconhecido: {type(no).__name__}")

    def visitar_Programa(self, programa: Programa):
        # O corpo do programa é um bloco, executamos ele
        self.executar(programa.declaracoes)

    def visitar_Bloco(self, bloco: Bloco):
        ambiente_anterior = self.ambiente_atual
        self.ambiente_atual = Ambiente(ambiente_anterior)
        try:
            for declaracao_ou_comando in bloco.declaracoes:
                self.executar(declaracao_ou_comando)
        finally:
            self.ambiente_atual = ambiente_anterior

    def visitar_DeclaracaoVariavel(self, declaracao: DeclaracaoVariavel):
        valor = None
        if declaracao.inicializador:
            valor = self.avaliar(declaracao.inicializador)
        self.ambiente_atual.definir(declaracao.identificador, valor)

    def visitar_DeclaracaoFuncao(self, declaracao: DeclaracaoFuncao):
        # Armazena a função junto com o ambiente onde ela foi definida
        funcao = Funcao(declaracao, self.ambiente_atual)
        self.ambiente_atual.definir(declaracao.nome, funcao)

    def visitar_ComandoAtribuicao(self, comando: ComandoAtribuicao):
        valor = self.avaliar(comando.expressao)
        self.ambiente_atual.atribuir(comando.identificador, valor)

    def visitar_ComandoSe(self, comando: ComandoSe):
        if self.avaliar(comando.condicao):
            self.executar(comando.comando_entao)
        elif comando.comando_senao:
            self.executar(comando.comando_senao)

    def visitar_ComandoEnquanto(self, comando: ComandoEnquanto):
        while self.avaliar(comando.condicao):
            self.executar(comando.comando)

    def visitar_ComandoPara(self, comando: ComandoPara):
        # O laço 'para' cria seu próprio escopo
        ambiente_anterior = self.ambiente_atual
        self.ambiente_atual = Ambiente(ambiente_anterior)
        try:
            self.executar(comando.inicializacao)
            while self.avaliar(comando.condicao):
                self.executar(comando.comando)
                self.executar(comando.incremento)
        finally:
            self.ambiente_atual = ambiente_anterior

    def visitar_ComandoEscreva(self, comando: ComandoEscreva):
        valores = [str(self.avaliar(expr)) for expr in comando.expressoes]
        print("".join(valores), end='\n')

    def visitar_ComandoLeia(self, comando: ComandoLeia):
        try:
            valor_lido = input()
            try:
                valor_lido = int(valor_lido)
            except ValueError:
                try:
                    valor_lido = float(valor_lido)
                except ValueError:
                    pass
            self.ambiente_atual.atribuir(comando.identificador, valor_lido)
        except EOFError:
            raise ErroExecucao("Erro de leitura: entrada inesperada.")

    def visitar_ComandoRetorne(self, comando: ComandoRetorne):
        valor = self.avaliar(comando.expressao) if comando.expressao else None
        raise RetornoFuncao(valor)

    def visitar_ChamadaFuncao(self, chamada: ChamadaFuncao):
        return self.avaliar_ChamadaFuncao(chamada)

    def avaliar(self, no):
        metodo_nome = 'avaliar_' + type(no).__name__
        metodo = getattr(self, metodo_nome, self.avaliar_no_desconhecido)
        return metodo(no)

    def avaliar_no_desconhecido(self, no):
        raise ErroExecucao(f"Tipo de nó de expressão desconhecido: {type(no).__name__}")

    def avaliar_ExpressaoLiteral(self, expressao: ExpressaoLiteral):
        return expressao.valor

    def avaliar_ExpressaoIdentificador(self, expressao: ExpressaoIdentificador):
        return self.ambiente_atual.obter(expressao.nome)

    def avaliar_ExpressaoUnaria(self, expressao: ExpressaoUnaria):
        valor = self.avaliar(expressao.expressao)
        if expressao.operador == "-": return -valor
        if expressao.operador == "+": return +valor
        if expressao.operador == "!": return not valor
        raise ErroExecucao(f"Operador unário desconhecido: {expressao.operador}")

    def avaliar_ExpressaoBinaria(self, expressao: ExpressaoBinaria):
        esquerda = self.avaliar(expressao.esquerda)
        direita = self.avaliar(expressao.direita)
        op = expressao.operador

        if op in ('+', '-', '*', '/', '%') and isinstance(esquerda, str) and isinstance(direita, (int, float)):
            direita = str(direita)
        
        if op == "+": return esquerda + direita
        if op == "-": return esquerda - direita
        if op == "*": return esquerda * direita
        if op == "/":
            if direita == 0: raise ErroExecucao("Divisão por zero.")
            return esquerda / direita
        if op == "%": 
            if direita == 0: raise ErroExecucao("Módulo por zero.")
            return esquerda % direita
        if op == "==": return esquerda == direita
        if op == "!=": return esquerda != direita
        if op == "<": return esquerda < direita
        if op == "<=": return esquerda <= direita
        if op == ">": return esquerda > direita
        if op == ">=": return esquerda >= direita
        if op == "e": return esquerda and direita
        if op == "ou": return esquerda or direita
        raise ErroExecucao(f"Operador binário desconhecido: {op}")

    def avaliar_ChamadaFuncao(self, chamada: ChamadaFuncao):
        funcao_obj = self.ambiente_atual.obter(chamada.nome)
        if not isinstance(funcao_obj, Funcao):
            raise ErroExecucao(f"'{chamada.nome}' não é uma função.")

        declaracao = funcao_obj.declaracao
        if len(chamada.argumentos) != len(declaracao.parametros):
            raise ErroExecucao(f"Número incorreto de argumentos para '{chamada.nome}'.")

        # O novo ambiente é filho do ambiente onde a função foi DEFINIDA
        ambiente_funcao = Ambiente(funcao_obj.ambiente_definicao)
        for param, arg in zip(declaracao.parametros, chamada.argumentos):
            ambiente_funcao.definir(param.identificador, self.avaliar(arg))

        ambiente_anterior = self.ambiente_atual
        self.ambiente_atual = ambiente_funcao
        try:
            self.executar(declaracao.corpo)
            return None
        except RetornoFuncao as r:
            return r.valor
        finally:
            self.ambiente_atual = ambiente_anterior
