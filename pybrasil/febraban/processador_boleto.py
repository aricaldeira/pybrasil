# -*- coding: utf-8 -*-
#
# PySPED - Python libraries to deal with Brazil's SPED Project
#
# Copyright (C) 2010-2012
# Copyright (C) Aristides Caldeira <aristides.caldeira at tauga.com.br>
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
# PySPED - Bibliotecas Python para o
#          SPED - Sistema Público de Escrituração Digital
#
# Copyright (C) 2010-2012
# Copyright (C) Aristides Caldeira <aristides.caldeira arroba tauga.com.br>
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

from __future__ import division, print_function, unicode_literals

import sys

if sys.version_info.major == 2:
    from httplib import HTTPSConnection, HTTPConnection

else:
    from http.client import HTTPSConnection, HTTPConnection

import json
import html

from ..base import DicionarioObjeto, gera_objeto_xml, tira_namespaces, unescape_xml, gera_objeto_xml
from ..certificado import Certificado
from ..webservice import Conexao


class ProcessadorBoleto(object):
    def __init__(self, certificado=None):
        self.certificado = certificado or Certificado()
        self.salvar_arquivos = True
        self.caminho_temporario = ''

    def configuracao_boleto(self, boleto):
        self.configuracao = boleto.banco.configuracao_json

    def prepara_conexao(self, operacao):
        conexao = Conexao()
        conexao.certificado = self.certificado

        configuracao = DicionarioObjeto(self.configuracao[operacao].conexao)

        conexao.servidor = configuracao.servidor or ''
        conexao.porta = configuracao.porta or 443
        conexao.url = configuracao.url or ''
        conexao.metodo = configuracao.metodo or ''
        conexao.header = configuracao.header or {}
        conexao.forca_tls = configuracao.forca_tls or False
        conexao.forca_http = configuracao.forca_http or False
        conexao.forca_cadeia_conexao = configuracao.forca_cadeia_conexao or False
        conexao.sem_certificado = configuracao.sem_certificado or False

        return conexao

    def limpa_namespace(self, operacao, xml):
        xml = tira_namespaces(xml)

        if not (self.configuracao[operacao].assinatura and self.configuracao[operacao].assinatura.namespaces):
            return xml

        for namespace, url in self.configuracao[operacao].assinatura.namespaces.items():
            xml = xml.replace('xmlns:{namespace}="{url}"'.format(namespace=namespace, url=url), '')
            xml = xml.replace('xmlns="{url}"'.format(url=url), '')

        return xml

    def unescape_xml(self, xml):
        xml = unescape_xml(xml)
        xml = xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        xml = xml.replace('<?xml version="1.0" encoding="utf-8"?>', '')
        xml = xml.replace('<?xml version="1.0" encoding="UTF-8" ?>', '')
        xml = xml.replace('<?xml version="1.0" encoding="utf-8" ?>', '')
        return xml

    def assina_envio(self, envio):
        if not (self.configuracao.envio_boleto and self.configuracao.envio_boleto.assina):
            return envio

        #envio = 'Content-Type: application/json;\r\n\r\n' + envio

        assinatura = self.certificado.assina_texto(envio, tipo_hash='sha256', formato='pkcs7')

        return assinatura

    def envia_boleto(self, boleto):
        self.configuracao_boleto(boleto)

        configuracao = DicionarioObjeto(self.configuracao.envio_boleto)

        envio = boleto.json

        if configuracao.escapa_envio_json:
            envio = html.escape(envio)

        if configuracao.assina:
            envio = self.assina_envio(envio)

        conexao = self.prepara_conexao('envio_boleto')
        conexao.conectar_servico(envio)

        if configuracao.resposta_xml:
            xml = conexao.resposta

            if configuracao.escapa_resposta:
                xml = self.unescape_xml(xml)

            xml = self.limpa_namespace('envio_boleto', xml)

            resposta = gera_objeto_xml(xml)

            if configuracao.tag_retorno:
                tag_retorno = resposta.getroottree().findall('//' + configuracao.tag_retorno)
            else:
                tag_retorno = []

            if configuracao.tag_erro:
                tag_erro = resposta.getroottree().findall('//' + configuracao.tag_erro)
            else:
                tag_erro = []

            if tag_retorno:
                tag_retorno = tag_retorno[0]

                if configuracao.retorno_json:
                    retorno_json = tag_retorno.text

                    if configuracao.escapa_retorno_json:
                        retorno_json = html.unescape(retorno_json)

                    conexao.retorno = DicionarioObjeto(json.loads(retorno_json))
                else:
                    conexao.retorno = tag_retorno

            if configuracao.retorno_json:
                mensagem_erro = ''
                deu_certo = False

                #
                # Trata o caso do Bradesco, que manda o código de retorno de sucesso no mesmo campo dos erros
                #
                if configuracao.tag_sucesso_codigo and configuracao.tag_sucesso_codigo == configuracao.tag_erro_codigo:
                    texto_sucesso = getattr(conexao.retorno, configuracao.tag_sucesso_codigo, '')

                    if texto_sucesso == configuracao.tag_sucesso_codigo_valor:
                        deu_certo = True

                if not deu_certo:
                    if configuracao.tag_erro_codigo:
                        texto_erro = getattr(conexao.retorno, configuracao.tag_erro_codigo, '')
                        mensagem_erro += 'Código de retorno: {texto_erro}\n'.format(texto_erro=texto_erro)

                    if configuracao.tag_erro_descricao:
                        texto_erro = getattr(conexao.retorno, configuracao.tag_erro_descricao, '')
                        mensagem_erro += 'Mensagem: {texto_erro}\n'.format(texto_erro=texto_erro)

                conexao.mensagem_erro = mensagem_erro

            elif tag_erro:
                mensagem_erro = ''

                for erro in tag_erro:
                    conexao.erros.append(erro)

                    if configuracao.tag_erro_codigo:
                        texto_erro = getattr(erro, configuracao.tag_erro_codigo, '')
                        mensagem_erro += 'Código de retorno: {texto_erro}\n'.format(texto_erro=texto_erro)

                    if configuracao.tag_erro_descricao:
                        texto_erro = getattr(erro, configuracao.tag_erro_descricao, '')
                        mensagem_erro += 'Mensagem: {texto_erro}\n'.format(texto_erro=texto_erro)

                conexao.mensagem_erro = mensagem_erro

        return conexao
