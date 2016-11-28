# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from ..base import modulo11


def limpa_formatacao(cnpj_cpf):
    u'''Limpa os caracteres de formatação
    '''
    return cnpj_cpf.replace('.', '').replace('-', '').replace('/', '').replace(' ', '').replace('(', '').replace(')', '')


def eh_tudo_igual(valor):
    u'''Verifica que todos os algarismos no CPF ou CNPJ não sejam iguais
    '''
    tudo_igual = True

    for i in range(1, len(valor)):
        tudo_igual = tudo_igual and (valor[i - 1] == valor[i])

        if not tudo_igual:
            break

    return tudo_igual


def valida_cpf(cpf):
    u'''Verifica que o CPF seja válido de acordo com os dígitos verificadores
    '''
    cpf = limpa_formatacao(cpf)

    if len(cpf) != 11:
        return False

    if not cpf.isdigit():
        return False

    if eh_tudo_igual(cpf):
        return False

    digito = cpf[-2:]

    d1 = modulo11(cpf[:9], pesos=range(2, 11))
    d2 = modulo11(cpf[:10], pesos=range(2, 12))
    digitocalc = d1 + d2

    return digito == digitocalc


def valida_cnpj(cnpj):
    u'''Verifica que o CNPJ seja válido de acordo com os dígitos verificadores
    '''
    cnpj = limpa_formatacao(cnpj)

    if len(cnpj) != 14:
        return False

    if not cnpj.isdigit():
        return False

    if eh_tudo_igual(cnpj):
        return False

    digito = cnpj[-2:]

    d1 = modulo11(cnpj[:12])
    d2 = modulo11(cnpj[:13])
    digitocalc = d1 + d2

    return digito == digitocalc


def formata_cpf(cpf):
    if not valida_cpf(cpf):
        return cpf

    cpf = limpa_formatacao(cpf)

    return cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:11]


def formata_cnpj(cnpj):
    if not valida_cnpj(cnpj):
        return cnpj

    cnpj = limpa_formatacao(cnpj)

    return cnpj[:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:14]
