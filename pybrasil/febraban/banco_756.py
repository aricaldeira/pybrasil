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
    calculo_digito = str(boleto.beneficiario.agencia.numero).zfill(4)
    calculo_digito += str(boleto.beneficiario.codigo.numero).zfill(9)
    calculo_digito += str(boleto.beneficiario.codigo.digito).zfill(1)
    calculo_digito += str(boleto.nosso_numero).zfill(7)

    return self.modulo11(calculo_digito, pesos=[3, 7, 9, 1])


def agencia_conta(self, boleto):
    agencia = str(boleto.beneficiario.agencia.numero).zfill(4)
    return '%s / %s-%s' % (agencia, str(boleto.beneficiario.codigo.numero).zfill(6), str(boleto.beneficiario.codigo.digito).zfill(1))


def fator_vencimento(self, boleto):
    fator_vencimento = boleto.data_vencimento - date(2000, 7, 3)
    return fator_vencimento.days + 1000


def campo_livre(self, boleto):
    boleto.banco.carteira = str(boleto.banco.carteira).zfill(1)
    boleto.beneficiario.agencia.numero = str(boleto.beneficiario.agencia.numero).zfill(4)
    boleto.beneficiario.codigo.numero = str(boleto.beneficiario.codigo.numero).zfill(6)
    boleto.beneficiario.codigo.digito = str(boleto.beneficiario.codigo.digito).zfill(1)
    boleto.nosso_numero = str(boleto.nosso_numero).zfill(7)

    campo_livre = boleto.banco.carteira
    campo_livre += boleto.beneficiario.agencia.numero

    if len(str(boleto.banco.modalidade)) == 3:
        campo_livre += str(boleto.banco.modalidade).zfill(3)[1:]
    elif len(str(boleto.banco.modalidade)) == 4:
        campo_livre += str(boleto.banco.modalidade).zfill(4)[1:3]
    else:
        campo_livre += str(boleto.banco.modalidade).zfill(2)

    campo_livre += boleto.beneficiario.codigo.numero.zfill(6)
    campo_livre += boleto.beneficiario.codigo.digito.zfill(1)
    campo_livre += boleto.nosso_numero
    campo_livre += str(boleto.digito_nosso_numero).zfill(1)
    campo_livre += str(boleto.parcela).zfill(3)

    return campo_livre


def header_remessa_240(self, remessa):
    boleto = remessa.boletos[0]
    beneficiario = boleto.beneficiario
    #
    # Header do arquivo
    #
    texto = '756'
    texto += '0000'
    texto += '0'
    texto += ''.ljust(9)

    if beneficiario.tipo_pessoa == 'PF':
        texto += '1'

    else:
        texto += '2'

    texto += beneficiario.cnpj_cpf_numero.zfill(14)
    texto += ''.ljust(20)
    texto += beneficiario.agencia.numero.zfill(5)
    texto += beneficiario.agencia.digito.zfill(1)
    texto += beneficiario.conta.numero.zfill(12)
    texto += beneficiario.conta.digito.zfill(1)
    texto += ' '
    texto += beneficiario.nome.ljust(30)[:30]
    texto += 'SICOOB'.ljust(30)
    texto += ''.ljust(10)
    texto += '1'
    texto += remessa.data_hora.strftime(b'%d%m%Y')
    texto += remessa.data_hora.strftime(b'%H%M%S')
    texto += str(remessa.sequencia).zfill(6)
    texto += '081'
    texto += '00000'
    texto += ''.ljust(20)
    texto += ''.ljust(20)
    texto += ''.ljust(29)
    texto += '\n'

    #
    # Header do lote (sempre somente 1 por arquivo)
    #
    texto += '756'
    texto += '0001'  # Número do lote
    texto += '1'
    texto += 'R'
    texto += '01'
    texto += ''.ljust(2)
    texto += '040'
    texto += ' '

    if beneficiario.tipo_pessoa == 'PF':
        texto += '1'

    else:
        texto += '2'

    texto += beneficiario.cnpj_cpf_numero.zfill(15)
    texto += ''.ljust(20)
    texto += beneficiario.agencia.numero.zfill(5)
    texto += beneficiario.agencia.digito.zfill(1)
    texto += beneficiario.conta.numero.zfill(12)
    texto += beneficiario.conta.digito.zfill(1)
    texto += ' '
    texto += beneficiario.nome.ljust(30)[:30]
    texto += ''.ljust(40)  # Mensagem 1
    texto += ''.ljust(40)  # Mensagem 2
    texto += str(remessa.sequencia).zfill(8)
    texto += remessa.data_hora.strftime(b'%d%m%Y')
    texto += '00000000'
    texto += ''.ljust(33)

    return texto.encode('iso-8859-1')


