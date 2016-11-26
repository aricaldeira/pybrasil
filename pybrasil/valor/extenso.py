#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Números por extenso, cardinais, ordinais e cardinais com unidades de medida

Compatível com as versões 2 e 3 do Python
'''

from __future__ import division, print_function, unicode_literals

from pybrasil.valor.decimal import Decimal as D
from fractions import Fraction as F

PLURAL = 1
SINGULAR = 0

CARDINAL = 1
ORDINAL = 0

MASCULINO = 1
FEMININO = 0


FRACOES = {
    F(1, 2): '½',
    F(1, 3): '⅓',
    F(2, 3): '⅔',
    F(1, 4): '¼',
    F(3, 4): '¾',
    F(1, 5): '⅕',
    F(2, 5): '⅖',
    F(3, 5): '⅗',
    F(4, 5): '⅘',
    F(1, 6): '⅙',
    F(5, 6): '⅚',
    F(1, 7): '⅐',
    F(1, 8): '⅛',
    F(3, 8): '⅜',
    F(5, 8): '⅝',
    F(7, 8): '⅞',
    F(1, 9): '⅑',
    F(1, 10): '⅒',
}

class NumeroPorExtenso(object):
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
    CARDINAL_16 = 'dezesseis'
    CARDINAL_17 = 'dezessete'
    CARDINAL_18 = 'dezoito'
    CARDINAL_19 = 'dezenove'
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
        10 ** 9: ('bilhão', 'bilhões'),
        10 ** 12: ('trilhão', 'trilhões'),
        10 ** 15: ('quatrilhão', 'quatrilhões'),
        10 ** 18: ('quintilhão', 'quintilhões'),
        10 ** 21: ('sextilhão', 'sextilhões'),
        10 ** 24: ('setilhão', 'setilhões'),
        10 ** 27: ('octilhão', 'octilhões'),
        10 ** 30: ('nonilhão', 'nonilhões'),
        10 ** 33: ('decilhão', 'decilhões'),
        10 ** 36: ('undecilhão', 'undecilhões'),
        10 ** 39: ('dodecilhão', 'duodecilhões'),
        10 ** 42: ('tredecilhão', 'tredecilhões'),
        10 ** 45: ('quatuordecilhão', 'quatuordecilhões'),
        10 ** 48: ('quindecilhão', 'quindecilhões'),
        10 ** 51: ('sesdecilhão', 'sesdecilhões'),
        10 ** 54: ('septendecilhão', 'septendecilhões'),
        10 ** 57: ('octodecilhão', 'octodecilhões'),
        10 ** 60: ('nonidecilhão', 'nonidecilhões'),
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
    ORDINAL_80 = 'octagésimo'
    ORDINAL_90 = 'nonagésimo'

    ORDINAL_100 = 'centésimo'
    ORDINAL_200 = 'ducentésimo'
    ORDINAL_300 = 'tricentésimo'
    ORDINAL_400 = 'quadringentésimo'
    ORDINAL_500 = 'quinquagentésimo'
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
    ORDINAL_80_FEMININO = 'octagésima'
    ORDINAL_90_FEMININO = 'nonagésima'

    ORDINAL_100_FEMININO = 'centésima'
    ORDINAL_200_FEMININO = 'ducentésima'
    ORDINAL_300_FEMININO = 'tricentésima'
    ORDINAL_400_FEMININO = 'quadringentésima'
    ORDINAL_500_FEMININO = 'quinquagentésima'
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

    def __init__(self, numero=0, unidade=('real', 'reais'), genero_unidade_masculino=True,
                 precisao_decimal=2, unidade_decimal=('centavo', 'centavos'),
                 genero_unidade_decimal_masculino=True, mascara_negativo=('menos %s', 'menos %s'),
                 fator_relacao_decimal=10, usa_meio=False, usa_fracao=False, usa_virgula=False):
        self.numero = D(numero or 0)
        self.unidade = unidade
        self.genero_unidade_masculino = genero_unidade_masculino
        self.precisao_decimal = precisao_decimal
        self.fator_relacao_decimal = fator_relacao_decimal
        self.unidade_decimal = unidade_decimal
        self.genero_unidade_decimal_masculino = genero_unidade_decimal_masculino
        self.mascara_negativo = mascara_negativo
        self.usa_meio = usa_meio
        self.usa_fracao = usa_fracao
        self.usa_virgula = usa_virgula

    def get_numero(self):
        return self._numero

    def set_numero(self, valor):
        if D(str(valor)) > self.VALOR_MAXIMO:
            raise OverflowError('valor maior do que o máximo permitido: %s' % self.VALOR_MAXIMO)

        self._numero = D(str(valor))

    numero = property(get_numero, set_numero)

    def get_fator_relacao_decimal(self):
        return self._fator_relacao_decimal

    def set_fator_relacao_decimal(self, valor):
        self._fator_relacao_decimal = D(str(valor)) / D('10')

    fator_relacao_decimal = property(get_fator_relacao_decimal, set_fator_relacao_decimal)

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
            return self.EXTENSO[tipo][genero][cabeca] + ' e ' + self._centena_dezena_unidade(corpo, tipo, genero)
        else:
            return self.EXTENSO[tipo][genero][cabeca] + ' ' + self._centena_dezena_unidade(corpo, tipo, genero)

    def _potencia(self, numero, tipo=CARDINAL, genero=MASCULINO):
        potencia_10 = 1000 ** int((len(str(int(numero))) - 1) / 3)

        if potencia_10 <= 100:
            return self._centena_dezena_unidade(numero, tipo, genero)

        este_grupo = int(numero / potencia_10)
        proximo_grupo = numero - (este_grupo * potencia_10)

        #
        # Tratamento especial para o número 1.000:
        #     cardinais:
        #         um mil -> mil
        #         uma mil -> mil
        #
        if (tipo == CARDINAL) and (potencia_10 == 1000) and (este_grupo == 1):
            texto = ''

        #
        # Tratamento especial para os números 1.000, 1.000.000 etc.
        #     ordinais:
        #         primeiro milésimo -> milésimo
        #         primeira milésima -> milésima
        #         primeiro milionésimo -> milionésimo
        #         primeira milionésima -> milionésima
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

        texto += self.NOME_POTENCIA[tipo][genero][potencia_10][este_grupo > 1]

        #
        # Conexão entre os grupos
        #
        if proximo_grupo > 0:
            if tipo == CARDINAL:
                tamanho = len(str(proximo_grupo)) % 3 or 3
                proximo_grupo_3 = int(str(proximo_grupo)[:tamanho])
                proximo_grupo_zeros = int(str(proximo_grupo)[tamanho:] or '0')
                if proximo_grupo in self.EXTENSO[tipo][genero]:
                    texto += ' e '
                elif proximo_grupo_3 in self.EXTENSO[tipo][genero] and proximo_grupo_zeros == 0:
                    texto += ' e '
                elif potencia_10 != 1000:
                    texto += ', '
                elif potencia_10 == 1000 and proximo_grupo_3 > 0 and proximo_grupo_3 <= 100:
                    texto += ' e '
                else:
                    texto += ' '
            else:
                texto += ' '

            texto += self._potencia(proximo_grupo, tipo, genero)

        return texto

    def get_extenso_cardinal(self):
        '''
        Número cardinal sem unidade, somente a parte inteira, somente números positivos
        '''
        if self.genero_unidade_masculino:
            return self._potencia(abs(int(self.numero)), tipo=CARDINAL, genero=MASCULINO)
        else:
            return self._potencia(abs(int(self.numero)), tipo=CARDINAL, genero=FEMININO)

    extenso_cardinal = property(get_extenso_cardinal)

    def get_extenso_ordinal(self):
        '''
        Número ordinal sem unidade, considerando o gênero da unidade
        '''
        if self._numero == 0:
            return ''

        return self._potencia(abs(int(self.numero)), tipo=ORDINAL, genero=self.genero_unidade_masculino)

    extenso_ordinal = property(get_extenso_ordinal)

    def get_extenso_unidade(self):
        '''
        Número ordinal com unidade, parte inteira e decimal, com tratamento de negativos
        '''
        #
        # Tratamento do zero, cuja unidade é sempre no plural: zero reais, zero graus etc.
        #
        if self.numero == 0:
            texto = self.CARDINAL_0

            if len(self.unidade[PLURAL]):
                texto += ' ' + self.unidade[PLURAL]

            return texto

        #
        # Separação da parte decimal com a precisão desejada
        #
        negativo = self.numero < 0
        numero = abs(self.numero)
        inteiro = int(numero)
        decimal = int(((numero - inteiro) * self.fator_relacao_decimal) * (10 ** self.precisao_decimal))

        #
        # Extenso da parte inteira
        #
        if inteiro > 0:
            texto_inteiro = self._potencia(inteiro, genero=self.genero_unidade_masculino)

            if (inteiro == 1) and (len(self.unidade[SINGULAR])):
                texto_inteiro += ' ' + self.unidade[SINGULAR]
            elif len(self.unidade[PLURAL]):
                #
                # De milhão pra cima, acrescenta ' de ' antes da unidade
                #
                if texto_inteiro[-2:] == 'ão' or texto_inteiro[-3:] == 'ões':
                    if decimal > 0:
                        fracao = F(str(numero - inteiro))

                        if self.usa_meio and fracao == F(1, 2):
                            texto_inteiro += ' e meio'
                            #palavras = texto_inteiro.split()
                            #palavras.insert(-1, 'e meio')
                            #palavras[-1] = palavras[-1].replace('ão', 'ões')
                            #texto_inteiro = ' '.join(palavras)
                            decimal = 0

                    texto_inteiro += ' de'

                texto_inteiro += ' ' + self.unidade[PLURAL]

        #
        # Extenso da parte decimal
        #
        usa_com = False

        if decimal > 0:
            if ' com ' in self.unidade[PLURAL] or ' de ' in self.unidade[PLURAL]:
                usa_com = True

            fracao = F(str(numero - inteiro))

            if self.usa_meio and fracao == F(1, 2):
                if self.genero_unidade_masculino:
                    texto_decimal = 'meio'
                else:
                    texto_decimal = 'meia'

                if inteiro == 0 and (not usa_com):
                    texto_decimal += ' ' + self.unidade[SINGULAR]

            #elif self.usa_fracao and fracao in FRACOES:
                #texto_decimal = FRACOES[fracao]

            else:
                if not self.usa_virgula:
                    texto_decimal = self._potencia(decimal, genero=self.genero_unidade_decimal_masculino)
                    if (decimal == 1) and (len(self.unidade_decimal[SINGULAR])):
                        texto_decimal += ' ' + self.unidade_decimal[SINGULAR]
                    elif len(self.unidade_decimal[PLURAL]):
                        texto_decimal += ' ' + self.unidade_decimal[PLURAL]
                else:
                    potencia_10 = int(10 ** int(D(decimal).log10()))
                    cabeca = int(decimal / potencia_10) * potencia_10
                    corpo = int(decimal % potencia_10)

                    if corpo == 0 and potencia_10 > 1:
                        cabeca = int(decimal / potencia_10)
                        texto_decimal = self._potencia(cabeca, genero=self.genero_unidade_masculino)

                    else:
                        texto_decimal = self._potencia(decimal, genero=self.genero_unidade_masculino)

                        if decimal > 0 and decimal < 10:
                            texto_decimal = 'zero ' + texto_decimal

                    if (decimal == 0) and len(self.unidade[PLURAL]):
                        texto_decimal += ' ' + self.unidade[PLURAL]

        if ((inteiro > 0) and (decimal > 0)) or (usa_com):
            if (not self.usa_virgula) or (self.usa_meio and fracao == F(1, 2)):
                if usa_com:
                    texto_inteiro = texto_inteiro.replace(self.unidade[PLURAL], '')
                    texto_inteiro = texto_inteiro.replace(self.unidade[SINGULAR], '')

                texto = texto_inteiro + ' e ' + texto_decimal

                if usa_com:
                    texto += ' ' + self.unidade[PLURAL]

            else:
                texto_inteiro = texto_inteiro.replace(self.unidade[PLURAL], '')
                texto_inteiro = texto_inteiro.replace(self.unidade[SINGULAR], '')
                palavras_inteiro = texto_inteiro.split()

                palavras_decimal = texto_decimal.split()

                if palavras_inteiro[-1] == 'de':
                    #palavras_decimal.append('de')
                    palavras_inteiro.pop(-1)

                #if 'ão' in palavras_inteiro[-1] or 'ões' in palavras_inteiro[-1]:
                    #palavras_inteiro[-1] = palavras_inteiro[-1].replace('ão', 'ões')

                    #if palavras_decimal[-1] == 'de':
                        #palavras_decimal.insert(-1, palavras_inteiro[-1])
                    #else:
                        #palavras_decimal.append(palavras_inteiro[-1])

                    #palavras_inteiro.pop(-1)

                texto_inteiro = ' '.join(palavras_inteiro)
                texto_decimal = ' '.join(palavras_decimal)

                if len(self.unidade[PLURAL]) and (not usa_com):
                    texto_decimal += ' ' + self.unidade[PLURAL]

                texto = texto_inteiro + ' vírgula ' + texto_decimal

                if usa_com:
                    texto += ' ' + self.unidade[PLURAL]

        elif inteiro > 0:
            texto = texto_inteiro
        else:
            texto = texto_decimal

        if negativo:
            if ((inteiro > 1) or (decimal > 1)):
                texto = self.mascara_negativo[PLURAL] % texto
            else:
                texto = self.mascara_negativo[SINGULAR] % texto

        return texto

    extenso_unidade = property(get_extenso_unidade)


def numero_por_extenso(numero=0, genero_unidade_masculino=True):
    return NumeroPorExtenso(numero=numero, genero_unidade_masculino=genero_unidade_masculino).extenso_cardinal


def numero_por_extenso_ordinal(numero=0, genero_unidade_masculino=True):
    return NumeroPorExtenso(numero=numero, genero_unidade_masculino=genero_unidade_masculino).extenso_ordinal


def numero_por_extenso_unidade(numero=0, unidade=('real', 'reais'), genero_unidade_masculino=True,
                               precisao_decimal=2, unidade_decimal=('centavo', 'centavos'),
                               genero_unidade_decimal_masculino=True,
                               mascara_negativo=('menos %s', 'menos %s'),
                               fator_relacao_decimal=10, usa_meio=False, usa_fracao=False, usa_virgula=False):
    return NumeroPorExtenso(numero, unidade, genero_unidade_masculino,
                            precisao_decimal, unidade_decimal, genero_unidade_decimal_masculino,
                            mascara_negativo, fator_relacao_decimal, usa_meio, usa_fracao, usa_virgula).extenso_unidade


if __name__ == '__main__':
    import sys

    e = NumeroPorExtenso(sys.argv[1])

    ##print('Numeral cardinal simples:', e.extenso_cardinal)
    ##print('Numeral ordinal simples:', e.extenso_ordinal)
    ##print('Valor monetário em R$:', e.extenso_unidade)

    ###
    ### Unidades sempre definidas na forma
    ### (unidade_no_singular, unidade_no_plural)
    ###
    ##e.unidade = ('quilo', 'quilos')
    ###
    ### 3 casas decimais de precisão, pois 1 quilograma são 1000 gramas
    ###
    ##e.precisao_decimal = 3
    ##e.unidade_decimal = ('grama', 'gramas')
    ##print('Valor em quilos e gramas (com 3 casas decimais de precisão):', e.extenso_unidade)

    ##e.unidade = ('tonelada', 'toneladas')
    ##e.genero_unidade_masculino = False
    ###
    ### 3 casas decimais de precisão, pois 1 tonelada são 1000 quilogramas
    ###
    ##e.precisao_decimal = 3
    ##e.unidade_decimal = ('quilo', 'quilos')
    ##e.genero_unidade_decimal_masculino = True
    ##print('Valor em toneladas (feminino) e quilos (masculino, com 3 casa decimais de precisão):', e.extenso_unidade)

    ##e.unidade = ('dia', 'dias')
    ##e.precisao_decimal = 1
    ##e.genero_unidade_masculino = True
    ##e.unidade_decimal = ('hora', 'horas')
    ##e.genero_unidade_decimal_masculino = False
    ###
    ### Se a relação entre a unidade e a unidade decimal não for, bem, decimal...
    ### No caso, se a precisão é 1; 0,1 dias são quantas horas?
    ###
    ##e.fator_relacao_decimal = D('2.4')
    ##print('Valor em dias e horas (com 1 casa decimal de precisão):', e.extenso_unidade)

    ##e.unidade = ('pé', 'pés')
    ##e.precisao_decimal = 2
    ##e.unidade_decimal = ('polegada', 'polegadas')
    ###
    ### Se a relação entre a unidade e a unidade decimal não for, bem, decimal...
    ### No caso, se a precisão é 2; 0,01 pés são quantas polegadas?
    ### Melhor informar em Decimal para evitar problemas de arredondamento
    ###
    ##e.fator_relacao_decimal = D('0.12')
    ##print('Valor em pés e polegadas (com 2 casas decimais de precisão):', e.extenso_unidade)

    ##e.unidade = ('grau Celsius', 'graus Celsius')
    ##e.genero_unidade_masculino = True
    ##e.precisao_decimal = 1
    ##e.unidade_decimal = ('décimo', 'décimos')
    ##e.genero_unidade_decimal_masculino = True
    ##print('Valor em graus Celsius e décimos (com 1 casa decimais de precisão):', e.extenso_unidade)

    ##e.unidade = ('ponto percentual', 'pontos percentuais')
    ##e.genero_unidade_masculino = True
    ##e.precisao_decimal = 0
    ##print('Valor em pontos percentuais (somente inteiros):', e.extenso_unidade)

    ##e.numero *= -1
    ##print('Valor em pontos percentuais negativos (somente inteiros):', e.extenso_unidade)

    ##e.unidade = ('grau Celsius', 'graus Celsius')
    ##e.mascara_negativo = ('%s negativo', '%s negativos')
    ##print('Valor em graus Celsius negativos:', e.extenso_unidade)

    e.usa_virgula = True
    e.usa_meio = True
    e.numero = '1.5'
    print(e.extenso_unidade)
    e.numero = '1000000.5'
    print(e.extenso_unidade)

    e.usa_meio = False
    e.numero = '1.5'
    print(e.extenso_unidade)
    e.numero = '1000000.5'
    print(e.extenso_unidade)

    e.numero = '1.1'
    print(e.extenso_unidade)
    e.numero = '1000000.1'
    print(e.extenso_unidade)

    e.numero = '1.11'
    print(e.extenso_unidade)
    e.numero = '1000000.11'
    print(e.extenso_unidade)

    e.numero = '1.01'
    print(e.extenso_unidade)
    e.numero = '1000000.01'
    print(e.extenso_unidade)
