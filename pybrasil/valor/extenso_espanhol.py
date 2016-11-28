#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Números por extenso, cardinais, ordinais e cardinais com unidades de medida

Compatível com as versones 2 e 3 do Python
'''

from __future__ import division, print_function, unicode_literals

import re
from decimal import Decimal as D
from .extenso import NumeroPorExtenso, CARDINAL, MASCULINO, FEMININO, ORDINAL


class NumeroPorExtensoEspanhol(NumeroPorExtenso):
    CARDINAL_0 = 'cero'
    CARDINAL_1 = 'uno'
    CARDINAL_2 = 'dos'
    CARDINAL_3 = 'tres'
    CARDINAL_4 = 'cuatro'
    CARDINAL_5 = 'cinco'
    CARDINAL_6 = 'seis'
    CARDINAL_7 = 'siete'
    CARDINAL_8 = 'ocho'
    CARDINAL_9 = 'nueve'

    CARDINAL_10 = 'diez'
    CARDINAL_11 = 'once'
    CARDINAL_12 = 'doce'
    CARDINAL_13 = 'trece'
    CARDINAL_14 = 'catorce'
    CARDINAL_15 = 'quince'
    CARDINAL_16 = 'dieciséis'
    CARDINAL_17 = 'diecisiete'
    CARDINAL_18 = 'dieciocho'
    CARDINAL_19 = 'diecinueve'
    CARDINAL_20 = 'veinte'
    CARDINAL_21 = 'veintiuno'
    CARDINAL_22 = 'veintidós'
    CARDINAL_23 = 'veintitrés'
    CARDINAL_24 = 'veinticuatro'
    CARDINAL_25 = 'veinticinco'
    CARDINAL_26 = 'veintiséis'
    CARDINAL_27 = 'veintisiete'
    CARDINAL_28 = 'veintiocho'
    CARDINAL_29 = 'veintinueve'
    CARDINAL_30 = 'treinta'
    CARDINAL_40 = 'cuarenta'
    CARDINAL_50 = 'cincuenta'
    CARDINAL_60 = 'sesenta'
    CARDINAL_70 = 'setenta'
    CARDINAL_80 = 'ochenta'
    CARDINAL_90 = 'noventa'

    CARDINAL_100_ISOLADO = 'cien'

    CARDINAL_100 = 'ciento'
    CARDINAL_200 = 'doscientos'
    CARDINAL_300 = 'trescientos'
    CARDINAL_400 = 'cuatrocientos'
    CARDINAL_500 = 'quinientos'
    CARDINAL_600 = 'seiscientos'
    CARDINAL_700 = 'setecientos'
    CARDINAL_800 = 'ochocientos'
    CARDINAL_900 = 'novecientos'

    CARDINAL_1_FEMININO = 'una'
    CARDINAL_21_FEMININO = 'vientiuna'

    CARDINAL_200_FEMININO = 'docientas'
    CARDINAL_300_FEMININO = 'trecientas'
    CARDINAL_400_FEMININO = 'cuatrocientas'
    CARDINAL_500_FEMININO = 'quinientas'
    CARDINAL_600_FEMININO = 'seiscientas'
    CARDINAL_700_FEMININO = 'setecientas'
    CARDINAL_800_FEMININO = 'ochocientas'
    CARDINAL_900_FEMININO = 'novecientas'

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
        21: CARDINAL_21,
        22: CARDINAL_22,
        23: CARDINAL_23,
        24: CARDINAL_24,
        25: CARDINAL_25,
        26: CARDINAL_26,
        27: CARDINAL_27,
        28: CARDINAL_28,
        29: CARDINAL_29,
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
        21: CARDINAL_21_FEMININO,
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
        10 ** 6: ('millón', 'millones'),
        #10 ** 9: ('mil millones', 'mil millones'),
        10 ** 12: ('billón', 'billones'),
        #10 ** 15: ('mil billones', 'mil billones'),
        10 ** 18: ('trillón', 'trillones'),
        #10 ** 21: ('mil trillones', 'mil trillones'),
        10 ** 24: ('quatrillón', 'quatrillones'),
        #10 ** 27: ('mil quatrillones', 'mil quatrillones'),
        10 ** 30: ('quintillón', 'quintillones'),
        #10 ** 33: ('mil quintillones', 'mil quintillones'),
        10 ** 36: ('sextillón', 'sextillones'),
        #10 ** 39: ('mil sextillones', 'mil sextillones'),
        10 ** 42: ('septillón', 'septillones'),
        #10 ** 45: ('mil septillones', 'mil septillones'),
        10 ** 48: ('octillón', 'octillones'),
        #10 ** 51: ('mil octillones', 'mil octillones'),
        10 ** 54: ('nonillón', 'nonillones'),
        #10 ** 57: ('mil nonillones', 'mil nonillones'),
        10 ** 60: ('decillón', 'decillones'),
        #10 ** 36: ('undecillón', 'undecillones'),
        #10 ** 39: ('dodecillón', 'duodecillones'),
        #10 ** 42: ('tredecillón', 'tredecillones'),
        #10 ** 45: ('quatuordecillón', 'quatuordecillones'),
        #10 ** 48: ('quindecillón', 'quindecillones'),
        #10 ** 51: ('sesdecillón', 'sesdecillones'),
        #10 ** 54: ('septendecillón', 'septendecillones'),
        #10 ** 57: ('octodecillón', 'octodecillones'),
        #10 ** 60: ('nonidecillón', 'nonidecillones'),
    }

    REGRA_UNO_UN = re.compile(r'uno (.il.*)')

    ORDINAL_1 = 'primero'
    ORDINAL_1_ANTES_DE_VOGAL = 'primer'
    ORDINAL_2 = 'segundo'
    ORDINAL_3 = 'tercero'
    ORDINAL_4 = 'cuarto'
    ORDINAL_5 = 'quinto'
    ORDINAL_6 = 'sexto'
    ORDINAL_7 = 'séptimo'
    ORDINAL_8 = 'octavo'
    ORDINAL_9 = 'novena'

    ORDINAL_10 = 'décimo'
    ORDINAL_11 = 'undécimo'
    ORDINAL_12 = 'duodécimo'
    ORDINAL_13 = ORDINAL_10.replace('é', 'e') + ORDINAL_3
    ORDINAL_14 = ORDINAL_10.replace('é', 'e') + ORDINAL_4
    ORDINAL_15 = ORDINAL_10.replace('é', 'e') + ORDINAL_5
    ORDINAL_16 = ORDINAL_10.replace('é', 'e') + ORDINAL_6
    ORDINAL_17 = ORDINAL_10.replace('é', 'e') + ORDINAL_7
    ORDINAL_18 = 'decimoctavo'
    ORDINAL_19 = ORDINAL_10.replace('é', 'e') + ORDINAL_9
    ORDINAL_20 = 'vigésimo'
    ORDINAL_30 = 'trigésimo'
    ORDINAL_40 = 'cuadragésimo'
    ORDINAL_50 = 'quincuagésimo'
    ORDINAL_60 = 'sexagésimo'
    ORDINAL_70 = 'septuagésimo'
    ORDINAL_80 = 'octagésimo'
    ORDINAL_90 = 'nonagésimo'

    ORDINAL_100 = 'centésimo'
    ORDINAL_200 = 'ducentésimo'
    ORDINAL_300 = 'tricentésimo'
    ORDINAL_400 = 'cuadringentésimo'
    ORDINAL_500 = 'quincuagentésimo'
    ORDINAL_600 = 'sexcentésimo'
    ORDINAL_700 = 'septuagentésimo'
    ORDINAL_800 = 'octingentésimo'
    ORDINAL_900 = 'noningentésimo'

    ORDINAL_1_FEMININO = 'primera'
    ORDINAL_2_FEMININO = 'segunda'
    ORDINAL_3_FEMININO = 'tercera'
    ORDINAL_4_FEMININO = 'cuarta'
    ORDINAL_5_FEMININO = 'quinta'
    ORDINAL_6_FEMININO = 'sexta'
    ORDINAL_7_FEMININO = 'séptima'
    ORDINAL_8_FEMININO = 'octava'
    ORDINAL_9_FEMININO = 'novena'

    ORDINAL_10_FEMININO = 'décima'
    ORDINAL_11_FEMININO = 'undécima'
    ORDINAL_12_FEMININO = 'duodécima'
    ORDINAL_13_FEMININO = ORDINAL_10_FEMININO.replace('é', 'e') + ORDINAL_3_FEMININO
    ORDINAL_14_FEMININO = ORDINAL_10_FEMININO.replace('é', 'e') + ORDINAL_4_FEMININO
    ORDINAL_15_FEMININO = ORDINAL_10_FEMININO.replace('é', 'e') + ORDINAL_5_FEMININO
    ORDINAL_16_FEMININO = ORDINAL_10_FEMININO.replace('é', 'e') + ORDINAL_6_FEMININO
    ORDINAL_17_FEMININO = ORDINAL_10_FEMININO.replace('é', 'e') + ORDINAL_7_FEMININO
    ORDINAL_18_FEMININO = 'decimoctava'
    ORDINAL_19_FEMININO = ORDINAL_10_FEMININO.replace('é', 'e') + ORDINAL_9_FEMININO
    ORDINAL_20_FEMININO = 'vigésima'
    ORDINAL_30_FEMININO = 'trigésima'
    ORDINAL_40_FEMININO = 'cuadragésima'
    ORDINAL_50_FEMININO = 'quincuagésima'
    ORDINAL_60_FEMININO = 'sexagésima'
    ORDINAL_70_FEMININO = 'septuagésima'
    ORDINAL_80_FEMININO = 'octagésima'
    ORDINAL_90_FEMININO = 'nonagésima'

    ORDINAL_100_FEMININO = 'centésima'
    ORDINAL_200_FEMININO = 'ducentésima'
    ORDINAL_300_FEMININO = 'tricentésima'
    ORDINAL_400_FEMININO = 'cuadringentésima'
    ORDINAL_500_FEMININO = 'quincuagentésima'
    ORDINAL_600_FEMININO = 'sexcentésima'
    ORDINAL_700_FEMININO = 'septuagentésima'
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

    def _centena_dezena_unidade(self, numero, tipo=CARDINAL, genero=MASCULINO):
        assert 0 <= numero < 1000

        #
        # Tratamento especial do número 100
        #
        if (numero == 100) and (tipo == CARDINAL):
            return self.CARDINAL_100_ISOLADO

        if numero in self.EXTENSO[tipo][genero]:
            return self.EXTENSO[tipo][genero][numero]

        potencia_10 = int(10 ** int(D(numero).log10()))
        cabeca = int(numero / potencia_10) * potencia_10
        corpo = int(numero % potencia_10)

        if tipo == CARDINAL:
            if cabeca < 100:
                return self._centena_dezena_unidade(cabeca, CARDINAL, genero) + ' y ' + self._centena_dezena_unidade(corpo, tipo, genero)

            else:
                return self.EXTENSO[tipo][genero][cabeca] + ' ' + self._centena_dezena_unidade(corpo, tipo, genero)
        else:
            return self.EXTENSO[tipo][genero][cabeca] + ' ' + self._centena_dezena_unidade(corpo, tipo, genero)

    def _potencia(self, numero, tipo=CARDINAL, genero=MASCULINO):
        potencia_10 = 1000 ** int((len(str(int(numero))) - 1) / 3)

        if potencia_10 <= 100:
            return self._centena_dezena_unidade(numero, tipo, genero)

        este_grupo = int(numero / potencia_10)
        proximo_grupo = numero - (este_grupo * potencia_10)

        #
        # Nome da potencia
        #
        if potencia_10 in self.NOME_POTENCIA[tipo][genero]:
            nome_potencia = self.NOME_POTENCIA[tipo][genero][potencia_10][este_grupo > 1]
        else:
            nome_potencia = 'mil ' + self.NOME_POTENCIA[tipo][genero][potencia_10 / 1000][1]

        if (potencia_10 / 1000) in self.NOME_POTENCIA[tipo][genero]:
            potencia_anterior = self.NOME_POTENCIA[tipo][genero][potencia_10 / 1000][1]
        else:
            potencia_anterior = ''

        #
        # Tratamento especial para o número 1.000:
        #     cardinais:
        #         uno mil -> mil
        #         una mil -> mil
        #
        if (tipo == CARDINAL) and (este_grupo == 1) and (nome_potencia == 'mil' or nome_potencia.startswith('mil ')):
            texto = ''

        #
        # Tratamento especial para os números 1.000, 1.000.000 etc.
        #     ordinais:
        #         primero milésimo -> milésimo
        #         primera milésima -> milésima
        #         primero milionésimo -> milionésimo
        #         primera milionésima -> milionésima
        #
        elif (tipo == ORDINAL) and (potencia_10 >= 1000) and (este_grupo == 1):
            texto = ''

        else:
            #
            # Nos número cardinais, o gênero feminino só é usado até os milhares
            #
            if (tipo == CARDINAL) and (potencia_10 > 1000):
                texto = self._centena_dezena_unidade(este_grupo, tipo, MASCULINO)
            else:
                texto = self._centena_dezena_unidade(este_grupo, tipo, genero)

        if len(texto):
            texto += ' '

        texto += nome_potencia
        texto = self.REGRA_UNO_UN.sub(r'un \1', texto)

        #
        # Conexão entre os grupos
        #
        if proximo_grupo > 0:
            if tipo == CARDINAL:
                texto += ', '
            else:
                texto += ' '

            texto += self._potencia(proximo_grupo, tipo, genero)

            if potencia_anterior:
                texto = texto.replace(' ' + potencia_anterior + ', ', ' ', 1)

        return texto


def numero_por_extenso(numero=0):
    return NumeroPorExtensoEspanhol(numero).extenso_cardinal


def numero_por_extenso_ordinal(numero=0, genero_unidade_masculino=True):
    return NumeroPorExtensoEspanhol(numero, genero_unidade_masculino).extenso_ordinal


def numero_por_extenso_unidade(numero=0, unidade=('real', 'reais'), genero_unidade_masculino=True,
                               precisao_decimal=2, unidade_decimal=('centavo', 'centavos'),
                               genero_unidade_decimal_masculino=True,
                               mascara_negativo=('menos %s', 'menos %s'),
                               fator_relacao_decimal=1):
    return NumeroPorExtensoEspanhol(numero, unidade, genero_unidade_masculino,
                            precisao_decimal, unidade_decimal, genero_unidade_decimal_masculino,
                            mascara_negativo, fator_relacao_decimal).extenso_unidade