def trailler_remessa_240(self, remessa):
    boleto = remessa.boletos[0]
    #
    # Trailler do lote (sempre somente 1 por arquivo)
    #
    texto = '756'
    texto += '0001'  # Número do lote
    texto += '5'
    texto += ''.ljust(9)

    #
    # Quantidade de registros no lote
    # São 4 linhas por boleto
    #
    registros_no_lote = len(remessa.boletos) * 4
    texto += str(registros_no_lote).zfill(6)

    #
    # Quantidade de boletos para registro em cobrança simples
    #
    texto += str(len(remessa.boletos)).zfill(6)

    #
    # Valor total dos boletos para registro em cobrança simples
    #
    total_cobranca = 0
    for boleto in remessa.boletos:
        total_cobranca += boleto.documento.valor

    texto += str(int(total_cobranca * 100)).zfill(17)

    #
    # Quantidade e valor para cobrança vinculada
    #
    texto += ''.zfill(6)
    texto += ''.zfill(17)

    #
    # Quantidade e valor para cobrança caucionada
    #
    texto += ''.zfill(6)
    texto += ''.zfill(17)

    #
    # Quantidade e valor para cobrança descontada
    #
    texto += ''.zfill(6)
    texto += ''.zfill(17)

    texto += ''.ljust(8)
    texto += ''.ljust(117)
    texto += '\n'

    #
    # Trailler do arquivo
    #
    texto += '756'
    texto += '9999'  # Número do lote
    texto += '9'
    texto += ''.ljust(9)
    texto += '000001'  # Quantidade de lotes no arquivo (sempre 1)

    #
    # Quantidade de registros no arquivo
    # Registros no lote + header do arquivo + header do lote + trailler do lote + trailler do arquivo
    #
    texto += str(registros_no_lote + 4).zfill(6)

    texto += ''.zfill(6)
    texto += ''.ljust(205)

    return texto.encode('iso-8859-1')


