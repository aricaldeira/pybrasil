# -*- coding: utf-8 -*-
#
# PyBrasil - Functions useful for most Brazil's ERPs
#
# Copyright (C) 2017-
# Copyright (C) Ari Caldeira <ari.caldeira at tauga.com.br>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation, either version 2.1 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# PyBrasil - Funções de validação necessárias a ERPs no Brasil
#
# Copyright (C) 2017-
# Copyright (C) Ari Caldeira <ari.caldeira arroba tauga.com.br>
#
# Este programa é um software livre: você pode redistribuir e/ou modificar
# este programa sob os termos da licença GNU Library General Public License,
# publicada pela Free Software Foundation, em sua versão 2.1 ou, de acordo
# com sua opção, qualquer versão posterior.
#
# Este programa é distribuido na esperança de que venha a ser útil,
# porém SEM QUAISQUER GARANTIAS, nem mesmo a garantia implícita de
# COMERCIABILIDADE ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. Veja a
# GNU Library General Public License para mais detalhes.
#
# Você deve ter recebido uma cópia da GNU Library General Public License
# juntamente com este programa. Caso esse não seja o caso, acesse:
# <http://www.gnu.org/licenses/>
#

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)

from pybrasil.valor.decimal import Decimal as D
from pybrasil.data import parse_datetime
from pybrasil.febraban.boleto import Boleto
from datetime import date


def calcula_digito_nosso_numero(self, boleto):
    if boleto.banco.carteira in ('126', '131', '145', '150', '168'):
        calculo_digito = str(boleto.banco.carteira).zfill(3)[:3]
        calculo_digito += str(boleto.nosso_numero).zfill(8)[:8]
    else:
        calculo_digito = str(boleto.beneficiario.agencia.numero).zfill(4)[:4]
        calculo_digito += str(boleto.beneficiario.codigo.numero).zfill(5)[:5]
        calculo_digito += str(boleto.banco.carteira).zfill(3)[:3]
        calculo_digito += str(boleto.nosso_numero).zfill(8)[:8]

    return self.modulo10(calculo_digito)


def carteira_nosso_numero(self, boleto):
    return '%s/%s-%s' % (boleto.banco.carteira, str(boleto.nosso_numero).zfill(8), boleto.digito_nosso_numero)


def fator_vencimento(self, boleto):
    fator_vencimento = boleto.data_vencimento - date(2000, 7, 3)
    return fator_vencimento.days + 1000


def campo_livre(self, boleto):
    boleto.banco.carteira = str(boleto.banco.carteira).zfill(1)
    boleto.beneficiario.agencia.numero = str(boleto.beneficiario.agencia.numero).zfill(4)
    boleto.banco.modalidade = str(boleto.banco.modalidade).zfill(2)
    boleto.beneficiario.codigo.numero = str(boleto.beneficiario.codigo.numero).zfill(5)
    boleto.beneficiario.codigo.digito = str(boleto.beneficiario.codigo.digito).zfill(1)

    nosso_numero = str(boleto.banco.carteira).zfill(2) + str(boleto.nosso_numero).zfill(15)

    campo_livre = str(boleto.banco.carteira).zfill(3)
    campo_livre += str(boleto.nosso_numero).zfill(8)
    campo_livre += str(boleto.digito_nosso_numero).zfill(1)
    campo_livre += boleto.beneficiario.agencia.numero
    campo_livre += boleto.beneficiario.codigo.numero
    campo_livre += boleto.beneficiario.codigo.digito
    campo_livre += '000'

    return campo_livre


def header_remessa_400(self, remessa):
    boleto = remessa.boletos[0]
    beneficiario = boleto.beneficiario
    #
    # Header do arquivo
    #
    texto = '0'
    texto += '1'
    texto += 'REMESSA' # Na fase de teste informar REM.TST, em produção REMESSA
    texto += '01'
    texto += 'COBRANCA'.ljust(15)
    texto += str(beneficiario.agencia.numero).zfill(4)
    texto += '00'
    texto += str(beneficiario.conta.numero).zfill(5)[:5]
    texto += str(beneficiario.conta.digito).zfill(1)
    texto += ''.ljust(8)
    texto += beneficiario.nome.ljust(30)[:30]
    texto += '341'
    texto += 'BANCO ITAU SA'.ljust(15)
    texto += remessa.data_hora.strftime(b'%d%m%y')
    texto += ''.ljust(294)
    texto += '1'.zfill(6)

    return self.tira_acentos(texto.upper())


def trailler_remessa_400(self, remessa):
    #
    # Trailler do arquivo
    #
    texto = '9'
    texto += ''.ljust(393)
    texto += str(len(remessa.registros) + 1).zfill(6)

    return self.tira_acentos(texto.upper())


