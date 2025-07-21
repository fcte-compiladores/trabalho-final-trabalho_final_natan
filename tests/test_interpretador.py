import unittest
from unittest.mock import patch
import io
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lark import Lark
from portugol.transformer import PortugolTransformer
from portugol.interpretador import Interpretador

class TestInterpretador(unittest.TestCase):

    def setUp(self):
        """Configura o parser e o interpretador para cada teste."""
        with open("portugol/grammar.lark", "r", encoding="utf-8") as f:
            grammar = f.read()
        self.parser = Lark(grammar, start="programa", parser="lalr")
        self.transformer = PortugolTransformer()

    def _executar_codigo(self, codigo, entrada_mock=""):
        """Função auxiliar para executar um trecho de código e capturar a saída."""
        tree = self.parser.parse(codigo)
        ast = self.transformer.transform(tree)
        interpretador = Interpretador()

        stdout_capture = io.StringIO()
        with patch('sys.stdout', stdout_capture):
            with patch('builtins.input', side_effect=entrada_mock.splitlines()):
                interpretador.interpretar(ast)
        
        return stdout_capture.getvalue()

    def test_declaracao_e_atribuicao(self):
        codigo = """
        programa {
            inteiro a = 10;
            escreva(a);
            a = 25;
            escreva(a);
        }
        """
        saida = self._executar_codigo(codigo)
        self.assertEqual(saida, "10\n25\n")

    def test_expressoes_aritmeticas(self):
        codigo = """
        programa {
            escreva(10 + 5 * 2);
            escreva((10 + 5) * 2);
            escreva(10 - 2);
            escreva(10 / 2);
            escreva(10 % 3);
        }
        """
        saida = self._executar_codigo(codigo)
        self.assertEqual(saida, "20\n30\n8\n5.0\n1\n")

    def test_comando_se_senao(self):
        codigo_se = """
        programa {
            se (10 > 5) {
                escreva("maior");
            }
        }
        """
        saida_se = self._executar_codigo(codigo_se)
        self.assertEqual(saida_se, "maior\n")

        codigo_senao = """
        programa {
            se (2 > 5) {
                escreva("maior");
            } senao {
                escreva("menor");
            }
        }
        """
        saida_senao = self._executar_codigo(codigo_senao)
        self.assertEqual(saida_senao, "menor\n")

    def test_comando_enquanto(self):
        codigo = """
        programa {
            inteiro i = 0;
            enquanto (i < 3) {
                escreva(i);
                i = i + 1;
            }
        }
        """
        saida = self._executar_codigo(codigo)
        self.assertEqual(saida, "0\n1\n2\n")

    def test_comando_para(self):
        codigo = """
        programa {
            para (inteiro i = 0; i < 3; i = i + 1) {
                escreva(i);
            }
        }
        """
        saida = self._executar_codigo(codigo)
        self.assertEqual(saida, "0\n1\n2\n")

    def test_leia_e_escreva(self):
        codigo = """
        programa {
            inteiro x;
            leia(x);
            escreva("O valor lido foi: ", x);
        }
        """
        saida = self._executar_codigo(codigo, entrada_mock="42")
        self.assertEqual(saida, "O valor lido foi: 42\n")

    def test_funcao_simples(self):
        codigo = """
        programa {
            funcao inteiro soma(inteiro a, inteiro b) {
                retorne a + b;
            }
            escreva(soma(10, 5));
        }
        """
        saida = self._executar_codigo(codigo)
        self.assertEqual(saida, "15\n")

    def test_funcao_recursiva_fatorial(self):
        codigo = """
        programa {
            funcao inteiro fatorial(inteiro n) {
                se (n == 0) {
                    retorne 1;
                } senao {
                    retorne n * fatorial(n - 1);
                }
            }
            escreva(fatorial(5));
        }
        """
        saida = self._executar_codigo(codigo)
        self.assertEqual(saida, "120\n")

if __name__ == '__main__':
    unittest.main()