import re
from locale import setlocale, LC_ALL, currency


def aplica_desconto(preco, desconto):
    return preco * (100 - desconto) / 100


def formata_preco(preco):
    setlocale(LC_ALL, 'pt_BR.UTF-8')
    return currency(preco, grouping=True)


def cart_total_qtd(carrinho):
    return sum([valores['quantidade'] for valores in carrinho.values()])


def calc_total_compra(carrinho):
    return sum([
        item['preco_quantitativo_descontado']
        if item['preco_quantitativo_descontado']
        else item['preco_quantitativo']
        for item in carrinho.values()
    ])


def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11:
        return False

    novo_cpf = cpf[:-2]                 # Elimina os dois últimos digitos do CPF
    reverso = 10                        # Contador reverso
    total = 0

    # Loop do CPF
    for index in range(19):
        if index > 8:                   # Primeiro índice vai de 0 a 9,
            index -= 9                  # São os 9 primeiros digitos do CPF

        total += int(novo_cpf[index]) * reverso  # Valor total da multiplicação

        reverso -= 1                    # Decrementa o contador reverso
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d > 9:                   # Se o digito for > que 9 o valor é 0
                d = 0
            total = 0                   # Zera o total
            novo_cpf += str(d)          # Concatena o digito gerado no novo cpf

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Descobri que sequências avaliavam como verdadeiro, então também
    # adicionei essa checagem aqui
    if cpf == novo_cpf and not sequencia:
        return True
    else:
        return False
