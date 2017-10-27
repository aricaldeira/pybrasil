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


from dateutil.relativedelta import relativedelta
from datetime import date
from ..data import hoje, parse_datetime, data_hora_horario_brasilia, DIA_SEXTA, DIA_DOMINGO
from .feriado import (FERIADOS, monta_dicionario_datas)


def data_eh_feriado(data_referencia=hoje(), estado=None, municipio=None):
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()
    feriados = monta_dicionario_datas(data_referencia, tipo='F', estado=estado, municipio=municipio)

    if data_referencia in feriados:
        return feriados[data_referencia]

    return []


def data_eh_feriado_bancario(data_referencia=hoje(), estado=None, municipio=None):
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()
    feriados = monta_dicionario_datas(data_referencia, tipo=['F', 'B'], estado=estado, municipio=municipio)

    if data_referencia in feriados:
        return feriados[data_referencia]

    return []


def data_eh_feriado_emendado(data_referencia=hoje(), estado=None, municipio=None):
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()

    if data_referencia is None:
        return False

    #
    # Feriado emendado é um dia vago entre 2 feriados ou
    # 1 feriado e 1 final de semana
    #
    dia_antes = data_referencia + relativedelta(days=-1)
    dia_depois = data_referencia + relativedelta(days=+1)

    dia_antes_eh_util = dia_antes.weekday() <= DIA_SEXTA and \
        data_eh_feriado(dia_antes, estado, municipio) == []
    dia_depois_eh_util = dia_depois.weekday() <= DIA_SEXTA and \
        data_eh_feriado(dia_depois, estado, municipio) == []

    return not (dia_antes_eh_util or dia_depois_eh_util)


def data_eh_feriado_bancario_emendado(data_referencia=hoje(), estado=None, municipio=None):
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()

    if data_referencia is None:
        return False

    #
    # Feriado emendado é um dia vago entre 2 feriados ou
    # 1 feriado e 1 final de semana
    #
    dia_antes = data_referencia + relativedelta(days=-1)
    dia_depois = data_referencia + relativedelta(days=+1)

    dia_antes_eh_util = dia_antes.weekday() <= DIA_SEXTA and \
        data_eh_feriado_bancario(dia_antes, estado, municipio) == []
    dia_depois_eh_util = dia_depois.weekday() <= DIA_SEXTA and \
        data_eh_feriado_bancario(dia_depois, estado, municipio) == []

    return not (dia_antes_eh_util or dia_depois_eh_util)


def conta_feriados(data_inicial=hoje(), data_final=hoje(), estado=None, municipio=None):
    data_inicial = data_hora_horario_brasilia(parse_datetime(data_inicial)).date()
    data_final = data_hora_horario_brasilia(parse_datetime(data_final)).date()

    if data_inicial is None or data_final is None:
        return 0

    total = 0

    data = data_inicial

    while data <= data_final:
        feriados = data_eh_feriado(data, estado, municipio)
        if feriados != []:
            total += 1
        data += relativedelta(days=+1)

    return total


def conta_feriados_sem_domingo(data_inicial=hoje(), data_final=hoje(), estado=None, municipio=None):
    data_inicial = data_hora_horario_brasilia(parse_datetime(data_inicial)).date()
    data_final = data_hora_horario_brasilia(parse_datetime(data_final)).date()

    if data_inicial is None or data_final is None:
        return 0

    total = 0

    data = data_inicial

    while data <= data_final:
        if data.weekday() != DIA_DOMINGO:
            feriados = data_eh_feriado(data, estado, municipio)

            if feriados != []:
                total += 1

        data += relativedelta(days=+1)

    return total


FERIADOS_PERIODO = {}


def feriados_no_periodo(data_inicial, data_final, estado, municipio):
    data_inicial = parse_datetime(data_inicial).date().toordinal()
    data_final = parse_datetime(data_final).date().toordinal()

    periodo = str(data_inicial) + '_' + str(data_final)

    if estado in FERIADOS_PERIODO:
        if municipio in FERIADOS_PERIODO[estado]:
            if periodo in FERIADOS_PERIODO[estado][municipio]:
                return FERIADOS_PERIODO[estado][municipio][periodo]

    data = data_inicial
    feriados = {}
    while data <= data_final:
        feriados[data] = None
        feriado = data_eh_feriado(date.fromordinal(data), estado, municipio)

        if feriado:
            feriados[data] = feriado

        data += 1

    if not estado in FERIADOS_PERIODO:
        FERIADOS_PERIODO[estado] = {}

    if not municipio in FERIADOS_PERIODO[estado]:
        FERIADOS_PERIODO[estado][municipio] = {}

    if not periodo in FERIADOS_PERIODO[estado][municipio]:
        FERIADOS_PERIODO[estado][municipio][periodo] = feriados

    return FERIADOS_PERIODO[estado][municipio][periodo]
