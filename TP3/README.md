 <div align="center">

# **TPC — Analisador Léxico**

## **Autor**

**Nome:** Luis Miguel Torres Martins

**ID:** A110241

**Foto:**

<img src="../img/me.jpeg" alt="Foto do autor" width="150"/>

</div>

## **Resumo**

Este trabalho consiste na construção de um **analisador léxico em Python** para uma linguagem de query utilizada para escrever consultas semelhantes às realizadas sobre a DBpedia.

O objetivo é desenvolver um programa capaz de percorrer uma query e identificar os diferentes elementos que a constituem, classificando-os em tokens.

O analisador reconhece os seguintes elementos:

- Comentários iniciados pelo caráter `#`;
- Variáveis iniciadas pelo caráter `?`;
- Identificadores de língua iniciados pelo caráter `@`;
- Valores do tipo string delimitados por aspas;
- Identificadores de conceitos;
- Delimitadores, nomeadamente `{`, `}` e `.`;
- O caráter `:` presente em identificadores como `dbo:MusicalArtist`;
- A palavra reservada `LIMIT`;
- Valores numéricos.

Os comentários e os espaços em branco são ignorados, uma vez que não produzem tokens.

## **Implementação em Python**

A implementação foi realizada em Python, utilizando operações sobre strings e métodos como `isalnum()`, `isalpha()` e `isdigit()` para reconhecer os diferentes tipos de tokens.

O ficheiro com a implementação encontra-se em:

**[`lexer.py`](./lexer.py)**

O programa está organizado numa função principal:

```python
def lexer(texto):
```

Esta função recebe uma string com a query completa, percorre o texto da esquerda para a direita e devolve uma lista de tokens.

Cada token é representado por um par constituído pelo tipo e pelo valor reconhecido.

Por exemplo:

```python
("VARIAVEL", "?nome")
("IDENTIFICADOR", "select")
("NUMERO", "1000")
```

---

## **Funcionamento do analisador**

O analisador utiliza um ciclo `while` para percorrer o texto, recorrendo a uma variável `i` que indica a posição atual.

```python
tokens = []
i = 0
```

A lista `tokens` armazena os elementos reconhecidos, enquanto `i` permite avançar pelo texto à medida que cada token é identificado.

Sempre que um token é reconhecido, o programa guarda o seu tipo e valor e continua a análise a partir da posição seguinte.

Esta abordagem permite analisar a query sem ser necessário dividi-la previamente em linhas ou palavras.

---

## **Tratamento de comentários**

O caráter `#` marca o início de um comentário que se prolonga até ao fim da linha.

Por exemplo:

```text
# DBPedia: obras de Chuck Berry
select ?nome
```

O comentário é ignorado, sendo apenas analisados os elementos da segunda linha.

O código utilizado é:

```python
if texto[i] == '#':
    while i < len(texto) and texto[i] != '\n':
        i += 1
    continue
```

O ciclo avança até encontrar uma mudança de linha ou até chegar ao fim do texto.

A instrução `continue` permite retomar a análise sem criar um token para o comentário.

---

## **Reconhecimento de variáveis**

As variáveis são identificadas pelo caráter `?`, seguido de uma sequência de caracteres alfanuméricos.

Por exemplo:

```text
?nome
?desc
?s
?w
```

Cada uma destas expressões é reconhecida como um único token do tipo `VARIAVEL`.

A implementação começa por guardar a posição inicial e avançar para o caráter seguinte ao ponto de interrogação.

```python
if texto[i] == '?':
    inicio = i
    i += 1

    while i < len(texto) and texto[i].isalnum():
        i += 1
```

O método `isalnum()` verifica se o caráter é uma letra ou um algarismo.

Depois de recolher a variável, o programa adiciona-a à lista de tokens.

Por exemplo:

```text
?nome
```

produz:

```text
VARIAVEL: ?nome
```

Se o caráter `?` não for seguido de nenhum caráter alfanumérico, é gerado um erro lexical.

---

## **Reconhecimento de identificadores de língua**

O caráter `@` inicia um identificador de língua constituído por dois caracteres alfabéticos.

Por exemplo:

```text
@en
```

é reconhecido como:

```text
LINGUA: @en
```

O programa verifica se existem dois caracteres disponíveis e se ambos são letras, utilizando o método `isalpha()`.

Estes identificadores aparecem associados a valores do tipo string, como no exemplo:

```text
"Chuck Berry"@en
```

Neste caso, são produzidos dois tokens:

```text
STRING: Chuck Berry
LINGUA: @en
```

O identificador de língua é tratado separadamente do valor da string.

---

## **Reconhecimento de strings**

Qualquer sequência entre aspas duplas é considerada um valor do tipo string.

Por exemplo:

```text
"Chuck Berry"
```

produz o token:

```text
STRING: Chuck Berry
```

Quando encontra uma aspa inicial, o analisador percorre o texto até encontrar a aspa de fecho.

O conteúdo existente entre as duas aspas é guardado como valor do token, sem incluir as próprias aspas.

Se não for encontrada uma aspa de fecho, o programa gera um erro através de `ValueError`.

Nesta implementação, as aspas escapadas dentro de strings não são tratadas como uma regra especial.

---

## **Reconhecimento de delimitadores**

Os caracteres `{`, `}` e `.` são delimitadores da linguagem.

