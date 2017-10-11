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

from ..base import modulo10
from ..valor import formata_valor
from ..data import parse_datetime, formata_data
from .pessoa import Beneficiario, Pagador
from .banco import Banco
from .codigo_barras import monta_linha_digitavel_boleto
from datetime import date, datetime


class Documento(object):
    def __init__(self):
        self.numero = ''
        self.data = None
        self.valor = 0
        self.especie = 'DM'
        self.numero_original = ''

    def _set_data(self, valor):
        if valor is None or isinstance(valor, date):
            return valor

        if isinstance(valor, datetime):
            return valor.date()

        if isinstance(valor, (str, unicode)):
            try:
                data = parse_datetime(valor)
                return data.date()
            except:
                return

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, valor):
        self._data = self._set_data(valor)

    @property
    def data_formatada(self):
        if self.data:
            return formata_data(self.data)
        else:
            return ''

    @property
    def valor_formatado(self):
        return formata_valor(self.valor)


class Boleto(object):
    def __init__(self, **kwargs):
        self.banco = Banco()
        self.beneficiario = Beneficiario()
        self.pagador = Pagador()
        self.sacador = Beneficiario()

        self.local_pagamento = 'Pagável em qualquer banco até o vencimento'
        self.aceite = 'N'
        self.moeda = '9'
        self.especie = 'R$'
        self.parcela = 1
        self.total_parcelas = 1

        self.nosso_numero = ''
        self.identificacao = ''

        self.documento = Documento()

        self.data_vencimento = None
        self.data_processamento = None
        self.data_ocorrencia = None
        self.data_credito = None
        self.data_abatimento = None
        self.data_desconto = None
        self.data_juros = None
        self.data_multa = None
        self.dias_protesto = 0
        self.dias_nao_recebimento = 0
        self.dias_negativacao = 0
        self.dias_baixa = 0
        self.dias_atraso = 0
        self.data_protesto = None
        self.data_baixa = None
        self.data_nao_recebimento = None
        self.data_negativacao = None
        self.comando = ''
        self.motivo = ''

        self.valor_despesa_cobranca = 0
        self.valor_abatimento = 0
        self.valor_desconto = 0
        self.valor_juros = 0
        self.percentual_juros = 0
        self.valor_multa = 0
        self.percentual_multa = 0
        self.valor_iof = 0
        self.valor_outras_despesas = 0
        self.valor_outros_creditos = 0
        self.valor_recebido = 0

        self.imprime_desconto = 0
        self.imprime_juros_multa = 0
        self.imprime_outras_deducoes = 0
        self.imprime_outros_acrescimos = 0
        self.imprime_valor_cobrado = 0

        self.pagamento_duplicado = False

        self.descricao = []
        self.instrucoes = []

    def _set_data(self, valor):
        if valor is None or isinstance(valor, date):
            return valor

        if isinstance(valor, datetime):
            return valor.date()

        if isinstance(valor, (str, unicode)):
            try:
                data = parse_datetime(valor)
                return data.date()
            except:
                return

    @property
    def data_vencimento(self):
        return self._data_vencimento

    @data_vencimento.setter
    def data_vencimento(self, valor):
        self._data_vencimento = self._set_data(valor)

    @property
    def data_processamento(self):
        return self._data_processamento

    @data_processamento.setter
    def data_processamento(self, valor):
        self._data_processamento = self._set_data(valor)

    @property
    def data_ocorrencia(self):
        return self._data_ocorrencia

    @data_ocorrencia.setter
    def data_ocorrencia(self, valor):
        self._data_ocorrencia = self._set_data(valor)

    @property
    def data_credito(self):
        return self._data_credito

    @data_credito.setter
    def data_credito(self, valor):
        self._data_credito = self._set_data(valor)

    @property
    def data_abatimento(self):
        return self._data_abatimento

    @data_abatimento.setter
    def data_abatimento(self, valor):
        self._data_abatimento = self._set_data(valor)

    @property
    def data_desconto(self):
        return self._data_desconto

    @data_desconto.setter
    def data_desconto(self, valor):
        self._data_desconto = self._set_data(valor)

    @property
    def data_juros(self):
        return self._data_juros

    @data_juros.setter
    def data_juros(self, valor):
        self._data_juros = self._set_data(valor)

    @property
    def data_multa(self):
        return self._data_multa

    @data_multa.setter
    def data_multa(self, valor):
        self._data_multa = self._set_data(valor)

    @property
    def data_protesto(self):
        return self._data_protesto

    @data_protesto.setter
    def data_protesto(self, valor):
        self._data_protesto = self._set_data(valor)

    @property
    def data_baixa(self):
        return self._data_baixa

    @data_baixa.setter
    def data_baixa(self, valor):
        self._data_baixa = self._set_data(valor)

    @property
    def data_nao_recebimento(self):
        return self._data_nao_recebimento

    @data_nao_recebimento.setter
    def data_nao_recebimento(self, valor):
        self._data_nao_recebimento = self._set_data(valor)

    @property
    def data_negativacao(self):
        return self._data_negativacao

    @data_negativacao.setter
    def data_negativacao(self, valor):
        self._data_negativacao = self._set_data(valor)

    @property
    def imprime_desconto_formatado(self):
        if self.imprime_desconto:
            return formata_valor(self.imprime_desconto)
        else:
            return u''

    @property
    def imprime_juros_multa_formatado(self):
        if self.imprime_juros_multa:
            return formata_valor(self.imprime_juros_multa)
        else:
            return u''

    @property
    def imprime_outras_deducoes_formatado(self):
        if self.imprime_outras_deducoes:
            return formata_valor(self.imprime_outras_deducoes)
        else:
            return u''

    @property
    def imprime_outros_acrescimos_formatado(self):
        if self.imprime_outros_acrescimos:
            return formata_valor(self.imprime_outros_acrescimos)
        else:
            return u''

    @property
    def imprime_valor_cobrado_formatado(self):
        if self.imprime_valor_cobrado:
            return formata_valor(self.imprime_valor_cobrado)
        else:
            return u''

    @property
    def data_vencimento_formatada(self):
        return formata_data(self.data_vencimento)

    @property
    def data_processamento_formatada(self):
        if self.data_processamento:
            return formata_data(self.data_processamento)
        else:
            return ''

    @property
    def digito_nosso_numero(self):
        return self.banco.calcula_digito_nosso_numero(self)

    @property
    def codigo_barras(self):
        #
        # O código de barras de todos os bancos é formado da mesma forma:
        #
        # Posição  #   Conteúdo
        # 01 a 03  03  Número do banco
        # 04       01  Código da Moeda - 9 para Real
        # 05       01  Digito verificador do Código de Barras
        # 06 a 09  04  Data de vencimento em dias partis de 07/10/1997
        # 10 a 19  10  Valor do boleto (8 inteiros e 2 decimais)
        # 20 a 44  25  Campo Livre definido por cada banco
        # Total    44
        #
        if self.banco.codigo == '136':
            codigo_barras = '237'
        else:
            codigo_barras = str(self.banco.codigo or '0').zfill(3)

        codigo_barras += str(self.moeda or '9').zfill(1)
        codigo_barras += str(self.banco.fator_vencimento(self) or '0').zfill(4)
        codigo_barras += str(int((self.documento.valor * 100) or 0)).zfill(10)
        codigo_barras += str(self.banco.campo_livre(self)).zfill(25)

        dv = self.banco.calcula_digito_codigo_barras(codigo_barras)

        #
        # Insere o dígito verificador na 5ª posição do código
        #
        codigo_barras = codigo_barras[:4] + dv + codigo_barras[4:]

        return codigo_barras

    @property
    def linha_digitavel(self):
        return monta_linha_digitavel_boleto(self.codigo_barras)

    @property
    def descricao_impressao(self):
        return '<br/>'.join(self.descricao)

    @property
    def instrucoes_impressao(self):
        return '<br/>'.join(self.instrucoes)

    @property
    def comando_remessa_descricao(self):
        if self.comando in self.banco.descricao_comandos_remessa:
            return self.banco.descricao_comandos_remessa[self.comando]
        else:
            return self.comando

    @property
    def comando_retorno_descricao(self):
        if self.comando in self.banco.descricao_comandos_retorno:
            return self.banco.descricao_comandos_retorno[self.comando]
        else:
            return self.comando

    @property
    def comando_remessa_descricao_grupo(self):
        if self.comando in self.banco.descricao_comandos_remessa:
            return self.comando + ' - ' + self.banco.descricao_comandos_remessa[self.comando]
        else:
            return self.comando

    @property
    def comando_retorno_descricao_grupo(self):
        if self.comando in self.banco.descricao_comandos_retorno:
            return self.comando + ' - ' + self.banco.descricao_comandos_retorno[self.comando]
        else:
            return self.comando

    @property
    def imprime_carteira_nosso_numero(self):
        return self.banco.carteira_nosso_numero(self)

    @property
    def imprime_agencia_conta(self):
        return self.banco.agencia_conta(self)

    @property
    def imprime_agencia_beneficiario(self):
        return self.banco.agencia_beneficiario(self)

    @property
    def imprime_carteira(self):
        return self.banco.imprime_carteira(self)
