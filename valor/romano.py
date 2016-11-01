# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals


ROMANOS = (
    (1000000, 'M̅'),
    (100000, 'C̅'),
    (10000, 'M̅'),
    (5000, 'V̅'),
    (4000, 'I̅V̅'),
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
)

ROMANOS_UNICODE = (
    (1000000, 'Ⅿ̅'),
    (100000, 'Ⅽ̅'),
    (10000, 'Ⅿ̅'),
    (5000, 'Ⅴ̅̅'),
    (4000, 'Ⅰ̅̅Ⅴ̅'),
    (1000, 'Ⅿ'),
    (900, 'ⅭⅯ'),
    (500, 'Ⅾ'),
    (400, 'ⅭⅮ'),
    (100, 'Ⅽ'),
    (90, 'ⅩⅭ'),
    (50, 'Ⅼ'),
    (40, 'ⅩⅬ'),
    (10, 'Ⅹ'),
    (9, 'ⅠⅩ'),
    (5, 'Ⅴ'),
    (4, 'ⅠⅤ'),
    (1, 'Ⅰ'),
)

ROMANOS_MES_HORA_UNICODE = {
    1: 'Ⅰ',
    2: 'Ⅱ',
    3: 'Ⅲ',
    4: 'Ⅳ',
    5: 'Ⅴ',
    6: 'Ⅵ',
    7: 'Ⅶ',
    8: 'Ⅷ',
    9: 'Ⅸ',
    10: 'Ⅹ',
    11: 'Ⅺ',
    12: 'Ⅻ',
}


def romano(numero):
    numero_romano = ''

    for valor, letra in ROMANOS:
        quantidade = numero // valor
        numero_romano += letra * quantidade
        numero -= valor * quantidade

    return numero_romano


def romano_mes_hora(mes_hora):
    if mes_hora > 12:
        mes_hora = mes_hora % 12

    if mes_hora not in ROMANOS_MES_HORA_UNICODE:
        return ''

    return ROMANOS_MES_HORA_UNICODE[mes_hora]