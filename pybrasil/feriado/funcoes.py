# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from dateutil.relativedelta import relativedelta
from datetime import date
from ..data import hoje, parse_datetime, data_hora_horario_brasilia
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

    dia_antes_eh_util = dia_antes.weekday() <= 4 and \
        data_eh_feriado(dia_antes, estado, municipio) == []
    dia_depois_eh_util = dia_depois.weekday() <= 4 and \
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

    dia_antes_eh_util = dia_antes.weekday() <= 4 and \
        data_eh_feriado_bancario(dia_antes, estado, municipio) == []
    dia_depois_eh_util = dia_depois.weekday() <= 4 and \
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
        if data.weekday() != 6:
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
