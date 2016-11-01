# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


import re
from datetime import date, time, datetime
from .nome import *
from ..valor import numero_por_extenso, numero_por_extenso_ordinal, numero_por_extenso_unidade, romano
from .parse_datetime import parse_datetime
from .fuso_horario import agora, hoje


def dia_por_extenso(data=hoje()):
    data = parse_datetime(data)
    if data.day == 1:
        return numero_por_extenso_ordinal(1)
    else:
        return numero_por_extenso(data.day)


def dia_da_semana_por_extenso(data=hoje()):
    data = parse_datetime(data)
    return DIA_DA_SEMANA[data.weekday()]


def dia_da_semana_por_extenso_abreviado(data):
    data = parse_datetime(data)
    return DIA_DA_SEMANA_ABREVIADO[data.weekday()]


def mes_por_extenso(data=hoje()):
    data = parse_datetime(data)
    return MES[data.month]


def mes_por_extenso_abreviado(data=hoje()):
    data = parse_datetime(data)
    return MES_ABREVIADO[data.month]


def mes_romano(data=hoje()):
    data = parse_datetime(data)
    return romano(data.month)


def ano_por_extenso(data=hoje()):
    data = parse_datetime(data)
    return numero_por_extenso(data.year)


def ano_romano(data=hoje()):
    data = parse_datetime(data)
    return romano(data.year)


def data_por_extenso(data=hoje(), numeros_por_extenso=False, legales=False):
    data = parse_datetime(data)

    if numeros_por_extenso:
        texto_data = ''
        if legales:
            if data.day == 1:
                texto_data += 'no '
            else:
                texto_data += 'aos '
        
        texto_data += dia_por_extenso(data)
        
        if legales:
            if data.day == 1:
                texto_data += ' dia'
            else:
                texto_data += ' dias'
                
            texto_data += ' do mês de ' + mes_por_extenso(data)
            texto_data += ' do ano de ' + numero_por_extenso(data.year)
                
        else:
            texto_data += ' de ' + mes_por_extenso(data)
            texto_data += ' de ' + numero_por_extenso(data.year)
    else:
        texto_data = unicode(data.day)

        if data.day == 1:
            texto_data += 'º'

        texto_data += ' de ' + mes_por_extenso(data)
        texto_data += ' de ' + unicode(data.year)

    return texto_data


