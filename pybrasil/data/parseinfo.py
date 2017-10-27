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

from dateutil.parser import parserinfo


class ParserInfoBrasil(parserinfo):
    HMS = [
        ('h', 'hora', 'horas'),
        ('m', 'minuto', 'minutos'),
        ('s', 'segundo', 'segundos')
    ]

    JUMP = [
        ' ',
        '.',
        ',',
        ';',
        '-',
        '/',
        "'",
        'em',
        'no',
        'na',
        'de',
        'e',
        'º',
        'ª',
        '°',
    ]

    MONTHS = [
        ('jan', 'janeiro', 'Jan', 'Janeiro'),
        ('fev', 'fevereiro', 'Fev', 'Fevereiro'),
        ('mar', 'março', 'Mar', 'Março', 'marco', 'Marco'),
        ('abr', 'abril', 'Abr', 'Abril'),
        ('mai', 'maio', 'Mai', 'Maio'),
        ('jun', 'junho', 'Jun', 'Junho'),
        ('jul', 'julho', 'Jul', 'Julho'),
        ('ago', 'agosto', 'Ago', 'Agosto'),
        ('set', 'setembro', 'Set', 'Setembro'),
        ('out', 'outubro', 'Out', 'Outubro'),
        ('nov', 'novembro', 'Nov', 'Novembro'),
        ('dez', 'dezembro', 'Dez', 'Dezembro')
    ]

    PERTAIN = [
        'de'
    ]

    WEEKDAYS = [
        ('seg', 'segunda-feira', 'segunda', 'Seg', 'Segunda-Feira', 'Segunda', 'Segunda-feira'),
        ('ter', 'terça-feira', 'terça', 'Ter', 'Terça-Feira', 'Terça', 'Terça-feira', 'terca-feira', 'Terca-Feira', 'Terca-feira'),
        ('qua', 'quarta-feira', 'quarta', 'Qua', 'Quarta-Feira', 'Quarta', 'Quarta-feira'),
        ('qui', 'quinta-feira', 'quinta', 'Qui', 'Quinta-Feira', 'Quinta', 'Quinta-feira'),
        ('sex', 'sexta-feira', 'sexta', 'Sex', 'Sexta-Feira', 'Sexta', 'Sexta-feira'),
        ('sáb', 'sábado', 'Sáb', 'Sábado', 'sab', 'sabado', 'Sab', 'Sabado'),
        ('dom', 'domingo', 'Dom', 'Domingo')
    ]

    dayfirst = True
