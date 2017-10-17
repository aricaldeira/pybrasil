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

import os
import base64
from StringIO import StringIO
from datetime import date
from ..base import modulo11, modulo10, tira_acentos

CURDIR = os.path.dirname(os.path.abspath(__file__))


class Banco(object):
    def __init__(self, codigo='', nome=''):
        self.codigo = codigo
        self.nome = nome
        self.arquivo_logo = os.path.join(CURDIR, 'logo', codigo + '.jpg')

        if os.path.exists(self.arquivo_logo):
            self.logo = base64.b64encode(open(self.arquivo_logo, 'rb').read())
        else:
            self.logo = None
            self.arquivo_logo = ''

        self.arquivo_template_boleto = os.path.join(CURDIR,
            'template_boleto', codigo + '.odt')
        self.arquivo_template_boleto_geral = os.path.join(CURDIR,
            'template_boleto', 'boleto.odt')

        if os.path.exists(self.arquivo_template_boleto):
            self.template_boleto = StringIO()
            self.template_boleto.write(
                open(self.arquivo_template_boleto, 'rb').read())
            self.template_boleto.seek(0)
        elif os.path.exists(self.arquivo_template_boleto_geral):
            self.template_boleto = StringIO()
            self.template_boleto.write(open(
                self.arquivo_template_boleto_geral, 'rb').read())
            self.template_boleto.seek(0)
        else:
            self.template_boleto = None
            self.arquivo_template_boleto = ''

        self.carteira = ''
        self.modalidade = ''
        self.convenio = ''
        self.modulo10 = modulo10
        self.modulo11 = modulo11
        self.tira_acentos = tira_acentos
        self.descricao_comandos_remessa = {}
        self.descricao_comandos_retorno = {}
        self.comandos_liquidacao = {}
        self.comandos_baixa = []

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        return self.nome + ' - ' + self.codigo

    def __repr__(self):
        return str(self)

    @property
    def digito(self):
        #
        # SICREDI não tem dígito
        #
        if self.codigo == '748':
            return 'X'

        #
        # VIACREDI o dígito não é por módulo
        #
        elif self.codigo == '085':
            return '1'

        #
        # UNICRED usa o leiaute do Bradesco
        #
        elif self.codigo == '136':
            return modulo11('237')

        else:
            return modulo11(self.codigo)

    @property
    def codigo_digito(self):
        #
        # UNICRED usa o leiaute do Bradesco
        #
        if self.codigo == '136':
            return '%s-%s' % ('237', self.digito)

        else:
            return '%s-%s' % (self.codigo.zfill(3), self.digito)

    def fator_vencimento(self, boleto):
        fator_vencimento = boleto.data_vencimento - date(1997, 10, 7)
        return fator_vencimento.days

    def calcula_digito_codigo_barras(self, codigo_barras):
        return modulo11(codigo_barras, mapa_digitos={0: 1, 1: 1, 10: 1, 11: 1})

    def calcula_digito_nosso_numero(self, boleto):
        return self.modulo10(boleto.nosso_numero)

    def campo_livre(self, boleto):
        return ''

    def carteira_nosso_numero(self, boleto):
        return '%s/%s-%s' % (boleto.banco.carteira, boleto.nosso_numero,
                             boleto.digito_nosso_numero)

    def agencia_conta(self, boleto):
        if boleto.beneficiario.conta.digito:
            return '%s/%s-%s' % (boleto.beneficiario.agencia.numero,
                                 boleto.beneficiario.conta.numero,
                                 boleto.beneficiario.conta.digito)

        else:
            return '%s/%s' % (boleto.beneficiario.agencia.numero,
                              boleto.beneficiario.conta.numero)

    def agencia_codigo_beneficiario(self, boleto):
        if boleto.beneficiario.codigo.digito:
            return '%s/%s-%s' % (boleto.beneficiario.agencia.numero,
                                 boleto.beneficiario.codigo.numero,
                                 boleto.beneficiario.codigo.digito)

        else:
            return '%s/%s' % (boleto.beneficiario.agencia.numero,
                              boleto.beneficiario.codigo.numero)

    def imprime_carteira(self, boleto):
        return boleto.banco.carteira
