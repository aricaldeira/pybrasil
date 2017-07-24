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

from datetime import date

from ..base import modulo10, modulo11
from ..inscricao import limpa_formatacao
from ..valor.decimal import Decimal as D
from ..data import parse_datetime
from .codigo_barras_arrecadacao_segmento import \
    CODIGO_BARRAS_ARRECADACAO_SEGMENTOS

#
# Informações sobre a interpretação dos códigos de barras de recolhimento
# de impostos, guias e pagamento de contas de água, luz etc. retiradas de:
# http://wiki.biserp.com.br/index.php/Especificação_de_Guias_e_Boletos
#

def valida_codigo_barras(codigo_barras):
    codigo_barras = limpa_formatacao(codigo_barras)

    if not codigo_barras.isdigit():
        return False

    if len(codigo_barras) != 44:
        return False

    #
    # O primeiro dígito é 8 somente para documentos de arrecadação (contas,
    # impostos, guias etc.)
    #
    if codigo_barras[0] == '8':
        return valida_codigo_barras_arrecadacao(codigo_barras)

    return valida_codigo_barras_boleto(codigo_barras)


def valida_codigo_barras_boleto(codigo_barras):
    '''
    Validação de código de barras de boletos

    >>> valida_codigo_barras_boleto(
        '34192000000000000001754987341392525045163000')
    True
    >>> valida_codigo_barras_boleto(
        '74892721100010434951117202504903073701148103')
    True
    >>> valida_codigo_barras_boleto(
        '34199000000000000001754987341392525045163000')
    False
    >>> valida_codigo_barras_boleto(
        '74899721100010434951117202504903073701148103')
    False
    '''
    codigo_barras = limpa_formatacao(codigo_barras)

    if not codigo_barras.isdigit():
        return False

    if len(codigo_barras) != 44:
        return False

    #
    # O primeiro dígito é 8 somente para documentos de arrecadação (contas,
    # impostos, guias etc.)
    #
    if codigo_barras[0] == '8':
        return False

    dv_informado = codigo_barras[4]
    codigo_barras_informado = codigo_barras[0:4] + codigo_barras[5:]

    dv_calculado = modulo11(codigo_barras_informado,
                            mapa_digitos={0: 1, 1: 1, 10: 1, 11: 1})

    return dv_calculado == dv_informado


def valida_codigo_barras_arrecadacao(codigo_barras):
    '''
    Validação de código de barras de documento de arrecadação

    >>> valida_codigo_barras_arrecadacao(
        '82680000001512100191001174006376273132400512')
    True
    >>> valida_codigo_barras_boleto(
        '83660000001130301380000565199951100028446847')
    True
    >>> valida_codigo_barras_arrecadacao(
        '82660000001512100191001174006376273132400512')
    False
    >>> valida_codigo_barras_boleto(
        '83680000001130301380000565199951100028446847')
    False
    '''
    codigo_barras = limpa_formatacao(codigo_barras)

    if not codigo_barras.isdigit():
        return False

    if len(codigo_barras) != 44:
        return False

    #
    # O primeiro dígito é 8 somente para documentos de arrecadação (contas,
    # impostos, guias etc.)
    #
    if codigo_barras[0] != '8':
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
    tipo_dv = codigo_barras[2]
    dv_informado = codigo_barras[3]

    codigo_barras_informado = codigo_barras[0:3] + codigo_barras[4:]

    if tipo_dv in ['6', '7']:
        dv_calculado = modulo10(codigo_barras_informado)
    else:
        dv_calculado = modulo11(codigo_barras_informado)

    return dv_calculado == dv_informado


def identifica_codigo_barras(codigo_barras):
    if not valida_codigo_barras(codigo_barras):
        return

    if valida_codigo_barras_boleto(codigo_barras):
        return identifica_codigo_barras_boleto(codigo_barras)
    elif valida_codigo_barras_arrecadacao(codigo_barras):
        return identifica_codigo_barras_arrecadacao(codigo_barras)


def identifica_codigo_barras_boleto(codigo_barras):
    if not valida_codigo_barras_boleto(codigo_barras):
        return

    banco = codigo_barras[0:3]
    moeda = codigo_barras[3]
    dv = codigo_barras[4]
    vencimento = codigo_barras[5:9]
    valor = codigo_barras[9:19]
    campo_livre = codigo_barras[19:]

    #
    # Trata o vencimento
    #
    dias_vencimento = int(vencimento)  # Dias a partir de 07/10/1997

    if dias_vencimento == 0:
        vencimento = None

    else:
        vencimento = date(1997, 10, 7).toordinal() + dias_vencimento
        vencimento = date.fromordinal(vencimento)

    #
    # Trata o valor
    #
    valor = D(valor) / 100

    identificacao = {
        'banco': banco,
        'moeda': moeda,
        'dv': dv,
        'vencimento': vencimento,
        'valor': valor,
        'campo_livre': campo_livre,
    }

    return identificacao


