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
    calculo_digito = str(boleto.banco.modalidade).zfill(2)
    calculo_digito += str(boleto.nosso_numero).zfill(15)

    return self.modulo11(calculo_digito)


def fator_vencimento(self, boleto):
    fator_vencimento = boleto.data_vencimento - date(2000, 7, 3)
    return fator_vencimento.days + 1000


def imprime_carteira(self, boleto):
    if str(boleto.banco.carteira).zfill(2) == '01':
        return 'RG'
    else:
        return 'SR'


def campo_livre(self, boleto):
    boleto.beneficiario.agencia.numero = str(boleto.beneficiario.agencia.numero).zfill(4)
    boleto.beneficiario.codigo.numero = str(boleto.beneficiario.codigo.numero).zfill(6)
    boleto.beneficiario.codigo.digito = str(boleto.beneficiario.codigo.digito).zfill(1)

    nosso_numero = str(boleto.banco.modalidade).zfill(2) + str(boleto.nosso_numero).zfill(15)

    campo_livre = boleto.beneficiario.codigo.numero
    campo_livre += boleto.beneficiario.codigo.digito
    campo_livre += nosso_numero[2:5]
    campo_livre += nosso_numero[0]
    campo_livre += nosso_numero[5:8]
    campo_livre += nosso_numero[1]
    campo_livre += nosso_numero[8:]

    dv = self.modulo11(campo_livre)

    return campo_livre + dv


def agencia_conta(self, boleto):
    agencia = str(boleto.beneficiario.agencia.numero).zfill(4)

    return '%s / %s-%s' % (agencia, str(boleto.beneficiario.codigo.numero).zfill(6), str(boleto.beneficiario.codigo.digito).zfill(1))


def carteira_nosso_numero(self, boleto):
    return '%s%s-%s' % (str(boleto.banco.modalidade).zfill(2), str(boleto.nosso_numero).zfill(15), boleto.digito_nosso_numero)


