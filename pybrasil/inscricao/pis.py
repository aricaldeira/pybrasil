# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from ..base import modulo11
from .cnpj_cpf import eh_tudo_igual
from .inscricao_estadual import LIMPA


def valida_pis(pis):
    u'''Verifica que o PIS seja válido
    de acordo com os dígitos verificadores
    '''
    pis = LIMPA.sub('', pis)

    if len(pis) < 11:
        pis = pis.zfill(11)

    if len(pis) != 11:
        return False

    if not pis.isdigit():
        return False

    if eh_tudo_igual(pis):
        return False

    digito = pis[-1]

    digito = pis[-1]

    d1 = modulo11(pis[:-1], pesos=range(2, 10))

    print(d1, 'digito')

    return digito == unicode(d1)


def formata_pis(pis):
    if not valida_pis(pis):
        return pis

    pis = LIMPA.sub('', pis)
    pis = str(int(pis))
    digito = pis[-1]
    numero = pis[:-1][::-1]
    numero = numero[0:2] + '.' + numero[2:7] + '.' + numero[7:]
    numero = numero[::-1]


    return numero + '-' + digito