def identifica_codigo_barras_arrecadacao(codigo_barras):
    if not valida_codigo_barras_arrecadacao(codigo_barras):
        return

    #
    # O segundo dígito indica qual o tipo de empresa/órgão está sendo pago:
    #
    # 1 - Prefeitura
    # 2 - Saneamento (água e esgoto) etc.
    # 3 - Enegia elétrica, gás etc.
    # 4 - Telecomunicações
    # 5 - Órãos governamentais
    # 6 - Carnês e assemelhados, ou demais empresas/órgãos, que serão
    #     identificados pelo CNPJ
    # 7 - Multas de trânsito
    # 9 - Uso exclusivo do banco
    #
    segmento = codigo_barras[1]

    #
    # O terceiro dígito indica como o DV vai ser calculado, se por módulo 10
    # ou 11, e onde está o valor dentro do código de barras:
    #
    # 6 - DV por módulo 10, valor em reais
    # 7 - DV por módulo 10, valor indexado
    # 8 - DV por módulo 11, valor em reais
    # 9 - DV por módulo 11, valor indexado
    #
    tipo_dv = codigo_barras[2]
    dv = codigo_barras[3]

    #
    # O valor em reais ou indexado (pode ser zerado)
    #
    valor = codigo_barras[4:15]

    #
    # Caso de empresa identificada por código
    #
    if segmento != '6':
        empresa = codigo_barras[15:19]
        campo_livre = codigo_barras[19:]
    else:
        empresa = codigo_barras[15:23]
        campo_livre = codigo_barras[23:]

    #
    # O campo livre pode conter, como os primeiros 10 dígitos, a data de
    # vencimento, mas não é obrigatório
    #
    try:
        data = campo_livre[:8]
        vencimento = parse_datetime(data, ano_primeiro=True)
    except:
        vencimento = None

    #
    # Trata o valor
    #
    valor = D(valor) / 100

    #
    # Detalhe do segmento/campo livre
    #
    detalhe_empresa = None
    detalhe_campo_livre = None
    if segmento != '6':
        if empresa in CODIGO_BARRAS_ARRECADACAO_SEGMENTOS[segmento]:
            detalhe_empresa = \
                CODIGO_BARRAS_ARRECADACAO_SEGMENTOS[segmento][empresa]

        if segmento == '5':
            #
            # Simples Nacional
            #
            if empresa == '0328':
                detalhe_campo_livre = {
                    'codigo_recolhimento': campo_livre[0:5],
                    'numero_documento': campo_livre[5:23],
                }

            else:
                detalhe_campo_livre = {
                    'codigo_recolhimento': campo_livre[0:4],
                    'uf_gestao': campo_livre[4:9],
                    'tipo_contribuinte': campo_livre[9],
                    'cnpj_cpf': campo_livre[10:],
                }

    identificacao = {
        'segmento': segmento,
        'tipo_dv': tipo_dv,
        'dv': dv,
        'valor': valor,
        'empresa': empresa,
        'campo_livre': campo_livre,
        'vencimento': vencimento,
        'detalhe_empresa': detalhe_empresa,
        'detalhe_campo_livre': detalhe_campo_livre,
    }

    return identificacao


def monta_linha_digitavel(codigo_barras):
    if valida_codigo_barras_boleto(codigo_barras):
        return monta_linha_digitavel_boleto(codigo_barras)
    elif valida_codigo_barras_arrecadacao(codigo_barras):
        return monta_linha_digitavel_arrecadacao(codigo_barras)


def monta_linha_digitavel_boleto(codigo_barras):
    if not valida_codigo_barras_boleto(codigo_barras):
        return

    #
    # Monta a linha digitável
    #
    campo_1 = codigo_barras[0:4] + codigo_barras[19:24]
    campo_2 = codigo_barras[24:34]
    campo_3 = codigo_barras[34:44]
    campo_4 = codigo_barras[4]
    campo_5 = codigo_barras[5:19]

    #
    # Dígitos verificadores
    #
    campo_1 += str(modulo10(campo_1, modulo=False))
    campo_2 += str(modulo10(campo_2, modulo=False))
    campo_3 += str(modulo10(campo_3, modulo=False))

    campo_1 = campo_1[:5] + '.' + campo_1[5:]
    campo_2 = campo_2[:5] + '.' + campo_2[5:]
    campo_3 = campo_3[:5] + '.' + campo_3[5:]

    return ' '.join([campo_1, campo_2, campo_3, campo_4, campo_5])


def monta_linha_digitavel_arrecadacao(codigo_barras):
    if not valida_codigo_barras_arrecadacao(codigo_barras):
        return

    #
    # Monta a linha digitável
    #
    campo_1 = codigo_barras[0:11]
    campo_2 = codigo_barras[11:22]
    campo_3 = codigo_barras[22:33]
    campo_4 = codigo_barras[33:]

    #
    # Dígitos verificadores
    #
    campo_1 += str(modulo10(campo_1, modulo=False))
    campo_2 += str(modulo10(campo_2, modulo=False))
    campo_3 += str(modulo10(campo_3, modulo=False))
    campo_4 += str(modulo10(campo_4, modulo=False))

    campo_1 = campo_1[0:11] + '-' + campo_1[11]
    campo_2 = campo_2[0:11] + '-' + campo_2[11]
    campo_3 = campo_3[0:11] + '-' + campo_3[11]
    campo_4 = campo_4[0:11] + '-' + campo_4[11]

    return ' '.join([campo_1, campo_2, campo_3, campo_4])
