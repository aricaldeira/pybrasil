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
from dateutil.relativedelta import relativedelta


def limpa_nome(texto):
    probibidos = u'.,-_;:?!=+*/&#$%{}[]()<>|@"\´`~^¨' + u"'"

    for c in probibidos:
        texto = texto.replace(c, ' ')

    while '  ' in texto:
        texto = texto.replace('  ', ' ')

    return texto


def calcula_digito_nosso_numero(self, boleto):
    dv = self.modulo11(str(boleto.nosso_numero).zfill(12), pesos=range(2, 9))
    return dv


def campo_livre(self, boleto):
    boleto.nosso_numero = str(boleto.nosso_numero).zfill(12)

    campo_livre = '9'
    campo_livre += str(boleto.beneficiario.codigo.numero).zfill(7)[:7]
    campo_livre += str(boleto.nosso_numero).zfill(12)
    campo_livre += str(boleto.digito_nosso_numero).zfill(1)
    campo_livre += '0'
    campo_livre += str(boleto.banco.carteira).zfill(3)

    return campo_livre

def carteira_nosso_numero(self, boleto):
    return '%s-%s' % (boleto.nosso_numero.zfill(12), boleto.digito_nosso_numero)


def agencia_conta(self, boleto):
    return '%s-%s/%s' % (str(boleto.beneficiario.agencia.numero).zfill(4), boleto.beneficiario.agencia.digito, boleto.beneficiario.codigo.numero.zfill(7)[:7])


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
    texto += str(boleto.beneficiario.agencia.numero).zfill(4)
    texto += str(beneficiario.codigo.numero).zfill(8)[:8]
    texto += str(boleto.beneficiario.conta.numero).zfill(9)[:8]
    texto += beneficiario.nome.ljust(30)[:30]
    texto += '033'
    texto += 'SANTANDER'.ljust(15)
    texto += remessa.data_hora.strftime(b'%d%m%y')
    texto += ''.zfill(16)
    texto += ''.ljust(275)
    texto += str(remessa.sequencia).zfill(3)
    texto += str(1).zfill(6)

    return self.tira_acentos(texto.upper())


def trailler_remessa_400(self, remessa):
    #
    # Trailler do arquivo
    #
    texto = '9'
    texto += str(len(remessa.registros) + 1).zfill(6)  # Quantidade de registros
    texto += str(int(remessa.valor_total * 100)).zfill(13)[:13] # 24-41 somatória dos valores
    texto += ''.zfill(374)
    texto += str(len(remessa.registros) + 1).zfill(6)  # Quantidade de registros

    return self.tira_acentos(texto.upper())


