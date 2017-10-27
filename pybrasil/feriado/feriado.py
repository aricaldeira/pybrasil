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
from builtins import str
from past.builtins import basestring
from io import open
from ..data import hoje, data_hora_horario_brasilia, parse_datetime, formata_data
from ..ibge import (Local, Municipio, Estado, MUNICIPIO_ESTADO_NOME, MUNICIPIO_IBGE, MUNICIPIO_SIAFI, ESTADO_IBGE, ESTADO_SIGLA)
from ..base import tira_acentos
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta
from copy import copy


CURDIR = os.path.dirname(os.path.abspath(__file__))


@python_2_unicode_compatible
class Feriado(Local):
    def __init__(self, **kwargs):
        super(Feriado, self).__init__(**kwargs)
        self.nome = kwargs.get('nome', '')
        self.tipo = kwargs.get('tipo', 'F')
        self.abrangencia = kwargs.get('abrangencia', 'N')
        self.quando = kwargs.get('quando', None)
        self.dia = kwargs.get('dia', None)
        self.dia_da_semana = kwargs.get('dia_da_semana', None)
        self.mes = kwargs.get('mes', None)
        self.ano = kwargs.get('ano', None)
        self.dias_de_diferenca = kwargs.get('dias_de_diferenca', 0)
        self.ajuste = kwargs.get('ajuste', None)
        self.data_referencia = hoje()

    def __str__(self):
        txt = self.nome + ' - ' + formata_data(self.data_feriado, '%a, %d-%b-%Y')

        if self.abrangencia == 'E':
            txt += ', somente em ' + str(self.estado)
        elif self.abrangencia == 'M':
            txt += ', somente em ' + str(self.municipio)

        return txt

    def __repr__(self):
        return str(self)

    def data(self, data_referencia=None):
        if data_referencia is not None:
            self.data_referencia = parse_datetime(data_referencia)

        ano = self.data_referencia.year
        mes = self.data_referencia.month
        dia = self.data_referencia.day
        data_feriado = data_referencia

        if self.quando == 'A':
            data_feriado = date(self.ano, self.mes, self.dia)

        elif self.quando == 'M':
            data_feriado = date(ano, self.mes, self.dia)

        elif self.quando == 'D':
            data_feriado = date(ano, mes, self.dia)

        elif self.quando == 'P':
            data_feriado = data_hora_horario_brasilia(easter(ano))

        elif self.quando == 'S':
            data_feriado = date(ano, self.mes, 1)

            #
            # Dias para chegar no dia da semana
            #
            dias_a_avancar = self.dia_da_semana - data_feriado.weekday()

            #
            # Dias para chegar no nº dia da semana no mês
            #
            if self.dia > 1:
                dias_a_avancar += (self.dia - 1) * 7

            data_feriado = data_feriado + relativedelta(days=dias_a_avancar)

        data_feriado += relativedelta(days=self.dias_de_diferenca)

        if self.ajuste:
            if self.ajuste == 'AC':
                #
                # Se o feriado cair na terça, quarta ou quinta,
                # avança para sexta
                #
                if data_feriado.weekday() in (1, 2, 3):
                    dias_a_avancar = 4 - data_feriado.weekday()
                    data_feriado += relativedelta(days=dias_a_avancar)

            elif self.ajuste == 'SC':
                #
                # Se o feriado cair em dia útil,
                # avança para sábado
                #
                if data_feriado.weekday() in (0, 1, 2, 3, 4, 5):
                    dias_a_avancar = 6 - data_feriado.weekday()
                    data_feriado += relativedelta(days=dias_a_avancar)

        self._data_feriado = data_hora_horario_brasilia(data_feriado).date()
        return self._data_feriado

    @property
    def data_feriado(self):
        return self.data()


def _monta_lista_feriados():
    lista = []

    arquivo = open(os.path.join(CURDIR, 'feriado.txt'), 'r', encoding='utf-8')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        nome, tipo, abrangencia, estado, municipio_ibge, municipio_nome, quando, dia, dia_da_semana, mes, ano, dias_de_diferenca, ajuste = campos

        if dia != '':
            dia = int(dia)

        if dia_da_semana != '':
            dia_da_semana = int(dia_da_semana)

        if mes != '':
            mes = int(mes)

        if ano != '':
            ano = int(ano)

        if dias_de_diferenca != '':
            dias_de_diferenca = int(dias_de_diferenca)

        f = Feriado(nome=nome, tipo=tipo, abrangencia=abrangencia, estado=estado, municipio=municipio_ibge, quando=quando, dia=dia, dia_da_semana=dia_da_semana, mes=mes, ano=ano, dias_de_diferenca=dias_de_diferenca, ajuste=ajuste)

        lista.append(f)

    return lista


if not hasattr(sys.modules[__name__], 'FERIADOS'):
    FERIADOS = _monta_lista_feriados()


_numero_de_feriados = 0
_memoria_feriados = {}


def _monta_dicionario_datas(data_referencia=hoje()):
    global _numero_de_feriados
    global _memoria_feriados
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()

    if len(FERIADOS) == _numero_de_feriados and data_referencia in _memoria_feriados:
        return _memoria_feriados[data_referencia]

    dicionario = {}

    for f in FERIADOS:
        data = f.data(data_referencia)

        if data in dicionario:
            dicionario[data].append(f)
        else:
            dicionario[data] = [f]

    if _numero_de_feriados != len(FERIADOS):
        _numero_de_feriados = len(FERIADOS)
        _memoria_feriados = {}

    _memoria_feriados[data_referencia] = dicionario

    return dicionario


def monta_dicionario_datas(data_referencia=hoje(), tipo=None, estado=None, municipio=None):
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()

    f_teste = Feriado()
    f_teste.estado = estado
    f_teste.municipio = municipio

    dicionario = {}

    for data, feriados in _monta_dicionario_datas(data_referencia).iteritems():
        for f in feriados:
            if tipo is not None:
                if isinstance(tipo, (list, tuple)):
                    if f.tipo not in tipo:
                        continue

                elif isinstance(tipo, basestring):
                    if f.tipo != tipo:
                        continue

            if estado is not None:
                if f.abrangencia == 'E' and f.estado != f_teste.estado:
                    continue

                elif f.abrangencia == 'M' and f.municipio.estado != f_teste.estado:
                    continue

            if municipio is not None:
                if f.abrangencia == 'E' and f.estado != f_teste.municipio.estado:
                    continue

                elif f.abrangencia == 'M' and f.municipio != f_teste.municipio:
                    continue

            if data in dicionario:
                dicionario[data].append(f)
            else:
                dicionario[data] = [f]

    return dicionario
