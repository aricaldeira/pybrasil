# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


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