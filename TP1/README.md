<div align="center">

# **TP 1 — Expressão Regular**

## **Autor**

**Nome:** Luis Miguel Torres Martins

**ID:** A110241

**Foto:**

<img src="../img/me.jpeg" alt="me" width="150"/>

</div>

## **Resumo**

Este trabalho consiste na construção de uma **expressão regular** capaz de reconhecer strings binárias que **não contenham a substring `011`**.

O objetivo é aplicar os conceitos de **linguagens regulares** e **expressões regulares**, construindo uma expressão que aceite apenas cadeias constituídas pelos símbolos `0` e `1` e que não possuam `011` como substring.

A expressão regular encontrada para resolver o problema é:

```regex
^(?!(0*1*)+011)(0*1*)+
```

### **Descrição da expressão**

A expressão utiliza diferentes componentes para garantir as condições pretendidas:

* `^` — indica o início da string.

* `(0*1*)+` — permite reconhecer strings constituídas por zeros e uns.

* `(?!(0*1*)+011)` — utiliza um *negative lookahead* para impedir que a string contenha a substring `011`.

* `(0*1*)+` — permite reconhecer strings constituídas por zeros e uns, garantindo que a expressão continue a analisar toda a cadeia.

* `$` — pode ser utilizado para indicar o fim da string, garantindo que toda a cadeia seja analisada.

Assim, a expressão regular procura reconhecer apenas strings binárias que não contenham a sequência `011`.

## **Implementação em Python**

Para testar a expressão regular e verificar automaticamente quais as strings aceites ou rejeitadas, foi criada uma implementação em Python.

O ficheiro com a implementação encontra-se em:

**[`regex_tp1.py`](./regex_tp1.py)**

O programa utiliza o módulo `re` do Python para aplicar a expressão regular a uma lista de strings de teste.

O programa apresenta no terminal se cada string é **Accepted** ou **Rejected**.

## **Lista de resultados**

### Strings aceites

```text
ε
0
1
00
01
10
11
000
101
111
1001
```

### Strings rejeitadas

```text
011
0011
0110
1011
00110
01101
```

Os resultados apresentados acima correspondem aos testes realizados através da implementação em Python.

---

## **Conclusão**

A expressão regular apresentada permite identificar strings binárias que não contêm a substring `011`, recorrendo a uma combinação de uma expressão para strings binárias e de um *negative lookahead* para excluir as cadeias que apresentam a sequência proibida.

A implementação em Python permite ainda testar automaticamente diferentes strings e verificar o comportamento da expressão regular.
