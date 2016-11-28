# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)

#from dateutil.parser import parse as parse_datetime_original
from dateutil.parser import parser
from datetime import datetime as datetime_sem_fuso, date, time
from pytz import (datetime, timezone, tzinfo, UTC)
from .parserinfo import ParserInfoBrasil
from time import strftime
from dateutil.relativedelta import relativedelta


#AVALIAR_DATA_BRASIL = ParserInfoBrasil()


HB = timezone('America/Sao_Paulo')


def fuso_horario_sistema():
    diferenca = int(strftime('%z')) // 100

    if diferenca < 0:
        return timezone('Etc/GMT+' + str(diferenca * -1))

    if diferenca > 0:
        return timezone('Etc/GMT-' + str(diferenca))

    return UTC



def parse_datetime(timestr, parserinfo=ParserInfoBrasil(), **kwargs):
    if isinstance(timestr, (datetime.datetime, datetime_sem_fuso, date, time)):
        return timestr

    if not isinstance(timestr, (str, unicode)):
        return None

    if isinstance(timestr, (str, unicode)) and (timestr.strip() == '' or timestr.replace('0', '') == '') :
        return None

    #
    # Assume dia/mes/ano
    #
    if timestr.isdigit():
        if kwargs.get('ano_primeiro', False):
            if len(timestr) == 8:
                timestr = timestr[6:] + '/' + timestr[4:6] + '/' + timestr[:4]
            elif len(timestr) == 6:
                timestr = timestr[4:] + '/' + timestr[2:4] + '/20' + timestr[:2]
            elif len(timestr) == 4:
                timestr = timestr[2:] + '/' + timestr[:2] + '/' + str(datetime.now().year)
        else:
            if len(timestr) == 8:
                timestr = timestr[:2] + '/' + timestr[2:4] + '/' + timestr[4:]
            elif len(timestr) == 6:
                timestr = timestr[:2] + '/' + timestr[2:4] + '/20' + timestr[4:]
            elif len(timestr) == 4:
                timestr = timestr[:2] + '/' + timestr[2:] + '/' + str(datetime.now().year)

    #
    # Os valores padrão para campos faltantes são a data
    # atual em Brasília, ao meio-dia
    #
    if 'default' not in kwargs:
        default = datetime_sem_fuso.now()
        default = fuso_horario_sistema().localize(default)
        default = UTC.normalize(default)
        default = HB.normalize(default)
        default += relativedelta(hour=12, minute=0, second=0, microsecond=0)
        kwargs['default'] = default

    if 'ano_primeiro' in kwargs:
        del kwargs['ano_primeiro']

    #
    # Trata corretamente o formato ano-mes-dia
    #
    if timestr[4] == '-' and timestr[7] == '-':
        parserinfo.dayfirst = False
        parserinfo.yearfirst = True
    else:
        parserinfo.dayfirst = True
        parserinfo.yearfirst = False

    kwargs['dayfirst'] = parserinfo.dayfirst
    kwargs['yearfirst'] = parserinfo.yearfirst

    #print('data original', timestr)
    #print('parserinfo', parserinfo)
    #print('kwargs', kwargs)
    data = parser(parserinfo).parse(timestr, **kwargs)
    #data = parse_datetime_original(timestr, parserinfo, **kwargs)
    #print('data tratada', data)

    return data
