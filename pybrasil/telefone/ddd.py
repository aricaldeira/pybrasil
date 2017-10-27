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

DDD = [
    '11',  # SP
    '12',  # SP
    '13',  # SP
    '14',  # SP
    '15',  # SP
    '16',  # SP
    '17',  # SP
    '18',  # SP
    '19',  # SP
    '21',  # RJ
    '22',  # RJ
    '24',  # RJ
    '27',  # ES
    '28',  # ES
    '31',  # MG
    '32',  # MG
    '33',  # MG
    '34',  # MG
    '35',  # MG
    '37',  # MG
    '38',  # MG
    '41',  # PR
    '41',  # SC
    '42',  # PR
    '42',  # SC
    '43',  # PR
    '44',  # RS
    '44',  # PR
    '45',  # PR
    '46',  # PR
    '47',  # SC
    '48',  # SC
    '49',  # SC
    '51',  # RS
    '53',  # RS
    '54',  # RS
    '55',  # RS
    '61',  # DF
    '61',  # GO
    '62',  # GO
    '63',  # TO
    '64',  # GO
    '65',  # MT
    '66',  # MT
    '67',  # MS
    '68',  # AC
    '69',  # RO
    '71',  # BA
    '73',  # BA
    '74',  # BA
    '75',  # BA
    '77',  # BA
    '79',  # SE
    '81',  # PE
    '82',  # AL
    '83',  # PB
    '84',  # RN
    '85',  # CE
    '86',  # PI
    '87',  # PE
    '88',  # CE
    '89',  # PI
    '91',  # PA
    '92',  # AM
    '93',  # PA
    '94',  # PA
    '95',  # RR
    '96',  # AP
    '97',  # AM
    '98',  # MA
    '99',  # MA
]


DDDS = r'(' + '|'.join(DDD) + ')'
