#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Números por extenso, cardinais, ordinais e cardinais com unidades de medida

Compatível com as versões 2 e 3 do Python
'''

from __future__ import division, print_function, unicode_literals

from .extenso import NumeroPorExtenso, CARDINAL, MASCULINO, FEMININO, ORDINAL


class NumeroPorExtensoEuropeu(NumeroPorExtenso):
    CARDINAL_0 = 'zero'
    CARDINAL_1 = 'um'
    CARDINAL_2 = 'dois'
    CARDINAL_3 = 'três'
    CARDINAL_4 = 'quatro'
    CARDINAL_5 = 'cinco'
    CARDINAL_6 = 'seis'
    CARDINAL_7 = 'sete'
    CARDINAL_8 = 'oito'
    CARDINAL_9 = 'nove'

    CARDINAL_10 = 'dez'
    CARDINAL_11 = 'onze'
    CARDINAL_12 = 'doze'
    CARDINAL_13 = 'treze'
    CARDINAL_14 = 'catorze'
    CARDINAL_15 = 'quinze'
    CARDINAL_16 = 'dezasseis'
    CARDINAL_17 = 'dezassete'
    CARDINAL_18 = 'dezoito'
    CARDINAL_19 = 'dezanove'
    CARDINAL_20 = 'vinte'
    CARDINAL_30 = 'trinta'
    CARDINAL_40 = 'quarenta'
    CARDINAL_50 = 'cinquenta'
    CARDINAL_60 = 'sessenta'
    CARDINAL_70 = 'setenta'
    CARDINAL_80 = 'oitenta'
    CARDINAL_90 = 'noventa'

    CARDINAL_100_ISOLADO = 'cem'

    CARDINAL_100 = 'cento'
    CARDINAL_200 = 'duzentos'
    CARDINAL_300 = 'trezentos'
    CARDINAL_400 = 'quatrocentos'
    CARDINAL_500 = 'quinhentos'
    CARDINAL_600 = 'seiscentos'
    CARDINAL_700 = 'setecentos'
    CARDINAL_800 = 'oitocentos'
    CARDINAL_900 = 'novecentos'

    CARDINAL_1_FEMININO = 'uma'
    CARDINAL_2_FEMININO = 'duas'

    CARDINAL_200_FEMININO = 'duzentas'
    CARDINAL_300_FEMININO = 'trezentas'
    CARDINAL_400_FEMININO = 'quatrocentas'
    CARDINAL_500_FEMININO = 'quinhentas'
    CARDINAL_600_FEMININO = 'seiscentas'
    CARDINAL_700_FEMININO = 'setecentas'
    CARDINAL_800_FEMININO = 'oitocentas'
    CARDINAL_900_FEMININO = 'novecentas'

    CARDINAL_MASCULINO = {
        0: CARDINAL_0,
        1: CARDINAL_1,
        2: CARDINAL_2,
        3: CARDINAL_3,
        4: CARDINAL_4,
        5: CARDINAL_5,
        6: CARDINAL_6,
        7: CARDINAL_7,
        8: CARDINAL_8,
        9: CARDINAL_9,
        10: CARDINAL_10,
        11: CARDINAL_11,
        12: CARDINAL_12,
        13: CARDINAL_13,
        14: CARDINAL_14,
        15: CARDINAL_15,
        16: CARDINAL_16,
        17: CARDINAL_17,
        18: CARDINAL_18,
        19: CARDINAL_19,
        20: CARDINAL_20,
        30: CARDINAL_30,
        40: CARDINAL_40,
        50: CARDINAL_50,
        60: CARDINAL_60,
        70: CARDINAL_70,
        80: CARDINAL_80,
        90: CARDINAL_90,
        100: CARDINAL_100,
        200: CARDINAL_200,
        300: CARDINAL_300,
        400: CARDINAL_400,
        500: CARDINAL_500,
        600: CARDINAL_600,
        700: CARDINAL_700,
        800: CARDINAL_800,
        900: CARDINAL_900,
    }

    CARDINAL_FEMININO = CARDINAL_MASCULINO.copy()

    CARDINAL_FEMININO.update({
        1: CARDINAL_1_FEMININO,
        2: CARDINAL_2_FEMININO,
        200: CARDINAL_200_FEMININO,
        300: CARDINAL_300_FEMININO,
        400: CARDINAL_400_FEMININO,
        500: CARDINAL_500_FEMININO,
        600: CARDINAL_600_FEMININO,
        700: CARDINAL_700_FEMININO,
        800: CARDINAL_800_FEMININO,
        900: CARDINAL_900_FEMININO,
    })

    NOME_CARDINAL_POTENCIA = {
        10 ** 3: ('mil', 'mil'),
        10 ** 6: ('milhão', 'milhões'),
        10 ** 9: ('mil milhões', 'mil milhões'),
        10 ** 12: ('bilião', 'biliões'),
        10 ** 15: ('mil biliões', 'mil biliões'),
        10 ** 18: ('trilião', 'triliões'),
        10 ** 21: ('mil triliões', 'mil triliões'),
        10 ** 24: ('quatrilião', 'quatriliões'),
        10 ** 27: ('mil quatriliões', 'mil quatriliões'),
        10 ** 30: ('quintilião', 'quintiliões'),
        10 ** 33: ('mil quintiliões', 'mil quintiliões'),
        10 ** 36: ('sextilião', 'sextiliões'),
        10 ** 39: ('mil sextiliões', 'mil sextiliões'),
        10 ** 42: ('septilião', 'septiliões'),
        10 ** 45: ('mil septiliões', 'mil septiliões'),
        10 ** 48: ('octilião', 'octiliões'),
        10 ** 51: ('mil octiliões', 'mil octiliões'),
        10 ** 54: ('nonilião', 'noniliões'),
        10 ** 57: ('mil noniliões', 'mil noniliões'),
        10 ** 60: ('decilião', 'deciliões'),
        #10 ** 36: ('undecilhão', 'undecilhões'),
        #10 ** 39: ('dodecilhão', 'duodecilhões'),
        #10 ** 42: ('tredecilhão', 'tredecilhões'),
        #10 ** 45: ('quatuordecilhão', 'quatuordecilhões'),
        #10 ** 48: ('quindecilhão', 'quindecilhões'),
        #10 ** 51: ('sesdecilhão', 'sesdecilhões'),
        #10 ** 54: ('septendecilhão', 'septendecilhões'),
        #10 ** 57: ('octodecilhão', 'octodecilhões'),
        #10 ** 60: ('nonidecilhão', 'nonidecilhões'),
    }

    ORDINAL_0 = 'zerésimo'
    ORDINAL_1 = 'primeiro'
    ORDINAL_2 = 'segundo'
    ORDINAL_3 = 'terceiro'
    ORDINAL_4 = 'quarto'
    ORDINAL_5 = 'quinto'
    ORDINAL_6 = 'sexto'
    ORDINAL_7 = 'sétimo'
    ORDINAL_8 = 'oitavo'
    ORDINAL_9 = 'nono'

    ORDINAL_10 = 'décimo'
    ORDINAL_11 = ORDINAL_10 + ' ' + ORDINAL_1
    ORDINAL_12 = ORDINAL_10 + ' ' + ORDINAL_2
    ORDINAL_13 = ORDINAL_10 + ' ' + ORDINAL_3
    ORDINAL_14 = ORDINAL_10 + ' ' + ORDINAL_4
    ORDINAL_15 = ORDINAL_10 + ' ' + ORDINAL_5
    ORDINAL_16 = ORDINAL_10 + ' ' + ORDINAL_6
    ORDINAL_17 = ORDINAL_10 + ' ' + ORDINAL_7
    ORDINAL_18 = ORDINAL_10 + ' ' + ORDINAL_8
    ORDINAL_19 = ORDINAL_10 + ' ' + ORDINAL_9
    ORDINAL_20 = 'vigésimo'
    ORDINAL_30 = 'trigésimo'
    ORDINAL_40 = 'quadragésimo'
    ORDINAL_50 = 'quinquagésimo'
    ORDINAL_60 = 'sexagésimo'
    ORDINAL_70 = 'septuagésimo'
    ORDINAL_80 = 'octogésimo'
    ORDINAL_90 = 'nonagésimo'

    ORDINAL_100 = 'centésimo'
    ORDINAL_200 = 'ducentésimo'
    ORDINAL_300 = 'tricentésimo'
    ORDINAL_400 = 'quadringentésimo'
    ORDINAL_500 = 'quingentésimo'
    ORDINAL_600 = 'seiscentésimo'
    ORDINAL_700 = 'septigentésimo'
    ORDINAL_800 = 'octingentésimo'
    ORDINAL_900 = 'noningentésimo'

    ORDINAL_0_FEMININO = 'zerésima'
    ORDINAL_1_FEMININO = 'primeira'
    ORDINAL_2_FEMININO = 'segunda'
    ORDINAL_3_FEMININO = 'terceira'
    ORDINAL_4_FEMININO = 'quarta'
    ORDINAL_5_FEMININO = 'quinta'
    ORDINAL_6_FEMININO = 'sexta'
    ORDINAL_7_FEMININO = 'sétima'
    ORDINAL_8_FEMININO = 'oitava'
    ORDINAL_9_FEMININO = 'nona'

    ORDINAL_10_FEMININO = 'décima'
    ORDINAL_11_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_1_FEMININO
    ORDINAL_12_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_2_FEMININO
    ORDINAL_13_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_3_FEMININO
    ORDINAL_14_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_4_FEMININO
    ORDINAL_15_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_5_FEMININO
    ORDINAL_16_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_6_FEMININO
    ORDINAL_17_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_7_FEMININO
    ORDINAL_18_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_8_FEMININO
    ORDINAL_19_FEMININO = ORDINAL_10_FEMININO + ' ' + ORDINAL_9_FEMININO
    ORDINAL_20_FEMININO = 'vigésima'
    ORDINAL_30_FEMININO = 'trigésima'
    ORDINAL_40_FEMININO = 'quadragésima'
    ORDINAL_50_FEMININO = 'quinquagésima'
    ORDINAL_60_FEMININO = 'sexagésima'
    ORDINAL_70_FEMININO = 'septuagésima'
    ORDINAL_80_FEMININO = 'octogésima'
    ORDINAL_90_FEMININO = 'nonagésima'

    ORDINAL_100_FEMININO = 'centésima'
    ORDINAL_200_FEMININO = 'ducentésima'
    ORDINAL_300_FEMININO = 'tricentésima'
    ORDINAL_400_FEMININO = 'quadringentésima'
    ORDINAL_500_FEMININO = 'quingentésima'
    ORDINAL_600_FEMININO = 'seiscentésima'
    ORDINAL_700_FEMININO = 'septigentésima'
    ORDINAL_800_FEMININO = 'octingentésima'
    ORDINAL_900_FEMININO = 'noningentésima'

    ORDINAL_MASCULINO = {
        0: CARDINAL_0,
        1: ORDINAL_1,
        2: ORDINAL_2,
        3: ORDINAL_3,
        4: ORDINAL_4,
        5: ORDINAL_5,
        6: ORDINAL_6,
        7: ORDINAL_7,
        8: ORDINAL_8,
        9: ORDINAL_9,
        10: ORDINAL_10,
        11: ORDINAL_11,
        12: ORDINAL_12,
        13: ORDINAL_13,
        14: ORDINAL_14,
        15: ORDINAL_15,
        16: ORDINAL_16,
        17: ORDINAL_17,
        18: ORDINAL_18,
        19: ORDINAL_19,
        20: ORDINAL_20,
        30: ORDINAL_30,
        40: ORDINAL_40,
        50: ORDINAL_50,
        60: ORDINAL_60,
        70: ORDINAL_70,
        80: ORDINAL_80,
        90: ORDINAL_90,
        100: ORDINAL_100,
        200: ORDINAL_200,
        300: ORDINAL_300,
        400: ORDINAL_400,
        500: ORDINAL_500,
        600: ORDINAL_600,
        700: ORDINAL_700,
        800: ORDINAL_800,
        900: ORDINAL_900,
    }

    ORDINAL_FEMININO = {
        0: CARDINAL_0,
        1: ORDINAL_1_FEMININO,
        2: ORDINAL_2_FEMININO,
        3: ORDINAL_3_FEMININO,
        4: ORDINAL_4_FEMININO,
        5: ORDINAL_5_FEMININO,
        6: ORDINAL_6_FEMININO,
        7: ORDINAL_7_FEMININO,
        8: ORDINAL_8_FEMININO,
        9: ORDINAL_9_FEMININO,
        10: ORDINAL_10_FEMININO,
        11: ORDINAL_11_FEMININO,
        12: ORDINAL_12_FEMININO,
        13: ORDINAL_13_FEMININO,
        14: ORDINAL_14_FEMININO,
        15: ORDINAL_15_FEMININO,
        16: ORDINAL_16_FEMININO,
        17: ORDINAL_17_FEMININO,
        18: ORDINAL_18_FEMININO,
        19: ORDINAL_19_FEMININO,
        20: ORDINAL_20_FEMININO,
        30: ORDINAL_30_FEMININO,
        40: ORDINAL_40_FEMININO,
        50: ORDINAL_50_FEMININO,
        60: ORDINAL_60_FEMININO,
        70: ORDINAL_70_FEMININO,
        80: ORDINAL_80_FEMININO,
        90: ORDINAL_90_FEMININO,
        100: ORDINAL_100_FEMININO,
        200: ORDINAL_200_FEMININO,
        300: ORDINAL_300_FEMININO,
        400: ORDINAL_400_FEMININO,
        500: ORDINAL_500_FEMININO,
        600: ORDINAL_600_FEMININO,
        700: ORDINAL_700_FEMININO,
        800: ORDINAL_800_FEMININO,
        900: ORDINAL_900_FEMININO,
    }

    NOME_ORDINAL_POTENCIA_MASCULINO = {
        10 ** 3: ('milésimo', 'milésimo'),
        10 ** 6: ('milionésimo', 'milionésimo'),
        10 ** 9: ('bilionésimo', 'bilionésimo'),
        10 ** 12: ('trilionésimo', 'trilionésimo'),
        10 ** 15: ('quatrilionésimo', 'quatrilionésimo'),
        10 ** 18: ('quintilionésimo', 'quitilionésimo'),
        10 ** 21: ('sextilionésimo', 'sextilionésimo'),
        10 ** 24: ('setilionésimo', 'setilionésimo'),
        10 ** 27: ('octilionésimo', 'octilionésimo'),
        10 ** 30: ('nonilionésimo', 'nonilionésimo'),
        10 ** 33: ('decilionésimo', 'decilionésimo'),
        10 ** 36: ('undecilionésimo', 'undecilionésimo'),
        10 ** 39: ('dodecilionésimo', 'duodecilionésimo'),
        10 ** 42: ('tredecilionésimo', 'tredecilionésimo'),
        10 ** 45: ('quatuordecilionésimo', 'quatuordecilionésimo'),
        10 ** 48: ('quindecilionésimo', 'quindecilionésimo'),
        10 ** 51: ('sesdecilionésimo', 'sesdecilionésimo'),
        10 ** 54: ('septendecilionésimo', 'septendecilionésimo'),
        10 ** 57: ('octodecilionésimo', 'octodecilionésimo'),
        10 ** 60: ('nonidecilionésimo', 'nonidecilionésimo'),
    }

    NOME_ORDINAL_POTENCIA_FEMININO = {
        10 ** 3: ('milésima', 'milésima'),
        10 ** 6: ('milionésima', 'milionésima'),
        10 ** 9: ('bilionésima', 'bilionésima'),
        10 ** 12: ('trilionésima', 'trilionésima'),
        10 ** 15: ('quatrilionésima', 'quatrilionésima'),
        10 ** 18: ('quintilionésima', 'quintilionésima'),
        10 ** 21: ('sextilionésima', 'sextilionésima'),
        10 ** 24: ('setilionésima', 'setilionésima'),
        10 ** 27: ('octilionésima', 'octilionésima'),
        10 ** 30: ('nonilionésima', 'nonilionésima'),
        10 ** 33: ('decilionésima', 'decilionésima'),
        10 ** 36: ('undecilionésima', 'undecilionésima'),
        10 ** 39: ('dodecilionésima', 'duodecilionésima'),
        10 ** 42: ('tredecilionésima', 'tredecilionésima'),
        10 ** 45: ('quatuordecilionésima', 'quatuordecilionésima'),
        10 ** 48: ('quindecilionésima', 'quindecilionésima'),
        10 ** 51: ('sesdecilionésima', 'sesdecilionésima'),
        10 ** 54: ('septendecilionésima', 'septendecilionésima'),
        10 ** 57: ('octodecilionésima', 'octodecilionésima'),
        10 ** 60: ('nonidecilionésima', 'nonidecilionésima'),
    }

    EXTENSO = {
        CARDINAL: {
            MASCULINO: CARDINAL_MASCULINO,
            FEMININO: CARDINAL_FEMININO,
        },
        ORDINAL: {
            MASCULINO: ORDINAL_MASCULINO,
            FEMININO: ORDINAL_FEMININO,
        }
    }

    NOME_POTENCIA = {
        CARDINAL: {
            MASCULINO: NOME_CARDINAL_POTENCIA,
            FEMININO: NOME_CARDINAL_POTENCIA,
        },
        ORDINAL: {
            MASCULINO: NOME_ORDINAL_POTENCIA_MASCULINO,
            FEMININO: NOME_ORDINAL_POTENCIA_FEMININO,
        },
    }

    VALOR_MAXIMO = (max(NOME_CARDINAL_POTENCIA) * 1000) - 1


def numero_por_extenso(numero=0):
    return NumeroPorExtensoEuropeu(numero).extenso_cardinal


def numero_por_extenso_ordinal(numero=0, genero_unidade_masculino=True):
    return NumeroPorExtensoEuropeu(numero, genero_unidade_masculino).extenso_ordinal


def numero_por_extenso_unidade(numero=0, unidade=('real', 'reais'), genero_unidade_masculino=True,
                               precisao_decimal=2, unidade_decimal=('centavo', 'centavos'),
                               genero_unidade_decimal_masculino=True,
                               mascara_negativo=('menos %s', 'menos %s'),
                               fator_relacao_decimal=1):
    return NumeroPorExtensoEuropeu(numero, unidade, genero_unidade_masculino,
                            precisao_decimal, unidade_decimal, genero_unidade_decimal_masculino,
                            mascara_negativo, fator_relacao_decimal).extenso_unidade
