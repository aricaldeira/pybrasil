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


import base64
from io import BytesIO
import qrcode
import qrcode.image.svg
import barcode
from barcode.writer import ImageWriter

from ..base.tira_acentos import tira_acentos_ascii


def code128_png(texto):
    if not texto:
        return ''

    texto = tira_acentos_ascii(texto)

    arq = BytesIO()
    barcode.generate('Code128', texto, writer=ImageWriter(), output=arq, writer_options={'write_text': False})
    return arq.getvalue()


def code128_png_base64(texto):
    if not texto:
        return ''

    imagem = code128_png(texto)

    return base64.b64encode(imagem).decode('utf-8')


def code128_svg(texto):
    if not texto:
        return ''

    texto = tira_acentos_ascii(texto)

    arq = BytesIO()
    barcode.generate('Code128', texto, output=arq, writer_options={'write_text': False})
    return arq.getvalue()


def code128_svg_base64(texto):
    if not texto:
        return ''

    imagem = code128_svg(texto)

    return base64.b64encode(imagem).decode('utf-8')
