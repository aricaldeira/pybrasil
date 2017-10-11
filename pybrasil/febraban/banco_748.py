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
from pybrasil.inscricao import limpa_formatacao

#
# No contexto deste banco, o campo
# modalidade do SICOOB é o posto do SICREDI
#

def calcula_digito_nosso_numero(self, boleto):
    calculo_digito = str(boleto.beneficiario.agencia.numero).zfill(4)
    calculo_digito += str(int(boleto.banco.modalidade[0:2])).zfill(2)[0:2]  # Posto
    calculo_digito += str(boleto.beneficiario.codigo.numero).zfill(5)
    calculo_digito += str(boleto.documento.data.year).zfill(4)[2:4]
    calculo_digito += str(boleto.nosso_numero).zfill(6)

    return self.modulo11(calculo_digito, mapa_digitos={10: 0, 11: 0})


def carteira_nosso_numero(self, boleto):
    return '%s/%s-%s' % (str(boleto.documento.data.year).zfill(4)[2:4], boleto.nosso_numero, boleto.digito_nosso_numero)


def agencia_conta(self, boleto):
    return '%s.%s.%s' % (str(boleto.beneficiario.agencia.numero).zfill(4),
        str(int(boleto.banco.modalidade[0:2])).zfill(2)[0:2],  # Posto
        str(boleto.beneficiario.codigo.numero).zfill(5))


def fator_vencimento(self, boleto):
    fator_vencimento = boleto.data_vencimento - date(2000, 7, 3)
    return fator_vencimento.days + 1000


def campo_livre(self, boleto):
    boleto.banco.carteira = str(int(boleto.banco.carteira)).zfill(1)
    boleto.beneficiario.agencia.numero = str(boleto.beneficiario.agencia.numero).zfill(4)
    boleto.banco.modalidade = str(int(boleto.banco.modalidade[0:2])).zfill(2)
    boleto.beneficiario.codigo.numero = str(boleto.beneficiario.codigo.numero).zfill(5)
    boleto.beneficiario.codigo.digito = str(boleto.beneficiario.codigo.digito).zfill(1)
    boleto.nosso_numero = str(boleto.nosso_numero).zfill(6)

    campo_livre = str(int(boleto.banco.carteira[:2])).zfill(1)[0]
    campo_livre += '1'  #  Carteira simples
    campo_livre += str(boleto.documento.data.year).zfill(4)[2:4]
    campo_livre += boleto.nosso_numero
    campo_livre += boleto.digito_nosso_numero
    campo_livre += boleto.beneficiario.agencia.numero
    campo_livre += boleto.banco.modalidade
    campo_livre += boleto.beneficiario.codigo.numero.zfill(5)

    if boleto.documento.valor > 0:
        campo_livre += '1'
    else:
        campo_livre += '0'

    campo_livre += '0'  # filler

    campo_livre += self.modulo11(campo_livre, mapa_digitos={10: 0, 11: 0})

    return campo_livre


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
    #texto += str(beneficiario.agencia.numero).zfill(4)
    #texto += str(beneficiario.agencia.digito).zfill(1)
    texto += str(beneficiario.codigo.numero).zfill(5)
    #texto += str(beneficiario.codigo.digito).zfill(1)
    #texto += str(beneficiario.conta.numero).zfill(6)
    texto += beneficiario.cnpj_cpf_numero.zfill(14)
    texto += ''.ljust(31)
    texto += '748'
    texto += 'SICREDI'.ljust(15)
    texto += remessa.data_hora.strftime(b'%Y%m%d')
    texto += ''.ljust(8)
    texto += str(remessa.sequencia).zfill(7)
    texto += ''.ljust(273)
    texto += '2.00'
    texto += str(1).zfill(6)

    return self.tira_acentos(texto)


def trailler_remessa_400(self, remessa):
    boleto = remessa.boletos[0]
    beneficiario = boleto.beneficiario
    #
    # Trailler do arquivo
    #
    texto = '9'
    texto += '1'
    texto += '748'
    texto += str(beneficiario.codigo.numero).zfill(5)
    texto += ''.ljust(384)
    texto += str(len(remessa.registros) + 1).zfill(6)  # Quantidade de registros

    return self.tira_acentos(texto)