def header_remessa_400(self, remessa):
    boleto = remessa.boletos[0]
    beneficiario = boleto.beneficiario
    #
    # Header do arquivo
    #
    texto = '0' # 01-01 fixo
    texto += '1' # 02-02 fixo
    texto += 'REMESSA' # 03-09 Na fase de teste informar REM.TST, em produção REMESSA
    texto += '01' # 10-11 fixo
    texto += 'COBRANCA'.ljust(15) # 12-26 fixo
    texto += str(boleto.beneficiario.agencia.numero).zfill(4)[:4]

    #
    # Alterado dia 09/06/2017 em função da homologação da Protege Limeira
    #
    texto += str(beneficiario.codigo.numero).zfill(6)[:6] # 27-42 código da empresa na CAIXA
    texto += ''.ljust(6)

    ##texto += str(boleto.banco.modalidade).zfill(3)[:3]
    ###
    ### Campo seguinte com 9 posições, informado o dígito por tentativa e erro
    ### no dia 07/04/2015
    ### O manual da Caixa não informa se deveria ser informado ou não o dígito,
    ### mas durante a implantação na ASP chegamos a conclusão de que esse problema
    ### não permitiu o envio correto do arquivo
    ###
    ##texto += str(beneficiario.codigo.numero).zfill(8)[:8] # 27-42 código da empresa na CAIXA
    ##texto += str(beneficiario.codigo.digito).zfill(1)[0]

    texto += ''.ljust(4)
    texto += beneficiario.nome.ljust(30)[:30]
    texto += '104'
    texto += 'C ECON FEDERAL'.ljust(15)
    texto += remessa.data_hora.strftime(b'%d%m%y')
    texto += ''.ljust(289)
    texto += str(remessa.sequencia).zfill(5)[:5]
    texto += str(1).zfill(6)[:6]

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
    banco = boleto.banco

    #
    # Registro Tipo 1 – Registro Detalhe Cobrança de Títulos – Arquivo Remessa
    #
    texto = '1' # 01-01 FIXO

    if beneficiario.tipo_pessoa == 'PJ': # 02-03  01 P/ CPF e 2 /P CNPJ
        texto += '02'
    else:
        texto += '01'

    texto += str(beneficiario.cnpj_cpf_numero).zfill(14) # 04-17  cnpj

    texto += str(boleto.beneficiario.agencia.numero).zfill(4)[:4]
    texto += str(beneficiario.codigo.numero).zfill(6)[:6]
    #texto += str(beneficiario.codigo.digito).zfill(1)[0]
    texto += '2' # posição 28 - 2 - cliente emite
    texto += '0' # posição 29 - 0 - cliente posta
    texto += '00' # 30-31  Taxa de permanência
    texto += str(boleto.identificacao).ljust(25)[:25] # 32-56 identificação boleto da empresa
    texto += str(boleto.banco.modalidade).zfill(2)[:2]
    texto += str(boleto.nosso_numero).zfill(15)[:15] # 59-73 identificação boleto na caixa (nosso numero)
    texto += ''.ljust(3) # 74-76 brancos
    texto += ''.ljust(30) # 77-106 brancos
    texto += str(banco.carteira).zfill(2)[:2] # 107-108 Código da Carteira
    texto += boleto.comando or '01'  # 109-110 ocorrencia do titulo
    texto += str(boleto.documento.numero).ljust(10)[:10] # 111-120 ocorrencia do titulo
    texto += boleto.data_vencimento.strftime('%d%m%y') # 121-126 data vencimento
    texto += str(int(boleto.documento.valor * 100)).zfill(13)[:13] #  127-139 valor
    texto += '104' # 140-142 fixo

    #
    # Agência cobradora, deve ir zerada
    #
    texto += ''.zfill(5) # 143-147 agencia cobradora

    texto += '01' # 148-149 tipo do titulo nota 06

    texto += boleto.aceite  # 150-150 Aceite / Não aceite

    texto += boleto.data_processamento.strftime('%d%m%y') # 151-156 data de emissao

    if boleto.dias_protesto:
        texto += '01'.zfill(2) # 157-158 Primeira Instrução de Cobrança
    else:
        texto += '02'.zfill(2) # 157-158 Primeira Instrução de Cobrança

    texto += ''.zfill(2) # 159-160 Segunda Instrução de Cobrança

    texto += str(int(boleto.valor_juros * 100)).zfill(13) # 161-173 Juros de Mora por dia/Valor

    if boleto.data_desconto: # 174-192 data descont e valor desconto
        texto += boleto.data_desconto.strftime('%d%m%y')
        texto += str(int(boleto.valor_desconto * 100)).zfill(13)
    else:
        texto += ''.zfill(6)
        texto += ''.zfill(13)

    texto += str(int(boleto.valor_iof * 100)).zfill(13) # 193-205 iof
    texto += str(int(boleto.valor_abatimento * 100)).zfill(13) # 206-218 valor abatimento

    if pagador.tipo_pessoa == 'PJ': # 219-220 identificador sacado
        texto += '02'
    else:
        texto += '01'

    texto += pagador.cnpj_cpf_numero.zfill(14)[:14] # 221-234 cnpj sacado
    texto += pagador.nome.ljust(40)[:40] # 235-274 nome sacado
    texto += pagador.endereco_numero_complemento.ljust(40)[:40] # 275-314 logradouro
    texto += pagador.bairro.ljust(12)[:12] # 315-326 bairro sacado
    texto += pagador.cep.replace('-', '').zfill(8)[:8] # 327-334 CEP
    texto += pagador.cidade.ljust(15)[:15] # 335-349 cidade
    texto += pagador.estado[:2] # 350-351 uf
    texto += boleto.data_vencimento.strftime('%d%m%y') # 352-357 Definição da data para pagamento de multa
    texto += str(int(boleto.valor_multa * 100)).zfill(10) # 358-367 Valor nominal da multa
    texto += ''.ljust(22)[:22] # 368-389 Nome do Sacador/Avalista
    texto += ''.zfill(2) # 390-391 Terceira Instrução de Cobrança

    if boleto.dias_protesto:
        texto += str(boleto.dias_protesto).zfill(2) # 392-393 dias de protesto
    elif boleto.dias_nao_receber:
        texto += str(boleto.dias_nao_receber).zfill(2) # 392-393 Terceira Instrução de Cobrança
    else:
        texto += ''.zfill(2)

    texto += '1' # 394-394
    texto += str(len(remessa.registros) + 1).zfill(6) #395-400 nº do registro

    return self.tira_acentos(texto.upper())


