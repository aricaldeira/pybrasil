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
from .fuso_horario import data_hora_horario_brasilia, agora
from .parse_datetime import parse_datetime
from datetime import timedelta, time
from ..valor.decimal import Decimal as D
from .dias_uteis import dias_uteis, dias_uteis_bancarios


PERIODO_UTIL_MANHA = (time( 8,  0, 0), time(12, 0, 0))
PERIODO_UTIL_TARDE = (time(13, 30, 0), time(18, 0, 0))
HORA_INI_MANHA, HORA_FIM_MANHA = PERIODO_UTIL_MANHA
HORA_INI_TARDE, HORA_FIM_TARDE = PERIODO_UTIL_TARDE


def _ajusta_data(data, adianta=False):
    if data.time() < HORA_INI_MANHA:
        data += relativedelta(hour=HORA_INI_MANHA.hour, minute=HORA_INI_MANHA.minute, second=HORA_INI_MANHA.second)

    elif data.time() > HORA_FIM_MANHA and data.time() < HORA_INI_TARDE:
        if adianta:
            data += relativedelta(hour=HORA_FIM_MANHA.hour, minute=HORA_FIM_MANHA.minute, second=HORA_FIM_MANHA.second)
        else:
            data += relativedelta(hour=HORA_INI_TARDE.hour, minute=HORA_INI_TARDE.minute, second=HORA_INI_TARDE.second)

    elif data.time() > HORA_FIM_TARDE:
        data += relativedelta(hour=HORA_FIM_TARDE.hour, minute=HORA_FIM_TARDE.minute, second=HORA_FIM_TARDE.second)

    return data


def _intervalo_util(data_inicial, data_final):
    intervalo = data_final - data_inicial

    if data_inicial.time() < HORA_FIM_MANHA and data_final.time() > HORA_INI_TARDE:
        #
        # 1 hora e meia a menos
        #
        intervalo -= timedelta(seconds=1.5*60*60)

    return intervalo


def horas_uteis(data_inicial=agora(), data_final=agora()):
    data_inicial = parse_datetime(data_inicial)
    data_inicial = data_hora_horario_brasilia(data_inicial)

    #
    # Se não for dia útil - segunda a sexta, avança para a próxima
    # segunda-feira, às 8 da manhã
    #
    if data_inicial.weekday() == 5:
        #print('a', data_inicial)
        data_inicial += relativedelta(days=+2)
        #print('b', data_inicial)
        data_inicial += relativedelta(hour=HORA_INI_MANHA.hour, minute=HORA_INI_MANHA.minute, second=HORA_INI_MANHA.second)
        #print('c', data_inicial)
    elif data_inicial.weekday() == 6:
        #print('d', data_inicial)
        data_inicial += relativedelta(days=+1)
        #print('e', data_inicial)
        data_inicial += relativedelta(hour=HORA_INI_MANHA.hour, minute=HORA_INI_MANHA.minute, second=HORA_INI_MANHA.second)
        #print('f', data_inicial)

    data_inicial = _ajusta_data(data_inicial)
    #print('ff', data_inicial)

    data_final = parse_datetime(data_final)
    data_final = data_hora_horario_brasilia(data_final)

    #
    # Se não for dia útil - segunda a sexta, avança para a próxima
    # segunda-feira, às 8 da manhã
    #
    if data_final.weekday() == 5:
        #print('g', data_final)
        data_final += relativedelta(days=+2)
        #print('h', data_final)
        data_final += relativedelta(hour=HORA_INI_MANHA.hour, minute=HORA_INI_MANHA.minute, second=HORA_INI_MANHA.second)
        #print('i', data_final)
    elif data_final.weekday() == 6:
        #print('j', data_final)
        data_final += relativedelta(days=+1)
        #print('k', data_final)
        data_final += relativedelta(hour=HORA_INI_MANHA.hour, minute=HORA_INI_MANHA.minute, second=HORA_INI_MANHA.second)
        #print('l', data_final)

    data_final = _ajusta_data(data_final)
    #print('ll', data_final)

    intervalo = timedelta(days=0, seconds=0)

    if data_inicial.date() == data_final.date():
        intervalo = data_final - data_inicial

    else:
        #
        # Quantos dias de diferença?
        #
        dias = dias_uteis_bancarios(data_inicial, data_final, municipio='JOINVILLE', estado='SC', emenda_feriado=True)
        #print(dias)
        dias = len(dias) - 2
        if dias < 0:
            dias = 0

        #
        # Agora, conta as horas do 1º dia
        #
        intervalo_primeiro_dia = _intervalo_util(data_inicial, data_inicial + relativedelta(hour=HORA_FIM_TARDE.hour, minute=HORA_FIM_TARDE.minute, seconds=HORA_FIM_TARDE.second))

        #print('a2', data_inicial)
        #print('b2', data_inicial + relativedelta(hour=HORA_FIM_TARDE.hour, minute=HORA_FIM_TARDE.minute, seconds=HORA_FIM_TARDE.second))
        #print('c2', intervalo_primeiro_dia)

        #
        # E as do último dia
        #
        #print('d2', data_final)
        #print('e2', data_final + relativedelta(hour=HORA_INI_MANHA.hour, minute=HORA_INI_MANHA.minute, seconds=HORA_INI_MANHA.second))
        intervalo_ultimo_dia = _intervalo_util(data_final + relativedelta(hour=HORA_INI_MANHA.hour, minute=HORA_INI_MANHA.minute, seconds=HORA_INI_MANHA.second), data_final)
        #print('f2', intervalo_ultimo_dia)

        intervalo += intervalo_primeiro_dia
        intervalo += intervalo_ultimo_dia
        #print('intervalo', intervalo)
        #print(dias)
        #print(timedelta(seconds=dias*8.5*60*60))
        intervalo += timedelta(seconds=dias*8.5*60*60)

    return intervalo