def linha_remessa_400(self, remessa, boleto):
    beneficiario = boleto.beneficiario
    banco = boleto.banco
    pagador = boleto.pagador

    #
    # Começa aqui
    #
    texto = '1'

    if beneficiario.tipo_pessoa == 'PJ':
        texto += '02'
    else:
        texto += '01'

    texto += beneficiario.cnpj_cpf_numero.zfill(14)
    texto += str(boleto.beneficiario.agencia.numero).zfill(4)
    texto += str(beneficiario.codigo.numero).zfill(8)[:8]
    texto += str(boleto.beneficiario.conta.numero).zfill(9)[:8]
    texto += boleto.identificacao.ljust(10)[:10]
    texto += ''.ljust(15)
    texto += str(boleto.nosso_numero).zfill(7)
    texto += str(boleto.digito_nosso_numero).zfill(1)
    texto += '000000'
    texto += ' '

    if boleto.valor_multa > 0:
        texto += '4'
        percentual_multa = D(str(boleto.valor_multa)) / D(str(boleto.documento.valor)) * D('100')
        texto += str(int(percentual_multa * 100)).zfill(4)
    else:
        texto += '0'
        texto += '0000'

    texto += '00'  # unidade (outra moeda)
    texto += ''.zfill(13)  # valor do titulo em outra moeda
    texto += ''.ljust(4)

    #
    # Multa após o vencimento
    #
    texto += (boleto.data_vencimento + relativedelta(days=1)).strftime('%d%m%y')

    if boleto.banco.modalidade:
        texto += boleto.banco.modalidade[0] or '1'
    elif boleto.banco.carteira == '101':
        texto += '5'
    else:
        texto += '4'

    texto += boleto.comando or '01'  # Registro do boleto no banco

    texto += boleto.identificacao.ljust(10)[:10]

    texto += boleto.data_vencimento.strftime('%d%m%y')
    texto += str(int(boleto.documento.valor * 100)).zfill(13)
    texto += '033'
    texto += ''.zfill(5)
    texto += '01'  # Tipo do documento - 01 Duplicata
    texto += 'N' # Aceite
    texto += boleto.documento.data.strftime('%d%m%y')
    texto += '00'  # Primeira instrução de cobrança

    if boleto.dias_protesto:
        texto += '06'  # Segunda instrução de cobrança, protestar
    else:
        texto += '03'  # Segunda instrução de cobrança, baixar após 30 dias do vencimento

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
    texto += pagador.bairro.ljust(12)[:12]
    texto += pagador.cep.replace('-', '').zfill(8)
    texto += pagador.cidade.ljust(15)[:15]
    texto += pagador.estado.ljust(2)[:2]
    texto += ''.ljust(30)  # Sacador/avalista - não existe mais
    texto += ' '
    texto += 'I'
    texto += str(boleto.beneficiario.conta.numero).zfill(9)[8]
    texto += str(boleto.beneficiario.conta.digito).zfill(1)[0]
    texto += ''.ljust(6)

    if boleto.dias_protesto:
        texto += str(boleto.dias_protesto).zfill(2)
    else:
        texto += '00'

    texto += ' '
    texto += str(len(remessa.registros) + 1).zfill(6)  # nº do registro

    return self.tira_acentos(texto.upper())


def header_retorno_400(self, retorno):
    header = retorno.linhas[0]

    beneficiario = retorno.beneficiario

    beneficiario.codigo.numero = str(D(header[110:117]))
    beneficiario.nome = header[46:76]

    retorno.data_hora = parse_datetime(header[94:100]).date()
    retorno.sequencia = int(header[391:394])


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
    '06': 'Liquidação normal',
    '07': 'Liquidação por conta',
    '08': 'Liquidação por saldo',
    '09': 'Baixa de título',
    '10': 'Baixa a pedido do beneficiário ou protesto',
    '11': 'Títulos em aberto',
    '12': 'Abatimento concedido',
    '13': 'Abatimento cancelado',
    '14': 'Alteração de vencimento',
    '15': 'Enviado para cartório',
    '16': 'Título já baixado/liquidado',
    '17': 'Liquidação em cartório',
    #'17': 'Liquidação após baixa ou sem registro',
    #'18': 'Acerto de depositária',
    #'19': 'Instrução de protesto',
    #'20': 'Sustação de protesto',
    '21': 'Entrada em cartório',
    '22': 'Retirado de cartório',
    #'23': 'Encaminhado a protesto',
    '24': 'Custas de cartório',
    '25': 'Instrução de protesto',
    '26': 'Sustar protesto',
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

    if linha[107] == '5':
        self.carteira = '101'
    else:
        self.carteira = '102'

    beneficiario.agencia.numero = linha[17:21]
    beneficiario.conta.numero = linha[21:29]
    #beneficiario.conta.digito = linha[36]

    for i in range(1, len(retorno.linhas) - 1):
        linha = retorno.linhas[i]
        boleto = Boleto()
        boleto.beneficiario = retorno.beneficiario
        boleto.banco = self

        boleto.identificacao = linha[37:62]

        #
        # Para pegar o último dígito (que não era o DV antes) - 01/06/2016 10:15
        # boleto.nosso_numero = str(D(linha[62:70]))
        #
        # Para ignorar o último dígito (que passou a ser o DV) - 01/06/2016 10:15
        # boleto.nosso_numero = str(D(linha[62:69]))
        #
        boleto.nosso_numero = str(D(linha[62:69]))
        #boleto.nosso_numero_digito = linha[82]

        if linha[107] == '5':
            boleto.banco.carteira = '101'
        else:
            boleto.banco.carteira = '102'

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

        #boleto.pagador.cnpj_cpf = linha[342:357]

        retorno.boletos.append(boleto)
