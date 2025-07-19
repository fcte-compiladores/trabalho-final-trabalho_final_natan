import sys
from lark import Lark
from portugol.transformer import PortugolTransformer
from portugol.interpretador import Interpretador, ErroExecucao

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <arquivo_portugol>")
        sys.exit(1)

    arquivo_portugol = sys.argv[1]

    try:
        with open("portugol/grammar.lark", "r", encoding="utf-8") as f:
            grammar = f.read()
        
        parser = Lark(grammar, start="programa", parser="lalr")

        with open(arquivo_portugol, "r", encoding="utf-8") as f:
            codigo = f.read()

        tree = parser.parse(codigo)
        # print("Parse Tree:\n", tree.pretty())

        # Aplicar o transformer para converter a parse tree em AST
        ast = PortugolTransformer().transform(tree)

        interpretador = Interpretador()
        interpretador.interpretar(ast)

    except FileNotFoundError:
        print(f"Erro: Arquivo \'{arquivo_portugol}\' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