Cada um é reconhecido individualmente e produz um token do tipo `DELIMITADOR`.

A implementação é:

```python
if texto[i] in '{}.':
    tokens.append(("DELIMITADOR", texto[i]))
    i += 1
    continue
```

Por exemplo, a expressão:

```text
{
    ?s dbo:MusicalArtist.
}
```

contém os delimitadores `{`, `.` e `}`.

Estes elementos ajudam a identificar a estrutura da query, mas o analisador léxico não verifica se as chavetas estão corretamente emparelhadas.

---

## **Reconhecimento do caráter `:`**

O caráter `:` aparece em identificadores de conceitos, como:

```text
dbo:MusicalArtist
foaf:name
dbo:artist
```

Como o enunciado não define explicitamente uma regra para este caráter, foi decidido reconhecê-lo como um token separado, do tipo `DOIS_PONTOS`.

Por exemplo:

```text
dbo:MusicalArtist
```

produz três tokens:

```text
IDENTIFICADOR: dbo
DOIS_PONTOS: :
IDENTIFICADOR: MusicalArtist
```

Desta forma, nenhuma parte da expressão é perdida durante a análise lexical.

---

## **Reconhecimento de identificadores, palavras reservadas e números**

As sequências alfanuméricas são analisadas depois de serem tratados os restantes elementos.

O programa recolhe todos os caracteres alfanuméricos consecutivos e classifica o resultado em três categorias.

### **Identificadores**

As sequências que não correspondem às restantes categorias são identificadores genéricos.

Por exemplo:

```text
select
where
dbo
MusicalArtist
```

produzem tokens do tipo `IDENTIFICADOR`.

### **Palavra reservada**

A palavra `LIMIT` é reconhecida como uma palavra reservada.

```text
LIMIT
```

produz:

```text
LIMIT: LIMIT
```

Esta verificação é realizada antes da classificação como identificador genérico.

### **Números**

As sequências constituídas exclusivamente por algarismos são classificadas como números.

Por exemplo:

```text
1000
```

produz:

```text
NUMERO: 1000
```

Para reconhecer estes valores, o programa utiliza o método `isdigit()`.

---

## **Tratamento de erros lexicais**

Quando o analisador encontra um caráter que não corresponde a nenhuma das regras definidas, gera um erro através de `ValueError`.

Por exemplo, um caráter não reconhecido pode originar uma mensagem semelhante a:

```text
Caráter inválido '$' na posição 10
```

Também são detetadas variáveis sem nome, identificadores de língua incompletos ou inválidos e strings sem aspa de fecho.

Este mecanismo permite identificar entradas que não respeitam as regras implementadas.

---

## **Função principal**

A função:

```python
def lexer(texto):
```

reúne todas as regras de análise lexical.

A sua execução segue, de forma geral, esta ordem:

1. Ignorar espaços em branco;
2. Ignorar comentários;
3. Reconhecer variáveis;
4. Reconhecer identificadores de língua;
5. Reconhecer strings;
6. Reconhecer delimitadores;
7. Reconhecer o caráter `:`;
8. Reconhecer sequências alfanuméricas;
9. Classificar as sequências como palavras reservadas, números ou identificadores;
10. Gerar um erro caso seja encontrado um caráter não reconhecido.

A ordem é importante porque alguns caracteres têm um significado específico e devem ser tratados antes das regras mais genéricas.

Por exemplo, `LIMIT` deve ser reconhecido como palavra reservada antes de ser classificado como identificador.

---

## **Testes**

Para testar o funcionamento do programa, foi utilizada a seguinte query:

```text
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
```

### **Teste de comentário**

Entrada:

```text
# Comentário de exemplo
select
```

Saída:

```text
IDENTIFICADOR: select
```

### **Teste de variável**

Entrada:

```text
?nome ?desc
```

Saída:

```text
VARIAVEL: ?nome
VARIAVEL: ?desc
```

### **Teste de string e língua**

Entrada:

```text
"Chuck Berry"@en
```

Saída:

```text
STRING: Chuck Berry
LINGUA: @en
```

### **Teste de delimitadores**

Entrada:

```text
{ ?s dbo:artist ?w. }
```

Saída:

```text
DELIMITADOR: {
VARIAVEL: ?s
IDENTIFICADOR: dbo
DOIS_PONTOS: :
IDENTIFICADOR: artist
VARIAVEL: ?w
DELIMITADOR: .
DELIMITADOR: }
```

### **Teste de palavra reservada e número**

Entrada:

```text
LIMIT 1000
```

Saída:

```text
LIMIT: LIMIT
NUMERO: 1000
```

---

## **Conclusão**

Este trabalho permitiu desenvolver um analisador léxico simples em Python para uma linguagem de query semelhante à utilizada pela DBpedia.

O programa reconhece diferentes tipos de tokens, incluindo variáveis, identificadores de língua, strings, identificadores genéricos, delimitadores, palavras reservadas e números.

A utilização de um ciclo `while` para percorrer o texto, juntamente com condições e métodos de manipulação de strings, permite implementar as regras de reconhecimento de forma organizada.

O trabalho também permitiu compreender a importância da ordem das regras de análise e do tratamento de erros lexicais.

Conclui-se que o analisador consegue decompor uma query nos seus elementos fundamentais, constituindo uma primeira etapa para o desenvolvimento de um analisador sintático ou de um interpretador de uma linguagem de query.
