# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)
import os
import sys
from ..base import tira_acentos
from .pais import PAIS_BRASIL
from .estado import ESTADO_SIGLA, Estado


CURDIR = os.path.dirname(os.path.abspath(__file__))


class Municipio(object):
    def __init__(self, nome='', estado='', codigo_ibge='', codigo_siafi='', codigo_anp='',
                 pais=None, ddd='', cep=''):
        self.nome = nome

        if estado:
            self.estado = ESTADO_SIGLA[estado]
        else:
            self.estado = Estado()

        self.codigo_ibge = codigo_ibge
        self.codigo_siafi = codigo_siafi
        self.codigo_anp = codigo_anp
        self.pais = pais
        self.ddd = ddd
        self.cep = cep

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        return self.nome + ' - ' + self.estado.sigla

    def __repr__(self):
        return str(self)


def _monta_dicionario_ibge():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'municipio.txt'), 'r')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.decode('utf-8').replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        m = Municipio(nome=campos[0], estado=campos[1], codigo_ibge=campos[2], codigo_siafi=campos[3], codigo_anp=campos[4], ddd=campos[5], cep=campos[6])

        if m.estado != 'EX':
            m.pais = PAIS_BRASIL

        dicionario[m.codigo_ibge] = m

    return dicionario


def _monta_dicionario_siafi():
    dicionario = {}

    for k, v in MUNICIPIO_IBGE.items():
        if v.codigo_siafi:
            dicionario[v.codigo_siafi] = v

    return dicionario


def _monta_dicionario_estado_nome():
    dicionario = {}

    for k, v in MUNICIPIO_IBGE.items():
        if not v.estado.sigla in dicionario:
            dicionario[v.estado.sigla] = {}

        dicionario[v.estado.sigla][tira_acentos(v.nome).upper()] = v

    return dicionario


def _monta_dicionario_nome():
    dicionario = {}

    for k, v in MUNICIPIO_IBGE.items():
        if not tira_acentos(v.nome).upper() in dicionario:
            dicionario[tira_acentos(v.nome).upper()] = []

        dicionario[tira_acentos(v.nome).upper()].append(v)

    return dicionario


if not hasattr(sys.modules[__name__], 'MUNICIPIO_IBGE'):
    MUNICIPIO_IBGE = _monta_dicionario_ibge()


if not hasattr(sys.modules[__name__], 'MUNICIPIO_SIAFI'):
    MUNICIPIO_SIAFI = _monta_dicionario_siafi()


if not hasattr(sys.modules[__name__], 'MUNICIPIO_ESTADO_NOME'):
    MUNICIPIO_ESTADO_NOME = _monta_dicionario_estado_nome()


if not hasattr(sys.modules[__name__], 'MUNICIPIO_NOME'):
    MUNICIPIO_NOME = _monta_dicionario_nome()
