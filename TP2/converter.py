import re


def converter_cabecalhos(texto):
    padroes = [
        (r'^### (.*)$', r'<h3>\1</h3>'),
        (r'^## (.*)$', r'<h2>\1</h2>'),
        (r'^# (.*)$', r'<h1>\1</h1>')
    ]

    for padrao, substituicao in padroes:
        texto = re.sub(padrao, substituicao, texto, flags=re.MULTILINE)

    return texto


def converter_negrito(texto):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', texto)


def converter_italico(texto):
    return re.sub(r'\*(.+?)\*', r'<i>\1</i>', texto)


def converter_lista_numerada(texto):
    padrao_item = r'^\d+\.\s+(.*)$'

    itens = re.findall(padrao_item, texto, flags=re.MULTILINE)

    if not itens:
        return texto

    lista = '<ol>\n'

    for item in itens:
        lista += f'<li>{item}</li>\n'

    lista += '</ol>'

    return lista


def converter_links(texto):
    padrao = r'\[(.*?)\]\((.*?)\)'

    return re.sub(
        padrao,
        r'<a href="\2">\1</a>',
        texto
    )


def converter_imagens(texto):
    padrao = r'!\[(.*?)\]\((.*?)\)'

    return re.sub(
        padrao,
        r'<img src="\2" alt="\1"/>',
        texto
    )


def converter(texto):
    texto = converter_cabecalhos(texto)

    texto = converter_negrito(texto)

    texto = converter_italico(texto)

    texto = converter_lista_numerada(texto)

    texto = converter_imagens(texto)

    texto = converter_links(texto)

    return texto


# Testes

print(converter_cabecalhos("# Exemplo"))

print(converter_negrito("Este é um **exemplo** ..."))

print(converter_italico("Este é um *exemplo* ..."))

print(converter_lista_numerada(
    "1. Primeiro item\n"
    "2. Segundo item\n"
    "3. Terceiro item"
))

print(converter_links(
    "Como pode ser consultado em [página da UC](http://www.uc.pt)"
))

print(converter_imagens(
    "Como se vê na imagem seguinte: "
    "![imagem dum coelho](http://www.coelho.com) ..."
))
