from lark import Transformer, Token
from .ast import (
    Programa, Tipo, ExpressaoLiteral, ExpressaoIdentificador,
    ExpressaoBinaria, ExpressaoUnaria, ChamadaFuncao,
    ComandoAtribuicao, ComandoSe, ComandoEnquanto, ComandoPara,
    ComandoEscreva, ComandoLeia, ComandoRetorne, Bloco,
    DeclaracaoVariavel, Parametro, DeclaracaoFuncao
)


class PortugolTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def programa(self, args): return Programa(args[0])
    def bloco(self, args): return Bloco(args)

    # Declarações
    def declaracao(self, args): return args[0]

    def declaracao_variavel(self, args): return args[0]
    def declaracao_variavel_base(self, args):
        tipo, identificador, *expressao = args
        inicializador = expressao[0] if expressao else None
        return DeclaracaoVariavel(tipo, str(identificador), inicializador)

    def declaracao_funcao(self, args):
        tipo, nome, *resto = args
        parametros = resto.pop(0) if isinstance(resto[0], list) else []
        corpo = resto[0]
        return DeclaracaoFuncao(tipo, str(nome), parametros, corpo)

    def parametros(self, args): return args
    def parametro(self, args): return Parametro(args[0], str(args[1]))

    # Comandos
    def comando(self, args): return args[0]

    def comando_atribuicao(self, args): return args[0] # Passa o resultado da regra base
    def atribuicao_base(self, args):
        identificador, expressao = args
        return ComandoAtribuicao(str(identificador), expressao)

    def comando_se(self, args):
        condicao, comando_entao, *comando_senao = args
        return ComandoSe(condicao, comando_entao, comando_senao[0] if comando_senao else None)

    def comando_enquanto(self, args): return ComandoEnquanto(args[0], args[1])

    def comando_para(self, args):
        inicializacao, condicao, incremento, comando = args
        return ComandoPara(inicializacao, condicao, incremento, comando)

    def comando_escreva(self, args): return ComandoEscreva(args[0] if args else [])
    def comando_leia(self, args): return ComandoLeia(str(args[0]))
    def comando_retorne(self, args): return ComandoRetorne(args[0] if args else None)

    # Expressões
    def lista_expressoes(self, args): return args

    def _criar_expressao_binaria(self, args):
        expr = args[0]
        for i in range(1, len(args), 2):
            op = str(args[i])
            direita = args[i+1]
            expr = ExpressaoBinaria(expr, op, direita)
        return expr

    def expressao_logica(self, args): return self._criar_expressao_binaria(args)
    def expressao_relacional(self, args): return self._criar_expressao_binaria(args)
    def expressao_aditiva(self, args): return self._criar_expressao_binaria(args)
    def expressao_multiplicativa(self, args): return self._criar_expressao_binaria(args)

    def expressao_unaria(self, args):
        if len(args) == 1:
            return args[0]
        return ExpressaoUnaria(str(args[0]), args[1])

    def expressao_primaria(self, args): return args[0]
    def expressao(self, args): return args[0]

    def identificador_expr(self, args): return ExpressaoIdentificador(str(args[0]))

    def chamada_funcao(self, args):
        nome, *argumentos = args
        return ChamadaFuncao(str(nome), argumentos[0] if argumentos else [])

    # Tipos e Tokens
    def tipo(self, args): return Tipo(str(args[0]))

    def T_INTEIRO(self, token): return token.value
    def T_REAL(self, token): return token.value
    def T_CARACTERE(self, token): return token.value
    def T_LOGICO(self, token): return token.value
    def T_CADEIA(self, token): return token.value

    def NUMERO(self, token): return ExpressaoLiteral(int(token.value))
    def NUMERO_REAL(self, token): return ExpressaoLiteral(float(token.value))
    def STRING(self, token): return ExpressaoLiteral(str(token.value[1:-1]))
    def CARACTERE(self, token): return ExpressaoLiteral(str(token.value[1:-1]))
    def BOOLEANO(self, token): return ExpressaoLiteral(token.value == 'verdadeiro')
    def IDENTIFICADOR(self, token): return token.value
