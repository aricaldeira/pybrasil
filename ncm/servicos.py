# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)
import os
import sys
from decimal import Decimal as D


CURDIR = os.path.dirname(os.path.abspath(__file__))


class Servicos(object):
    def __init__(self, codigo='', descricao='', al_ibpt_nacional=0, al_ibpt_internacional=0):
        self.codigo = codigo
        self.descricao = descricao
        self.al_ibpt_nacional = al_ibpt_nacional
        self.al_ibpt_internacional = al_ibpt_internacional

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        return self.codigo_formatado + ' - ' + self.descricao

    def __repr__(self):
        return str(self)

    @property
    def codigo_formatado(self):
        texto = self.codigo.zfill(4)
        texto = texto[:2] + '.' + texto[2:]
        return texto


def _monta_dicionario():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'servicos.txt'), 'r')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.decode('utf-8').replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        e = Servicos(codigo=campos[0], descricao=campos[1], al_ibpt_nacional=D(campos[2] or '0'), al_ibpt_internacional=D(campos[3] or 0))

        dicionario[e.codigo] = e

    return dicionario


if not hasattr(sys.modules[__name__], 'SERVICOS_CODIGO'):
    SERVICOS_CODIGO = _monta_dicionario()
