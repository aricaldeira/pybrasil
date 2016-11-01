# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


MAPA_DIGITOS = {
    10: 0,
    11: 0,
}


def modulo11(texto='', pesos=range(2, 10), resto=False, mapa_digitos=MAPA_DIGITOS):
    '''
    '''
    peso = 0
    soma = 0

    for c in texto[::-1]:
        soma += int(c) * pesos[peso]
        peso += 1

        if peso >= len(pesos):
            peso = 0

    if resto:
        digito = soma % 11

    else:
        digito = 11 - (soma % 11)

        if digito in mapa_digitos:
            digito = mapa_digitos[digito]

    return str(digito)
