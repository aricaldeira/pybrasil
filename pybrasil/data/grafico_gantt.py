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


from dateutil.relativedelta import relativedelta
from .fuso_horario import hoje
from .parse_datetime import parse_datetime


def tempo_tarefa(data_inicial_periodo=hoje(), data_final_periodo=hoje(), data_inicial_tarefa=hoje(), data_final_tarefa=hoje(), marcador_sim='█', marcador_nao=' '):
    data_inicial_periodo = parse_datetime(data_inicial_periodo)
    data_final_periodo = parse_datetime(data_final_periodo)
    data_inicial_tarefa = parse_datetime(data_inicial_tarefa)
    data_final_tarefa = parse_datetime(data_final_tarefa)

    texto = ''

    data = data_inicial_periodo

    while data <= data_final_periodo:
        if data >= data_inicial_tarefa and data <= data_final_tarefa:
            texto += marcador_sim
        else:
            texto += marcador_nao

        data += relativedelta(days=+1)

    return texto
