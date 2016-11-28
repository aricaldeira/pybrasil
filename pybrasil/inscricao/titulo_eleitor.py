# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from ..base import modulo11
from .cnpj_cpf import eh_tudo_igual
from .inscricao_estadual import LIMPA
from ..valor import formata_valor


#
# Validação do Título de Eleitor de acordo com
# http://www.tse.jus.br/legislacao/codigo-eleitoral/normas-editadas-pelo-tse/resolucao-nb0-21.538-de-14-de-outubro-de-2003-brasilia-2013-df
#

DIGITOS_ESTADOS = {
    '01': 'São Paulo',
    '02': 'Minas Gerais',
    '03': 'Rio de Janeiro',
    '04': 'Rio Grande do Sul',
    '05': 'Bahia',
    '06': 'Paraná',
    '07': 'Ceará',
    '08': 'Pernambuco',
    '09': 'Santa Catarina',
    '10': 'Goiás',
    '11': 'Maranhão',
    '12': 'Paraíba',
    '13': 'Pará',
    '14': 'Espírito Santo',
    '15': 'Piauí',
    '16': 'Rio Grande do Norte',
    '17': 'Alagoas',
    '18': 'Mato Grosso',
    '19': 'Mato Grosso do Sul',
    '20': 'Distrito Federal',
    '21': 'Sergipe',
    '22': 'Amazonas',
    '23': 'Rondônia',
    '24': 'Acre',
    '25': 'Amapá',
    '26': 'Roraima',
    '27': 'Tocantins',
    '28': 'Exterior (ZZ)',
}


def valida_titulo_eleitor(titulo_eleitor):
    u'''Verifica que o título de eleitor seja válido
    de acordo com os dígitos verificadores
    '''
    titulo_eleitor = LIMPA.sub('', titulo_eleitor)

    if len(titulo_eleitor) < 12:
        titulo_eleitor = titulo_eleitor.zfill(12)

    if len(titulo_eleitor) != 12:
        return False

    if not titulo_eleitor.isdigit():
        return False

    if eh_tudo_igual(titulo_eleitor):
        return False

    #
    # Verifica os dígitos referentes ao estado
    #
    digito_estado = titulo_eleitor[8:10]
    if digito_estado not in DIGITOS_ESTADOS:
        return False

    digito = titulo_eleitor[-2:]

    d1 = modulo11(titulo_eleitor[:8], pesos=range(2, 11), resto=True)

    #
    # Tratamento especial do 1º dígito
    # para SP e MG
    #
    if digito_estado in ['01', '02']:
        if d1 == '1':
            d1 = '0'
        elif d1 == '0':
            d1 = '1'
        else:
            d1 = str(11 - int(d1))
    else:
        if d1 == '1' or d1 == '0':
            d1 = '0'
        else:
            d1 = str(11 - int(d1))

    d2 = modulo11(titulo_eleitor[8:11], pesos=range(2, 11))

    print(d1, d2)
    digitocalc = d1 + d2

    return digito == digitocalc


def formata_titulo_eleitor(titulo_eleitor):
    if not valida_titulo_eleitor(titulo_eleitor):
        return titulo_eleitor

    titulo_eleitor = LIMPA.sub('', titulo_eleitor)
    titulo_eleitor = str(int(titulo_eleitor))
    digitos = titulo_eleitor[-2:]
    numero = titulo_eleitor[:-2]
    numero = formata_valor(int(numero), casas_decimais=0)
    return numero + '-' + digitos
