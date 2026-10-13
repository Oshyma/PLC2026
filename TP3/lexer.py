def lexer(texto):
    """
    Analisa lexicalmente uma query e devolve uma lista de tokens.

    Cada token é representado por um par:
    (tipo, valor)
    """

    tokens = []
    i = 0

    while i < len(texto):

        # Ignora espaços em branco e mudanças de linha
        if texto[i].isspace():
            i += 1
            continue

        # Comentários
        if texto[i] == '#':
            while i < len(texto) and texto[i] != '\n':
                i += 1
            continue

        # Variáveis: ? 
        if texto[i] == '?':
            inicio = i
            i += 1

            while i < len(texto) and texto[i].isalnum():
                i += 1

            if i == inicio + 1:
                raise ValueError(
                    f"Variável sem nome na posição {inicio}"
                )

            tokens.append(("VARIAVEL", texto[inicio:i]))
            continue

        # Identificadores de língua: @ 
        if texto[i] == '@':
            inicio = i
            i += 1

            if i + 2 > len(texto):
                raise ValueError(
                    f"Identificador de língua incompleto "
                    f"na posição {inicio}"
                )

            lingua = texto[i:i + 2]

            if not lingua.isalpha():
                raise ValueError(
                    f"Identificador de língua inválido "
                    f"na posição {inicio}"
                )

            tokens.append(("LINGUA", '@' + lingua))
            i += 2
            continue

        # Strings: entre aspas
        if texto[i] == '"':
            inicio = i
            i += 1

            while i < len(texto) and texto[i] != '"':
                i += 1

            if i == len(texto):
                raise ValueError(
                    f"String sem aspas de fecho na posição {inicio}"
                )

            valor = texto[inicio + 1:i]
            tokens.append(("STRING", valor))
            i += 1
            continue

        # Delimitadores
        if texto[i] in '{}.':
            tokens.append(("DELIMITADOR", texto[i]))
            i += 1
            continue

        # Separador 
        if texto[i] == ':':
            tokens.append(("DOIS_PONTOS", ':'))
            i += 1
            continue

        # Sequências alfanuméricas
        if texto[i].isalnum():
            inicio = i

            while i < len(texto) and texto[i].isalnum():
                i += 1

            valor = texto[inicio:i]

            # Palavra reservada
            if valor == "LIMIT":
                tokens.append(("LIMIT", valor))

            # Números
            elif valor.isdigit():
                tokens.append(("NUMERO", valor))

            # Identificadores genéricos
            else:
                tokens.append(("IDENTIFICADOR", valor))

            continue

        # Caráter inválido
        raise ValueError(
            f"Caráter inválido {texto[i]!r} na posição {i}"
        )

    return tokens


if __name__ == "__main__":
    query = '''
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
'''

    for tipo, valor in lexer(query):
        print(f"{tipo}: {valor}")
