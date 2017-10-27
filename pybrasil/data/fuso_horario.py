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


from pytz import (datetime, timezone, tzinfo, UTC)
from datetime import datetime as datetime_sem_fuso, date, time
from time import strftime
from dateutil.relativedelta import relativedelta
from .parse_datetime import parse_datetime
from ..valor.decimal import Decimal as D


HB = timezone('America/Sao_Paulo')


def fuso_horario_sistema():
    diferenca = int(strftime('%z')) // 100

    if diferenca < 0:
        return timezone('Etc/GMT+' + str(diferenca * -1))

    if diferenca > 0:
        return timezone('Etc/GMT-' + str(diferenca))

    return UTC


def data_hora_horario_brasilia(data):
    if not isinstance(data, (datetime.datetime, datetime_sem_fuso, date, time)):
        return None

    if isinstance(data, datetime.datetime):
        if not data.tzinfo:
            data = fuso_horario_sistema().localize(data)

    elif isinstance(data, date):
        #
        # Ajusta date para datetime ao meio-dia,
        # pra não voltar a data pro dia anterior
        # Define depois a hora para meia-noite
        #
        data = datetime_sem_fuso(data.year, data.month, data.day, 12, 0, 0, 0)
        data = data_hora_horario_brasilia(data)
        data = data + relativedelta(hour=0, minute=0, second=0, microsecond=0)
        return data

    elif isinstance(data, time):
        #
        # Hora sem data, assume a data de hoje
        #
        hora = data
        data = datetime.datetime.now()
        data = data_hora_horario_brasilia(data)
        data = data + relativedelta(hour=hora.hour, minute=hora.minute, second=hora.second, microsecond=hora.microsecond)
        return data

    elif isinstance(data, datetime_sem_fuso):
        data = fuso_horario_sistema().localize(data)

    data = UTC.normalize(data)
    data = HB.normalize(data)
    return data


def agora():
    agora = datetime.datetime.now()
    return data_hora_horario_brasilia(agora)

def hoje():
    return agora().date()

def amanha(quando=agora()):
    quando = parse_datetime(quando)
    amanha = quando + relativedelta(days=+1)
    return data_hora_horario_brasilia(amanha).date()

def ontem(quando=agora()):
    quando = parse_datetime(quando)
    ontem = quando + relativedelta(days=-1)
    return data_hora_horario_brasilia(ontem).date()

def mes_que_vem(quando=agora()):
    quando = parse_datetime(quando)
    amanha = quando + relativedelta(months=+1)
    return data_hora_horario_brasilia(amanha).date()

def mes_passado(quando=agora()):
    quando = parse_datetime(quando)
    ontem = quando + relativedelta(months=-1)
    return data_hora_horario_brasilia(ontem).date()

def ano_que_vem(quando=agora()):
    quando = parse_datetime(quando)
    amanha = quando + relativedelta(years=+1)
    return data_hora_horario_brasilia(amanha).date()

def ano_passado(quando=agora()):
    quando = parse_datetime(quando)
    ontem = quando + relativedelta(years=-1)
    return data_hora_horario_brasilia(ontem).date()

def semana_que_vem(quando=agora()):
    quando = parse_datetime(quando)
    amanha = quando + relativedelta(weeks=+1)
    return data_hora_horario_brasilia(amanha).date()

def semana_passada(quando=agora()):
    quando = parse_datetime(quando)
    ontem = quando + relativedelta(weeks=-1)
    return data_hora_horario_brasilia(ontem).date()

def primeiro_dia_mes(quando=agora()):
    #print('quando', quando)
    quando = parse_datetime(quando)
    pdm = quando

    if quando:
        pdm = quando + relativedelta(day=1)

    return data_hora_horario_brasilia(pdm).date()

def ultimo_dia_mes(quando=agora()):
    quando = parse_datetime(quando)
    pdm = primeiro_dia_mes(quando)
    udm = pdm + relativedelta(months=+1, days=-1)
    return data_hora_horario_brasilia(udm).date()


def hora_decimal_to_horas_minutos_segundos(valor):
    if valor is None:
        return None

    valor = D(valor)
    horas = D(int(valor))
    minutos = D(int((valor * 60) - (horas * 60)))
    segundos = D(int((valor * 60 * 60) - (horas * 60 * 60) - (minutos * 60)))

    return horas, minutos, segundos


def horario_decimal_to_hora_decimal(valor):
    if valor is None:
        return None

    valor = D(valor)
    horas = D(int(valor))
    minutos = D(int((valor * 100) - (horas * 100)))
    segundos = D(int((valor * 100 * 100) - (horas * 100 * 100) - (minutos * 100)))

    valor = (horas * 60) + minutos + (segundos / 60)
    valor /= 60

    return valor


def horas_minutos_segundos_to_hora_decimal(horas, minutos, segundos):
    return D(horas) + (D(minutos) / 60) + (D(segundos) / 60 / 60)


def horas_minutos_segundos_to_horario_decimal(horas, minutos, segundos):
    return D(horas) + (D(minutos) / 100) + (D(segundos) / 100 / 100)
