# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


MES = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'março',
    4: 'abril',
    5: 'maio',
    6: 'junho',
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro',
}

MES_ABREVIADO = {
    1: 'jan',
    2: 'fev',
    3: 'mar',
    4: 'abr',
    5: 'mai',
    6: 'jun',
    7: 'jul',
    8: 'ago',
    9: 'set',
    10: 'out',
    11: 'nov',
    12: 'dez',
}

DIA_DA_SEMANA = {
    0: 'segunda-feira',
    1: 'terça-feira',
    2: 'quarta-feira',
    3: 'quinta-feira',
    4: 'sexta-feira',
    5: 'sábado',
    6: 'domingo',
}

DIA_DA_SEMANA_ABREVIADO = {
    0: 'seg',
    1: 'ter',
    2: 'qua',
    3: 'qui',
    4: 'sex',
    5: 'sáb',
    6: 'dom',
}

MEIO_DIA = 'meio-dia'
MEIA_NOITE = 'meia-noite'
MADRUGADA = 'da madrugada'
MANHA = 'da manhã'
TARDE = 'da tarde'
NOITE = 'da noite'

PERIODO = {
    MEIA_NOITE: [0, 24],
    MADRUGADA: [1, 2, 3, 4, 5],
    MANHA: [6, 7, 8, 9, 10, 11],
    MEIO_DIA: [12],
    TARDE: [13, 14, 15, 16, 17, 18],
    NOITE: [19, 20, 21, 22, 23],
}
