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
