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
from future.utils import python_2_unicode_compatible
from io import open


CURDIR = os.path.dirname(os.path.abspath(__file__))


@python_2_unicode_compatible
class Estado(object):
    def __init__(self, sigla='', nome='', codigo_ibge='', fuso_horario='America/Sao_Paulo',
                 codigo_geoip=''):
        self.sigla = sigla
        self.nome = nome
        self.codigo_ibge = codigo_ibge
        self.fuso_horario = fuso_horario
        self.codigo_geoip = codigo_geoip

    def __str__(self):
        return self.nome + ' - ' + self.sigla

    def __repr__(self):
        return str(self)

    @property
    def uf(self):
        return self.sigla


def _monta_dicionario_ibge():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'estado.txt'), 'r', encoding='utf-8')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        e = Estado(sigla=campos[0], nome=campos[1], codigo_ibge=campos[2], fuso_horario=campos[3], codigo_geoip=campos[4])

        dicionario[e.codigo_ibge] = e

    return dicionario


def _monta_dicionario_sigla():
    dicionario = {}

    for k, v in ESTADO_IBGE.items():
        dicionario[v.sigla] = v

    return dicionario


if not hasattr(sys.modules[__name__], 'ESTADO_IBGE'):
    ESTADO_IBGE = _monta_dicionario_ibge()


if not hasattr(sys.modules[__name__], 'ESTADO_SIGLA'):
    ESTADO_SIGLA = _monta_dicionario_sigla()
