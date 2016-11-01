# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)
import os
import sys
from ..data import hoje, data_hora_horario_brasilia, parse_datetime
from ..ibge import (Local, Municipio, Estado, MUNICIPIO_ESTADO_NOME, MUNICIPIO_IBGE, MUNICIPIO_SIAFI, ESTADO_IBGE, ESTADO_SIGLA)
from ..base import tira_acentos
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta
from copy import copy


CURDIR = os.path.dirname(os.path.abspath(__file__))


class Feriado(Local):
    def __init__(self, **kwargs):
        super(Feriado, self).__init__(**kwargs)
        self.nome = kwargs.get('nome', '')
        self.tipo = kwargs.get('tipo', 'F')
        self.abrangencia = kwargs.get('abrangencia', 'N')
        self.quando = kwargs.get('quando', None)
        self.dia = kwargs.get('dia', None)
        self.dia_da_semana = kwargs.get('dia_da_semana', None)
        self.mes = kwargs.get('mes', None)
        self.ano = kwargs.get('ano', None)
        self.dias_de_diferenca = kwargs.get('dias_de_diferenca', 0)
        self.ajuste = kwargs.get('ajuste', None)

    def __str__(self):
        return unicode.encode(self.__unicode__(), 'utf-8')

    def __unicode__(self):
        txt = self.nome + ' - ' + self.data().strftime('%a, %d-%b-%Y').decode('utf-8')

        if self.abrangencia == 'E':
            txt += ', somente em ' + unicode(self.estado)
        elif self.abrangencia == 'M':
            txt += ', somente em ' + unicode(self.municipio)

        return txt

    def __repr__(self):
        return str(self)

    def data(self, data_referencia=hoje()):
        data_referencia = parse_datetime(data_referencia)
        ano = data_referencia.year
        mes = data_referencia.month
        dia = data_referencia.day
        data_feriado = data_referencia

        if self.quando == 'A':
            data_feriado = date(self.ano, self.mes, self.dia)

        elif self.quando == 'M':
            data_feriado = date(ano, self.mes, self.dia)

        elif self.quando == 'D':
            data_feriado = date(ano, mes, self.dia)

        elif self.quando == 'P':
            data_feriado = data_hora_horario_brasilia(easter(ano))

        elif self.quando == 'S':
            data_feriado = date(ano, self.mes, 1)

            #
            # Dias para chegar no dia da semana
            #
            dias_a_avancar = self.dia_da_semana - data_feriado.weekday()

            #
            # Dias para chegar no nº dia da semana no mês
            #
            if self.dia > 1:
                dias_a_avancar += (self.dia - 1) * 7

            data_feriado = data_feriado + relativedelta(days=dias_a_avancar)

        data_feriado += relativedelta(days=self.dias_de_diferenca)

        if self.ajuste:
            if self.ajuste == 'AC':
                #
                # Se o feriado cair na terça, quarta ou quinta,
                # avança para sexta
                #
                if data_feriado.weekday() in (1, 2, 3):
                    dias_a_avancar = 4 - data_feriado.weekday()
                    data_feriado += relativedelta(days=dias_a_avancar)

            elif self.ajuste == 'SC':
                #
                # Se o feriado cair em dia útil,
                # avança para sábado
                #
                if data_feriado.weekday() in (0, 1, 2, 3, 4, 5):
                    dias_a_avancar = 6 - data_feriado.weekday()
                    data_feriado += relativedelta(days=dias_a_avancar)

        return data_hora_horario_brasilia(data_feriado).date()


def _monta_lista_feriados():
    lista = []

    arquivo = open(os.path.join(CURDIR, 'feriado.txt'), 'r')

    #
    # Pula a primeira linha
    #
    arquivo.readline()

    for linha in arquivo:
        linha = linha.decode('utf-8').replace('\n', '').replace('\r', '')
        campos = linha.split('|')
        nome, tipo, abrangencia, estado, municipio_ibge, municipio_nome, quando, dia, dia_da_semana, mes, ano, dias_de_diferenca, ajuste = campos

        if dia != '':
            dia = int(dia)

        if dia_da_semana != '':
            dia_da_semana = int(dia_da_semana)

        if mes != '':
            mes = int(mes)

        if ano != '':
            ano = int(ano)

        if dias_de_diferenca != '':
            dias_de_diferenca = int(dias_de_diferenca)

        f = Feriado(nome=nome, tipo=tipo, abrangencia=abrangencia, estado=estado, municipio=municipio_ibge, quando=quando, dia=dia, dia_da_semana=dia_da_semana, mes=mes, ano=ano, dias_de_diferenca=dias_de_diferenca, ajuste=ajuste)

        lista.append(f)

    return lista


if not hasattr(sys.modules[__name__], 'FERIADOS'):
    FERIADOS = _monta_lista_feriados()


_numero_de_feriados = 0
_memoria_feriados = {}


def _monta_dicionario_datas(data_referencia=hoje()):
    global _numero_de_feriados
    global _memoria_feriados
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()

    if len(FERIADOS) == _numero_de_feriados and data_referencia in _memoria_feriados:
        return _memoria_feriados[data_referencia]

    dicionario = {}

    for f in FERIADOS:
        data = f.data(data_referencia)

        if data in dicionario:
            dicionario[data].append(f)
        else:
            dicionario[data] = [f]

    if _numero_de_feriados != len(FERIADOS):
        _numero_de_feriados = len(FERIADOS)
        _memoria_feriados = {}

    _memoria_feriados[data_referencia] = dicionario

    return dicionario


def monta_dicionario_datas(data_referencia=hoje(), tipo=None, estado=None, municipio=None):
    data_referencia = data_hora_horario_brasilia(parse_datetime(data_referencia)).date()

    f_teste = Feriado()
    f_teste.estado = estado
    f_teste.municipio = municipio

    dicionario = {}

    for data, feriados in _monta_dicionario_datas(data_referencia).iteritems():
        for f in feriados:
            if tipo is not None:
                if isinstance(tipo, (list, tuple)):
                    if f.tipo not in tipo:
                        continue

                elif isinstance(tipo, (str, unicode)):
                    if f.tipo != tipo:
                        continue

            if estado is not None:
                if f.abrangencia == 'E' and f.estado != f_teste.estado:
                    continue

                elif f.abrangencia == 'M' and f.municipio.estado != f_teste.estado:
                    continue

            if municipio is not None:
                if f.abrangencia == 'E' and f.estado != f_teste.municipio.estado:
                    continue

                elif f.abrangencia == 'M' and f.municipio != f_teste.municipio:
                    continue

            if data in dicionario:
                dicionario[data].append(f)
            else:
                dicionario[data] = [f]

    return dicionario
