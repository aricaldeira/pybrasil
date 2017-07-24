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
from ..base import tira_acentos
from .pais import PAIS_BRASIL
from .estado import ESTADO_SIGLA, Estado


CURDIR = os.path.dirname(os.path.abspath(__file__))


class Municipio(object):
    def __init__(self, nome='', estado='', codigo_ibge='', codigo_siafi='', codigo_anp='',
                 pais=None, ddd='', cep=''):
        self.nome = nome

        if estado:
            self.estado = ESTADO_SIGLA[estado]
        else:
            self.estado = Estado()

        self.codigo_ibge = codigo_ibge
        self.codigo_siafi = codigo_siafi
        self.codigo_anp = codigo_anp
        self.pais = pais
        self.ddd = ddd
        self.cep = cep

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        return self.nome + ' - ' + self.estado.sigla

    def __repr__(self):
        return str(self)


def _monta_dicionario_ibge():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'municipio.txt'), 'r')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.decode('utf-8').replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        m = Municipio(nome=campos[0], estado=campos[1], codigo_ibge=campos[2], codigo_siafi=campos[3], codigo_anp=campos[4], ddd=campos[5], cep=campos[6])

        if m.estado != 'EX':
            m.pais = PAIS_BRASIL

        dicionario[m.codigo_ibge] = m

    return dicionario


def _monta_dicionario_siafi():
    dicionario = {}

    for k, v in MUNICIPIO_IBGE.items():
        if v.codigo_siafi:
            dicionario[v.codigo_siafi] = v

    return dicionario


def _monta_dicionario_estado_nome():
    dicionario = {}

    for k, v in MUNICIPIO_IBGE.items():
        if not v.estado.sigla in dicionario:
            dicionario[v.estado.sigla] = {}

        dicionario[v.estado.sigla][tira_acentos(v.nome).upper()] = v

    return dicionario


def _monta_dicionario_nome():
    dicionario = {}

    for k, v in MUNICIPIO_IBGE.items():
        if not tira_acentos(v.nome).upper() in dicionario:
            dicionario[tira_acentos(v.nome).upper()] = []

        dicionario[tira_acentos(v.nome).upper()].append(v)

    return dicionario


if not hasattr(sys.modules[__name__], 'MUNICIPIO_IBGE'):
    MUNICIPIO_IBGE = _monta_dicionario_ibge()


if not hasattr(sys.modules[__name__], 'MUNICIPIO_SIAFI'):
    MUNICIPIO_SIAFI = _monta_dicionario_siafi()


if not hasattr(sys.modules[__name__], 'MUNICIPIO_ESTADO_NOME'):
    MUNICIPIO_ESTADO_NOME = _monta_dicionario_estado_nome()


if not hasattr(sys.modules[__name__], 'MUNICIPIO_NOME'):
    MUNICIPIO_NOME = _monta_dicionario_nome()