def linha_remessa_400(self, remessa, boleto):
    beneficiario = boleto.beneficiario
    pagador = boleto.pagador

    texto = '1'
    texto += 'A'  # com registro
    texto += 'A'  # tipo da carteira
    texto += 'A'  # tipo da impressão
    texto += ''.ljust(12)
    texto += 'A'  # tipo da moeda
    texto += 'A'  # tipo de desconto (A - valor, B - %)
    texto += 'A'  # tipo de juros (A - valor, B - %)
    texto += ''.ljust(28)

    texto += str(boleto.documento.data.year).zfill(4)[2:4]
    texto += boleto.nosso_numero.zfill(6)
    texto += boleto.digito_nosso_numero

    texto += ''.ljust(6)
    texto += remessa.data_hora.strftime(b'%Y%m%d')

    #
    # Posição 071
    #
    texto += ' '

    texto += 'N'  # Postagem
    texto += ' '
    texto += 'B'  # Impressão pelo beneficiário

    # Tipo de impressa A '0000' se B com parcelas

    texto += '0000'  # Impressão pelo beneficiário

    #texto += str(boleto.parcela).zfill(2)
    #texto += '00' # total de parcelas do carnê


    texto += ''.ljust(4)
    texto += ''.zfill(10)  # Desconto por antecipação
    texto += str(int(boleto.percentual_multa * 100)).zfill(4)
    texto += ''.ljust(12)
    texto += boleto.comando or '01'
    #texto += str(boleto.documento.numero).ljust(10)[:10]
    texto += str(boleto.identificacao).replace('_', '').ljust(10)[:10]
    texto += boleto.data_vencimento.strftime('%d%m%y')
    texto += str(int(boleto.documento.valor * 100)).zfill(13)
    texto += ''.ljust(9)

    texto += 'A'  # Duplicata mercantil
    texto += boleto.aceite  # Aceite
    texto += boleto.documento.data.strftime('%d%m%y')

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

    texto += ''.zfill(13)
    texto += str(int(boleto.valor_abatimento * 100)).zfill(13)

    if pagador.tipo_pessoa == 'PJ':
        texto += '2'
    else:
        texto += '1'

    texto += '0'

    texto += pagador.cnpj_cpf_numero.zfill(14)
    texto += pagador.nome[:40].ljust(40)
    texto += pagador.endereco_numero_complemento.ljust(40)[:40]
    texto += ''.zfill(5)
    texto += ''.zfill(6)  # Filler
    texto += ' '  # Filler
    texto += pagador.cep.replace('-', '').zfill(8)
    #texto += str(boleto.identificacao).replace('id_', '').zfill(5)[:5]
    texto += ''.zfill(5)[:5]

    #
    # Sacador
    #
    texto += ''.ljust(14)
    texto += ''.ljust(41)
    texto += str(len(remessa.registros) + 1).zfill(6)  # nº do registro

    return self.tira_acentos(texto).upper()


def header_retorno_400(self, retorno):
    header = retorno.linhas[0]

    beneficiario = retorno.beneficiario

    beneficiario.codigo.numero = header[26:31]
    beneficiario.cnpj_cpf = header[31:45]
    #retorno.beneficiario.nome = header[46:76]

    retorno.data_hora = parse_datetime(header[94:102], ano_primeiro=True).date()
    retorno.sequencia = int(header[110:117])


DESCRICAO_COMANDO_REMESSA = {
    '01': 'Registro de título',
    '02': 'Solicitação de baixa',
    '03': 'Pedido de débito em conta',
    '04': 'Concessão de abatimento',
    '05': 'Cancelamento de abatimento',
    '06': 'Alteração de vencimento',
    '07': 'Alteração do número de controle',
    '08': 'Alteração de seu número',
    '09': 'Instrução para protestar',
    '10': 'Instrução para sustar protesto',
    '11': 'Instrução para dispensar juros',
    '12': 'Alteração de sacado',
    '30': 'Recusa de alegação do sacado',
    '31': 'Alteração de outros dados',
    '34': 'Baixa - pagamento direto ao beneficiário',
}


DESCRICAO_COMANDO_RETORNO = {
    '02': 'Confirmação de entrada do título',
    '03': 'Entrada do título rejeitada',
    '05': 'Liquidação sem registro',
    '06': 'Liquidação normal',
    '09': 'Baixa de título',
    '10': 'Baixa a pedido do beneficiário',
    '11': 'Títulos em aberto',
    '14': 'Alteração de vencimento',
    '15': 'Liquidação em cartório',
    '23': 'Encaminhado a protesto',
    '27': 'Confirmação de alteração de dados',
    '28': 'Tarifas',
}


COMANDOS_RETORNO_LIQUIDACAO = {
    '05': True,
    '06': True,
    '15': True,
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
    #beneficiario.cnpj_cpf = linha[3:17]
    #beneficiario.conta.numero = unicode(D(linha[22:30]))
    #beneficiario.conta.digito = linha[30]

    for i in range(1, len(retorno.linhas) - 1):
        linha = retorno.linhas[i]
        boleto = Boleto()
        boleto.beneficiario = retorno.beneficiario
        boleto.banco = self

        #boleto.nosso_numero = unicode(D(linha[47:56]))
        boleto.nosso_numero = unicode(D(linha[49:55]))
        #boleto.nosso_numero_digito = linha[73]
        #boleto.parcela = int(linha[74:76])
        #boleto.documento.especie = linha[83:85]
        #boleto.banco.modalidade = linha[106:108]
        boleto.comando = linha[108:110]
        boleto.data_ocorrencia = parse_datetime(linha[110:116])
        boleto.data_credito = parse_datetime(linha[328:336], ano_primeiro=True)
        boleto.valor_despesa_cobranca = D(linha[181:188]) / D('100')
        boleto.valor_multa = D(linha[188:201]) / D('100')
        boleto.valor_desconto = D(linha[240:253]) / D('100')
        boleto.valor_recebido = D(linha[253:266]) / D('100')
        boleto.valor_juros = D(linha[266:279]) / D('100')
        boleto.valor_outros_creditos = D(linha[279:292]) / D('100')
        boleto.documento.valor = boleto.valor_recebido
        boleto.documento.valor -= boleto.valor_juros
        boleto.documento.valor -= boleto.valor_multa
        boleto.documento.valor -= boleto.valor_outros_creditos
        boleto.documento.valor += boleto.valor_desconto
        #boleto.documento.valor += boleto.valor_despesa_cobranca


        #boleto.pagador.cnpj_cpf = linha[342:357]

        retorno.boletos.append(boleto)
