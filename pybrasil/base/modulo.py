# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


def _modulo(texto='', modulo=11, peso_inicial=2, peso_maximo=9, resto=False, parcial=False):
    '''
    '''
    peso = peso_inicial
    soma = 0

    for c in texto[::-1]:
        soma_parcial = int(c) * peso

        #
        # Quando a soma for parcial, se o produto do algarismo × peso
        # for maior do que 9, somamos os algarismos individuais
        #
        if parcial and soma_parcial > 9:
            soma_parcial = int(str(soma_parcial)[0]) + int(str(soma_parcial)[1])

        soma = soma + soma_parcial
        peso = peso + 1

        if peso > peso_maximo:
            peso = peso_inicial

    if resto:
        digito = soma % modulo

    else:
        digito = modulo - (soma % modulo)

        if digito > 9:
            digito = 0

    return str(digito)


def modulo11(texto='', peso_inicial=2, peso_maximo=9, resto=False, parcial=False):
    return _modulo(texto, 11, peso_inicial, peso_maximo, resto, parcial)

def modulo10(texto='', peso_inicial=2, peso_maximo=9, resto=True, parcial=True):
    return _modulo(texto, 10, peso_inicial, peso_maximo, resto, parcial)