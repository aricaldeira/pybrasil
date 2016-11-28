#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Números por extenso, cardinais, ordinais e cardinais com unidades de medida

Compatível com as versões 2 e 3 do Python
'''

from __future__ import division, print_function, unicode_literals

import re


PONTO_MILHAR = re.compile(r'(\d+)(\d{3})')
#PONTO_MILHAR_FINAL = re.compile(r'(\d{3})(\d+)')
PONTO_MILHAR_FINAL = re.compile(r'(\d+)(\d{3})')


def formata_valor(valor, casas_decimais=2, separador_milhar='.', separador_decimal=',', separador_milhar_decimal='', tamanho=0):
    negativo = valor < 0
    texto = str(abs(valor))

    if '.' in texto:
        inteiro, decimal = texto.split('.')

        if len(decimal) > casas_decimais:
            decimal = decimal[:casas_decimais]
        else:
            decimal = decimal[::-1].zfill(casas_decimais)[::-1]

    else:
        inteiro = texto
        decimal = ''.zfill(casas_decimais)

    if tamanho:
        inteiro = inteiro.zfill(tamanho)

    while PONTO_MILHAR.match(inteiro) and separador_milhar:
        inteiro = PONTO_MILHAR.sub(r'\1' + separador_milhar + r'\2', inteiro)

    while PONTO_MILHAR_FINAL.match(decimal) and separador_milhar_decimal:
        decimal = PONTO_MILHAR_FINAL.sub(r'\1' + separador_milhar_decimal + r'\2', decimal)

    texto = inteiro

    if decimal:
        texto += separador_decimal + decimal

    if negativo:
        texto = '-' + texto

    return texto
