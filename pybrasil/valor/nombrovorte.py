#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Números por extenso, cardinais, ordinais e cardinais com unidades de medida

Compatível com as versões 2 e 3 do Python
'''

from __future__ import division, print_function, unicode_literals

from decimal import Decimal as D


NOMBROVORTO = {
    0: 'nul',
    1: 'unu',
    2: 'du',
    3: 'tri',
    4: 'kvar',
    5: 'kvin',
    6: 'ses',
    7: 'sep',
    8: 'ok',
    9: 'naŭ',
    10: 'dek',
    100: 'cent',
    }

POTENCONOMO_OFICIALA = {
    10**3: 'mil',
    10**6: 'miliono',
    10**9: 'miliardo',
    10**12: 'biliono',
    #10**15: 'mil biliono',
    10**18: 'triliono',
    #10**21: 'mil triliono',
    10**24: 'kvadriliono',
    #10**27: 'mil kvadriliono',
    10**30: 'kvintiliono',
    #10**33: 'mil kvintiliono',
    10**36: 'sekstiliono',
    #10**39: 'mil sekstiliono',
    10**42: 'septiliono',
    #10**45: 'mil septiliono',
    10**48: 'oktiliono',
    #10**51: 'mil oktiliono',
    10**54: 'noniliono',
    #10**57: 'mil noniliono',
    10**60: 'deciliono',
    }

POTENCONOMO_SUFIKSA = {
    10**3: 'mil',
    10**6: 'miliono',
    10**9: 'miliardo',
    10**12: 'duiliono',
    10**15: 'duiliardo',
    10**18: 'triiliono',
    10**21: 'triiliardo',
    10**24: 'kvariliono',
    10**27: 'kvariliardo',
    10**30: 'kviniliono',
    10**33: 'kviniliardo',
    10**36: 'sesiliono',
    10**39: 'sesiliardo',
    10**42: 'sepiliono',
    10**45: 'sepiliardo',
    10**48: 'okiliono',
    10**51: 'okiliardo',
    10**54: 'naŭiliono',
    10**57: 'naŭiliardo',
    10**60: 'dekiliono',
    }

POTENCONOMO = POTENCONOMO_OFICIALA

MAKSIMUMA_NOMBRO = 999999 * max(POTENCONOMO)


class NombroVorto(object):
    def __init__(self, nombro=0, unuo='valuto', subunuo_precizeco=2, subunuo='centono', subnulo_masko='minus %s'):
        self.nombro = nombro
        self.unuo = unuo
        self.subunuo_precizeco = subunuo_precizeco
        self.subunuo = subunuo
        self.subnulo_masko = subnulo_masko
    @property
    def nombro(self):
        return self._nombro

    @nombro.setter
    def nombro(self, valor):
        if D(str(valor)) > MAKSIMUMA_NOMBRO:
            raise OverflowError('nombro tro granda; la maksimumo estas: %s' % MAKSIMUMA_NOMBRO)

        self._nombro = D(str(valor))

    def _cento_deko_unuo(self, nombro):
        assert 0 <= nombro < 1000

        if nombro in NOMBROVORTO:
            return NOMBROVORTO[nombro]

        potenco_10 = int(10 ** int(D(nombro).log10()))
        kapo = int(nombro / potenco_10) * potenco_10
        korpo = int(nombro % potenco_10)

        if kapo > 100:
            kapo = int(kapo / 100)
            korpo += 100
        elif 100 > kapo > 10:
            kapo = int(kapo / 10)
            korpo += 10

        teksto = NOMBROVORTO[kapo]

        if (kapo == 100) or (kapo == 10):
            teksto += ' '

        teksto += self._cento_deko_unuo(korpo)

        return teksto

    def _potenco(self, nombro, mila=False):
        potenco_10 = 1000 ** int((len(str(int(nombro))) - 1) / 3)
        potenco_1000 = 1000 ** (int((len(str(int(nombro))) - 1) / 3) - 1)

        if potenco_10 <= 100:
            return self._cento_deko_unuo(nombro)

        este_grupo = int(nombro / potenco_10)
        proximo_grupo = nombro - (este_grupo * potenco_10)

        if potenco_10 in POTENCONOMO:
            if (este_grupo > 1) or (potenco_10 >= 1000000):
                texto = self._cento_deko_unuo(este_grupo)
            else:
                texto = ''
        else:
            if (este_grupo > 1):
                texto = self._cento_deko_unuo(este_grupo)
            else:
                texto = ''

        if len(texto):
            texto += ' '

        if potenco_10 in POTENCONOMO:
            texto += POTENCONOMO[potenco_10]

            if ((potenco_10 > 1000) and (este_grupo > 1)) or mila:
                texto += 'j'

            mila = False

        else:
            if proximo_grupo == 0:
                texto += 'mil ' + POTENCONOMO[potenco_1000]
                texto += 'j'

            else:
                texto += 'mil'

            mila = True

        #
        # Conexão entre os grupos
        #
        if proximo_grupo > 0:
            texto += ' '
            texto += self._potenco(proximo_grupo, mila)

        return texto

    @property
    def vorto(self):
        return self._potenco(abs(int(self.nombro)))

    def alivortigu(self, vorto, finajho):
        if vorto[-1] == 'o':
            vorto = vorto[:-1]

        return vorto + finajho
    @property
    def vorto_o(self):
        teksto = self.vorto

        if teksto[-1] == 'j':
            teksto = teksto[:-1]

        teksto = teksto.replace(' ', '-').replace('oj-', 'o-')

        if teksto[-1] != 'o':
            teksto += 'o'

        return teksto

    @property
    def vorto_on(self):
        return self.alivortigu(self.vorto_o, 'on')

    @property
    def vorto_oj(self):
        return self.alivortigu(self.vorto_o, 'oj')

    @property
    def vorto_ojn(self):
        return self.alivortigu(self.vorto_o, 'ojn')

    @property
    def vorto_a(self):
        return self.alivortigu(self.vorto_o, 'a')

    @property
    def vorto_an(self):
        return self.alivortigu(self.vorto_o, 'an')

    @property
    def vorto_aj(self):
        return self.alivortigu(self.vorto_o, 'aj')

    @property
    def vorto_ajn(self):
        return self.alivortigu(self.vorto_o, 'ajn')

    @property
    def vorto_e(self):
        return self.alivortigu(self.vorto_o, 'e')

    @property
    def vorto_en(self):
        return self.alivortigu(self.vorto_o, 'en')

    @property
    def vorto_ono(self):
        return self.alivortigu(self.vorto_o, 'ono')

    @property
    def vorto_onon(self):
        return self.alivortigu(self.vorto_o, 'onon')

    @property
    def vorto_onoj(self):
        return self.alivortigu(self.vorto_o, 'onoj')

    @property
    def vorto_onojn(self):
        return self.alivortigu(self.vorto_o, 'onojn')

    @property
    def vorto_ona(self):
        return self.alivortigu(self.vorto_o, 'ona')

    @property
    def vorto_onan(self):
        return self.alivortigu(self.vorto_o, 'onan')

    @property
    def vorto_onaj(self):
        return self.alivortigu(self.vorto_o, 'onaj')

    @property
    def vorto_onajn(self):
        return self.alivortigu(self.vorto_o, 'onajn')

    @property
    def vorto_one(self):
        return self.alivortigu(self.vorto_o, 'one')

    @property
    def vorto_onen(self):
        return self.alivortigu(self.vorto_o, 'onen')

    @property
    def vorto_oblo(self):
        return self.alivortigu(self.vorto_o, 'oblo')

    @property
    def vorto_oblon(self):
        return self.alivortigu(self.vorto_o, 'oblon')

    @property
    def vorto_obloj(self):
        return self.alivortigu(self.vorto_o, 'obloj')

    @property
    def vorto_oblojn(self):
        return self.alivortigu(self.vorto_o, 'oblojn')

    @property
    def vorto_obla(self):
        return self.alivortigu(self.vorto_o, 'obla')

    @property
    def vorto_oblan(self):
        return self.alivortigu(self.vorto_o, 'oblan')

    @property
    def vorto_oblaj(self):
        return self.alivortigu(self.vorto_o, 'oblaj')

    @property
    def vorto_oblajn(self):
        return self.alivortigu(self.vorto_o, 'oblajn')

    @property
    def vorto_oble(self):
        return self.alivortigu(self.vorto_o, 'oble')

    @property
    def vorto_oblen(self):
        return self.alivortigu(self.vorto_o, 'oblen')

    @property
    def vorto_opo(self):
        return self.alivortigu(self.vorto_o, 'opo')

    @property
    def vorto_opon(self):
        return self.alivortigu(self.vorto_o, 'opon')

    @property
    def vorto_opoj(self):
        return self.alivortigu(self.vorto_o, 'opoj')

    @property
    def vorto_opojn(self):
        return self.alivortigu(self.vorto_o, 'opojn')

    @property
    def vorto_opa(self):
        return self.alivortigu(self.vorto_o, 'opa')

    @property
    def vorto_opan(self):
        return self.alivortigu(self.vorto_o, 'opan')

    @property
    def vorto_opaj(self):
        return self.alivortigu(self.vorto_o, 'opaj')

    @property
    def vorto_opajn(self):
        return self.alivortigu(self.vorto_o, 'opajn')

    @property
    def vorto_ope(self):
        return self.alivortigu(self.vorto_o, 'ope')

    @property
    def vorto_open(self):
        return self.alivortigu(self.vorto_o, 'open')

    @property
    def vorto_unuo(self):
        #
        # Separação da parte decimal com a precisão desejada
        #
        subnulo = self.nombro < 0
        nombro = abs(self.nombro)
        unuo_kvanto = int(nombro)
        subunuo_kvanto = int((nombro - unuo_kvanto) * (10 ** self.subunuo_precizeco))

        #
        # Vortigo de la unuo-kvanto
        #
        if unuo_kvanto >= 0:
            teksto_unuo = self._potenco(unuo_kvanto) + ' ' + self.unuo

            if unuo_kvanto > 1:
                teksto_unuo += 'j'

        #
        # Vortigo de la subunuo-kvanto
        #
        if subunuo_kvanto > 0:
            teksto_subunuo = self._potenco(subunuo_kvanto) + ' ' + self.subunuo

            if subunuo_kvanto > 1:
                teksto_subunuo += 'j'

        if (unuo_kvanto > 0) and (subunuo_kvanto > 0):
            teksto = teksto_unuo + ' kaj ' + teksto_subunuo
        elif unuo_kvanto >= 0:
            teksto = teksto_unuo
        elif unuo_kvanto < 0:
            teksto = teksto_subunuo

        if subnulo:
            teksto = self.subnulo_masko % teksto

        return teksto


if __name__ == '__main__':
    import sys

    e = NombroVorto(sys.argv[1])
    if len(sys.argv) >= 3:
        e.unuo = sys.argv[3]

    print(e.vorto)
    print(e.vorto_o)
    print(e.vorto_on)
    print(e.vorto_oj)
    print(e.vorto_ojn)
    print(e.vorto_a)
    print(e.vorto_an)
    print(e.vorto_aj)
    print(e.vorto_ajn)
    print(e.vorto_e)
    print(e.vorto_en)
    print(e.vorto_ono)
    print(e.vorto_onon)
    print(e.vorto_onoj)
    print(e.vorto_onojn)
    print(e.vorto_ona)
    print(e.vorto_onan)
    print(e.vorto_onaj)
    print(e.vorto_onajn)
    print(e.vorto_one)
    print(e.vorto_onen)
    print(e.vorto_oblo)
    print(e.vorto_oblon)
    print(e.vorto_obloj)
    print(e.vorto_oblojn)
    print(e.vorto_obla)
    print(e.vorto_oblan)
    print(e.vorto_oblaj)
    print(e.vorto_oblajn)
    print(e.vorto_oble)
    print(e.vorto_oblen)
    print(e.vorto_opo)
    print(e.vorto_opon)
    print(e.vorto_opoj)
    print(e.vorto_opojn)
    print(e.vorto_opa)
    print(e.vorto_opan)
    print(e.vorto_opaj)
    print(e.vorto_opajn)
    print(e.vorto_ope)
    print(e.vorto_open)
    print(e.vorto_unuo)

