# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)
import re


ESPACO_MULTIPLO = re.compile(r'\s+')

NUMERO_ROMANO = re.compile(r'^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')

PES = re.compile(r'(.*)([0-9])\s\'\s(.*)$')
POLEGADAS = re.compile(r'(.*)([0-9])\s\"\s(.*)$')

PREPOSICOES = [
    'e', 'o', 'os', 'a', 'as',
    'um', 'uns', 'uma', 'umas',
    'de', 'do', 'dos', 'da', 'das',
    'dum', 'duns', 'duma', 'dumas',
    'em', 'no', 'nos', 'na', 'nas',
    'num', 'nuns', 'numa', 'numas',
    'com', 'para', 'que',
    'a', 'ao', 'aos', 'à', 'às', 'até',
    'por', 'pelo', 'pelos', 'pela', 'pelas',
    'sob', 'entre', 'ou',
    'não',
    #
    # Nomes estrangeiros
    #
    'di', 'dello', 'della', 'dalla', 'del', 'dal', 'dall', 'in', 'con', 'su', 'per', 'fra', 'tra',
    'nel', 'nell', 'nello', 'nella'
    'and', 'at', 'upon', 'by', 'in',
    'in', 'aus', 'auf', 'von', 'über', 'uber', 'der', 'die', 'dem', 'den',
    'van',
    'en', 'sur', 'et', 'le', 'la', 'les', 'du', 'des',
    'y', 'u'
]

PREPOSICOES_ABREVIADAS = [
    ("d'", "d’"),
    ("del'", "del’"),
    ("dell'", "dell’"),
    ("dal'", "dal’"),
    ("dall'", "dall’"),
    ("l'", "l’"),
]

ACRONIMOS = [
    'epp',
    'me',
    'mei',
    's/a',
    's/c',
    's/s',
    's.a.',
    's.c.',
    's.s.',
    'eireli',
    'simei',

    #
    # Impostos
    #
    'icms',
    'inss',
    'iss',
    'issqn',
    'fgts',
    'pcc',
    'pis',
    'cofins',
    'csll',
    'irpf',
    'irpj',
    'irrf',
    'ipi',
    'pf',
    'pj',

    'nfe',
    'nfse',
    'nfce',
    'cte',

    'danfe'
    'danfce',
    'danfse',
    'dacte',

    #
    # Siglas dos Estados
    #
    'ac',
    'al',
    'am',
    'ap',
    'ba',
    'ce',
    'df',
    'es',
    'go',
    'ma',
    'mg',
    'ms',
    'mt',
    'pa',
    'pb',
    'pe',
    'pi',
    'pr',
    'rj',
    'rn',
    'ro',
    'rr',
    'rs',
    'sc',
    'se',
    'sp',
    'to',
    'ex',

    #
    # Outras palavras comuns
    #
    'tv',
    'pvc',
]

ABREVIATURAS = [
    'dr',
    'r',
    'av',
    'rod',
    'esq',
    'ltda',
    'cia',
]

LIMPEZA = [
    ('EIRELI - ME', 'EIRELI ME'),
    ('EIRELI   ME', 'EIRELI ME'),

    ('Ltda - ME', 'Ltda. ME'),
    ('Ltda   ME', 'Ltda. ME'),

    ('Ltda. - ME', 'Ltda. ME'),
    ('Ltda.   ME', 'Ltda. ME'),

    ('NFE', 'NF-e'),
    ('Nfe', 'NF-e'),
    ('Nf-E', 'NF-e'),
    ('Nf-e', 'NF-e'),

    ('NFSE', 'NFS-e'),
    ('Nfse', 'NFS-e'),
    ('Nfs-E', 'NFS-e'),
    ('Nfs-e', 'NFS-e'),

    ('NFCE', 'NFC-e'),
    ('Nfce', 'NFC-e'),
    ('Nfc-E', 'NFC-e'),
    ('Nfc-e', 'NFC-e'),

    ('CTE', 'CT-e'),
    ('Cte', 'CT-e'),
    ('Ct-E', 'CT-e'),
    ('Ct-e', 'CT-e'),

    ('Danfe', 'DANFE'),
    ('DANF-e', 'DANFE'),
    ('Danfse', 'DANFSE'),
    ('DANFS-e', 'DANFSE'),
    ('Danfce', 'DANFCE'),
    ('DANFC-e', 'DANFCE'),
    ('Dacte', 'DACTE'),
    ('DACT-e', 'DACTE'),
]


