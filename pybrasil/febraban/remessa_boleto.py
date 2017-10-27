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
from ..data import data_hora_horario_brasilia
from datetime import date, datetime


class RemessaBoleto(object):
    def __init__(self):
        self.data_hora = None
        self.data_debito = None
        self.sequencia = 0
        self.boletos = []
        self.registros = []
        self.tipo = 'CNAB_400'
        self.valor_total = 0

    def _set_data_hora(self, valor):
        if valor is None or isinstance(valor, (date, datetime)):
            return valor

        if isinstance(valor, basestring):
            try:
                return data_hora_horario_brasilia(valor)
            except:
                return

    @property
    def data_hora(self):
        return self._data_hora

    @data_hora.setter
    def data_hora(self, valor):
        self._data_hora = self._set_data_hora(valor)

    @property
    def arquivo_remessa(self):
        if len(self.boletos):
            boleto = self.boletos[0]
            banco = boleto.banco
        else:
            banco = self.beneficiario.banco

        self.registros = []

        if self.tipo == 'CNAB_400':
            header = banco.header_remessa_400(self).split('\n')
        elif self.tipo == 'CNAB_240':
            header = banco.header_remessa_240(self).split('\n')

        if isinstance(header, list):
            self.registros += header
        else:
            self.registros += (header,)

        self.valor_total = 0

        for boleto in self.boletos:
            if self.tipo == 'CNAB_400':
                linhas = banco.linha_remessa_400(self, boleto).split('\n')
            elif self.tipo == 'CNAB_240':
                linhas = banco.linha_remessa_240(self, boleto).split('\n')

            self.valor_total += boleto.documento.valor

            if isinstance(linhas, list):
                self.registros += linhas
            else:
                self.registros += (linhas,)

        if self.tipo == 'CNAB_400':
            trailler = banco.trailler_remessa_400(self).split('\n')
        elif self.tipo == 'CNAB_240':
            trailler = banco.trailler_remessa_240(self).split('\n')

        if isinstance(trailler, list):
            self.registros += trailler
        else:
            self.registros += (trailler,)

        texto = '\r\n'.join(self.registros) + '\r\n'

        return texto

    @property
    def nome_arquivo(self):
        nome_remessa = str(self.sequencia).zfill(8) + '.REM'

        #
        # Bradesco
        #
        if self.boletos[0].banco.codigo == '237':
            nome_remessa = 'CB' + self.data_hora.strftime('%d%m') + str(self.sequencia).zfill(2) + '.TXT'

        #
        # Caixa Econômica
        #
        elif self.boletos[0].banco.codigo == '104':
            nome_remessa = 'E' + str(self.sequencia).zfill(8) + '.REM'

        #
        # SICREDI... meu, isso é bagunçado pro usuário...
        #
        elif self.boletos[0].banco.codigo == '748':
            nome_remessa = self.boletos[0].beneficiario.codigo.numero[:5].zfill(5)
            data = str(self.data_hora)

            if '-01-' in data:
                nome_remessa += '1'
            elif '-02-' in data:
                nome_remessa += '2'
            elif '-03-' in data:
                nome_remessa += '3'
            elif '-04-' in data:
                nome_remessa += '4'
            elif '-05-' in data:
                nome_remessa += '5'
            elif '-06-' in data:
                nome_remessa += '6'
            elif '-07-' in data:
                nome_remessa += '7'
            elif '-08-' in data:
                nome_remessa += '8'
            elif '-09-' in data:
                nome_remessa += '9'
            elif '-10-' in data:
                nome_remessa += 'O'
            elif '-11-' in data:
                nome_remessa += 'N'
            elif '-12-' in data:
                nome_remessa += 'D'

            nome_remessa += data[8:10]
            nome_remessa += '.CRM'

        return nome_remessa
