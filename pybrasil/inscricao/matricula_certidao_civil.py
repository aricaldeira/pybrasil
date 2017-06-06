# -*- coding: utf-8 -*-
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


from ..base import modulo11, modulo10
from .cnpj_cpf import eh_tudo_igual
import re


LIMPA = re.compile(r'[^0-9]')

TIPO_CERTIDAO_CIVIL = {
    '1': 'Livro A (certidão de nascimento)',
    '2': 'Livro B (certidão de casamento)',
    '3': 'Livro B auxiliar (casamento religioso com efeito civil)',
    '4': 'Livro C (certidão de óbito)',
    '5': 'Livro C auxiliar (natimorto)',
    '6': 'Livro D (registro de proclamas)',
    '7': 'Livro E (demais atos relativos ao registro civil ou livro E único)',
    '8': 'Livro E (desdobrado para registro específico das Emancipações)',
    '9': 'Livro E (Desdobrado para registro específico das Interdições)',
}

TIPO_CERTIDAO_CIVIL_NASCIMENTO = '1'
TIPO_CERTIDAO_CIVIL_CASAMENTO = '2'
TIPO_CERTIDAO_CIVIL_CASAMENTO_RELIGIOSO = '3'


#
# O código da matrícula da certidão civil tem o seguinte formato:
#
# SSSSSS aa 55 AAAA T LLLLL FFF NNNNNNN DD
#
# SSSSSS: 6 dígitos indicando o cartório
# aa: 2 dígitos indicando o acervo, pode ser: 01 - acervo próprio, 02 - acervo incorporado
# AAAA: 4 dígitos para o ano
# T: tipo da certidão
# LLLLL: 5 dígitos para o número do livro
# FFF: 3 dígitos para a folha
# NNNNNNN: 7 dígitos para o número do termo propriamente dito
# DD: 2 dígitos verificadores
#


def valida_certidao_civil(certidao, tipo_valido=''):
    u'''Verifica que a certidão seja válida
    de acordo com os dígitos verificadores
    '''
    certidao = LIMPA.sub('', certidao)

    if len(certidao) != 32:
        return False

    if not certidao.isdigit():
        return False

    if eh_tudo_igual(certidao):
        return False

    #
    # Verifica os dígitos referentes ao acervo
    #
    digito_acervo = certidao[6:8]
    if digito_acervo not in ['01', '02']:
        return False

    digito_civil = certidao[8:10]
    if digito_civil != '55':
        return False

    #
    # Verifica o tipo da certidão
    #
    tipo_certidao = certidao[14]
    if tipo_certidao not in TIPO_CERTIDAO_CIVIL:
        return False

    #
    # Precisa validar um tipo específico?
    #
    if tipo_valido and tipo_certidao != tipo_valido:
        return False

    pesos = range(9, -1, -1) + range(10, -1, -1) + range(10, 0, -1)
    d1 = modulo11(certidao[:30], pesos=pesos, resto=True)
    d2 = modulo11(certidao[:31], pesos=pesos, resto=True)

    digito = certidao[-2:]
    digitocalc = d1 + d2

    return digito == digitocalc


def separa_certidao_civil(certidao, tipo_valido=''):
    if not valida_certidao_civil(certidao, tipo_valido):
        return certidao

    certidao = LIMPA.sub('', certidao)
    digitos = certidao[-2:]
    cartorio = certidao[:6]
    acervo = certidao[6:8]
    civil = certidao[8:10]
    ano = certidao[10:14]
    tipo = certidao[14]
    livro = certidao[15:20]
    folha = certidao[20:23]
    numero = certidao[23:30]

    retorno = {
        'cartorio': cartorio,
        'acervo': acervo,
        'civil': civil,
        'ano': ano,
        'tipo': tipo,
        'livro': livro,
        'folha': folha,
        'numero': numero,
        'digitos': digitos,
    }

    return retorno


def formata_certidao_civil(certidao, tipo_valido=''):
    certidao = LIMPA.sub('', certidao)
    if not valida_certidao_civil(certidao, tipo_valido):
        return certidao

    campos_separados = separa_certidao_civil(certidao, tipo_valido)

    #formato = '{cartorio} {acervo} {civil} {ano} {tipo} {livro} {folha} {numero} {digitos}'
    formato = '{cartorio}{acervo}{civil}{ano}{tipo}{livro}{folha}{numero}{digitos}'

    return formato.format(**campos_separados)
