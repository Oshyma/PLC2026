<div align="center">

# **TPC — Conversão de Markdown para HTML**

## **Autor**

**Nome:** Luis Miguel Torres Martins

**ID:** A110241

**Foto:**

<img src="../img/me.jpeg" alt="Foto do autor" width="150"/>

</div>

## **Resumo**

Este trabalho consiste na construção de um programa em **Python** capaz de converter determinados elementos de **Markdown** para **HTML**, recorrendo ao módulo `re` e a **expressões regulares**.

O objetivo é reconhecer diferentes estruturas presentes num texto em Markdown, como:

* Cabeçalhos;
* Texto a **negrito**;
* Texto em *itálico*;
* Listas numeradas;
* Links;
* Imagens.

Depois de reconhecer cada elemento, o programa substitui a sintaxe Markdown correspondente pela respetiva marcação HTML.

Por exemplo:

```text
# Exemplo
```

é convertido para:

```html
<h1>Exemplo</h1>
```

## **Implementação em Python**

A implementação foi realizada em Python e utiliza o módulo `re`, que permite trabalhar com **expressões regulares** para procurar e substituir padrões dentro de strings.

O ficheiro com a implementação encontra-se em:

**[`converter.py`](./converter.py)**

O programa está dividido em várias funções, sendo que cada uma é responsável por converter um determinado elemento de Markdown.

---

## **Conversão de cabeçalhos**

A função:

```python
def converter_cabecalhos(texto):
```

é responsável por converter cabeçalhos Markdown para cabeçalhos HTML.

São reconhecidos três níveis:

```text
# Título
## Subtítulo
### Subsubtítulo
```

que são convertidos, respetivamente, para:

```html
<h1>Título</h1>
<h2>Subtítulo</h2>
<h3>Subsubtítulo</h3>
```

São utilizadas as seguintes expressões regulares:

```python
r'^### (.*)$'
r'^## (.*)$'
r'^# (.*)$'
```

Os símbolos utilizados têm o seguinte significado:

* `^` — indica o início da linha;
* `###`, `##`, `#` — identificam o nível do cabeçalho;
* `(.*)` — captura o conteúdo do cabeçalho;
* `$` — indica o fim da linha.

Os cabeçalhos são processados do maior para o menor nível, evitando que um cabeçalho `###` seja interpretado primeiro como um cabeçalho `#`.

---

## **Conversão de negrito**

A função:

```python
def converter_negrito(texto):
```

procura texto delimitado por dois asteriscos:

```text
**exemplo**
```

e converte-o para:

```html
<b>exemplo</b>
```

A expressão regular utilizada é:

```python
r'\*\*(.+?)\*\*'
```

Nesta expressão:

* `\*\*` — identifica os dois asteriscos iniciais;
* `(.+?)` — captura o texto que está entre os asteriscos;
* `\*\*` — identifica os dois asteriscos finais.

Esta conversão é realizada antes da conversão do itálico.

---

## **Conversão de itálico**

A função:

```python
def converter_italico(texto):
```

procura texto delimitado por um único asterisco:

```text
*exemplo*
```

e transforma-o em:

```html
<i>exemplo</i>
```

A expressão regular utilizada é:

```python
r'\*(.+?)\*'
```

O texto entre os dois asteriscos é capturado e colocado dentro da tag HTML `<i>`.

O itálico é processado depois do negrito para evitar que os asteriscos utilizados no negrito sejam interpretados incorretamente como itálico.

---

## **Conversão de listas numeradas**

A função:

```python
def converter_lista_numerada(texto):
```

permite reconhecer listas numeradas em Markdown.

Por exemplo:

```text
1. Primeiro item
2. Segundo item
3. Terceiro item
```

é convertido para:

```html
<ol>
<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>
</ol>
```

Para identificar cada item da lista é utilizada a expressão regular:

```python
r'^\d+\.\s+(.*)$'
```

Nesta expressão:

