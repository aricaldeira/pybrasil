# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)

from datetime import date


DDD = [
    '11',  # SP
    '12',  # SP
    '13',  # SP
    '14',  # SP
    '15',  # SP
    '16',  # SP
    '17',  # SP
    '18',  # SP
    '19',  # SP
    '21',  # RJ
    '22',  # RJ
    '24',  # RJ
    '27',  # ES
    '28',  # ES
    '31',  # MG
    '32',  # MG
    '33',  # MG
    '34',  # MG
    '35',  # MG
    '37',  # MG
    '38',  # MG
    '41',  # PR
    '41',  # SC
    '42',  # PR
    '42',  # SC
    '43',  # PR
    '44',  # RS
    '44',  # PR
    '45',  # PR
    '46',  # PR
    '47',  # SC
    '48',  # SC
    '49',  # SC
    '51',  # RS
    '53',  # RS
    '54',  # RS
    '55',  # RS
    '61',  # DF
    '61',  # GO
    '62',  # GO
    '63',  # TO
    '64',  # GO
    '65',  # MT
    '66',  # MT
    '67',  # MS
    '68',  # AC
    '69',  # RO
    '71',  # BA
    '73',  # BA
    '74',  # BA
    '75',  # BA
    '77',  # BA
    '79',  # SE
    '81',  # PE
    '82',  # AL
    '83',  # PB
    '84',  # RN
    '85',  # CE
    '86',  # PI
    '87',  # PE
    '88',  # CE
    '89',  # PI
    '91',  # PA
    '92',  # AM
    '93',  # PA
    '94',  # PA
    '95',  # RR
    '96',  # AP
    '97',  # AM
    '98',  # MA
    '99',  # MA
]


DDDS = r'(' + '|'.join(DDD) + ')'


DATAS_NONO_DIGITO = {
    '2012-07-29': [
        '11',  # SP
    ],
    '2013-08-25': [
        '12',  # SP
        '13',  # SP
        '14',  # SP
        '15',  # SP
        '16',  # SP
        '17',  # SP
        '18',  # SP
        '19',  # SP
    ],
    '2013-10-27': [
        '21',  # RJ
        '22',  # RJ
        '24',  # RJ
        '27',  # ES
        '28',  # ES
    ],
    '2014-12-31': [
        '92',  # AM
        '97',  # AM
        '96',  # AP
        '98',  # MA
        '99',  # MA
        '91',  # PA
        '93',  # PA
        '94',  # PA
        '95',  # RR
    ],
    '2015-05-31': [
        '81',  # PE
        '87',  # PE
        '82',  # AL
        '83',  # PB
        '84',  # RN
        '85',  # CE
        '88',  # CE
        '86',  # PI
        '89',  # PI
    ],
    '2015-10-11': [
        '31',  # MG
        '32',  # MG
        '33',  # MG
        '34',  # MG
        '35',  # MG
        '37',  # MG
        '38',  # MG
        '71',  # BA
        '73',  # BA
        '74',  # BA
        '75',  # BA
        '77',  # BA
        '79',  # SE
    ],
    '2016-05-29': [
        '61',  # DF
        '62',  # GO
        '63',  # TO
        '64',  # GO
        '65',  # MT
        '66',  # MT
        '67',  # MS
        '68',  # AC
        '69',  # RO
    ],
    '2016-11-06': [
        '41',  # PR
        '41',  # SC
        '42',  # PR
        '42',  # SC
        '43',  # PR
        '44',  # RS
        '44',  # PR
        '45',  # PR
        '46',  # PR
        '47',  # SC
        '48',  # SC
        '49',  # SC
        '51',  # RS
        '53',  # RS
        '54',  # RS
        '55',  # RS
    ]
}


DDDS_NONO_DIGITO = []


HOJE = date.today().strftime(b'%Y-%m-%d')


for data in DATAS_NONO_DIGITO:
    #print(data, HOJE, HOJE >= data)
    if HOJE >= data:
        DDDS_NONO_DIGITO += DATAS_NONO_DIGITO[data]
