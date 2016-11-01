#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Números por extenso, cardinais, ordinais e cardinais com unidades de medida

Compatível com as versões 2 e 3 do Python
'''

from __future__ import division, print_function, unicode_literals

from decimal import Decimal as D
from .extenso import NumeroPorExtenso, SINGULAR, PLURAL, CARDINAL, MASCULINO, FEMININO


class NumeroPorExtensoIngles(NumeroPorExtenso):
    CARDINAL_0 = 'zero'
    CARDINAL_1 = 'one'
    CARDINAL_2 = 'two'
    CARDINAL_3 = 'three'
    CARDINAL_4 = 'four'
    CARDINAL_5 = 'five'
    CARDINAL_6 = 'six'
    CARDINAL_6_TELEFONE = 'meia'
    CARDINAL_7 = 'seven'
    CARDINAL_8 = 'eight'
    CARDINAL_9 = 'nine'

    CARDINAL_10 = 'ten'
    CARDINAL_11 = 'eleven'
    CARDINAL_12 = 'twelve'
    CARDINAL_13 = 'thirteen'
    CARDINAL_14 = 'fourteen'
    CARDINAL_15 = 'fifteen'
    CARDINAL_16 = 'sixteen'
    CARDINAL_17 = 'seventeen'
    CARDINAL_18 = 'eighteen'
    CARDINAL_19 = 'nineteen'
    CARDINAL_20 = 'twenty'
    CARDINAL_30 = 'thirty'
    CARDINAL_40 = 'fourty'
    CARDINAL_50 = 'fifty'
    CARDINAL_60 = 'sixty'
    CARDINAL_70 = 'seventy'
    CARDINAL_80 = 'eighty'
    CARDINAL_90 = 'ninety'

    CARDINAL_100 = 'hundred'

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
    }

    CARDINAL_FEMININO = CARDINAL_MASCULINO.copy()

    NOME_CARDINAL_POTENCIA = {
        10 ** 3: ('thousand', 'thousand'),
        10 ** 6: ('million', 'million'),
        10 ** 9: ('billion', 'billion'),
        #10 ** 12: ('trilhão', 'trilhões'),
        #10 ** 15: ('quatrilhão', 'quatrilhões'),
        #10 ** 18: ('quintilhão', 'quintilhões'),
        #10 ** 21: ('sextilhão', 'sextilhões'),
        #10 ** 24: ('setilhão', 'setilhões'),
        #10 ** 27: ('octilhão', 'octilhões'),
        #10 ** 30: ('nonilhão', 'nonilhões'),
        #10 ** 33: ('decilhão', 'decilhões'),
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

    SUFIXO_ORDINAL = 'th'
    ORDINAL_1 = 'first'
    ORDINAL_2 = 'second'
    ORDINAL_3 = 'third'
    ORDINAL_5 = 'fifth'
    ORDINAL_8 = 'eighth'
    ORDINAL_9 = 'ninth'
    ORDINAL_12 = 'twelfth'

    ORDINAL_ESPECIAL = {
        CARDINAL_1: ORDINAL_1,
        CARDINAL_2: ORDINAL_2,
        CARDINAL_3: ORDINAL_3,
        CARDINAL_5: ORDINAL_5,
        CARDINAL_8: ORDINAL_8,
        CARDINAL_9: ORDINAL_9,
        CARDINAL_12: ORDINAL_12,
    }

    EXTENSO = {
        CARDINAL: {
            MASCULINO: CARDINAL_MASCULINO,
            FEMININO: CARDINAL_MASCULINO,
        },
    }

    NOME_POTENCIA = {
        CARDINAL: {
            MASCULINO: NOME_CARDINAL_POTENCIA,
            FEMININO: NOME_CARDINAL_POTENCIA,
        },
    }

    VALOR_MAXIMO = (max(NOME_CARDINAL_POTENCIA) * 1000) - 1

    def _centena_dezena_unidade(self, numero, tipo=CARDINAL, genero=MASCULINO):
        assert 0 <= numero < 1000

        if numero in self.EXTENSO[tipo][genero] and numero != 100:
            return self.EXTENSO[tipo][genero][numero]

        potencia_10 = int(10 ** int(D(numero).log10()))
        cabeca = int(numero / potencia_10) * potencia_10
        corpo = int(numero % potencia_10)

        #
        # Caso especial centena
        #
        centena = False
        if cabeca >= 100:
            centena = True
            cabeca = cabeca / 100

        if centena:
            if corpo:
                return self._centena_dezena_unidade(cabeca, CARDINAL, genero) + ' ' + self.CARDINAL_100 + ' and ' + self._centena_dezena_unidade(corpo, tipo, genero)
            else:
                return self._centena_dezena_unidade(cabeca, CARDINAL, genero) + ' ' + self.CARDINAL_100

        else:
            return self.EXTENSO[tipo][genero][cabeca] + '-' + self._centena_dezena_unidade(corpo, tipo, genero)

    def _potencia(self, numero, tipo=CARDINAL, genero=MASCULINO):
        potencia_10 = 1000 ** int((len(str(int(numero))) - 1) / 3)

        if potencia_10 <= 100:
            return self._centena_dezena_unidade(numero, tipo, genero)

        este_grupo = int(numero / potencia_10)
        proximo_grupo = numero - (este_grupo * potencia_10)

        texto = self._centena_dezena_unidade(este_grupo, CARDINAL, MASCULINO)

        if len(texto):
            texto += ' '

        texto += self.NOME_POTENCIA[tipo][genero][potencia_10][este_grupo > 1]

        #
        # Conexão entre os grupos
        #
        if proximo_grupo > 0:
            tamanho = len(str(proximo_grupo)) % 3 or 3
            proximo_grupo_3 = int(str(proximo_grupo)[:tamanho])
            proximo_grupo_zeros = int(str(proximo_grupo)[tamanho:] or '0')
            if proximo_grupo in self.EXTENSO[tipo][genero]:
                texto += ' and '
            elif proximo_grupo_3 in self.EXTENSO[tipo][genero] and proximo_grupo_zeros == 0:
                texto += ' and '
            else:
                texto += ', '

            texto += self._potencia(proximo_grupo, tipo, genero)

        return texto

    def get_extenso_ordinal(self):
        '''
        Número ordinal sem unidade
        '''
        if self._numero == 0:
            return ''

        texto = self._potencia(abs(int(self.numero)), tipo=CARDINAL, genero=self.genero_unidade_masculino)
        print(texto)
        #
        # Em inglês, só o último número é colocado no ordinal
        # e há somente 7 exceções
        #
        especial = False

        for cardinal, ordinal in self.ORDINAL_ESPECIAL.items():
            if texto.endswith(cardinal):
                texto = texto[::-1]
                texto = texto[len(cardinal):]
                texto = texto[::-1]
                texto += ordinal
                especial = True
                break

        if not especial:
            texto += self.SUFIXO_ORDINAL

        return texto

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
                texto_inteiro += ' ' + self.unidade[PLURAL]

        #
        # Extenso da parte decimal
        #
        if decimal > 0:
            texto_decimal = self._potencia(decimal, genero=self.genero_unidade_decimal_masculino)

            if (decimal == 1) and (len(self.unidade_decimal[SINGULAR])):
                texto_decimal += ' ' + self.unidade_decimal[SINGULAR]
            elif len(self.unidade_decimal[PLURAL]):
                texto_decimal += ' ' + self.unidade_decimal[PLURAL]

        if (inteiro > 0) and (decimal > 0):
            texto = texto_inteiro + ' and ' + texto_decimal
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


def numero_por_extenso(numero=0):
    return NumeroPorExtensoIngles(numero).extenso_cardinal


def numero_por_extenso_ordinal(numero=0, genero_unidade_masculino=True):
    return NumeroPorExtensoIngles(numero, genero_unidade_masculino).extenso_ordinal


def numero_por_extenso_unidade(numero=0, unidade=('real', 'reais'), genero_unidade_masculino=True,
                               precisao_decimal=2, unidade_decimal=('centavo', 'centavos'),
                               genero_unidade_decimal_masculino=True,
                               mascara_negativo=('minus %s', 'minus %s'),
                               fator_relacao_decimal=1):
    return NumeroPorExtensoIngles(numero, unidade, genero_unidade_masculino,
        precisao_decimal, unidade_decimal, genero_unidade_decimal_masculino,
        mascara_negativo, fator_relacao_decimal).extenso_unidade
