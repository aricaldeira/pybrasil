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
import os
import sys
from io import open
from ..base import tira_acentos
from ..ibge.municipio import MUNICIPIO_ESTADO_NOME


CURDIR = os.path.dirname(os.path.abspath(__file__))


def _monta_dicionario_segmento(segmento):
    dicionario = {}

    arquivo = open(os.path.join(CURDIR,
        'codigo_barras_arrecadacao_segmento_{segmento}.txt'.format(
            segmento=segmento)), 'r', encoding='utf-8')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.replace('\n', '').replace('\r', '')
        codigo, nome, estado = linha.split('|')
        codigo = codigo.strip()
        nome = nome.strip().upper()
        estado = estado.strip().upper()
        municipio = None

        if not (codigo and nome):
            continue

        #
        # Prefeituras de municípios
        #
        if segmento == '1':
            if estado in MUNICIPIO_ESTADO_NOME:
                if tira_acentos(nome) in MUNICIPIO_ESTADO_NOME[estado]:
                    municipio = \
                        MUNICIPIO_ESTADO_NOME[estado][tira_acentos(nome)]

        dicionario[codigo] = {
            'codigo': codigo,
            'nome': nome,
            'estado': estado,
            'municipio': municipio,
        }

    return dicionario


if not hasattr(sys.modules[__name__], 'CODIGO_BARRAS_ARRECADACAO_SEGMENTO_1'):
    CODIGO_BARRAS_ARRECADACAO_SEGMENTO_1 = _monta_dicionario_segmento('1')

if not hasattr(sys.modules[__name__], 'CODIGO_BARRAS_ARRECADACAO_SEGMENTO_2'):
    CODIGO_BARRAS_ARRECADACAO_SEGMENTO_2 = _monta_dicionario_segmento('2')

if not hasattr(sys.modules[__name__], 'CODIGO_BARRAS_ARRECADACAO_SEGMENTO_3'):
    CODIGO_BARRAS_ARRECADACAO_SEGMENTO_3 = _monta_dicionario_segmento('3')

if not hasattr(sys.modules[__name__], 'CODIGO_BARRAS_ARRECADACAO_SEGMENTO_4'):
    CODIGO_BARRAS_ARRECADACAO_SEGMENTO_4 = _monta_dicionario_segmento('4')

if not hasattr(sys.modules[__name__], 'CODIGO_BARRAS_ARRECADACAO_SEGMENTO_5'):
    CODIGO_BARRAS_ARRECADACAO_SEGMENTO_5 = _monta_dicionario_segmento('5')

if not hasattr(sys.modules[__name__], 'CODIGO_BARRAS_ARRECADACAO_SEGMENTO_7'):
    CODIGO_BARRAS_ARRECADACAO_SEGMENTO_7 = _monta_dicionario_segmento('7')

if not hasattr(sys.modules[__name__], 'CODIGO_BARRAS_ARRECADACAO_SEGMENTOS'):
    CODIGO_BARRAS_ARRECADACAO_SEGMENTOS = {
        '1': CODIGO_BARRAS_ARRECADACAO_SEGMENTO_1,
        '2': CODIGO_BARRAS_ARRECADACAO_SEGMENTO_2,
        '3': CODIGO_BARRAS_ARRECADACAO_SEGMENTO_3,
        '4': CODIGO_BARRAS_ARRECADACAO_SEGMENTO_4,
        '5': CODIGO_BARRAS_ARRECADACAO_SEGMENTO_5,
        '7': CODIGO_BARRAS_ARRECADACAO_SEGMENTO_7,
    }