def seculo(data=hoje()):
    data = parse_datetime(data)
    return (data.year // 100) + 1


def seculo_por_extenso(data=hoje()):
    data = parse_datetime(data)
    return numero_por_extenso(seculo(data))


def seculo_romano(data=hoje()):
    data = parse_datetime(data)
    return romano(seculo(data))


def milenio(data=hoje()):
    data = parse_datetime(data)
    return (data.year // 1000) + 1


def milenio_por_extenso(data=hoje()):
    data = parse_datetime(data)
    return numero_por_extenso_ordinal(milenio(data))


def milenio_romano(data=hoje()):
    data = parse_datetime(data)
    return romano(milenio(data))


def _hora_por_extenso(hora, unidade=True):
    if unidade:
        return numero_por_extenso_unidade(hora, genero_unidade_masculino=False, unidade=('hora', 'horas'))
    else:
        return numero_por_extenso_unidade(hora, genero_unidade_masculino=False, unidade=('', ''))


def _minuto_por_extenso(minuto, unidade=True):
    if unidade:
        return numero_por_extenso_unidade(minuto, unidade=('minuto', 'minutos'))
    else:
        return numero_por_extenso(minuto)


def _segundo_por_extenso(segundo, unidade=True):
    if unidade:
        return numero_por_extenso_unidade(segundo, unidade=('segundo', 'segundos'))
    else:
        return numero_por_extenso_unidade(segundo)


def hora_por_extenso(tempo=agora(), unidade=True, segundos=False, preposicao=False):
    tempo = parse_datetime(agora)
    texto_hora = _hora_por_extenso(tempo.hour, unidade)

    if tempo.minute or segundos:
        if not segundos:
            texto_hora += ' e ' + _minuto_por_extenso(tempo.minute, unidade)

        else:
            texto_hora += ', ' + _minuto_por_extenso(tempo.minute, unidade)
            texto_hora += ' e ' + _segundo_por_extenso(tempo.second, unidade)

    if preposicao:
        if tempo.hour == 1:
            texto_hora = 'a ' + texto_hora
        else:
            texto_hora = 'às ' + texto_hora

    return texto_hora


def hora_por_extenso_aproximada(tempo=agora(), unidade=False, periodo=True):
    tempo = parse_datetime(agora)
    hora = tempo.hour
    minuto = tempo.minute

    if (hora == 0 or hora == 24) and minuto <= 2:
        return MEIA_NOITE

    elif hora == 23 and minuto >= 58:
        return MEIA_NOITE

    elif hora == 12 and minuto <= 2:
        return MEIO_DIA

    elif hora == 11 and minuto >= 58:
        return MEIO_DIA

    if hora == 0 or hora == 24:
        if minuto <= 32:
            texto_hora = MEIA_NOITE
            texto_periodo = ''

        else:
            texto_hora = _hora_por_extenso(1, unidade)
            hora = 1
            texto_periodo = MADRUGADA

    elif hora == 23 and minuto > 32:
        texto_hora = MEIA_NOITE
        texto_periodo = ''

    elif hora == 12:
        if minuto <= 32:
            texto_hora = MEIO_DIA
            texto_periodo = ''

        else:
            if periodo:
                hora = 1
            else:
                hora = 13

            texto_hora = _hora_por_extenso(hora, unidade)
            texto_periodo = TARDE

    elif hora == 11 and minuto > 32:
        texto_hora = MEIO_DIA
        texto_periodo = ''

    else:
        if minuto > 32:
            hora += 1

        if hora in [1, 2, 3, 4, 5]:
            texto_periodo = MADRUGADA

        elif hora in [6, 7, 8, 9, 10, 11]:
            texto_periodo = MANHA

        elif hora in [13, 14, 15, 16, 17, 18]:
            texto_periodo = TARDE

        else:
            texto_periodo = NOITE

        if periodo and hora > 12:
            hora -= 12

        texto_hora = _hora_por_extenso(hora, unidade)

    if minuto <= 2:
        texto_minuto = '%s'

    elif minuto >= 28 and minuto <= 32:
        texto_minuto = '%s e meia'

    elif minuto < 30:
        if minuto % 5 >= 3:
            minuto = minuto - (minuto % 5) + 5

        elif minuto % 5 > 0:
            minuto = minuto - (minuto % 5)

        if minuto == 0:
            texto_minuto = '%s'
        else:
            texto_minuto = '%s e ' + _minuto_por_extenso(minuto, unidade)

    else:

        minuto = 60 - minuto

        if minuto % 5 >= 3:
            minuto = minuto - (minuto % 5) + 5

        elif minuto % 5 > 0:
            minuto = minuto - (minuto % 5)

        if minuto == 0:
            texto_minuto = '%s'

        elif hora == 1 or texto_hora == MEIA_NOITE:
            texto_minuto = _minuto_por_extenso(minuto, unidade) + ' para a %s'

        elif texto_hora == MEIO_DIA:
            texto_minuto = _minuto_por_extenso(minuto, unidade) + ' para o %s'

        else:
            texto_minuto = _minuto_por_extenso(minuto, unidade) + ' para as %s'

    texto = texto_minuto % texto_hora

    if periodo and texto_periodo:
        texto += ' ' + texto_periodo

    return texto

def formata_data(data=hoje(), formato='%d/%m/%Y'):
    data = parse_datetime(data)

    if data is None:
        return ''

    return data.strftime(formato.encode('utf-8')).decode('utf-8')