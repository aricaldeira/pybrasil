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


from dateutil.relativedelta import relativedelta
from .fuso_horario import data_hora_horario_brasilia, hoje
from .parse_datetime import parse_datetime
from ..feriado import data_eh_feriado_bancario, data_eh_feriado

DIAS_UTEIS = {}


def dias_uteis(data_inicial=hoje(), data_final=hoje(), estado=None, municipio=None):
    data_inicial = parse_datetime(data_inicial)
    data_inicial = data_hora_horario_brasilia(data_inicial)
    data_inicial = data_inicial.date()

    data_final = parse_datetime(data_final)
    data_final = data_hora_horario_brasilia(data_final)
    data_final = data_final.date()

    chave = unicode(data_inicial) + '_' + unicode(data_final) + '_' + unicode(estado) + '_' + unicode(municipio)

    if chave in DIAS_UTEIS:
        return DIAS_UTEIS[chave]

    du = []
    data = data_inicial
    while data <= data_final:
        #
        # Data não é nem sábado (5) nem domingo (6)
        #
        if data.weekday() < 5:
            if estado is not None and municipio is not None:
                if not data_eh_feriado(data, estado, municipio):
                    du.append(data)
            else:
                du.append(data)

        data += relativedelta(days=+1)

    DIAS_UTEIS[chave] = du
    return du


def dias_uteis_bancarios(data_inicial=hoje(), data_final=hoje(), estado=None, municipio=None):
    du = dias_uteis(data_inicial, data_final)

    i = 0
    while i < len(du):
        if data_eh_feriado_bancario(du[i], estado, municipio):
            du.pop(i)

        else:
            i += 1

    return du


def dia_util_pagamento(data_vencimento=hoje(), estado=None, municipio=None, antecipa=False):
    data_vencimento = parse_datetime(data_vencimento)
    data_vencimento = data_hora_horario_brasilia(data_vencimento)
    data_vencimento = data_vencimento.date()

    primeiro_dia = data_vencimento + relativedelta(months=-1)
    ultimo_dia = data_vencimento + relativedelta(months=+1)

    du = dias_uteis_bancarios(primeiro_dia, ultimo_dia, estado, municipio)

    data_antecipada = None

    for data in du:
        if antecipa:
            if data <= data_vencimento:
                data_antecipada = data
            else:
                return data_antecipada
        else:
            if data >= data_vencimento:
                return data
