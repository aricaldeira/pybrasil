# -*- coding: utf-8 -*-
#
# PyBrasil - Functions useful for most Brazil's ERPs
#
# Copyright (C) 2017-
# Copyright (C) Ari Caldeira <ari.caldeira at tauga.com.br>
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
# Copyright (C) 2017-
# Copyright (C) Ari Caldeira <ari.caldeira arroba tauga.com.br>
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

from past.builtins import basestring
from ..base import tira_acentos
from .lista_banco import BANCO_CODIGO
from .pessoa import Beneficiario
from .banco import Banco


class RetornoBoleto(object):
    def __init__(self):
        self.banco = Banco()
        self.beneficiario = Beneficiario()
        self.data_hora = None
        self.sequencia = 0
        self.boletos = []
        self.registros = []
        self.tipo = 'CNAB_400'
        self.linhas = []
        self.codigo_ocorrencia = ''

    def arquivo_retorno(self, arquivo):
        if isinstance(arquivo, basestring):
            arquivo = open(arquivo, 'r')

        for linha in arquivo.readlines():
            self.linhas.append(linha.decode('iso-8859-1').replace('\n', '').replace('\r', ''))

        header = self.linhas[0]

        if len(header) != 400 and len(header) != 240:
            return False

        #
        # O VIACREDI dá o retorno em CNAB 240 mesmo se a remessa for CNAB 400
        #
        if header[:3] == '085':
            codigo_banco= '085'
            if len(header) == 240:
                self.tipo ="CNAB_240"

        else:
            codigo_banco = header[76:79]

        if not codigo_banco in BANCO_CODIGO:
            return False

        banco = BANCO_CODIGO[codigo_banco]
        self.banco = banco

        if self.tipo == "CNAB_400" and not hasattr(banco, 'header_retorno_400'):
            return False

        if self.tipo == "CNAB_240" and not hasattr(banco, 'header_retorno_240'):
            return False

        if self.tipo == "CNAB_400":
            banco.header_retorno_400(self)
            banco.linha_retorno_400(self)

        elif self.tipo == "CNAB_240":
            banco.header_retorno_240(self)
            banco.linha_retorno_240(self)

        return True
