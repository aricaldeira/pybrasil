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


from collections import namedtuple
from dateutil.relativedelta import relativedelta
from .fuso_horario import data_hora_horario_brasilia, hoje
from .parse_datetime import parse_datetime


def tempo(data_inicial=hoje(), data_final=hoje()):
    data_inicial = parse_datetime(data_inicial)
    data_inicial = data_hora_horario_brasilia(data_inicial)
    data_inicial = data_inicial.date()

    data_final = parse_datetime(data_final)
    data_final = data_hora_horario_brasilia(data_final)
    data_final = data_final.date()

    dif = relativedelta(data_final, data_inicial)
    dif += relativedelta(days=+1)

    return dif


def idade_anos(data_nascimento, data_referencia=hoje()):
    dif = tempo(data_nascimento, data_referencia)
    dif += relativedelta(days=-1)

    return dif.years


def idade_meses(data_nascimento, data_referencia=hoje(), quinze_dias=False):
    dif = tempo(data_nascimento, data_referencia)
    dif += relativedelta(days=-1)

    meses = dif.months
    meses += dif.years * 12

    if data_nascimento.year == data_referencia.year and data_nascimento.month == data_referencia.month:
        if (data_referencia.day - data_nascimento.day + 1) >= 15:
            meses = 1

    return meses


def idade_meses_sem_dia(data_nascimento, data_referencia=hoje()):
    #
    # Considera que as duas datas ocorrem no mesmo dia do mês
    #
    data_nascimento = parse_datetime(data_nascimento)
    data_nascimento += relativedelta(day=1)

    data_referencia = parse_datetime(data_referencia)
    data_referencia += relativedelta(day=1)

    return idade_meses(data_nascimento, data_referencia)


def dias_coincidentes(data_inicial_periodo_1, data_final_periodo_1, data_inicial_periodo_2, data_final_periodo_2):
    data_inicial_periodo_1 = parse_datetime(data_inicial_periodo_1)
    data_inicial_periodo_1 = data_hora_horario_brasilia(data_inicial_periodo_1)
    data_inicial_periodo_1 = data_inicial_periodo_1.date()

    data_final_periodo_1 = parse_datetime(data_final_periodo_1)
    data_final_periodo_1 = data_hora_horario_brasilia(data_final_periodo_1)
    data_final_periodo_1 = data_final_periodo_1.date()

    data_inicial_periodo_2 = parse_datetime(data_inicial_periodo_2)
    data_inicial_periodo_2 = data_hora_horario_brasilia(data_inicial_periodo_2)
    data_inicial_periodo_2 = data_inicial_periodo_2.date()

    data_final_periodo_2 = parse_datetime(data_final_periodo_2)
    data_final_periodo_2 = data_hora_horario_brasilia(data_final_periodo_2)
    data_final_periodo_2 = data_final_periodo_2.date()

    Periodo = namedtuple('Periodo', ['data_inicial', 'data_final'])
    periodo_1 = Periodo(data_inicial=data_inicial_periodo_1, data_final=data_final_periodo_1)
    periodo_2 = Periodo(data_inicial=data_inicial_periodo_2, data_final=data_final_periodo_2)
    ultima_data_inicial = max(periodo_1.data_inicial, periodo_2.data_inicial)
    primeira_data_final = min(periodo_1.data_final, periodo_2.data_final)

    dias_coincidentes = (primeira_data_final - ultima_data_inicial).days + 1
    return dias_coincidentes