def linha_remessa_240(self, remessa, boleto):
    beneficiario = boleto.beneficiario
    banco = boleto.banco
    pagador = boleto.pagador

    #
    # 1º segmento
    #
    texto = '756'
    texto += '0001'  # Número do lote (sempre 1)
    texto += '3'
    texto += str(len(remessa.registros) - 2 + 1).zfill(5)  # nº da linha no lote
    texto += 'P'
    texto += ' '
    texto += boleto.comando or '01'  # Entrada de título
    texto += beneficiario.agencia.numero.zfill(5)
    texto += beneficiario.agencia.digito.zfill(1)
    texto += beneficiario.conta.numero.zfill(12)
    texto += beneficiario.conta.digito.zfill(1)
    texto += ' '
    texto += str(boleto.nosso_numero).zfill(9)
    texto += str(boleto.digito_nosso_numero).zfill(1)
    texto += str(boleto.parcela).zfill(2)

    if len(str(boleto.banco.modalidade)) == 3:
        texto += str(banco.modalidade).zfill(3)[1:]
    elif len(str(boleto.banco.modalidade)) == 4:
        texto += str(banco.modalidade).zfill(4)[1:3]
    else:
        texto += str(banco.modalidade).zfill(2)

    texto += '4'  # Papel A4
    texto += ''.ljust(5)

    texto += str(banco.carteira).zfill(1)
    texto += '0'
    texto += ' '
    texto += '2'  # Emissão pelo beneficiário
    texto += '2'  # Distribuição pelo beneficiário

    texto += str(boleto.documento.numero).ljust(15)
    texto += boleto.data_vencimento.strftime('%d%m%Y')
    texto += str(int(boleto.documento.valor * 100)).zfill(15)

    texto += '00000'
    texto += ' '

    texto += '23'  # NF - Nota fiscal

    texto += boleto.aceite

    texto += boleto.data_processamento.strftime('%d%m%Y')

    if boleto.data_juros:
        texto += '1'  # Juros diários
        texto += boleto.data_juros.strftime('%d%m%Y')
        texto += str(int(boleto.valor_juros * 100)).zfill(15)
    else:
        texto += '0'
        texto += ''.zfill(8)
        texto += ''.zfill(15)

    if boleto.data_desconto:
        texto += '1'  # Desconto fixo
        texto += boleto.data_desconto.strftime('%d%m%Y')
        texto += str(int(boleto.valor_juros * 100)).zfill(15)
    else:
        texto += '0'
        texto += ''.zfill(8)
        texto += ''.zfill(15)

    texto += str(int(boleto.valor_iof * 100)).zfill(15)
    texto += str(int(boleto.valor_abatimento * 100)).zfill(15)

    texto += str(boleto.identificacao).ljust(25)

    #
    # Protesto
    #
    texto += '1'
    texto += str(boleto.dias_protesto).zfill(2)
    texto += '0'
    texto += str(boleto.dias_baixa).zfill(3)
    texto += str(boleto.moeda).zfill(2)
    texto += ''.zfill(10)
    texto += ' '
    texto += '\n'

    #
    # 2º segmento
    #
    texto += '756'
    texto += '0001'  # Número do lote (sempre 1)
    texto += '3'
    texto += str(len(remessa.registros) - 2 + 2).zfill(5)  # nº da linha no lote
    texto += 'Q'
    texto += ' '
    texto += boleto.comando or '01'  # Entrada de título

    if pagador.tipo_pessoa == 'PF':
        texto += '1'
    else:
        texto += '2'

    texto += pagador.cnpj_cpf_numero.zfill(15)
    texto += pagador.nome.ljust(40)[:40]
    texto += pagador.endereco_numero_complemento.ljust(40)[:40]
    texto += pagador.bairro.ljust(15)[:15]
    texto += pagador.cep.replace('-', '').zfill(8)
    texto += pagador.cidade.ljust(15)[:15]
    texto += pagador.estado

    #
    # Sacador/avalista - não existe mais, o SICOOB orientou a usar os
    # dados do beneficário
    #
    if beneficiario.tipo_pessoa == 'PF':
        texto += '1'
    else:
        texto += '2'

    texto += beneficiario.cnpj_cpf_numero.zfill(15)
    texto += beneficiario.nome.ljust(40)[:40]

    texto += '000'
    texto += ''.ljust(20)
    texto += ''.ljust(8)
    texto += '\n'

    #
    # 3º segmento
    #
    texto += '756'
    texto += '0001'  # Número do lote (sempre 1)
    texto += '3'
    texto += str(len(remessa.registros) - 2 + 3).zfill(5)  # nº da linha no lote
    texto += 'R'
    texto += ' '
    texto += boleto.comando or '01'  # Entrada de título

    #
    # Desconto 2 e 3
    #
    texto += '0'  # Desconto fixo
    texto += ''.zfill(8)
    texto += ''.zfill(15)
    texto += '0'  # Desconto fixo
    texto += ''.zfill(8)
    texto += ''.zfill(15)

    #
    # Multa
    #
    if boleto.data_multa:
        texto += '1'  # Valor fixo
        texto += boleto.data_multa.strftime('%d%m%Y')
        texto += str(int(boleto.valor_multa * 100)).zfill(15)
    else:
        texto += '0'
        texto += ''.zfill(8)
        texto += ''.zfill(15)

    texto += ''.ljust(10)
    texto += ''.ljust(40)
    texto += ''.ljust(40)
    texto += ''.ljust(20)
    texto += ''.zfill(8)
    texto += ''.zfill(3)
    texto += ''.zfill(5)
    texto += ' '
    texto += ''.zfill(12)
    texto += ' '
    texto += ' '
    texto += '0'
    texto += ''.ljust(9)
    texto += '\n'

    #
    # 4º segmento
    #
    texto += '756'
    texto += '0001'  # Número do lote (sempre 1)
    texto += '3'
    texto += str(len(remessa.registros) - 2 + 4).zfill(5)  # nº da linha no lote
    texto += 'S'
    texto += ' '
    texto += boleto.comando or '01'  # Entrada de título
    texto += '3'

    instrucoes = '; '.join(boleto.instrucoes)
    instrucoes = instrucoes.ljust(200)
    texto += instrucoes[0:40]
    texto += instrucoes[40:80]
    texto += instrucoes[80:120]
    texto += instrucoes[120:160]
    texto += instrucoes[160:]
    texto += ''.ljust(22)

    return texto.encode('iso-8859-1')


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
    texto += 'COBRANÇA'.ljust(15)  # O SICOOB exige o Ç, a codificação usada deve ser a ISO-8859-1
    texto += str(beneficiario.agencia.numero).zfill(4)
    texto += str(beneficiario.agencia.digito).zfill(1)
    texto += str(beneficiario.codigo.numero).zfill(8)
    texto += str(beneficiario.codigo.digito).zfill(1)
    texto += str(beneficiario.conta.numero).zfill(6)
    texto += beneficiario.nome.ljust(30)[:30]
    texto += '756'
    texto += 'BANCOOBCED'.ljust(15)
    texto += remessa.data_hora.strftime(b'%d%m%y')
    texto += str(remessa.sequencia).zfill(7)
    texto += ''.ljust(287)
    texto += str(1).zfill(6)

    return texto.encode('iso-8859-1')


