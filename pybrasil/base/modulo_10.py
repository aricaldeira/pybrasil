# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


def modulo10(texto='', pesos=[2, 1], modulo=False):
    '''
    '''
    peso = 0
    soma = 0

    # texto[::-1] reverte o conteúdo do texto 123 -> 321
    for c in texto[::-1]:
        soma_parcial = int(c) * pesos[peso]

        if soma_parcial > 9:
            soma_parcial = int(str(soma_parcial)[0]) + int(str(soma_parcial)[1])

        soma += soma_parcial
        peso += 1

        if peso >= len(pesos):
            peso = 0

    if modulo:
        return soma % 10

    digito = 10 - (soma % 10)

    if digito > 9:
        digito = 0

    return str(digito)
