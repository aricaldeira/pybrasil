# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


TIPO_FERIADO = {
    'F': 'Feriado',
    'B': 'Feriado bancário',
    'C': 'Data comemorativa',
}


ABRANGENCIA_FERIADO = {
    'N': 'Nacional',
    'E': 'Estadual',
    'M': 'Municipal',
}


QUANDO_FERIADO = {
    'A': 'Data específica (dia, mês, ano)',
    'M': 'Data específica (dia, mês)',
    'D': 'Data específica (dia)',
    'S': 'Data específica (dia da semana, mês)',
    'P': 'Páscoa',
}


AJUSTE_FERIADO = {
    'AC': 'terça, quarta e quinta muda para sexta (estado do Acre)',
    'SC': 'dia útil muda para domingo (estado do Santa Catarina)',
}
