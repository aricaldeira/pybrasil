# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


import re
from datetime import date, time, datetime
from .nome import *
from ..valor import numero_por_extenso, numero_por_extenso_ordinal, numero_por_extenso_unidade

MASCARA = re.compile(r'(?<!\\)([aAbBcdDeEfFgGhHiIjlLmMnNoOPrsStTUuwWyYzZ])')
MASCARA_ESCAPADA = re.compile(r'\\(.)')


class FormataDataHora(object):
    def __init__(self, data=None):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, valor):
        if isinstance(valor, [date, datetime, time]):
            self._data = valor
        elif valor is None:
            self._data = datetime.now()

    def dia_por_extenso(self):
        if self.data.day == 1:
            return numero_por_extenso_ordinal(1)
        else:
            return numero_por_extenso(self.data.day)

    def dia_da_semana_por_extenso(self):
        return DIA_DA_SEMANA[self.data.weekday]

    def dia_da_semana_por_extenso_abreviado(self):
        return DIA_DA_SEMANA_ABREVIADO[self.data.weekday]

    def mes_por_extenso(self):
        return MES[self.data.month]

    def mes_por_extenso_abreviado(self):
        return MES_ABREVIADO[self.data.month]

    def seculo(self):
        return int(str(self.data.year)[0:2]) + 1