* `^` — início da linha;
* `\d+` — um ou mais algarismos;
* `\.` — representa o ponto depois do número;
* `\s+` — representa um ou mais espaços;
* `(.*)` — captura o conteúdo do item;
* `$` — fim da linha.

Depois de identificar os itens, o programa utiliza um ciclo `for` para construir a lista HTML.

---

## **Conversão de links**

A função:

```python
def converter_links(texto):
```

converte links escritos em Markdown.

Por exemplo:

```text
[página da UC](http://www.uc.pt)
```

é convertido para:

```html
<a href="http://www.uc.pt">página da UC</a>
```

A expressão regular utilizada é:

```python
r'\[(.*?)\]\((.*?)\)'
```

Os grupos capturados correspondem a:

* Primeiro grupo — texto apresentado no link;
* Segundo grupo — endereço do link.

Na substituição:

```python
r'<a href="\2">\1</a>'
```

o `\1` representa o texto do link e o `\2` representa o endereço.

---

## **Conversão de imagens**

A função:

```python
def converter_imagens(texto):
```

é semelhante à conversão de links, mas permite reconhecer imagens Markdown.

Por exemplo:

```text
![imagem dum coelho](http://www.coelho.com)
```

é convertido para:

```html
<img src="http://www.coelho.com" alt="imagem dum coelho"/>
```

A expressão regular utilizada é:

```python
r'!\[(.*?)\]\((.*?)\)'
```

O primeiro grupo corresponde ao texto alternativo da imagem e o segundo corresponde ao endereço da imagem.

A substituição utilizada é:

```python
r'<img src="\2" alt="\1"/>'
```

---

## **Função principal**

A função:

```python
def converter(texto):
```

é responsável por aplicar todas as conversões ao texto.

As transformações são realizadas pela seguinte ordem:

```python
texto = converter_cabecalhos(texto)
texto = converter_negrito(texto)
texto = converter_italico(texto)
texto = converter_lista_numerada(texto)
texto = converter_imagens(texto)
texto = converter_links(texto)
```

A ordem das operações é importante.

O **negrito é processado antes do itálico**, porque ambos utilizam o símbolo `*`.

As **imagens são processadas antes dos links**, porque a sintaxe de uma imagem contém também a estrutura utilizada num link:

```text
![texto](endereco)
```

enquanto um link utiliza:

```text
[texto](endereco)
```

Desta forma, a imagem é reconhecida primeiro e convertida corretamente.

---

## **Testes**

Foram realizados vários testes para verificar o funcionamento de cada função.

### **Cabeçalho**

Entrada:

```text
# Exemplo
```

Saída:

```html
<h1>Exemplo</h1>
```

### **Negrito**

Entrada:

```text
Este é um **exemplo** ...
```

Saída:

```html
Este é um <b>exemplo</b> ...
```

### **Itálico**

Entrada:

```text
Este é um *exemplo* ...
```

Saída:

```html
Este é um <i>exemplo</i> ...
```

### **Lista numerada**

Entrada:

```text
1. Primeiro item
2. Segundo item
3. Terceiro item
```

Saída:

```html
<ol>
<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>
</ol>
```

### **Link**

Entrada:

```text
[página da UC](http://www.uc.pt)
```

Saída:

```html
<a href="http://www.uc.pt">página da UC</a>
```

### **Imagem**

Entrada:

```text
![imagem dum coelho](http://www.coelho.com)
```

Saída:

```html
<img src="http://www.coelho.com" alt="imagem dum coelho"/>
```

---

## **Conclusão**

Este trabalho permitiu desenvolver um conversor simples de **Markdown para HTML**, utilizando **Python** e **expressões regulares**.

O programa consegue reconhecer e converter diferentes elementos de Markdown, nomeadamente **cabeçalhos, negrito, itálico, listas numeradas, links e imagens**.

A utilização de funções separadas para cada tipo de elemento torna o código mais organizado e facilita a compreensão e manutenção do programa.

A função `converter()` reúne todas as transformações, aplicando-as pela ordem adequada para garantir que elementos com sintaxes semelhantes, como **negrito/itálico** e **imagens/links**, sejam processados corretamente.
