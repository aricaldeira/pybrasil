# -*- coding: utf-8 -*-
#
# PyBrasil - Functions useful for most Brazil's ERPs
#
# Copyright (C) 2016-
# Copyright (C) Aristides Caldeira <aristides.caldeira at tauga.com.br>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation, either version 2.1 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# PyBrasil - Funções de validação necessárias a ERPs no Brasil
#
# Copyright (C) 2016-
# Copyright (C) Aristides Caldeira <aristides.caldeira arroba tauga.com.br>
#
# Este programa é um software livre: você pode redistribuir e/ou modificar
# este programa sob os termos da licença GNU Library General Public License,
# publicada pela Free Software Foundation, em sua versão 2.1 ou, de acordo
# com sua opção, qualquer versão posterior.
#
# Este programa é distribuido na esperança de que venha a ser útil,
# porém SEM QUAISQUER GARANTIAS, nem mesmo a garantia implícita de
# COMERCIABILIDADE ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. Veja a
# GNU Library General Public License para mais detalhes.
#
# Você deve ter recebido uma cópia da GNU Library General Public License
# juntamente com este programa. Caso esse não seja o caso, acesse:
# <http://www.gnu.org/licenses/>
#

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