def trailler_remessa_400(self, remessa):
    #
    # Trailler do arquivo
    #
    texto = '9'
    texto += ''.ljust(393)
    texto += str(len(remessa.registros) + 1).zfill(6)  # Quantidade de registros

    return texto.encode('iso-8859-1')


def linha_remessa_400(self, remessa, boleto):
    beneficiario = boleto.beneficiario
    pagador = boleto.pagador

    #
    # 1º segmento
    #
    texto = '1'

    if beneficiario.tipo_pessoa == 'PJ':
        texto += '02'
    else:
        texto += '01'

    texto += str(beneficiario.cnpj_cpf_numero).zfill(14)
    texto += str(beneficiario.agencia.numero).zfill(4)
    texto += str(beneficiario.agencia.digito).zfill(1)
    #texto += str(beneficiario.codigo.numero).zfill(8)
    #texto += str(beneficiario.codigo.digito).zfill(1)
    texto += str(beneficiario.conta.numero).zfill(8)
    texto += str(beneficiario.conta.digito).zfill(1)
    texto += ''.zfill(6)
    texto += str(boleto.identificacao).ljust(25)
    texto += str(boleto.nosso_numero).zfill(11)
    texto += str(boleto.digito_nosso_numero).zfill(1)
    texto += str(boleto.parcela).zfill(2)
    texto += '00'
    texto += ''.ljust(3)
    texto += ' '
    texto += ''.ljust(3)
    texto += ''.zfill(3)
    texto += ''.zfill(1)
    texto += ''.zfill(5)
    texto += ''.zfill(1)
    texto += ''.zfill(6)
    texto += ''.ljust(4)

    if len(str(boleto.banco.modalidade)) == 3:
        texto += str(boleto.banco.modalidade).zfill(3)
    elif len(str(boleto.banco.modalidade)) == 4:
        texto += str(boleto.banco.modalidade).zfill(4)[0:3]
    else:
        texto += ''.ljust(1)
        texto += str(boleto.banco.modalidade).zfill(2)

    texto += boleto.comando or '01'
    texto += str(boleto.documento.numero).ljust(10)[:10]
    texto += boleto.data_vencimento.strftime('%d%m%y')
    texto += str(int(boleto.documento.valor * 100)).zfill(13)
    texto += '756'
    texto += str(beneficiario.agencia.numero).zfill(4)
    texto += str(beneficiario.agencia.digito).zfill(1)
    texto += '01'  # Outros tipos de documento
    texto += '1' if boleto.aceite else '0'  # Aceite
    texto += boleto.data_processamento.strftime('%d%m%y')

    #
    # Instruções adicionais
    #
    if boleto.percentual_juros > 0:
        texto += '01'
    else:
        texto += '00'

    if boleto.dias_protesto in (3, 4, 5, 10, 15, 20):
        texto += str(boleto.dias_protesto).zfill(2)
    else:
        texto += '00'

    texto += str(int(boleto.percentual_juros * 10000)).zfill(6)
    texto += str(int(boleto.percentual_multa * 10000)).zfill(6)

    if len(str(boleto.banco.modalidade)) == 4:
        texto += str(boleto.banco.modalidade).zfill(4)[-1]
    else:
        texto += ' '

    if boleto.data_desconto:
        texto += boleto.data_desconto.strftime('%d%m%y')
        texto += str(int(boleto.valor_desconto * 100)).zfill(13)
    else:
        texto += ''.zfill(6)
        texto += ''.zfill(13)

    texto += '9' + str(int(boleto.valor_iof * 100)).zfill(12)
    texto += str(int(boleto.valor_abatimento * 100)).zfill(13)

    if pagador.tipo_pessoa == 'PJ':
        texto += '02'
    else:
        texto += '01'

    texto += pagador.cnpj_cpf_numero.zfill(14)
    texto += pagador.nome[:40].ljust(40)
    texto += pagador.endereco_numero_complemento.ljust(37)[:37]
    texto += pagador.bairro.ljust(15)[:15]
    texto += pagador.cep.replace('-', '').zfill(8)
    texto += pagador.cidade.ljust(15)[:15]
    texto += pagador.estado
    texto += ''.ljust(40)
    texto += str(boleto.dias_protesto).zfill(2)
    texto += ' '
    texto += str(len(remessa.registros) + 1).zfill(6)  # nº do registro

    return texto.encode('iso-8859-1')


