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


from .nome import (DIA_DA_SEMANA, DIA_DA_SEMANA_ABREVIADO, MES, MES_ABREVIADO,
   MES_JANEIRO, MES_FEVEREIRO, MES_MARCO, MES_ABRIL, MES_MAIO, MES_JUNHO,
   MES_JULHO, MES_AGOSTO, MES_SETEMBRO, MES_OUTUBRO, MES_NOVEMBRO,
   MES_DEZEMBRO, MESES, DIA_SEGUNDA, DIA_TERCA, DIA_QUARTA, DIA_QUINTA,
   DIA_SEXTA, DIA_SABADO, DIA_DOMINGO, DIAS_DA_SEMANA)
from .extenso import (data_por_extenso, dia_da_semana_por_extenso, dia_da_semana_por_extenso_abreviado, mes_por_extenso, mes_por_extenso_abreviado, mes_romano, seculo, seculo_por_extenso, seculo_romano, milenio, milenio_por_extenso, milenio_romano, hora_por_extenso, hora_por_extenso_aproximada, formata_data, ano_por_extenso, ano_romano)
from .parserinfo import ParserInfoBrasil
from .parse_datetime import parse_datetime
from .fuso_horario import (UTC, HB, fuso_horario_sistema, data_hora_horario_brasilia, agora, hoje, ontem, amanha, mes_passado, mes_que_vem, ano_passado, ano_que_vem, semana_passada, semana_que_vem, primeiro_dia_mes, ultimo_dia_mes, hora_decimal_to_horas_minutos_segundos, horario_decimal_to_hora_decimal, horas_minutos_segundos_to_hora_decimal, horas_minutos_segundos_to_horario_decimal)
from .idade import (tempo, idade_anos, idade_meses, idade_anos as idade, idade_meses_sem_dia, dias_coincidentes)
from .dias_uteis import (dias_uteis, dias_uteis_bancarios, dia_util_pagamento)
