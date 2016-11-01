# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals, absolute_import
import sys
import os
from ..base import tira_acentos

CURDIR = os.path.dirname(os.path.abspath(__file__))


class Pais(object):
    def __init__(self, nome='', codigo_bacen='', codigo_anp='',
                 codigo_siscomex='', nome_frances='', nome_ingles='', iso_3166_2='',
                 iso_3166_3='', iso_3166_numerico=''):
        self.nome = nome
        self.codigo_bacen = codigo_bacen
        self.codigo_anp = codigo_anp
        self.codigo_siscomex = codigo_siscomex
        self.nome_frances = nome_frances
        self.nome_ingles = nome_ingles
        self.iso_3166_2 = iso_3166_2
        self.iso_3166_3 = iso_3166_3
        self.iso_3166_numerico = iso_3166_numerico

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        return self.nome

    def __repr__(self):
        return str(self)

    @property
    def codigo_ibge(self):
        return self.codigo_bacen


def _monta_dicionario_bacen():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'pais.txt'), 'r')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.decode('utf-8').replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        p = Pais(nome=campos[0], codigo_bacen=campos[1], codigo_anp=campos[2], codigo_siscomex=campos[3], nome_frances=campos[4], nome_ingles=campos[5], iso_3166_2=campos[6], iso_3166_3=campos[7], iso_3166_numerico=campos[8])
        dicionario[p.codigo_bacen] = p

    return dicionario


def _monta_dicionario_nome():
    dicionario = {}

    for k, v in PAIS_BACEN.items():
        dicionario[tira_acentos(v.nome).upper()] = v

    return dicionario


def _monta_dicionario_iso_3166_2():
    dicionario = {}

    for k, v in PAIS_BACEN.items():
        dicionario[v.iso_3166_2] = v

    return dicionario


def _monta_dicionario_iso_3166_3():
    dicionario = {}

    for k, v in PAIS_BACEN.items():
        dicionario[v.iso_3166_3] = v

    return dicionario


if not hasattr(sys.modules[__name__], 'PAIS_BACEN'):
    PAIS_BACEN = _monta_dicionario_bacen()


if not hasattr(sys.modules[__name__], 'PAIS_BRASIL'):
    PAIS_BRASIL = PAIS_BACEN['1058']


if not hasattr(sys.modules[__name__], 'PAIS_NOME'):
    PAIS_NOME = _monta_dicionario_nome()


if not hasattr(sys.modules[__name__], 'PAIS_ISO_3166_2'):
    PAIS_ISO_3166_2 = _monta_dicionario_iso_3166_2()


if not hasattr(sys.modules[__name__], 'PAIS_ISO_3166_3'):
    PAIS_ISO_3166_3 = _monta_dicionario_iso_3166_3()