def header_retorno_400(self, retorno):
    header = retorno.linhas[0]

    beneficiario = retorno.beneficiario

    beneficiario.agencia.numero = header[26:30]
    beneficiario.agencia.digito = header[30]
    beneficiario.codigo.numero = unicode(D(header[31:39])).zfill(6)
    beneficiario.codigo.digito = header[39]
    beneficiario.nome = header[46:76]

    retorno.data_hora = parse_datetime(header[94:100]).date()
    retorno.sequencia = int(header[100:107])


def header_retorno_240(self, retorno):
    header = retorno.linhas[0]

    beneficiario = retorno.beneficiario

    beneficiario.cnpj_cpf = header[18:32]
    beneficiario.agencia.numero = unicode(D(header[52:57]))
    beneficiario.agencia.digito = header[57]
    beneficiario.conta.numero = unicode(D(header[58:70]))
    beneficiario.conta.digito = header[70]
    beneficiario.nome = header[72:102]
    retorno.data_hora = parse_datetime(header[143:151] + ' ' + header[151:157])
    retorno.sequencia = int(header[157:163])


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
    '05': 'Liquidação sem registro',
    '06': 'Liquidação normal',
    '06.1': 'Liquidação normal - sem data de crédito',
    '09': 'Baixa de título',
    '10': 'Baixa a pedido do beneficiário',
    '11': 'Títulos em aberto',
    '14': 'Alteração de vencimento',
    '15': 'Liquidação em cartório',
    '23': 'Encaminhado a protesto',
    '27': 'Confirmação de alteração de dados',
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
    beneficiario.cnpj_cpf = linha[3:17]
    beneficiario.conta.numero = unicode(D(linha[22:30]))
    beneficiario.conta.digito = linha[30]

    for i in range(1, len(retorno.linhas) - 1):
        linha = retorno.linhas[i]
        boleto = Boleto()
        boleto.beneficiario = retorno.beneficiario
        boleto.banco = self

        boleto.nosso_numero = unicode(D(linha[62:73]))
        #boleto.nosso_numero_digito = linha[73]
        boleto.parcela = int(linha[74:76])
        boleto.documento.especie = linha[83:85]
        boleto.banco.modalidade = linha[106:108]
        boleto.comando = linha[108:110]
        boleto.data_ocorrencia = parse_datetime(linha[110:116])
        boleto.data_credito = parse_datetime(linha[175:181])
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


        boleto.pagador.cnpj_cpf = linha[342:357]

        retorno.boletos.append(boleto)
