# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)

import sys

if sys.version >= '3':
    unicode = str

import re

#
# Regras descompiladas e tiradas do validador do SPED PIS-COFINS
# Arquivo: lib/br.gov.serpro.vepxml/vepxml-validador-comum.jar
# Classe Java: br.gov.serpro.vepxml.validador.regras.campo.RegraValidaIE{UF}
#


#LIMPA = re.compile(r'^(?!.*P?[0-9]{2-14}).*$|^(?!.*ISENTO).*$')
LIMPA = re.compile(r'[^0-9PR]')


class ValidaIE(object):
    '''
    Superclasse para as validações das inscrições estaduais

    >>> valida_ie = ValidaIE()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    '''
    def __init__(self, **kwargs):
        self.dv = kwargs.get('dv', [])
        self.pesos = kwargs.get('pesos', [])
        self.posicoes = kwargs.get('posicoes', [])
        self.formato = kwargs.get('formato', [])
        self.expressao = kwargs.get('expressao', r'')
        self.resto = kwargs.get('resto', False)
        self.inicio_soma = kwargs.get('inicio_soma', 0)
        self.dv_acima_10 = kwargs.get('dv_acima_10', 0)
        self.dv_acima_11 = kwargs.get('dv_acima_11', 0)
        self.tamanho_minimo = kwargs.get('tamanho_minimo', 0)

    @property
    def expressao(self):
        return self._expressao

    @expressao.setter
    def expressao(self, texto):
        self._expressao = re.compile(texto)

    def soma(self, ie, pesos, posicoes):
        soma = self.inicio_soma

        for i in range(len(pesos)):
            peso = pesos[i]
            posicao = posicoes[i]
            numero = int(ie[posicao])
            soma += numero * peso

        return soma

    def modulo(self, ie, pesos, posicoes):
        soma = self.soma(ie, pesos, posicoes)
        return soma % 11

    def digito(self, ie, pesos, posicoes):
        modulo = self.modulo(ie, pesos, posicoes)

        if self.resto:
            dv = modulo

            if dv > 9:
                dv = self.dv_acima_11

        else:
            dv = 11 - modulo

            if dv == 10:
                dv = self.dv_acima_10
            elif dv == 11:
                dv = self.dv_acima_11

        return unicode(dv)

    def pre_valida_formata(self, ie):
        ie = LIMPA.sub('', ie)

        if self.tamanho_minimo and ie:
            ie = ie.rjust(self.tamanho_minimo, '0')

        return ie

    def valida(self, ie):
        ie_a_validar = self.pre_valida_formata(ie)

        if not self.expressao.match(ie_a_validar):
            return False

        if not ie_a_validar:
            return False

        ie_valida = True
        for i in range(len(self.dv)):
            dv_posicao = self.dv[i]
            pesos = self.pesos[i]
            posicoes = self.posicoes[i]
            dv_original = ie_a_validar[dv_posicao]
            dv_calculado = self.digito(ie_a_validar, pesos, posicoes)

            ie_valida = ie_valida and (dv_original == dv_calculado)

        return ie_valida

    def formata(self, ie):
        if not self.valida(ie):
            return ie

        ie_a_formatar = self.pre_valida_formata(ie)

        formato = list(self.formato)

        posicao_inicial = 0
        for i in range(len(formato)):
            if type(formato[i]) is not int:
                continue

            posicao_final = posicao_inicial + formato[i]
            formato[i] = ie_a_formatar[posicao_inicial:posicao_final]
            posicao_inicial = posicao_final

        return ''.join(formato)


