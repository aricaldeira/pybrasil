# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from ..base import modulo11
from .cnpj_cpf import eh_tudo_igual
from .inscricao_estadual import LIMPA


def valida_cei(cei):
    u'''Verifica que o PIS seja válido
    de acordo com os dígitos verificadores
    '''
    cei = LIMPA.sub('', cei)

    if len(cei) < 11:
        cei = cei.zfill(11)

    if len(cei) != 11:
        return False

    if not cei.isdigit():
        return False

    if eh_tudo_igual(cei):
        return False

    digito = cei[-1]

    digito = cei[-1]

    d1 = modulo11(cei[:-1], pesos=range(2, 10))

    print(d1, 'digito')

    return digito == unicode(d1)


def formata_cei(cei):
    if not valida_cei(cei):
        return cei

    #formato CEI
    'XX.XXX.XXXXX/XX'

    cei = LIMPA.sub('', cei)
    cei = str(int(cei))
    digito = cei[-1]
    numero = cei[:-1][::-1]
    numero = numero[0:2] + '.' + numero[2:7] + '.' + numero[7:]
    numero = numero[::-1]


    return numero + '-' + digito
