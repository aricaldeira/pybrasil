# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)

import re
from ..inscricao.cnpj_cpf import eh_tudo_igual
from ..base import modulo10

LIMPA = re.compile(r'[^0-9]')


def valida_ean(codigo):
    codigo = LIMPA.sub('', codigo)
    
    if not codigo:
        return False
    
    if eh_tudo_igual(codigo):
        return False
    
    if len(codigo) not in (14, 13, 12, 8):
        return False
    
    if modulo10(codigo[:-1], modulo=True) != codigo[-1]:
        return False
    
    return True


