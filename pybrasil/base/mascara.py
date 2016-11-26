# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


def mascara(texto, mascara):
    j = 0
    texto_mascarado = ''
    for i in range(len(mascara)):
        if j < len(texto):
            if mascara[i] == ' ':
                texto_mascarado += texto[j]
                j += 1

            else:
                texto_mascarado += mascara[i]

    texto_mascarado = texto_mascarado.replace('·', ' ')

    return texto_mascarado
