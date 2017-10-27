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

from builtins import str
from pybrasil.valor.decimal import Decimal as D
from pybrasil.data import parse_datetime
from pybrasil.febraban.boleto import Boleto


def limpa_nome(texto):
    probibidos = u'.,-_;:?!=+*/&#$%{}[]()<>|@"\´`~^¨' + u"'"

    for c in probibidos:
        texto = texto.replace(c, ' ')

    while '  ' in texto:
        texto = texto.replace('  ', ' ')

    return texto


def calcula_digito_nosso_numero(self, boleto):
    boleto.banco.carteira = str(boleto.banco.carteira).zfill(2)
    boleto.nosso_numero = str(boleto.nosso_numero).zfill(11)
    return self.modulo11(boleto.banco.carteira + boleto.nosso_numero, pesos=range(2, 8), mapa_digitos={10: 'P', 11: 0})


def campo_livre(self, boleto):
    boleto.nosso_numero = str(boleto.nosso_numero).zfill(11)

    campo_livre = str(boleto.beneficiario.agencia.numero).zfill(4)
    campo_livre += str(boleto.banco.carteira).zfill(2)
    campo_livre += str(boleto.nosso_numero).zfill(11)
    campo_livre += str(boleto.beneficiario.conta.numero).zfill(7)
    campo_livre += '0'
    return campo_livre


def agencia_conta(self, boleto):
    agencia = str(boleto.beneficiario.agencia.numero).zfill(4)

    return '%s-%s / %s-%s' % (agencia, str(boleto.beneficiario.agencia.digito).zfill(1), str(boleto.beneficiario.codigo.numero).zfill(6), str(boleto.beneficiario.codigo.digito).zfill(1))


def header_remessa_400(self, remessa):
    boleto = remessa.boletos[0]
    beneficiario = boleto.beneficiario
    #
    # Header do arquivo
    #
    texto = '0'
    texto += '1'
    texto += 'REMESSA'
    texto += '01'
    texto += 'COBRANCA'.ljust(15)
    texto += str(beneficiario.codigo.numero).zfill(20)
    texto += beneficiario.nome.ljust(30)[:30]
    texto += '237'
    texto += 'BRADESCO'.ljust(15)
    texto += remessa.data_hora.strftime(b'%d%m%y')
    texto += ''.ljust(8)
    texto += 'MX'
    texto += str(remessa.sequencia).zfill(7)
    texto += ''.ljust(277)
    texto += str(1).zfill(6)

    return self.tira_acentos(texto.upper())


def trailler_remessa_400(self, remessa):
    #
    # Trailler do arquivo
    #
    texto = '9'
    texto += ''.ljust(393)
    texto += str(len(remessa.registros) + 1).zfill(6)  # Quantidade de registros

    return self.tira_acentos(texto.upper())


def linha_remessa_400(self, remessa, boleto):
    beneficiario = boleto.beneficiario
    banco = boleto.banco
    pagador = boleto.pagador

    #
    # 1º segmento
    #
    texto = '1'
    texto += '00000'
    texto += '0'
    texto += '00000'
    texto += '0000000'
    texto += '0'
    #
    # posições 21 a 37
    #
    texto += '0'
    texto += str(banco.carteira).zfill(3)
    texto += beneficiario.agencia.numero.zfill(5)
    texto += beneficiario.conta.numero.zfill(7)
    texto += beneficiario.conta.digito.zfill(1)

    texto += str(boleto.identificacao).ljust(25)
    texto += '000'  # Preencher com 237 somente se for débito automático

    if boleto.valor_multa > 0:
        texto += '2'
        percentual_multa = D(str(boleto.valor_multa)) / D(str(boleto.documento.valor)) * D('100')
        texto += str(int(percentual_multa * 100)).zfill(4)
    else:
        texto += '0'
        texto += '0000'

    texto += str(boleto.nosso_numero).zfill(11)
    texto += str(boleto.digito_nosso_numero).zfill(1)

    texto += ''.zfill(10)
    texto += '2'  # Beneficiário emite, banco registra
    texto += 'N'
    texto += ''.ljust(10)
    texto += ' '
    texto += '0'
    texto += '  '
    texto += boleto.comando or '01'  # Registro do boleto no banco
    texto += str(boleto.documento.numero).ljust(10)[:10]
    texto += boleto.data_vencimento.strftime('%d%m%y')
    texto += str(int(boleto.documento.valor * 100)).zfill(13)
    texto += '0'.zfill(3)
    texto += '0'.zfill(5)
    texto += '01'  # Tipo do documento - 99 outros
    texto += 'N'
    texto += boleto.data_processamento.strftime('%d%m%y')

    if boleto.dias_protesto:
        texto += '06'
        texto += str(boleto.dias_protesto).zfill(2)
    else:
        texto += '00'
        texto += '00'

    texto += str(int(boleto.valor_juros * 100)).zfill(13)

    if boleto.data_desconto:
        texto += boleto.data_desconto.strftime('%d%m%y')
        texto += str(int(boleto.valor_desconto * 100)).zfill(13)
    else:
        texto += ''.zfill(6)
        texto += ''.zfill(13)

    texto += str(int(boleto.valor_iof * 100)).zfill(13)
    texto += str(int(boleto.valor_abatimento * 100)).zfill(13)

    if pagador.tipo_pessoa == 'PJ':
        texto += '02'
    else:
        texto += '01'

    texto += pagador.cnpj_cpf_numero.zfill(14)
    texto += pagador.nome[:40].ljust(40)
    texto += pagador.endereco_numero_complemento.ljust(40)[:40]
    texto += ''.ljust(12)
    texto += pagador.cep.replace('-', '').zfill(8)

    #
    # Tem o sacador?
    #
    if boleto.sacador.cnpj_cpf:
        sacador = boleto.sacador

        if sacador.tipo_pessoa == 'PJ':
            #texto += '02'
            texto += sacador.cnpj_cpf_numero[::-1] + '0'

        else:
            #texto += '01'
            texto += sacador.cnpj_cpf_numero[::-1][0:2] + '0000' + sacador.cnpj_cpf_numero[::-1][2:] + '000'

        texto += '  '
        texto += sacador.nome[:43].ljust(43)

    else:
        texto += ''.ljust(60)  # Sacador/avalista - não existe mais

    texto += str(len(remessa.registros) + 1).zfill(6)  # nº do registro

    return self.tira_acentos(texto.upper())


