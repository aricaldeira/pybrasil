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

import re
from .ddd import DDDS


LIMPA = re.compile(r'[^\+0-9]')

NUMERO_FIXO = re.compile(r'^' + DDDS + r'[23456][0-9]{7}$')
NUMERO_FIXO_SEM_DDD = re.compile(r'^[23456][0-9]{7}$')
NUMERO_CELULAR = re.compile(r'^' + DDDS + r'9[0-9]{8}$')
NUMERO_CELULAR_SEM_DDD = re.compile(r'^9[0-9]{8}$')
NUMERO_INTERNACIONAL = re.compile(r'^\+[0-9]{2,14}')
NUMERO_INTERNACIONAL_BRASIL = re.compile(r'^\+55' + DDDS + r'([23456][0-9]{7}|9[0-9]{8})$')
NUMERO_ESPECIAL_0800 = re.compile(r'^0[3589]00[0-9]{6,7}$')
NUMERO_ESPECIAL_4000 = re.compile(r'^[43][0-9]{7,8}$')

FORMATO_CELULAR_3_2_4 = '3_2_4'
FORMATO_CELULAR_3_3_3 = '3_3_3'
FORMATO_CELULAR_1_4_4 = '1_4_4'
FORMATO_CELULAR_5_4 = '5_4'


def limpa_fone(fone):
    return LIMPA.sub('', fone)


def separa_fone(fone):
    fone = limpa_fone(fone)

    #
    # Telefone internacionais, sem DDI do Brasil
    #
    if fone and fone[0] == '+':
        if fone[0:3] != '+55':
            return '', fone

        fone = fone[3:]

    #
    # Telefones fixos e celulares sem DDD
    #
    if len(fone) <= 9:
        return '', fone

    #
    # Telefones fixos ou celulares com 8 dígitos e DDD = 10 dígitos
    # Celulares com 9 dígitos e DDD = 11 dígitos
    #
    if len(fone) == 10 or len(fone) == 11:
        return fone[0:2], fone[2:]

    #
    # Não dá pra saber o que é DDD e o que é número
    #
    return '', fone


def formata_fone(fone, valida_nono_digito=False, ddd_padrao='', formato_celular=FORMATO_CELULAR_5_4):
    if not valida_fone(fone, valida_nono_digito=valida_nono_digito):
        return fone

    fone = limpa_fone(fone)

    if NUMERO_ESPECIAL_0800.match(fone):
        dde, numero = fone[:4], fone[4:]

        if len(numero) == 6:
            formatado = '%s %s-%s' % (dde, numero[:2], numero[2:])
        else:
            formatado = '%s %s-%s' % (dde, numero[:3], numero[3:])

        return formatado

    if NUMERO_ESPECIAL_4000.match(fone):
        formatado = '%s-%s' % (fone[:4], fone[4:])

        return formatado

    tem_ddi = False
    if fone[0] == '+':
        if fone[0:3] != '+55':
            return fone

        tem_ddi = True
        fone = fone[3:]

    ddd, numero = separa_fone(fone)

    if not ddd and ddd_padrao:
        ddd = ddd_padrao

    if ddd:
        if valida_fone_celular(numero, valida_nono_digito=False):
            if len(numero) == 8:
                numero = '9' + numero

        if len(numero) == 9:
            if formato_celular == FORMATO_CELULAR_3_2_4:
                formatado = '(%s) %s-%s-%s' % (ddd, numero[-9:-6], numero[-6:-4], numero[-4:])
            elif formato_celular == FORMATO_CELULAR_3_3_3:
                formatado = '(%s) %s-%s-%s' % (ddd, numero[-9:-6], numero[-6:-3], numero[-3:])
            elif formato_celular == FORMATO_CELULAR_1_4_4:
                formatado = '(%s) %s-%s-%s' % (ddd, numero[-9], numero[-8:-4], numero[-4:])
            #elif formato_celular == FORMATO_CELULAR_5_4:
            else:
                formatado = '(%s) %s-%s' % (ddd, numero[-9:-4], numero[-4:])
        else:
            formatado = '(%s) %s-%s' % (ddd, numero[0:4], numero[4:])

        if tem_ddi:
            formatado = '+55 ' + formatado

        return formatado

    else:
        if len(numero) == 8:
            return '%s-%s' % (numero[0:4], numero[4:])
        elif len(numero) == 9:
            if formato_celular == FORMATO_CELULAR_3_2_4:
                return '%s-%s-%s' % (numero[-9:-6], numero[-6:-4], numero[-4:])
            elif formato_celular == FORMATO_CELULAR_3_3_3:
                return '%s-%s-%s' % (numero[-9:-6], numero[-6:-3], numero[-3:])
            elif formato_celular == FORMATO_CELULAR_1_4_4:
                return '%s-%s-%s' % (numero[-9], numero[-8:-4], numero[-4:])
            #elif formato_celular == FORMATO_CELULAR_5_4:
            else:
                return '%s-%s' % (numero[-9:-4], numero[-4:])
        else:
            return numero


def valida_fone_internacional(fone):
    fone = limpa_fone(fone)

    if not fone:
        return False

    if not NUMERO_INTERNACIONAL.match(fone):
        return False

    if fone[0:3] == '+55':
        return False

    return True


def valida_fone_fixo(fone):
    fone = limpa_fone(fone)

    if not fone:
        return False

    if NUMERO_INTERNACIONAL.match(fone):
        if fone[0:3] != '+55':
            return True

        fone = fone[3:]

    if not NUMERO_FIXO.match(fone) and not NUMERO_FIXO_SEM_DDD.match(fone):
        return False

    return True


def valida_fone_celular(fone, valida_nono_digito=False):
    fone = limpa_fone(fone)

    if not fone:
        return False

    if NUMERO_INTERNACIONAL.match(fone):
        if fone[0:3] != '+55':
            return True

        fone = fone[3:]

    if not NUMERO_CELULAR.match(fone) and not NUMERO_CELULAR_SEM_DDD.match(fone):
        return False

    ddd, fone = separa_fone(fone)

    if valida_nono_digito:
        if NUMERO_CELULAR_SEM_DDD.match(fone):
            return True
        else:
            return False

    if not NUMERO_CELULAR_SEM_DDD.match(fone):
        return False

    return True


def valida_fone_especial(fone):
    fone = limpa_fone(fone)

    if not fone:
        return False

    if not NUMERO_ESPECIAL_0800.match(fone) and not NUMERO_ESPECIAL_4000.match(fone):
        return False

    return True


def valida_fone(fone, valida_nono_digito=False):
    return valida_fone_internacional(fone) or valida_fone_fixo(fone) or valida_fone_celular(fone, valida_nono_digito=valida_nono_digito) or valida_fone_especial(fone)


def formata_varios_fones(varios_fones):
    formatado = []

    if '/' not in varios_fones:
        return formata_fone(varios_fones)

    fone_anterior = ''
    for fone in varios_fones.split('/'):
        #
        # Somente os últimos 4 dígitos
        #
        if len(limpa_fone(fone)) == 4 and len(fone_anterior) > 4:
            fone = fone_anterior[::-1][4:][::-1] + fone

        formatado.append(formata_fone(fone))
        fone_anterior = limpa_fone(fone)

    return '/'.join(formatado)
