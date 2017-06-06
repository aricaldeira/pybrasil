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

from __future__ import division, print_function, unicode_literals, absolute_import
import sys
import os
from ..base import tira_acentos

CURDIR = os.path.dirname(os.path.abspath(__file__))


class Pais(object):
    def __init__(self, nome='', codigo_bacen='', codigo_anp='',
                 codigo_siscomex='', nome_frances='', nome_ingles='', iso_3166_2='',
                 iso_3166_3='', iso_3166_numerico=''):
        self.nome = nome
        self.codigo_bacen = codigo_bacen
        self.codigo_anp = codigo_anp
        self.codigo_siscomex = codigo_siscomex
        self.nome_frances = nome_frances
        self.nome_ingles = nome_ingles
        self.iso_3166_2 = iso_3166_2
        self.iso_3166_3 = iso_3166_3
        self.iso_3166_numerico = iso_3166_numerico

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        return self.nome

    def __repr__(self):
        return str(self)

    @property
    def codigo_ibge(self):
        return self.codigo_bacen


def _monta_dicionario_bacen():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'pais.txt'), 'r')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.decode('utf-8').replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        p = Pais(nome=campos[0], codigo_bacen=campos[1], codigo_anp=campos[2], codigo_siscomex=campos[3], nome_frances=campos[4], nome_ingles=campos[5], iso_3166_2=campos[6], iso_3166_3=campos[7], iso_3166_numerico=campos[8])
        dicionario[p.codigo_bacen] = p

    return dicionario


def _monta_dicionario_nome():
    dicionario = {}

    for k, v in PAIS_BACEN.items():
        dicionario[tira_acentos(v.nome).upper()] = v

    return dicionario


def _monta_dicionario_iso_3166_2():
    dicionario = {}

    for k, v in PAIS_BACEN.items():
        dicionario[v.iso_3166_2] = v

    return dicionario


def _monta_dicionario_iso_3166_3():
    dicionario = {}

    for k, v in PAIS_BACEN.items():
        dicionario[v.iso_3166_3] = v

    return dicionario


if not hasattr(sys.modules[__name__], 'PAIS_BACEN'):
    PAIS_BACEN = _monta_dicionario_bacen()


if not hasattr(sys.modules[__name__], 'PAIS_BRASIL'):
    PAIS_BRASIL = PAIS_BACEN['1058']


if not hasattr(sys.modules[__name__], 'PAIS_NOME'):
    PAIS_NOME = _monta_dicionario_nome()


if not hasattr(sys.modules[__name__], 'PAIS_ISO_3166_2'):
    PAIS_ISO_3166_2 = _monta_dicionario_iso_3166_2()


if not hasattr(sys.modules[__name__], 'PAIS_ISO_3166_3'):
    PAIS_ISO_3166_3 = _monta_dicionario_iso_3166_3()
