# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)

from dateutil.parser import parserinfo


class ParserInfoBrasil(parserinfo):
    HMS = [
        ('h', 'hora', 'horas'),
        ('m', 'minuto', 'minutos'),
        ('s', 'segundo', 'segundos')
    ]

    JUMP = [
        ' ',
        '.',
        ',',
        ';',
        '-',
        '/',
        "'",
        'em',
        'no',
        'na',
        'de',
        'e',
        'º',
        'ª',
        '°',
        'às',
        'as',
    ]

    MONTHS = [
        ('jan', 'janeiro', 'Jan', 'Janeiro'),
        ('fev', 'fevereiro', 'Fev', 'Fevereiro'),
        ('mar', 'março', 'Mar', 'Março', 'marco', 'Marco'),
        ('abr', 'abril', 'Abr', 'Abril'),
        ('mai', 'maio', 'Mai', 'Maio'),
        ('jun', 'junho', 'Jun', 'Junho'),
        ('jul', 'julho', 'Jul', 'Julho'),
        ('ago', 'agosto', 'Ago', 'Agosto'),
        ('set', 'setembro', 'Set', 'Setembro'),
        ('out', 'outubro', 'Out', 'Outubro'),
        ('nov', 'novembro', 'Nov', 'Novembro'),
        ('dez', 'dezembro', 'Dez', 'Dezembro')
    ]

    PERTAIN = [
        'de'
    ]

    WEEKDAYS = [
        ('seg', 'segunda-feira', 'segunda', 'Seg', 'Segunda-Feira', 'Segunda', 'Segunda-feira'),
        ('ter', 'terça-feira', 'terça', 'Ter', 'Terça-Feira', 'Terça', 'Terça-feira', 'terca-feira', 'Terca-Feira', 'Terca-feira'),
        ('qua', 'quarta-feira', 'quarta', 'Qua', 'Quarta-Feira', 'Quarta', 'Quarta-feira'),
        ('qui', 'quinta-feira', 'quinta', 'Qui', 'Quinta-Feira', 'Quinta', 'Quinta-feira'),
        ('sex', 'sexta-feira', 'sexta', 'Sex', 'Sexta-Feira', 'Sexta', 'Sexta-feira'),
        ('sáb', 'sábado', 'Sáb', 'Sábado', 'sab', 'sabado', 'Sab', 'Sabado'),
        ('dom', 'domingo', 'Dom', 'Domingo')
    ]

    dayfirst = True
    yearfirst = False

    def __init__(self, dayfirst=True, yearfirst=False):
        super(ParserInfoBrasil, self).__init__(dayfirst, yearfirst)