def header_retorno_400(self, retorno):
    header = retorno.linhas[0]

    beneficiario = retorno.beneficiario

    #beneficiario.agencia.numero = header[26:30]
    #beneficiario.agencia.digito = header[30]
    beneficiario.codigo.numero = str(D(header[26:46]))
    #beneficiario.codigo.digito = header[39]
    beneficiario.nome = header[46:76]

    retorno.data_hora = parse_datetime(header[94:100]).date()
    retorno.sequencia = int(header[108:113])


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
    '02': 'Confirmação de entrada do título',
    '03': 'Rejeição de entrada do título',
    '06': 'Liquidação normal',
    '09': 'Baixa de título',
    '10': 'Baixa a pedido do beneficiário',
    '11': 'Títulos em aberto',
    '12': 'Abatimento concedido',
    '13': 'Abatimento cancelado',
    '14': 'Alteração de vencimento',
    '15': 'Liquidação em cartório',
    '16': 'Liquidação com cheque',
    '17': 'Liquidação após baixa ou sem registro',
    '18': 'Acerto de depositária',
    '19': 'Instrução de protesto',
    '20': 'Sustação de protesto',
    '21': 'Acerto do controle do participante',
    '22': 'Pagamento cancelado',
    '23': 'Encaminhado a protesto',
    '24': 'Rejeitado - CEP irregular',
    '25': 'Instrução de protesto falimentar',
    '27': 'Baixa rejeitada',
    '28': 'Débito de tarifas',
    '29': 'Ocorrência do pagador',
    '30': 'Alteração de outros dados rejeitados',
    '32': 'Instrução rejeitada',
    '33': 'Confirmação pedido de alteração de outros dados',
    '34': 'Retirado do cartório e manutenção carteira',
    '35': 'Desagendamento do débito automático',
    '40': 'Estorno de pagamento',
    '55': 'Sustação judicial',
    '68': 'Acerto do dados do rateio de crédito',
    '69': 'Cancelamento dos dados do rateio',
}


COMANDOS_RETORNO_LIQUIDACAO = {
    '06': True,
    '15': True,
    #'16': False,
    '17': True,
}


COMANDOS_RETORNO_BAIXA = [
    '09',
    '10',
]


def linha_retorno_400(self, retorno):
    beneficiario = retorno.beneficiario
    linha = retorno.linhas[1]

    #
    # Beneficiario
    #
    beneficiario.cnpj_cpf = linha[3:17]
    self.carteira = linha[23]
    beneficiario.agencia.numero = linha[25:29]
    beneficiario.conta.numero = linha[29:36]
    beneficiario.conta.digito = linha[36]

    for i in range(1, len(retorno.linhas) - 1):
        linha = retorno.linhas[i]
        boleto = Boleto()
        boleto.beneficiario = retorno.beneficiario
        boleto.banco = self

        boleto.identificacao = linha[37:62]
        boleto.nosso_numero = str(D(linha[70:81]))
        #boleto.nosso_numero_digito = linha[82]
        boleto.banco.carteira = linha[107]
        boleto.comando = linha[108:110]
        boleto.data_ocorrencia = parse_datetime(linha[110:116]).date()
        boleto.documento.numero = linha[116:126]
        if linha[146:152].strip() != '000000':
            boleto.data_vencimento = parse_datetime(linha[146:152]).date()
        boleto.documento.valor = D(linha[152:165]) / D('100')
        boleto.valor_despesa_cobranca = D(linha[175:188]) / D('100')
        #boleto.valor_outras_despesas = D(linha[188:201]) / D('100')
        boleto.valor_multa = D(linha[188:201]) / D('100')
        boleto.valor_iof = D(linha[214:227]) / D('100')
        boleto.valor_abatimento = D(linha[227:240]) / D('100')
        boleto.valor_desconto = D(linha[240:253]) / D('100')
        boleto.valor_recebido = D(linha[253:266]) / D('100')
        boleto.valor_juros = D(linha[266:279]) / D('100')
        boleto.valor_outros_creditos = D(linha[279:292]) / D('100')

        if len(linha[295:301].strip()) > 0 and linha[295:301] != '000000':
            boleto.data_credito = parse_datetime(linha[295:301]).date()

        boleto.pagador.cnpj_cpf = linha[342:357]

        retorno.boletos.append(boleto)
