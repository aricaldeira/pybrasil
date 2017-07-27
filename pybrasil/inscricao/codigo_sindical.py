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
# You should have recodigo_sindicalved a copy of the GNU Library General Public License
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
from .cnpj_cpf import eh_tudo_igual
from .inscricao_estadual import LIMPA


def valida_codigo_sindical(codigo_sindical):
    u'''Verifica que o código sindical seja válido
    de acordo com os dígitos verificadores

    XXX.YYY.ZZZ.SSSSS-S
    '''
    codigo_sindical = LIMPA.sub('', codigo_sindical)

    if len(codigo_sindical) < 15:
        codigo_sindical = codigo_sindical.zfill(15)

    if len(codigo_sindical) != 15:
        return False

    if not codigo_sindical.isdigit():
        return False

    if eh_tudo_igual(codigo_sindical):
        return False

    digito = codigo_sindical[-1]

    d1 = modulo11(codigo_sindical[:-1])

    return digito == unicode(d1)


def formata_codigo_sindical(codigo_sindical):
    if not valida_codigo_sindical(codigo_sindical):
        return codigo_sindical

    #
    #  Formato Código Sindical
    #  http://www.fenatracoop.com.br/site/mudancas-na-numeracao-do-codigo-sindical/
    #
    'XXX.YYY.ZZZ.SSSSS-S'

    codigo_sindical = LIMPA.sub('', codigo_sindical)
    codigo_sindical = str(int(codigo_sindical)).zfill(15)
    digito = codigo_sindical[-1]
    numero = codigo_sindical[:-1][::-1]
    numero = numero[0:5] + '.' + numero[5:8] + '.' + numero[8:11] + '.' + numero[11:]
    numero = numero[::-1]


    return numero + '-' + digito
