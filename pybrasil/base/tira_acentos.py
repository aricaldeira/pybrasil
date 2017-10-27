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


import sys
import unicodedata


def tira_acentos(texto):
    texto = texto.replace('°', 'o')
    if sys.version_info.major == 2:
        return unicodedata.normalize(b'NFKD', texto).encode('ascii', 'ignore').encode('utf-8')
    else:
        return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')


def somente_ascii(funcao):
    '''
    Usado como decorator
    '''
    def converter_para_ascii_puro(*args, **kwargs):
        texto = funcao(*args, **kwargs)
        texto = texto.replace('°', 'o')
        if sys.version_info.major == 2:
            return unicodedata.normalize(b'NFKD', texto).encode('ascii', 'ignore')
        else:
            return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')

    return converter_para_ascii_puro


def escape_xml(texto, aspas=True):
    if not texto:
        return texto

    texto = texto.replace('&', '&amp;')
    texto = texto.replace('<', '&lt;')
    texto = texto.replace('>', '&gt;')

    if aspas:
        texto = texto.replace('"', '&quot;')
        texto = texto.replace("'", '&apos;')

    return texto


def unescape_xml(texto):
    if not texto:
        return texto

    texto = texto.replace('&#39;', "'")
    texto = texto.replace('&apos;', "'")
    texto = texto.replace('&quot;', '"')
    texto = texto.replace('&gt;', '>')
    texto = texto.replace('&lt;', '<')
    texto = texto.replace('&amp;', '&')
    texto = texto.replace('&APOS;', "'")
    texto = texto.replace('&QUOT;', '"')
    texto = texto.replace('&GT;', '>')
    texto = texto.replace('&LT;', '<')
    texto = texto.replace('&AMP;', '&')

    return texto