def header_retorno_400(self, retorno):
    header = retorno.linhas[0]

    retorno.banco.codigo = header[76:79]

    beneficiario = retorno.beneficiario

    beneficiario.agencia.numero = header[26:30]
    beneficiario.codigo.numero = unicode(D(header[30:36])).zfill(6)
    beneficiario.nome = header[46:76]

    retorno.data_hora = parse_datetime(header[94:100]).date()
    retorno.sequencia = int(header[389:394])


def linha_retorno_400(self, retorno):
    beneficiario = retorno.beneficiario
    linha = retorno.linhas[1]

    #
    # Beneficiario
    #
    beneficiario.cnpj_cpf = linha[3:17]
    beneficiario.conta.numero = unicode(D(linha[22:30]))
    beneficiario.conta.digito = linha[30]

    for i in range(1, len(retorno.linhas) - 1):
        linha = retorno.linhas[i]
        boleto = Boleto()
        boleto.beneficiario = retorno.beneficiario
        boleto.banco = self

        boleto.identificacao = linha[31:56]
        boleto.banco.modalidade = linha[56:58]
        boleto.nosso_numero = unicode(D(linha[58:73]))
        #boleto.nosso_numero_digito = linha[73]
        #boleto.parcela = int(linha[74:76])
        #boleto.documento.especie = linha[83:85]
        boleto.comando = linha[108:110]
        boleto.data_ocorrencia = parse_datetime(linha[110:116])
        boleto.data_credito = parse_datetime(linha[293:299])


        boleto.valor_despesa_cobranca = D(linha[175:188]) / D('100')

        boleto.valor_desconto = D(linha[240:253]) / D('100')
        boleto.documento.valor = D(linha[253:266]) / D('100')
        boleto.valor_juros = D(linha[266:279]) / D('100')
        boleto.valor_multa = D(linha[279:292]) / D('100')

        boleto.valor_recebido = boleto.documento.valor - boleto.valor_desconto + boleto.valor_juros + boleto.valor_multa

        retorno.boletos.append(boleto)


DESCRICAO_COMANDO_REMESSA = {
    '01': 'Registro de título',
    '02': 'Solicitação de baixa',
    '03': 'Concessão de abatimento',
    '04': 'Cancelamento de abatimento',
    '05': 'Alteração de vencimento',
    '06': 'Alteração do uso da empresa',
    '07': 'Alteração do prazo de protesto',
    '08': 'Alteração do prazo de devolução',
    '09': 'Alteração de outros dados',
    '10': 'Alteração de outros dados',
    '11': 'Alteração de outros dados',
    '12': 'Alteração de outros dados',
}


DESCRICAO_COMANDO_RETORNO = {
    '01': 'Confirmação de entrada do título',
    '02': 'Confirmação de baixa do título',
    '03': 'Abatimento concedido',
    '04': 'Abatimento cancelado',
    '05': 'Vencimento alterado',
    '06': 'Uso da empresa alterado',
    '07': 'Prazo de protesto alterado',
    '08': 'Prazo de devolução alterado',
    '09': 'Alteração confirmada',
    '10': 'Alteração confirmada',
    '11': 'Alteração confirmada',
    '12': 'Alteração confirmada',

    '20': 'Em ser',
    '21': 'Liquidação normal',
    '22': 'Liquidação em cartório',
    '23': 'Baixa por devolução',
    '25': 'Baixa por protesto',
    '26': 'Encaminhado a protesto',
    '27': 'Sustação de protesto',
    '28': 'Estorno de protesto',
    '29': 'Estorno de sustação de protesto',

    '30': 'Alteração de título',
    '31': 'Tarifa sobre título vencido',
    '32': 'Outras tarifas de alteração',
    '33': 'Estorno de baixa/liquidação',
    '34': 'Tarifas diversas',
    '99': 'Rejeição do título',
}


COMANDOS_RETORNO_LIQUIDACAO = {
    '21': True,
    '22': True,
}


COMANDOS_RETORNO_BAIXA = [
    '23',
    '25',
]
