# -*- coding: utf-8 -*-

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
