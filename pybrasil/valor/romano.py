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

from __future__ import division, print_function, unicode_literals


ROMANOS = (
    (1000000, 'M̅'),
    (100000, 'C̅'),
    (10000, 'M̅'),
    (5000, 'V̅'),
    (4000, 'I̅V̅'),
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
)

ROMANOS_UNICODE = (
    (1000000, 'Ⅿ̅'),
    (100000, 'Ⅽ̅'),
    (10000, 'Ⅿ̅'),
    (5000, 'Ⅴ̅̅'),
    (4000, 'Ⅰ̅̅Ⅴ̅'),
    (1000, 'Ⅿ'),
    (900, 'ⅭⅯ'),
    (500, 'Ⅾ'),
    (400, 'ⅭⅮ'),
    (100, 'Ⅽ'),
    (90, 'ⅩⅭ'),
    (50, 'Ⅼ'),
    (40, 'ⅩⅬ'),
    (10, 'Ⅹ'),
    (9, 'ⅠⅩ'),
    (5, 'Ⅴ'),
    (4, 'ⅠⅤ'),
    (1, 'Ⅰ'),
)

ROMANOS_MES_HORA_UNICODE = {
    1: 'Ⅰ',
    2: 'Ⅱ',
    3: 'Ⅲ',
    4: 'Ⅳ',
    5: 'Ⅴ',
    6: 'Ⅵ',
    7: 'Ⅶ',
    8: 'Ⅷ',
    9: 'Ⅸ',
    10: 'Ⅹ',
    11: 'Ⅺ',
    12: 'Ⅻ',
}


def romano(numero):
    numero_romano = ''

    for valor, letra in ROMANOS:
        quantidade = numero // valor
        numero_romano += letra * quantidade
        numero -= valor * quantidade

    return numero_romano


def romano_mes_hora(mes_hora):
    if mes_hora > 12:
        mes_hora = mes_hora % 12

    if mes_hora not in ROMANOS_MES_HORA_UNICODE:
        return ''

    return ROMANOS_MES_HORA_UNICODE[mes_hora]
