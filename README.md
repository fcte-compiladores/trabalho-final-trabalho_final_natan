# Interpretador Portugol

## Integrantes

- **Nome:** Natan da Cruz Almeida
- **Matrícula:** 222006169
- **Turma:** 18hrs

## Introdução

Este projeto implementa um interpretador para uma versão simplificada da linguagem Portugol. O objetivo foi criar uma ferramenta capaz de analisar e executar códigos escritos em Portugol, cobrindo as etapas fundamentais do processo de interpretação: análise léxica, análise sintática e avaliação da árvore de sintaxe abstrata (AST).

A principal estratégia utilizada foi a biblioteca `lark` para a análise léxica e sintática. A gramática da linguagem foi definida em um arquivo `.lark`, que descreve os tokens e as regras de produção da linguagem. A partir da gramática, o `lark` gera uma árvore de análise (Parse Tree), que é então transformada em uma Árvore de Sintaxe Abstrata (AST) customizada. A AST é uma representação mais limpa e estruturada do código, facilitando a interpretação.

O interpretador percorre a AST (usando o padrão de projeto Visitor) e executa os comandos e expressões, gerenciando escopos de variáveis e o fluxo de controle do programa.

### Exemplo de Sintaxe e Semântica

A linguagem suporta variáveis, condicionais, laços, funções e operações básicas.

```portugol
programa 
{
    inteiro contador = 10;
    
    enquanto (contador > 0)
    {
        escreva ("Detonação em: ", contador);
        
        contador = contador - 1;
    }

    escreva ("Booom!");
}
```

## Instalação

Para instalar as dependências e executar o interpretador, siga os passos abaixo.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/fcte-compiladores/trabalho-final-trabalho_final_natan.git interpretador-portugol
    cd interpretador-portugol
    ```

2.  **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Execute o interpretador:**

    Para executar um arquivo de exemplo, use o seguinte comando:
    ```bash
    python3 main.py exemplos/nome_do_arquivo.ptg
    ```

## Testes

O projeto utiliza `pytest` para a automação dos testes, garantindo o funcionamento correto dos principais componentes do interpretador.

Para executar os testes, certifique-se de que as dependências de desenvolvimento estão instaladas e execute o seguinte comando na raiz do projeto:

```bash
pytest
```

Os testes cobrem as funcionalidades de:

-   Declaração e atribuição de variáveis.
-   Avaliação de expressões aritméticas.
-   Execução de estruturas de controle (`se`, `senao`, `enquanto`, `para`).
-   Operações de entrada e saída (`leia`, `escreva`).
-   Chamada de funções, incluindo funções recursivas.

## Exemplos

A pasta `exemplos/` contém arquivos de código na linguagem Portugol com complexidade variada.

## Referências

-   **Documentação da Linguagem Portugol:** O [portugol.dev](https://portugol.dev/) foi utilizada como referência para a sintaxe e semântica da linguagem.
-   **Repositório da Disciplina:** O [repositório da disciplina](https://github.com/fcte-compiladores/2025-1) foi utilizado para consulta de materiais e exemplos.

## Estrutura do Código

O código do projeto está organizado nos seguintes módulos principais:

-   `main.py`: Ponto de entrada do programa. É responsável por ler o arquivo de código fonte, invocar o parser do Lark e iniciar o processo de interpretação.

-   `portugol/grammar.lark`: Contém a definição formal da gramática da linguagem Portugol. A **análise léxica** (definição de tokens como `IDENTIFICADOR`, `NUMERO`, etc.) e a **análise sintática** (regras de produção como `comando_se`, `expressao`, etc.) são inteiramente realizadas pelo Lark com base neste arquivo.

-   `portugol/ast.py`: Define as classes que representam os nós da Árvore de Sintaxe Abstrata (AST). Cada classe (ex: `ComandoSe`, `ExpressaoBinaria`) corresponde a uma construção da linguagem.

-   `portugol/transformer.py`: Contém a classe `PortugolTransformer`, que herda de `lark.Transformer`. Sua função é transformar a Parse Tree gerada pelo Lark em nossa AST customizada, definida em `ast.py`. Esta etapa é crucial para criar uma estrutura de dados mais limpa e fácil de ser processada.

-   `portugol/interpretador.py`: O coração do projeto. A classe `Interpretador` realiza a **análise semântica** e a execução do código. Ela percorre a AST (usando o padrão Visitor) e executa as ações correspondentes a cada nó. A classe `Ambiente` é usada dentro do interpretador para gerenciar os escopos de variáveis e funções.

## Bugs/Limitações/Problemas Conhecidos

-   **Tratamento de Tipos:** O sistema de tipos é muito primitivo. Não há verificação estática de tipos, e a coerção de tipos em tempo de execução é limitada (ex: `escreva` converte tudo para string). Operações entre tipos incompatíveis (ex: `10 + "texto"`) podem causar um crash no interpretador.
-   **Tratamento de Erros:** As mensagens de erro são genéricas. Seria ideal melhorá-las para incluir o número da linha e da coluna onde o erro ocorreu, facilitando a depuração.
-   **Funções:** Não há suporte para funções aninhadas ou closures. Todas as funções são definidas no escopo global.
-   **Tipos de Dados:** A linguagem suporta apenas tipos primitivos. Não há suporte para estruturas de dados complexas como listas ou registros/structs.
-   **Escopo:** O gerenciamento de escopo é simples. Existe um escopo global e escopos locais para blocos e funções, mas não há um tratamento mais sofisticado.
