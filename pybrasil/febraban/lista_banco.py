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

from imp import load_source
import os
import sys
import types
from io import open
from .banco import Banco


CURDIR = os.path.dirname(os.path.abspath(__file__))


def _monta_dicionario_codigo():
    dicionario = {}

    arquivo = open(os.path.join(CURDIR, 'banco.txt'), 'r', encoding='utf-8')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        codigo = campos[0]
        nome = campos[1]

        arquivo_classe = os.path.join(CURDIR, 'banco_' + codigo + '.py')

        b = Banco(codigo, nome)

        if os.path.exists(arquivo_classe):
            modulo = load_source('banco_' + codigo, arquivo_classe)

            #
            # Cálculos de cada banco
            #
            if hasattr(modulo, 'campo_livre'):
                b.campo_livre = types.MethodType(getattr(modulo, 'campo_livre'), b)

            if hasattr(modulo, 'calcula_digito_nosso_numero'):
                b.calcula_digito_nosso_numero = types.MethodType(getattr(modulo, 'calcula_digito_nosso_numero'), b)

            if hasattr(modulo, 'fator_vencimento'):
                b.fator_vencimento = types.MethodType(getattr(modulo, 'fator_vencimento'), b)

            if hasattr(modulo, 'local_pagamento'):
                b.local_pagamento = types.MethodType(getattr(modulo, 'local_pagamento'), b)

            #
            # Impressão especial de cada banco
            #
            if hasattr(modulo, 'carteira_nosso_numero'):
                b.carteira_nosso_numero = types.MethodType(getattr(modulo, 'carteira_nosso_numero'), b)

            if hasattr(modulo, 'agencia_conta'):
                b.agencia_conta = types.MethodType(getattr(modulo, 'agencia_conta'), b)

            if hasattr(modulo, 'imprime_carteira'):
                b.imprime_carteira = types.MethodType(getattr(modulo, 'imprime_carteira'), b)

            #
            # CNAB 240
            #
            if hasattr(modulo, 'header_remessa_240'):
                b.header_remessa_240 = types.MethodType(getattr(modulo, 'header_remessa_240'), b)

            if hasattr(modulo, 'trailler_remessa_240'):
                b.trailler_remessa_240 = types.MethodType(getattr(modulo, 'trailler_remessa_240'), b)

            if hasattr(modulo, 'linha_remessa_240'):
                b.linha_remessa_240 = types.MethodType(getattr(modulo, 'linha_remessa_240'), b)

            if hasattr(modulo, 'header_retorno_240'):
                b.header_retorno_240 = types.MethodType(getattr(modulo, 'header_retorno_240'), b)

            if hasattr(modulo, 'trailler_retorno_240'):
                b.trailler_retorno_240 = types.MethodType(getattr(modulo, 'trailler_retorno_240'), b)

            if hasattr(modulo, 'linha_retorno_240'):
                b.linha_retorno_240 = types.MethodType(getattr(modulo, 'linha_retorno_240'), b)

            #
            # CNAB 400
            #
            if hasattr(modulo, 'header_remessa_400'):
                b.header_remessa_400 = types.MethodType(getattr(modulo, 'header_remessa_400'), b)

            if hasattr(modulo, 'trailler_remessa_400'):
                b.trailler_remessa_400 = types.MethodType(getattr(modulo, 'trailler_remessa_400'), b)

            if hasattr(modulo, 'linha_remessa_400'):
                b.linha_remessa_400 = types.MethodType(getattr(modulo, 'linha_remessa_400'), b)

            if hasattr(modulo, 'header_retorno_400'):
                b.header_retorno_400 = types.MethodType(getattr(modulo, 'header_retorno_400'), b)

            if hasattr(modulo, 'trailler_retorno_400'):
                b.trailler_retorno_400 = types.MethodType(getattr(modulo, 'trailler_retorno_400'), b)

            if hasattr(modulo, 'linha_retorno_400'):
                b.linha_retorno_400 = types.MethodType(getattr(modulo, 'linha_retorno_400'), b)

            #
            # Descrição dos comandos de cada banco
            #
            if hasattr(modulo, 'DESCRICAO_COMANDO_REMESSA'):
                b.descricao_comandos_remessa = getattr(modulo, 'DESCRICAO_COMANDO_REMESSA')

            if hasattr(modulo, 'DESCRICAO_COMANDO_RETORNO'):
                b.descricao_comandos_retorno = getattr(modulo, 'DESCRICAO_COMANDO_RETORNO')

            if hasattr(modulo, 'COMANDOS_RETORNO_LIQUIDACAO'):
                b.comandos_liquidacao = getattr(modulo, 'COMANDOS_RETORNO_LIQUIDACAO')

            if hasattr(modulo, 'COMANDOS_RETORNO_BAIXA'):
                b.comandos_baixa = getattr(modulo, 'COMANDOS_RETORNO_BAIXA')

        dicionario[b.codigo] = b

    return dicionario


if not hasattr(sys.modules[__name__], 'BANCO_CODIGO'):
    BANCO_CODIGO = _monta_dicionario_codigo()
