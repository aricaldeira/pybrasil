# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


import re
from .pais import (Pais, PAIS_BACEN, PAIS_NOME, PAIS_BRASIL, PAIS_ISO_3166_2, PAIS_ISO_3166_3)
from .estado import (Estado, ESTADO_IBGE, ESTADO_SIGLA)
from .municipio import (Municipio, MUNICIPIO_ESTADO_NOME, MUNICIPIO_IBGE, MUNICIPIO_SIAFI)
from ..base import tira_acentos


class Local(object):
    def __init__(self, **kwargs):
        self._pais = PAIS_BRASIL
        self._estado = Estado()
        self._municipio = Municipio()
        self.pais = kwargs.get('pais', None)
        self.estado = kwargs.get('estado', None)
        self.municipio = kwargs.get('municipio', None)

    @property
    def pais(self):
        return self._pais

    @pais.setter
    def pais(self, valor):
        if isinstance(valor, Pais):
            self._pais = valor

        elif isinstance(valor, (str, unicode)):
            if valor in PAIS_NOME:
                self.pais = PAIS_NOME[valor]
            elif valor in PAIS_BACEN:
                self.pais = PAIS_BACEN[valor]
            elif valor in PAIS_ISO_3166_2:
                self.pais = PAIS_ISO_3166_2[valor]
            elif valor in PAIS_ISO_3166_3:
                self.pais = PAIS_ISO_3166_3[valor]

        else:
            self._pais = PAIS_BRASIL

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if isinstance(valor, Estado):
            self._estado = valor

        elif isinstance(valor, (str, unicode)):
            if valor in ESTADO_SIGLA:
                self.estado = ESTADO_SIGLA[valor]
            elif valor in ESTADO_IBGE:
                self.municipio = ESTADO_IBGE[valor]

        else:
            self._estado = Estado()

    @property
    def municipio(self):
        return self._municipio

    @municipio.setter
    def municipio(self, valor):
        if isinstance(valor, Municipio):
            self._municipio = valor
            self.estado = self._municipio.estado
            self.pais = self._municipio.pais

        elif isinstance(valor, (list, tuple)) and len(valor) == 2:
            estado = unicode(valor[0]).upper()
            municipio = unicode(valor[1]).upper()
            municipio = tira_acentos(municipio)
            if estado in MUNICIPIO_ESTADO_NOME:
                if municipio in MUNICIPIO_ESTADO_NOME[estado]:
                    self.municipio = MUNICIPIO_ESTADO_NOME[estado][municipio]

        elif isinstance(valor, (str, unicode)):
            if valor in MUNICIPIO_IBGE:
                self.municipio = MUNICIPIO_IBGE[valor]
            elif valor in MUNICIPIO_SIAFI:
                self.municipio = MUNICIPIO_SIAFI[valor]
            elif isinstance(self.estado, Estado) and self.estado.sigla != '':
                estado = self.estado.sigla
                municipio = unicode(valor).upper()
                municipio = tira_acentos(municipio)
                self.municipio = (estado, municipio)

        else:
            self._municipio = Municipio()
