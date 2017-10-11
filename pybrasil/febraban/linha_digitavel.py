# -*- coding: utf-8 -*-
#
# PyBrasil - Functions useful for most Brazil's ERPs
#
# Copyright (C) 2017-
# Copyright (C) Ari Caldeira <ari.caldeira at tauga.com.br>
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
# Copyright (C) 2017-
# Copyright (C) Ari Caldeira <ari.caldeira arroba tauga.com.br>
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

from datetime import date

from ..base import modulo10, modulo11
from ..inscricao import limpa_formatacao
from .codigo_barras import (identifica_codigo_barras_boleto,
    identifica_codigo_barras_arrecadacao, monta_linha_digitavel_boleto,
    monta_linha_digitavel_arrecadacao)

#
# Informações sobre a interpretação dos códigos de barras de recolhimento
# de impostos, guias e pagamento de contas de água, luz etc. retiradas de:
# http://wiki.biserp.com.br/index.php/Especificação_de_Guias_e_Boletos
#

def valida_linha_digitavel(linha_digitavel):
    linha_digitavel = limpa_formatacao(linha_digitavel)

    if not linha_digitavel.isdigit():
        return False

    if len(linha_digitavel) != 48 and len(linha_digitavel) != 47:
        return False

    #
    # O primeiro dígito é 8 somente para documentos de arrecadação (contas,
    # impostos, guias etc.)
    #
    if linha_digitavel[0] == '8':
        return valida_linha_digitavel_arrecadacao(linha_digitavel)

    return valida_linha_digitavel_boleto(linha_digitavel)


def valida_linha_digitavel_boleto(linha_digitavel,
                                  retorna_codigo_barras=False):
    linha_digitavel = limpa_formatacao(linha_digitavel)

    if not linha_digitavel.isdigit():
        return False

    if len(linha_digitavel) != 47:
        return False

    #
    # O primeiro dígito é 8 somente para documentos de arrecadação (contas,
    # impostos, guias etc.)
    #
    if linha_digitavel[0] == '8':
        return False

    campo_1 = linha_digitavel[0:9]
    dv1_informado = linha_digitavel[9]
    campo_2 = linha_digitavel[10:20]
    dv2_informado = linha_digitavel[20]
    campo_3 = linha_digitavel[21:31]
    dv3_informado = linha_digitavel[31]
    dv_informado = linha_digitavel[32]
    campo_4 = linha_digitavel[33:37]
    campo_5 = linha_digitavel[37:]

    if retorna_codigo_barras:
        codigo_barras = campo_1[0:4] + dv_informado + campo_4 + campo_5 + \
            campo_1[4:] + campo_2 + campo_3
        return codigo_barras

    codigo_barras = campo_1[0:4] + campo_4 + campo_5 + campo_1[4:] + \
        campo_2 + campo_3

    dv1_calculado = str(modulo10(campo_1, modulo=False))
    dv2_calculado = str(modulo10(campo_2, modulo=False))
    dv3_calculado = str(modulo10(campo_3, modulo=False))
    dv_calculado = modulo11(codigo_barras,
                            mapa_digitos={0: 1, 1: 1, 10: 1, 11: 1})

    return (dv_calculado == dv_informado and dv1_calculado == dv1_informado
            and dv2_calculado == dv2_informado
            and dv3_calculado == dv3_informado)


def valida_linha_digitavel_arrecadacao(linha_digitavel,
                                       retorna_codigo_barras=False):
    linha_digitavel = limpa_formatacao(linha_digitavel)

    if not linha_digitavel.isdigit():
        return False

    if len(linha_digitavel) != 48:
        return False

    #
    # O primeiro dígito é 8 somente para documentos de arrecadação (contas,
    # impostos, guias etc.)
    #
    if linha_digitavel[0] != '8':
        return False

    #
    # O terceiro dígito indica como o DV vai ser calculado, se por módulo 10
    # ou 11, e onde está o valor dentro do código de barras:
    #
    # 6 - DV por módulo 10, valor em reais
    # 7 - DV por módulo 10, valor indexado
    # 8 - DV por módulo 11, valor em reais
    # 9 - DV por módulo 11, valor indexado
    #
    tipo_dv = linha_digitavel[2]
    dv_informado = linha_digitavel[3]

    campo_1 = linha_digitavel[0:11]
    dv1_informado = linha_digitavel[11]
    campo_2 = linha_digitavel[12:23]
    dv2_informado = linha_digitavel[23]
    campo_3 = linha_digitavel[24:35]
    dv3_informado = linha_digitavel[35]
    campo_4 = linha_digitavel[36:47]
    dv4_informado = linha_digitavel[47]

    codigo_barras = campo_1 + campo_2 + campo_3 + campo_4

    if retorna_codigo_barras:
        return codigo_barras

    if tipo_dv in ['6', '8']:
        dv_calculado = modulo10(codigo_barras)
    else:
        dv_calculado = modulo11(codigo_barras)

    dv1_calculado = str(modulo10(campo_1, modulo=False))
    dv2_calculado = str(modulo10(campo_2, modulo=False))
    dv3_calculado = str(modulo10(campo_3, modulo=False))
    dv4_calculado = str(modulo10(campo_4, modulo=False))

    return (dv_calculado == dv_informado and dv1_calculado == dv1_informado
            and dv2_calculado == dv2_informado
            and dv3_calculado == dv3_informado
            and dv4_calculado == dv4_informado)


def monta_codigo_barras(linha_digitavel):
    if not valida_linha_digitavel(linha_digitavel):
        return

    if valida_linha_digitavel_boleto(linha_digitavel):
        codigo_barras = valida_linha_digitavel_boleto(linha_digitavel,
                            retorna_codigo_barras=True)
        return codigo_barras
    elif valida_linha_digitavel_arrecadacao(linha_digitavel):
        codigo_barras = valida_linha_digitavel_arrecadacao(linha_digitavel,
                            retorna_codigo_barras=True)
        return codigo_barras


def identifica_linha_digitavel(linha_digitavel):
    if not valida_linha_digitavel(linha_digitavel):
        return

    if valida_linha_digitavel_boleto(linha_digitavel):
        codigo_barras = valida_linha_digitavel_boleto(linha_digitavel,
                            retorna_codigo_barras=True)
        return identifica_codigo_barras_boleto(codigo_barras)
    elif valida_linha_digitavel_arrecadacao(linha_digitavel):
        codigo_barras = valida_linha_digitavel_arrecadacao(linha_digitavel,
                            retorna_codigo_barras=True)
        return identifica_codigo_barras_arrecadacao(codigo_barras)


def formata_linha_digitavel(linha_digitavel):
    if not valida_linha_digitavel(linha_digitavel):
        return

    if valida_linha_digitavel_boleto(linha_digitavel):
        codigo_barras = valida_linha_digitavel_boleto(linha_digitavel,
                            retorna_codigo_barras=True)
        return monta_linha_digitavel_boleto(codigo_barras)
    elif valida_linha_digitavel_arrecadacao(linha_digitavel):
        codigo_barras = valida_linha_digitavel_arrecadacao(linha_digitavel,
                            retorna_codigo_barras=True)
        return monta_linha_digitavel_arrecadacao(codigo_barras)
