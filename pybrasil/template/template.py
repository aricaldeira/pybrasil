# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from mako.template import Template


class TemplateBrasil(Template):
    def __init__(self, *args, **kwargs):
        template_imports = [
            'import pybrasil',
            'import math',
            'from pybrasil.base import (tira_acentos, primeira_maiuscula)',
            'from pybrasil.data import (DIA_DA_SEMANA,',
            '   DIA_DA_SEMANA_ABREVIADO, MES, MES_ABREVIADO,',
            '   data_por_extenso, dia_da_semana_por_extenso,',
            '   dia_da_semana_por_extenso_abreviado, mes_por_extenso,',
            '   mes_por_extenso_abreviado, seculo, seculo_por_extenso,',
            '   hora_por_extenso, hora_por_extenso_aproximada, formata_data,',
            '   ParserInfoBrasil, parse_datetime, UTC, HB,',
            '   fuso_horario_sistema, data_hora_horario_brasilia, agora,',
            '   hoje, ontem, amanha, mes_passado, mes_que_vem, ano_passado,',
            '   ano_que_vem, semana_passada, semana_que_vem,',
            '   primeiro_dia_mes, ultimo_dia_mes, idade)',
            'from pybrasil.valor import (numero_por_extenso,',
            '   numero_por_extenso_ordinal, numero_por_extenso_unidade,',
            '   valor_por_extenso, valor_por_extenso_ordinal,',
            '   valor_por_extenso_unidade, formata_valor)',
            'from pybrasil.valor.decimal import Decimal as D',
            'from pybrasil.valor.decimal import Decimal',
        ]

        if not 'imports' in kwargs:
            kwargs['imports'] = template_imports

        if not 'input_encoding' in kwargs:
            kwargs['input_encoding'] = 'utf-8'

        if not 'output_encoding' in kwargs:
            kwargs['output_encoding'] = 'utf-8'

        if not 'strict_undefined' in kwargs:
            kwargs['strict_undefined'] = True

        return super(TemplateBrasil, self).__init__(*args, **kwargs)
