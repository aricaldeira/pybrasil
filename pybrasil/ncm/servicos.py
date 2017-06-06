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
import os
import sys
from decimal import Decimal as D


CURDIR = os.path.dirname(os.path.abspath(__file__))


class Servicos(object):
    def __init__(self, codigo='', descricao='', al_ibpt_nacional=0, al_ibpt_internacional=0):
        self.codigo = codigo
        self.descricao = descricao
        self.al_ibpt_nacional = al_ibpt_nacional
        self.al_ibpt_internacional = al_ibpt_internacional

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        return self.codigo_formatado + ' - ' + self.descricao

    def __repr__(self):
        return str(self)

    @property
    def codigo_formatado(self):
        texto = self.codigo.zfill(4)
        texto = texto[:2] + '.' + texto[2:]
        return texto


def _monta_dicionario():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'servicos.txt'), 'r')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.decode('utf-8').replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        e = Servicos(codigo=campos[0], descricao=campos[1], al_ibpt_nacional=D(campos[2] or '0'), al_ibpt_internacional=D(campos[3] or 0))

        dicionario[e.codigo] = e

    return dicionario


if not hasattr(sys.modules[__name__], 'SERVICOS_CODIGO'):
    SERVICOS_CODIGO = _monta_dicionario()
