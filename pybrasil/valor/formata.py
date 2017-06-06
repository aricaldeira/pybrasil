#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# PyBrasil - Functions useful for most Brazil's ERPs
#
# Copyright (C) 2016-
# Copyright (C) Aristides Caldeira <aristides.caldeira at tauga.com.br>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation, either version 2.1 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# PyBrasil - Funções de validação necessárias a ERPs no Brasil
#
# Copyright (C) 2016-
# Copyright (C) Aristides Caldeira <aristides.caldeira arroba tauga.com.br>
#
# Este programa é um software livre: você pode redistribuir e/ou modificar
# este programa sob os termos da licença GNU Library General Public License,
# publicada pela Free Software Foundation, em sua versão 2.1 ou, de acordo
# com sua opção, qualquer versão posterior.
#
# Este programa é distribuido na esperança de que venha a ser útil,
# porém SEM QUAISQUER GARANTIAS, nem mesmo a garantia implícita de
# COMERCIABILIDADE ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. Veja a
# GNU Library General Public License para mais detalhes.
#
# Você deve ter recebido uma cópia da GNU Library General Public License
# juntamente com este programa. Caso esse não seja o caso, acesse:
# <http://www.gnu.org/licenses/>
#
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
