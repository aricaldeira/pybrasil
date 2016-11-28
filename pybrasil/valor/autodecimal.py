# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from decimal import Decimal


class DecimalAutoFloat(Decimal):
    @classmethod
    def from_float(klass, valor):
        return klass(str(valor))