def linha_remessa_400(self, remessa, boleto):
    beneficiario = boleto.beneficiario
    pagador = boleto.pagador

    #
    # Registro Tipo 1 – Registro Detalhe Cobrança de Títulos – Arquivo Remessa
    #
    texto = '1'

    if beneficiario.tipo_pessoa == 'PJ':
        texto += '02'
    else:
        texto += '01'

    texto += str(beneficiario.cnpj_cpf_numero).zfill(14)
    texto += str(beneficiario.agencia.numero).zfill(4)
    texto += '00'
    texto += str(beneficiario.codigo.numero).zfill(5)
    texto += str(beneficiario.codigo.digito).zfill(1)
    texto += ''.ljust(4)
    texto += ''.zfill(4) #COD.INSTR.a ser cancelada
    texto += str(boleto.identificacao).ljust(25)[:25] # campo livre para informação do titulo pela empresa
    texto += str(boleto.nosso_numero).zfill(8)[:8]
    texto += ''.zfill(13)
    texto += boleto.banco.carteira.zfill(3)  # numero da carteira
    texto += ''.ljust(21) # identificação da operação no baance
    texto += 'I'  # código da carteira
    texto += boleto.comando or '01'  # identificador da ocorrencia
    texto += str(boleto.documento.numero).ljust(10)[:10]
    texto += boleto.data_vencimento.strftime('%d%m%y')
    texto += str(int(boleto.documento.valor * 100)).zfill(13)
    texto += '341'
    texto += ''.zfill(5) # agencia onde o titulo sera cobrado.
    texto += '01'  # especie do titulo'
    texto += 'A' if boleto.aceite != 'N' else 'N' # aceito e não aceito
    texto += boleto.data_processamento.strftime('%d%m%y')

    if boleto.dias_protesto:
        texto += '34'.zfill(2)  # protestar após XX dias corridos
    else:
        texto += ''.zfill(2)  # 1 instrução de cobrança

    if boleto.dias_negativacao:
        texto += '66'.zfill(2)  # 2 instrução de cobrança
    else:
        texto += ''.zfill(2)  # 2 instrução de cobrança

    texto += str(int(boleto.valor_juros * 100)).zfill(13)

    if boleto.data_desconto:
        texto += boleto.data_desconto.strftime('%d%m%y')
        texto += str(int(boleto.valor_desconto * 100)).zfill(13)[:13]
    else:
        texto += ''.zfill(6)
        texto += ''.zfill(13)

    texto += str(int(boleto.valor_iof * 100)).zfill(13)[:13]
    texto += str(int(boleto.valor_abatimento * 100)).zfill(13)[:13]

    if pagador.tipo_pessoa == 'PJ':
        texto += '02'
    else:
        texto += '01'

    texto += pagador.cnpj_cpf_numero.zfill(14)
    texto += pagador.nome.ljust(30)[:30]
    texto += ''.ljust(10)
    texto += pagador.endereco_numero_complemento.ljust(40)[:40]
    texto += pagador.bairro.ljust(12)[:12]
    texto += pagador.cep.replace('-', '').zfill(8)
    texto += pagador.cidade.ljust(15)[:15]
    texto += pagador.estado[:2]
    texto += ''.ljust(30)
    texto += ''.ljust(4)
    texto += boleto.data_vencimento.strftime('%d%m%y')

    if boleto.dias_protesto:
        texto += str(boleto.dias_protesto).zfill(2)[:2]  # protestar após XX dias corridos
    elif boleto.dias_negativacao:
        texto += str(boleto.dias_negativacao).zfill(2)[:2]
    else:
        texto += ''.zfill(2)

    texto += ''.ljust(1)
    texto += str(len(remessa.registros) + 1).zfill(6)[:06]  # nº do registro

    return self.tira_acentos(texto.upper())


def header_retorno_400(self, retorno):
    header = retorno.linhas[0]

    beneficiario = retorno.beneficiario

    beneficiario.agencia.numero = header[26:30]
    #beneficiario.agencia.digito = header[30]
    beneficiario.codigo.numero = header[32:36]
    beneficiario.codigo.digito = header[36]
    beneficiario.nome = header[46:76]

    retorno.data_hora = parse_datetime(header[94:100]).date()
    retorno.sequencia = int(header[108:113])