SINAIS = (
    ',',
    ';',
    ':',
    '/',
    '\\',
    '"',
    "'",
    '”',
    "’",
    '“',
    "‘",
)


#
# Código adaptado daqui:
# http://goncin.wordpress.com/2010/12/16/normalizando-nomes-proprios-com-php/
#
def primeira_maiuscula(texto, nome_proprio=True, acrescenta_ponto=False):
    termina_com_ponto = texto.endswith('.')
    #
    # A primeira tarefa da normalização é lidar com partes do nome que
    # porventura estejam abreviadas,considerando-se para tanto a existência de
    # pontos finais (p. ex. JOÃO A. DA SILVA, onde "A." é uma parte abreviada).
    # Dado que mais à frente dividiremos o nome em partes tomando em
    # consideração o caracter de espaço (" "), precisamos garantir que haja um
    # espaço após o ponto. Fazemos isso substituindo todas as ocorrências do
    # ponto por uma sequência de ponto e espaço.
    #
    texto = texto.replace('.', '. ')
    if termina_com_ponto and texto.endswith('. '):
        texto = texto.strip()

    #
    # O procedimento anterior, ou mesmo a digitação errônea, podem ter
    # introduzido espaços múltiplos entre as partes do nome, o que é totalmente
    # indesejado. Para corrigir essa questão, utilizamos uma substituição
    # baseada em expressão regular, a qual trocará todas as ocorrências de
    # espaços múltiplos por espaços simples.
    #
    texto = ESPACO_MULTIPLO.sub(' ', texto)

    #
    # Quebramos também os hífens, no caso de nomes próprios
    #
    if nome_proprio:
        texto = texto.replace('-', '- ')
        texto = texto.replace('-', ' -')

    #
    # Quebramos os outros sinais de pontuação
    #
    for sinal in SINAIS:
        texto = texto.replace(sinal, sinal + ' ')
        texto = texto.replace(sinal, ' ' + sinal)

    partes_nome = []

    for parte_nome in texto.lower().split(' '):
        if parte_nome in PREPOSICOES:
            partes_nome.append(parte_nome)
            continue

        if parte_nome.lower() in ACRONIMOS:
            partes_nome.append(parte_nome.upper())
            continue

        if NUMERO_ROMANO.match(parte_nome.upper()):
            partes_nome.append(parte_nome.upper())
            continue

        for pa_feia, pa_bonita in PREPOSICOES_ABREVIADAS:
            pa_feia = pa_feia.replace("'", "")

            if pa_feia == parte_nome:
                partes_nome.append(pa_feia)
                parte_nome = parte_nome.replace(pa_feia, '')
                break

        parte_nome = parte_nome[0].upper() + parte_nome[1:]
        partes_nome.append(parte_nome)

        if acrescenta_ponto and parte_nome.lower() in ABREVIATURAS:
            partes_nome.append('.')

    nome = ' '.join(partes_nome)

    if nome_proprio:
        nome = nome.replace(' -', '-')
        nome = nome.replace('- ', '-')

    if acrescenta_ponto:
        nome = nome.replace(' .', '.')
        nome = nome.replace('..', '.')

    nome = nome[0].upper() + nome[1:]

    while PES.match(nome):
        nome = PES.sub(r'\1\2 ’ \3', nome)

    while POLEGADAS.match(nome):
        nome = POLEGADAS.sub(r'\1\2 ” \3', nome)

    #
    # Retorna os outros sinais de pontuação
    #
    for sinal in SINAIS:
        nome = nome.replace(sinal + ' ', sinal)
        nome = nome.replace(' ' + sinal, sinal)

    #
    # Coloca as aspas bonitas
    #
    nome = nome.replace(' "', ' “')
    nome = nome.replace('" ', '” ')
    nome = nome.replace(" '", " ‘")
    nome = nome.replace("' ", "’ ")

    for pa_feia, pa_bonita in PREPOSICOES_ABREVIADAS:
        nome = nome.replace(pa_feia, pa_bonita)
        nome = nome.replace(pa_bonita + ' ', pa_bonita)

    for feio, bonito in LIMPEZA:
        if feio in nome:
            nome = nome.replace(feio, bonito)

    return nome
