# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


import unicodedata


def tira_acentos(texto):
    return unicodedata.normalize(b'NFKD', texto).encode('ascii', 'ignore').encode('utf-8')


def somente_ascii(funcao):
    '''
    Usado como decorator
    '''
    def converter_para_ascii_puro(*args, **kwargs):
        return unicodedata.normalize(b'NFKD', funcao(*args, **kwargs)).encode('ascii', 'ignore')

    return converter_para_ascii_puro


def escape_xml(texto, aspas=True):
    if not texto:
        return texto

    texto = texto.replace('&', '&amp;')
    texto = texto.replace('<', '&lt;')
    texto = texto.replace('>', '&gt;')

    if aspas:
        texto = texto.replace('"', '&quot;')
        texto = texto.replace("'", '&apos;')

    return texto


def unescape_xml(texto):
    if not texto:
        return texto

    texto = texto.replace('&#39;', "'")
    texto = texto.replace('&apos;', "'")
    texto = texto.replace('&quot;', '"')
    texto = texto.replace('&gt;', '>')
    texto = texto.replace('&lt;', '<')
    texto = texto.replace('&amp;', '&')
    texto = texto.replace('&APOS;', "'")
    texto = texto.replace('&QUOT;', '"')
    texto = texto.replace('&GT;', '>')
    texto = texto.replace('&LT;', '<')
    texto = texto.replace('&AMP;', '&')

    return texto