class ValidaIEAC(ValidaIE):
    """
    Valida e formata as inscrições estaduais do AC - Acre

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEAC()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('0100482300112')
    True
    >>> valida_ie.formata('0100482300112')
    u'01.004.823/001-12'
    """
    def __init__(self, **kwargs):
        super(ValidaIEAC, self).__init__(**kwargs)
        self.expressao = r'^01[0-9]{11}$'
        self.dv = [11, 12]
        self.pesos = [
            [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
            [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        ]
        self.posicoes = [range(11), range(12)]
        self.formato = [2, '.', 3, '.', 3, '/', 3, '-', 2]


class ValidaIEAL(ValidaIE):
    """
    Valida e formata as inscrições estaduais do AL - Alagoas

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * não tem formato no SINTEGRA, atribuído um que separa o dígito

    >>> valida_ie = ValidaIEAL()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('240000048')
    True
    >>> valida_ie.valida('241056373')
    True
    >>> valida_ie.valida('241038081')
    True
    >>> valida_ie.valida('242001475')
    True
    >>> valida_ie.formata('240000048')
    u'24.000.004-8'
    >>> valida_ie.formata('241056373')
    u'24.105.637-3'
    >>> valida_ie.formata('241038081')
    u'24.103.808-1'
    >>> valida_ie.formata('242001475')
    u'24.200.147-5'
    """
    def __init__(self, **kwargs):
        super(ValidaIEAL, self).__init__(**kwargs)
        #self.expressao = r'^24[03578][0-9]{6}$'
        self.expressao = r'^24[0-9]{7}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]
        self.resto = True

    def soma(self, ie, pesos, posicoes):
        soma = super(ValidaIEAL, self).soma(ie, pesos, posicoes)
        return soma * 10


class ValidaIEAM(ValidaIE):
    """
    Valida e formata as inscrições estaduais do AM - Amazonas

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEAM()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('999999990')
    True
    >>> valida_ie.valida('063000474')
    True
    >>> valida_ie.valida('63000474')
    True
    >>> valida_ie.formata('999999990')
    u'99.999.999-0'
    >>> valida_ie.formata('63000474')
    u'06.300.047-4'
    """
    def __init__(self, **kwargs):
        super(ValidaIEAM, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{8}$|^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]
        self.resto = True
        self.tamanho_minimo = 9

    def modulo(self, ie, pesos, posicoes):
        soma = self.soma(ie, pesos, posicoes)

        if soma < 11:
            modulo = 11 - soma

        else:
            modulo = soma % 11

            if modulo <= 1:
                modulo = 0
            else:
                modulo = 11 - modulo

        return modulo


class ValidaIEAP(ValidaIE):
    """
    Valida e formata as inscrições estaduais do AP - Amapá

    * Formato arbitrário, o AP não tem nem SINTEGRA...

    >>> valida_ie = ValidaIEAP()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('030123459')
    True
    >>> valida_ie.formata('030123459')
    u'03.012.345-9'
    """
    def __init__(self, **kwargs):
        super(ValidaIEAP, self).__init__(**kwargs)
        self.expressao = r'^03[0-9]{7}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]

    def digito(self, ie, pesos, posicoes):
        if '03000001' <= ie[0:9] <= '03017000':
            self.inicio_soma = 5
            self.dv_acima_11 = 0

        elif '03017001' <= ie[0:9] <= '03019022':
            self.inicio_soma = 9
            self.dv_acima_11 = 1

        return super(ValidaIEAP, self).digito(ie, pesos, posicoes)


class ValidaIEBA(ValidaIE):
    """
    Valida e formata as inscrições estaduais da BA - Bahia

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEBA()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('12345663')
    True
    >>> valida_ie.valida('100000306')
    True
    >>> valida_ie.valida('009378607')
    True
    >>> valida_ie.valida('09378607')
    True
    >>> valida_ie.formata('12345663')
    u'012.345.663'
    >>> valida_ie.formata('100000306')
    u'100.000.306'
    >>> valida_ie.formata('009378607')
    u'009.378.607'
    >>> valida_ie.formata('09378607')
    u'009.378.607'
    """
    def __init__(self, **kwargs):
        super(ValidaIEBA, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{8}$|^[0-9]{9}$'
        self.dv = [7, 8]
        self.pesos = [
            [9, 8, 7, 6, 5, 4, 3, 2],
            [8, 7, 6, 5, 4, 3, 2],
        ]
        self.posicoes = [
            [0, 1, 2, 3, 4, 5, 6, 8],
            [0, 1, 2, 3, 4, 5, 6],
        ]
        self.formato = [3, '.', 3, '.', 3]
        self.tamanho_minimo = 9

    def modulo(self, ie, pesos, posicoes):
        soma = self.soma(ie, pesos, posicoes)

        if ie[1] in '0123458':
            modulo = soma % 10

        else:
            modulo = soma % 11

        return modulo

    def digito(self, ie, pesos, posicoes):
        modulo = self.modulo(ie, pesos, posicoes)

        if ie[1] in '0123458':
            dv = 10 - modulo

            if dv > 9:
                dv = 0

        else:
            dv = 11 - modulo

            if dv > 9:
                dv = 0

        return unicode(dv)


class ValidaIECE(ValidaIE):
    """
    Valida e formata as inscrições estaduais do CE - Ceará

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIECE()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('060000015')
    True
    >>> valida_ie.valida('60000015')
    True
    >>> valida_ie.formata('060000015')
    u'06.000001-5'
    >>> valida_ie.formata('60000015')
    u'06.000001-5'
    """
    def __init__(self, **kwargs):
        super(ValidaIECE, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 6, '-', 1]
        self.tamanho_minimo = 9


class ValidaIEDF(ValidaIE):
    """
    Valida e formata as inscrições estaduais do DF - Distrito Federal

    * Formato/máscara verificado através de consulta ao SINTEGRA

38043832000168

    >>> valida_ie = ValidaIEDF()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('0730000100109')
    True
    >>> valida_ie.formata('0730000100109')
    u'07-300.001/001-09'
    """
    def __init__(self, **kwargs):
        super(ValidaIEDF, self).__init__(**kwargs)
        self.expressao = r'^07[0-9]{11}$'
        self.dv = [11, 12]
        self.pesos = [
            [4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
            [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
        ]
        self.posicoes = [range(11), range(12)]
        self.formato = [2, '-', 3, '.', 3, '/', 3, '-', 2]


class ValidaIEES(ValidaIE):
    """
    Valida e formata as inscrições estaduais do ES - Espírito Santo

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEES()
    >>> valida_ie.valida('999999990')
    True
    >>> valida_ie.valida('110272986')
    True
    >>> valida_ie.formata('999999990')
    u'999.999.99-0'
    >>> valida_ie.formata('110272986')
    u'110.272.98-6'
    """
    def __init__(self, **kwargs):
        super(ValidaIEES, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [3, '.', 3, '.', 2, '-', 1]


class ValidaIEGO(ValidaIE):
    """
    Valida e formata as inscrições estaduais de GO - Goiás

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEGO()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('109876547')
    True
    >>> valida_ie.valida('110944020')
    True
    >>> valida_ie.formata('109876547')
    u'10.987.654-7'
    >>> valida_ie.formata('110944020')
    u'11.094.402-0'
    """
    def __init__(self, **kwargs):
        super(ValidaIEGO, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]

    def digito(self, ie, pesos, posicoes):
        if '10103105' <= ie[0:9] <= '10119997':
            self.dv_acima_10 = 1
        else:
            self.dv_acima_10 = 0

        return super(ValidaIEGO, self).digito(ie, pesos, posicoes)


class ValidaIEMA(ValidaIE):
    """
    Valida e formata as inscrições estaduais do MA - Maranhão

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * não tem formato no SINTEGRA, atribuído um que separa o dígito

    >>> valida_ie = ValidaIEMA()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('120000385')
    True
    >>> valida_ie.formata('120000385')
    u'12.000.038-5'
    """
    def __init__(self, **kwargs):
        super(ValidaIEMA, self).__init__(**kwargs)
        self.expressao = r'^12[0-9]{7}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]


class ValidaIEMG(ValidaIE):
    """
    Valida e formata as inscrições estaduais de MG - Minas Gerais

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * Formato mesclado entre o SINTEGRA e a orientação sobre a validação

    >>> valida_ie = ValidaIEMG()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('0623079040081')
    True
    >>> valida_ie.formata('0623079040081')
    u'062.307.904/00-81'
    >>> valida_ie.valida('PR426587')
    True
    >>> valida_ie.formata('PR-42.65.87')
    u'PR426587'
    """
    def __init__(self, **kwargs):
        super(ValidaIEMG, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{13}$|^PR[0-9]{4,8}$'
        self.dv = [11, 12]
        self.pesos = [
            [1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2],
            [3, 2, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
        ]
        self.posicoes = [range(11), range(12)]
        self.formato = [3, '.', 3, '.', 3, '/', 2, '-', 2]
        self.produtor_rural = re.compile('^PR[0-9]{4,8}$')

    def soma_algarismo(self, ie, pesos, posicoes):
        soma_texto = ''

        for i in range(len(pesos)):
            peso = pesos[i]
            posicao = posicoes[i]
            numero = int(ie[posicao])
            soma_texto += unicode(numero * peso)

        soma = 0
        for c in soma_texto:
            soma += int(c)

        return soma

    def digito(self, ie, pesos, posicoes):
        if pesos == self.pesos[1]:
            return super(ValidaIEMG, self).digito(ie, pesos, posicoes)

        soma = self.soma_algarismo(ie, pesos, posicoes)

        acima = (soma - (soma % 10)) + 10
        dv = acima - soma

        if dv == 10:
            dv = 0

        return unicode(dv)

    def valida(self, ie):
        ie_a_validar = self.pre_valida_formata(ie)

        if self.produtor_rural.match(ie_a_validar):
            return True

        return super(ValidaIEMG, self).valida(ie)

    def formata(self, ie):
        if not self.valida(ie):
            return ie

        ie_a_formatar = self.pre_valida_formata(ie)

        if self.produtor_rural.match(ie_a_formatar):
            return ie_a_formatar

        return super(ValidaIEMG, self).formata(ie)


class ValidaIEMS(ValidaIE):
    """
    Valida e formata as inscrições estaduais do MS - Mato Grosso do Sul

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEMS()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('280000006')
    True
    >>> valida_ie.formata('280000006')
    u'28.000.000-6'
    """
    def __init__(self, **kwargs):
        super(ValidaIEMS, self).__init__(**kwargs)
        self.expressao = r'^28[0-9]{7}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]


class ValidaIEMT(ValidaIE):
    """
    Valida e formata as inscrições estaduais do MT - Mato Grosso

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * Só achei inscrições com 9 dígitos, a máscara é essa mesma,
    * exceto pelos 2 dígitos iniciais

    >>> valida_ie = ValidaIEMT()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('00130000019')
    True
    >>> valida_ie.valida('131863673')
    True
    >>> valida_ie.valida('130944629')
    True
    >>> valida_ie.valida('1301523663')
    True
    >>> valida_ie.formata('00130000019')
    u'00.13.000.001-9'
    >>> valida_ie.formata('131863673')
    u'00.13.186.367-3'
    >>> valida_ie.formata('130944629')
    u'00.13.094.462-9'
    >>> valida_ie.formata('1301523663')
    u'01.30.152.366-3'
    """
    def __init__(self, **kwargs):
        super(ValidaIEMT, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{11}$'
        self.dv = [10]
        self.pesos = [[3, 2, 9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(10)]
        self.formato = [2, '.', 2, '.', 3, '.', 3, '-', 1]
        self.tamanho_minimo = 11


class ValidaIEPA(ValidaIE):
    """
    Valida e formata as inscrições estaduais do PA - Pará

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEPA()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('159999995')
    True
    >>> valida_ie.formata('159999995')
    u'15.999.999-5'
    """
    def __init__(self, **kwargs):
        super(ValidaIEPA, self).__init__(**kwargs)
        self.expressao = r'^15[0-9]{7}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]


class ValidaIEPB(ValidaIE):
    """
    Valida e formata as inscrições estaduais da PB - Paraíba

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIEPB()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('060000015')
    True
    >>> valida_ie.formata('060000015')
    u'06.000.001-5'
    """
    def __init__(self, **kwargs):
        super(ValidaIEPB, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]


class ValidaIEPE(ValidaIE):
    """
    Valida e formata as inscrições estaduais de PE - Pernambuco

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * não tem formato no SINTEGRA, atribuído um que separa o dígito

    As inscrições antigas tinham 14 dígitos, estruturadas da seguinte forma:
        - 2 dígitos para o estado (sempre 18)
        - 1 dígito para o tipo (nunca 0)
        - 3 dígitos para o município
        - 7 para a inscrição propriamente dita
        - 1 dígito verificador

    A rotina converte, na formatação, automaticamente para a versão com
    9 dígitos, desprezando os 6 primeiros dígitos e o último, e calculando os
    2 novos dígitos verificadores.

    Isso foi feito pois na consulta do SINTEGRA de Pernambuco só vêm as
    inscrições novas, mesmo quando consultamos uma inscrição antiga.

    Essa conversão está disponível também através de um programa disponibilizado
    pela SEFAZ-PE em:

    http://www.sefaz.pe.gov.br/sintegra/consulta/download/InscricaoCadastro.zip

    >>> valida_ie = ValidaIEPE()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('18100100000049')
    True
    >>> valida_ie.valida('18100103325381')
    True
    >>> valida_ie.valida('18158000905761')
    True
    >>> valida_ie.valida('32141840')
    True
    >>> valida_ie.valida('13224190')
    True
    >>> valida_ie.valida('659940')
    True
    >>> valida_ie.valida('19726260')
    True
    >>> valida_ie.valida('29247306')
    True
    >>> valida_ie.formata('18100100000049')
    u'00.000.04-34'
    >>> valida_ie.formata('18100103325381')
    u'03.325.38-54'
    >>> valida_ie.formata('18158000905761')
    u'00.905.76-33'
    >>> valida_ie.formata('32141840')
    u'03.214.18-40'
    >>> valida_ie.formata('13224190')
    u'01.322.41-90'
    >>> valida_ie.formata('659940')
    u'00.065.99-40'
    >>> valida_ie.formata('19726260')
    u'01.972.62-60'
    >>> valida_ie.formata('29247306')
    u'02.924.73-06'
    """
    def __init__(self, **kwargs):
        super(ValidaIEPE, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$|^18[1-9][0-9]{11}$'
        self.tamanho_minimo = 9

    def valida(self, ie):
        ie_a_validar = self.pre_valida_formata(ie)

        if not self.expressao.match(ie_a_validar):
            return False

        if len(ie_a_validar) == 9:
            self.dv = [7, 8]
            self.pesos = [
                [8, 7, 6, 5, 4, 3, 2],
                [9, 8, 7, 6, 5, 4, 3, 2]
            ]
            self.posicoes = [range(7), range(8)]
            self.formato = [2, '.', 3, '.', 2, '-', 2]
            self.dv_acima_11 = 0

        elif len(ie_a_validar) == 14:
            self.dv = [13]
            self.pesos = [[5, 4, 3, 2, 1, 9, 8, 7, 6, 5, 4, 3, 2]]
            self.posicoes = [range(13)]
            self.formato = [2, '.', 1, '.', 3, '.', 7, '-', 1]
            self.dv_acima_11 = 1

        return super(ValidaIEPE, self).valida(ie)

    def formata(self, ie):
        if not self.valida(ie):
            return ie

        ie_a_formatar = self.pre_valida_formata(ie)

        #
        # Conversão para a versão nova
        #
        if len(ie_a_formatar) == 14:
            ie_a_formatar = ie_a_formatar[6:13]
            dv1 = self.digito(ie_a_formatar, [8, 7, 6, 5, 4, 3, 2], range(8))
            ie_a_formatar += dv1
            dv2 = self.digito(ie_a_formatar, [9, 8, 7, 6, 5, 4, 3, 2], range(9))
            ie_a_formatar += dv2

        return super(ValidaIEPE, self).formata(ie_a_formatar)


class ValidaIEPI(ValidaIE):
    """
    Valida e formata as inscrições estaduais do PI - Piauí

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * não tem formato no SINTEGRA, atribuído um que separa o dígito

    >>> valida_ie = ValidaIEPI()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('012345679')
    True
    >>> valida_ie.formata('012345679')
    u'01.234.567-9'
    """
    def __init__(self, **kwargs):
        super(ValidaIEPI, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]


class ValidaIEPR(ValidaIE):
    """
    Valida e formata as inscrições estaduais do PR - Paraná

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * Formato mesclado entre o SINTEGRA e a orientação sobre a validação

    >>> valida_ie = ValidaIEPR()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('1234567850')
    True
    >>> valida_ie.formata('1234567850')
    u'123.45678-50'
    """
    def __init__(self, **kwargs):
        super(ValidaIEPR, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{10}$'
        self.dv = [8, 9]
        self.pesos = [
            [3, 2, 7, 6, 5, 4, 3, 2],
            [4, 3, 2, 7, 6, 5, 4, 3, 2],
        ]
        self.posicoes = [range(8), range(9)]
        self.formato = [3, '.', 5, '-', 2]


class ValidaIERJ(ValidaIE):
    """
    Valida e formata as inscrições estaduais do RJ - Rio de Janeiro

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * Formato mesclado entre o SINTEGRA e a orientação sobre a validação

    >>> valida_ie = ValidaIERJ()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('99999993')
    True
    >>> valida_ie.formata('99999993')
    u'99.999.99-3'
    """
    def __init__(self, **kwargs):
        super(ValidaIERJ, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{8}$'
        self.dv = [7]
        self.pesos = [[2, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(7)]
        self.formato = [2, '.', 3, '.', 2, '-', 1]


class ValidaIERN(ValidaIE):
    """
    Valida e formata as inscrições estaduais do RN - Rio Grande do Norte

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIERN()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('200400401')
    True
    >>> valida_ie.valida('2000400400')
    True
    >>> valida_ie.formata('200400401')
    u'20.040.040-1'
    >>> valida_ie.formata('2000400400')
    u'200.040.040-0'
    """
    def __init__(self, **kwargs):
        super(ValidaIERN, self).__init__(**kwargs)
        self.expressao = r'^20[0-9]{7}$|^20[0-9]{8}$'
        self.resto = True

    def soma(self, ie, pesos, posicoes):
        soma = super(ValidaIERN, self).soma(ie, pesos, posicoes)
        return soma * 10

    def valida(self, ie):
        ie_a_validar = self.pre_valida_formata(ie)

        if not self.expressao.match(ie_a_validar):
            return False

        if len(ie_a_validar) == 9:
            self.dv = [8]
            self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
            self.posicoes = [range(8)]
            self.formato = [2, '.', 3, '.', 3, '-', 1]

        else:
            self.dv = [9]
            self.pesos = [[10, 9, 8, 7, 6, 5, 4, 3, 2]]
            self.posicoes = [range(9)]
            self.formato = [3, '.', 3, '.', 3, '-', 1]

        return super(ValidaIERN, self).valida(ie)


class ValidaIERO(ValidaIE):
    """
    Valida e formata as inscrições estaduais de RO - Rondônia

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * SINTEGRA não funciona...

    As inscrições antigas tinham 9 dígitos, estruturadas da seguinte forma:
        - 3 dígitos para o município
        - 5 para a inscrição propriamente dita
        - 1 dígito verificador

    A rotina converte, na formatação, automaticamente para a versão com
    14 dígitos, desprezando os 3 primeiros dígitos, e completando com zeros
    à esquerda.

    >>> valida_ie = ValidaIERO()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('101625213')
    True
    >>> valida_ie.valida('00000000625213')
    True
    >>> valida_ie.formata('101625213')
    u'0.000.000.062.521-3'
    >>> valida_ie.formata('00000000625213')
    u'0.000.000.062.521-3'
    """
    def __init__(self, **kwargs):
        super(ValidaIERO, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$|^[0-9]{14}$'
        self.dv = [13]
        self.pesos = [[6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(13)]
        self.formato = [1, '.', 3, '.', 3, '.', 3, '.', 3, '-', 1]
        self.tamanho_minimo = 14

    def pre_valida_formata(self, ie):
        ie = LIMPA.sub('', ie)

        if len(ie) == 9:
            ie = ie[3:]

        return super(ValidaIERO, self).pre_valida_formata(ie)


class ValidaIERR(ValidaIE):
    """
    Valida e formata as inscrições estaduais de RR - Roraima

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIERR()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('240034290')
    True
    >>> valida_ie.valida('240066281')
    True
    >>> valida_ie.valida('240073562')
    True
    >>> valida_ie.valida('240013603')
    True
    >>> valida_ie.valida('240054674')
    True
    >>> valida_ie.valida('240041455')
    True
    >>> valida_ie.valida('240061536')
    True
    >>> valida_ie.valida('240017556')
    True
    >>> valida_ie.valida('240013407')
    True
    >>> valida_ie.valida('240082668')
    True
    >>> valida_ie.formata('240013603')
    u'24.001.360-3'
    """
    def __init__(self, **kwargs):
        super(ValidaIERR, self).__init__(**kwargs)
        self.expressao = r'^24[0-9]{7}$'
        self.dv = [8]
        self.pesos = [range(1, 9)]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]

    def modulo(self, ie, pesos, posicoes):
        soma = self.soma(ie, pesos, posicoes)
        return soma % 9

    def digito(self, ie, pesos, posicoes):
        dv = self.modulo(ie, pesos, posicoes)
        return unicode(dv)


class ValidaIERS(ValidaIE):
    """
    Valida e formata as inscrições estaduais do RS - Rio Grande do Sul

    >>> valida_ie = ValidaIERS()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('2243658792')
    True
    >>> valida_ie.formata('2243658792')
    u'224/365.879-2'
    """
    def __init__(self, **kwargs):
        super(ValidaIERS, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{10}$'
        self.dv = [9]
        self.pesos = [[2, 9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(9)]
        self.formato = [3, '/', 3, '.', 3, '-', 1]
        self.tamanho_minimo = 10


class ValidaIESC(ValidaIE):
    """
    Valida e formata as inscrições estaduais de SC - Santa Catarina

    * Formato/máscara verificado através de consulta ao SINTEGRA
    * Formato mesclado entre o SINTEGRA e a orientação sobre a validação

    >>> valida_ie = ValidaIESC()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('251040852')
    True
    >>> valida_ie.formata('251040852')
    u'251.040.852'
    """
    def __init__(self, **kwargs):
        super(ValidaIESC, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [3, '.', 3, '.', 3]


class ValidaIESE(ValidaIE):
    """
    Valida e formata as inscrições estaduais de SE - Sergipe

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIESE()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('271234563')
    True
    >>> valida_ie.formata('271234563')
    u'27.123.456-3'
    """
    def __init__(self, **kwargs):
        super(ValidaIESE, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 3, '.', 3, '-', 1]


class ValidaIESP(ValidaIE):
    """
    Valida e formata as inscrições estaduais de SP - São Paulo

    * Formato/máscara verificado através de consulta ao SINTEGRA

    >>> valida_ie = ValidaIESP()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('110042490114')
    True
    >>> valida_ie.valida('P011004243002')
    True
    >>> valida_ie.formata('110042490114')
    u'110.042.490.114'
    >>> valida_ie.formata('P011004243002')
    u'P-011.004.243/002'
    """
    def __init__(self, **kwargs):
        super(ValidaIESP, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{12}$|^P[0-9]{12}$'
        self.resto = True

    def valida(self, ie):
        ie_a_validar = self.pre_valida_formata(ie)

        if not self.expressao.match(ie_a_validar):
            return False

        if len(ie_a_validar) == 12:
            self.dv = [8, 11]
            self.pesos = [
                [1, 3, 4, 5, 6, 7, 8, 10],
                [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2]
            ]
            self.posicoes = [range(8), range(11)]
            self.formato = [3, '.', 3, '.', 3, '.', 3]

        else:
            self.dv = [9]
            self.pesos = [[1, 3, 4, 5, 6, 7, 8, 10]]
            self.posicoes = [range(1, 9)]
            self.formato = [1, '-', 3, '.', 3, '.', 3, '/', 3]

        return super(ValidaIESP, self).valida(ie)


class ValidaIETO(ValidaIE):
    """
    Valida e formata as inscrições estaduais do TO - Tocantins

    * Formato/máscara verificado através de consulta ao SINTEGRA

    As inscrições antigas tinham 11 dígitos, estruturadas da seguinte forma:
        - 2 dígitos para o estado
        - 2 dígitos para o tipo
        - 6 para a inscrição propriamente dita
        - 1 dígito verificador

    Os 2 dígitos do tipo não entravam no cálculo do dígito verificador.

    A rotina converte, na formatação, automaticamente para a versão com
    9 dígitos, desprezando os 2 dígitos do tipo.

    >>> valida_ie = ValidaIETO()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('29010227836')
    True
    >>> valida_ie.valida('131578766')
    True
    >>> valida_ie.formata('29010227836')
    u'29.022.783-6'
    >>> valida_ie.formata('131578766')
    u'13.157.876-6'
    """
    def __init__(self, **kwargs):
        super(ValidaIETO, self).__init__(**kwargs)
        self.expressao = r'^[0-9]{2}(01|02|03|99)[0-9]{7}$|^[0-9]{9}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [[0, 1, 2, 3, 4, 5, 6, 7]]
        self.formato = [2, '.', 3, '.', 3, '-', 1]

    def valida(self, ie):
        ie_a_validar = self.pre_valida_formata(ie)

        if not self.expressao.match(ie_a_validar):
            return False

        if len(ie_a_validar) == 11:
            ie_a_validar = ie_a_validar[0:2] + ie_a_validar[4:]

        return super(ValidaIETO, self).valida(ie_a_validar)

    def formata(self, ie):
        if not self.valida(ie):
            return ie

        ie_a_formatar = self.pre_valida_formata(ie)

        if len(ie_a_formatar) == 11:
            ie_a_formatar = ie_a_formatar[0:2] + ie_a_formatar[4:]

        return super(ValidaIETO, self).formata(ie_a_formatar)


class ValidaIESUFRAMA(ValidaIE):
    """
    Valida e formata as inscrições estaduais da SUFRAMA

    >>> valida_ie = ValidaIESUFRAMA()
    >>> valida_ie.valida('ISENTO')
    False
    >>> valida_ie.valida('isento')
    False
    >>> valida_ie.valida('')
    False
    >>> valida_ie.valida('100698107')
    True
    >>> valida_ie.valida('111279100')
    True
    >>> valida_ie.valida('100955100')
    True
    >>> valida_ie.valida('101040105')
    True
    >>> valida_ie.valida('101362102')
    True
    >>> valida_ie.valida('100695108')
    True
    >>> valida_ie.valida('101160100')
    True
    >>> valida_ie.valida('600215105')
    True
    >>> valida_ie.valida('111266106')
    True
    >>> valida_ie.valida('100170102')
    True
    >>> valida_ie.valida('101416105')
    True
    >>> valida_ie.valida('101200102')
    True
    >>> valida_ie.valida('110344103')
    True
    >>> valida_ie.valida('111273102')
    True
    >>> valida_ie.valida('100480101')
    True
    >>> valida_ie.valida('100628109')
    True
    >>> valida_ie.valida('100394108')
    True
    >>> valida_ie.valida('101289103')
    True
    >>> valida_ie.valida('101139101')
    True
    >>> valida_ie.valida('100880100')
    True
    >>> valida_ie.valida('100826105')
    True
    >>> valida_ie.valida('110410106')
    True
    >>> valida_ie.valida('100764100')
    True
    >>> valida_ie.valida('110425103')
    True
    >>> valida_ie.valida('100965105')
    True
    >>> valida_ie.valida('isento')
    False
    """
    def __init__(self, **kwargs):
        super(ValidaIESUFRAMA, self).__init__(**kwargs)
        self.expressao = r'^(1|2)[0-9]{4}(01|10|30)[0-9]{1}$|^(01|02|10|11|20|60)[0-9]{4}(01|10|30)[0-9]{1}$'
        self.dv = [8]
        self.pesos = [[9, 8, 7, 6, 5, 4, 3, 2]]
        self.posicoes = [range(8)]
        self.formato = [2, '.', 4, '.', 2, '-', 1]
        self.resto = True
        self.tamanho_minimo = 9

    def modulo(self, ie, pesos, posicoes):
        soma = self.soma(ie, pesos, posicoes)

        if soma < 11:
            modulo = 11 - soma

        else:
            modulo = soma % 11

            if modulo <= 1:
                modulo = 0
            else:
                modulo = 11 - modulo

        return modulo


CLASSE_VALIDA_IE_ESTADO = {
    'AC': ValidaIEAC,
    'AL': ValidaIEAL,
    'AM': ValidaIEAM,
    'AP': ValidaIEAP,
    'BA': ValidaIEBA,
    'CE': ValidaIECE,
    'DF': ValidaIEDF,
    'ES': ValidaIEES,
    'GO': ValidaIEGO,
    'MA': ValidaIEMA,
    'MG': ValidaIEMG,
    'MS': ValidaIEMS,
    'MT': ValidaIEMT,
    'PA': ValidaIEPA,
    'PB': ValidaIEPB,
    'PE': ValidaIEPE,
    'PI': ValidaIEPI,
    'PR': ValidaIEPR,
    'RJ': ValidaIERJ,
    'RN': ValidaIERN,
    'RO': ValidaIERO,
    'RR': ValidaIERR,
    'RS': ValidaIERS,
    'SC': ValidaIESC,
    'SE': ValidaIESE,
    'SP': ValidaIESP,
    'TO': ValidaIETO,
    'SUFRAMA': ValidaIESUFRAMA,
}


def valida_ie(ie, estado):
    #
    # Brasileiros podem não ter inscrição estadual, ou serem isentos
    # Quando forem isentos, o valor aceito na IE é ISENTO
    #
    if ie == '' or ie == 'ISENTO':
        return True

    ie = LIMPA.sub('', ie)

    if not estado:
        return False

    estado = estado.upper()

    #
    # Estado inválido
    #
    if estado not in CLASSE_VALIDA_IE_ESTADO:
        return False

    #
    # Estrangeiros não têm inscrição estadual
    #
    if estado == 'EX':
        return ie == ''

    #
    # Caso contrário, validar de acordo com estado
    #
    validador_ie = CLASSE_VALIDA_IE_ESTADO[estado]()

    return validador_ie.valida(ie)


def formata_ie(ie, estado):
    if not valida_ie(ie, estado):
        return ie

    if ie == '' or ie == 'ISENTO':
        return ie

    ie = LIMPA.sub('', ie)

    validador_ie = CLASSE_VALIDA_IE_ESTADO[estado]()

    return validador_ie.formata(ie)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
