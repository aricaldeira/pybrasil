# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from . import (base, data, ibge, inscricao, ncm, telefone, valor, template,
               febraban)
from .python_pt_BR import python_pt_BR

import sys
import locale

if sys.version_info.major == 2:
    locale.setlocale(locale.LC_ALL, b'pt_BR.UTF-8')
    locale.setlocale(locale.LC_COLLATE, b'pt_BR.UTF-8')
else:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