def linha_retorno_400(self, retorno):
    beneficiario = retorno.beneficiario
    linha = retorno.linhas[1]

    #
    # Beneficiario
    #
    beneficiario.cnpj_cpf = linha[3:17]
    beneficiario.agencia.numero = linha[17:21]

    beneficiario.codigo.numero = linha[23:28]
    beneficiario.codigo.digito = linha[28]

    beneficiario.conta.numero = linha[23:28]
    beneficiario.conta.digito = linha[28]

    for i in range(1, len(retorno.linhas) - 1):
        linha = retorno.linhas[i]
        boleto = Boleto()
        boleto.beneficiario = retorno.beneficiario
        boleto.banco = self

        boleto.identificacao = linha[37:62]
        boleto.nosso_numero = unicode(D(linha[62:70]))
        boleto.comando = linha[108:110]
        boleto.data_ocorrencia = parse_datetime(linha[110:116])
        boleto.documento.numero = linha[116:126]

        if linha[146:152].strip() != '000000':
            boleto.data_vencimento = parse_datetime(linha[146:152]).date()

        boleto.documento.valor = D(linha[152:165]) / D('100')
        boleto.valor_despesa_cobranca = D(linha[175:188]) / D('100')
        #boleto.valor_outras_despesas = D(linha[188:201]) / D('100')
        #boleto.valor_multa = D(linha[188:201]) / D('100')
        boleto.valor_iof = D(linha[214:227]) / D('100')
        boleto.valor_abatimento = D(linha[227:240]) / D('100')
        boleto.valor_desconto = D(linha[240:253]) / D('100')
        boleto.valor_recebido = D(linha[253:266]) / D('100')
        boleto.valor_juros = D(linha[266:279]) / D('100')
        boleto.valor_outros_creditos = D(linha[279:292]) / D('100')

        if len(linha[295:301].strip()) > 0 and linha[295:301] != '000000':
            boleto.data_credito = parse_datetime(linha[295:301]).date()

        retorno.boletos.append(boleto)


DESCRICAO_COMANDO_REMESSA = {
    '01': 'Registro de título',
    '02': 'Solicitação de baixa',
    '03': 'Pedido protesto falimentar',
    '04': 'Concessão de abatimento',
    '05': 'Cancelamento de abatimento',
    '06': 'Alteração de vencimento',
    '07': 'Alteração do número de controle',
    '08': 'Alteração de seu número',
    '09': 'Instrução para protestar',
    '18': 'Sustar protesto e baixar título',
    '19': 'Sustar protesto e manter título',
    '22': 'Transferência de cessão de crédito',
    '23': 'Transferência entre carteiras',
    '24': 'Devolução de transf. entre carteiras',
    '31': 'Alteração de outros dados',
    '68': 'Acerto do dados do rateio de crédito',
    '69': 'Cancelamento dos dados do rateio',
}


DESCRICAO_COMANDO_RETORNO = {
    '01': 'Título não existe',
    '02': 'Confirmação de entrada do título',
    '03': 'Rejeição de entrada do título',
    #04
    #05
    '06': 'Liquidação normal',
    '07': 'Liquidação parcial',
    '08': 'Liquidação em cartório',
    '09': 'Baixa de título',
    '10': 'Baixa a pedido do beneficiário ou protesto',
    #'11': 'Títulos em aberto',
    #'12': 'Abatimento concedido',
    #'13': 'Abatimento cancelado',
    #'14': 'Alteração de vencimento',
    #'15': 'Enviado para cartório',
    #'16': 'Título já baixado/liquidado',
    #'17': 'Liquidação em cartório',
    #'17': 'Liquidação após baixa ou sem registro',
    #'18': 'Acerto de depositária',
    #'19': 'Instrução de protesto',
    #'20': 'Sustação de protesto',
    #'21': 'Entrada em cartório',
    #'22': 'Retirado de cartório',
    #'23': 'Encaminhado a protesto',
    #'24': 'Custas de cartório',
    #'25': 'Instrução de protesto',
    #'26': 'Sustar protesto',
    #'27': 'Baixa rejeitada',
    #'28': 'Débito de tarifas',
    #'29': 'Ocorrência do pagador',
    #'30': 'Alteração de outros dados rejeitados',
    #'32': 'Instrução rejeitada',
    #'33': 'Confirmação pedido de alteração de outros dados',
    #'34': 'Retirado do cartório e manutenção carteira',
    #'35': 'Desagendamento do débito automático',
    #'40': 'Estorno de pagamento',
    #'55': 'Sustação judicial',
    #'68': 'Acerto do dados do rateio de crédito',
    #'69': 'Cancelamento dos dados do rateio',
}


COMANDOS_RETORNO_LIQUIDACAO = {
    '06': True,
    '07': True,
    '08': True,
    #'16': False,
    #'17': True,
}


COMANDOS_RETORNO_BAIXA = [
    '09',
    '10',
]
