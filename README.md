# pybrasil

[![Build Status](https://travis-ci.org/odoo-brazil/pybrasil.svg?branch=master)](https://travis-ci.org/odoo-brazil/pybrasil)

Diversas funções de validação necessárias a ERPs no Brasil:

(Os nomes das funções são prolixos e longos, propositalmente, para facilitar o uso por usuários finais [usuários de RH, advogados etc.])

Submódulo base:
---------------
    - modulo_10: Cálculo do módulo 10, usada em boletos e carteiras de cobrança
    - modulo_11: Cálculo do módulo 11, usada em boletos e carteiras de cobrança
    - mascara: Aplicação de máscaras em strings, de forma parecida com a função Mask do Delphi
    - primeira_maiuscula: Capitalização específica para nomes encontrados no Brasil
    - tira_acentos: Remove acentos (mas mantém caracteres especiais), usada em boletos e carteiras de cobrança
    - somente_ascii: Remove inclusive caracteres ditos "especiais" pelos bancos
    - escape_xml: Escapa os caracteres para xmls de prefeituras que não respeitam os padrões xml
    - unescape_xml: Idem acima

Submódulo ibge:
---------------

    - Classes: Pais, Estado, Municipio, Local
    - Dicionários e constantes:
      - PAIS_BACEN, PAIS_BRASIL, PAIS_NOME, PAIS_ISO_3166_2, PAIS_ISO_3166_3
      - ESTADO_IBGE, ESTADO_SIGLA
      - MUNICIPIO_IBGE, MUNICIPIO_SIAFI, MUNICIPIO_ESTADO_NOME, MUNICIPIO_NOME

Submódulo data:
---------------

    - DIA_DA_SEMANA, DIA_DA_SEMANA_ABREVIADO, MES, MES_ABREVIADO: constantes usadas para tradução e tratamento de datas pelo parse_datetime (vide abaixo)
    - Datas e horas por extenso (usada no preenchimento de Folha de Pagamento e Contratos):
      - data_por_extenso
      - dia_da_semana_por_extenso
      - dia_da_semana_por_extenso_abreviado
      - mes_por_extenso
      - mes_por_extenso_abreviado
      - mes_romano
      - seculo
      - seculo_por_extenso
      - seculo_romano
      - milenio
      - milenio_por_extenso
      - milenio_romano
      - hora_por_extenso
      - hora_por_extenso_aproximada
      - formata_data
      - ano_por_extenso
      - ano_romano
    - Tratamento de fuso horário e datas UTC e Brasília (várias são usadas na folha de pagamento):
      - UTC: timezoneinfo UTC
      - HB: timezoneinfo hora oficial de Brasília
      - fuso_horario_sistema
      - data_hora_horario_brasilia
      - agora
      - hoje
      - ontem
      - amanha
      - mes_passado
      - mes_que_vem
      - ano_passado
      - ano_que_vem
      - semana_passada
      - semana_que_vem
      - primeiro_dia_mes
      - ultimo_dia_mes
      - hora_decimal_to_horas_minutos_segundos
      - horario_decimal_to_hora_decimal
      - horas_minutos_segundos_to_hora_decimal
      - horas_minutos_segundos_to_horario_decimal
    - Cálculos de idade (idem, são usadas principalmente na FP):
      - tempo
      - idade_anos
      - idade_meses
      - idade_meses_sem_dia
    - Dias úteis (idem, FP e financeiro):
      - dias_uteis
      - dias_uteis_bancarios
      - dias_uteis_bancarios

Submódulo feriado:
------------------

    - Feriados (idem, tratamento de várias situações de feriados no Brasil):
      - data_eh_feriado
      - data_eh_feriado_bancario
      - data_eh_feriado_emendado
      - data_eh_feriado_bancario_emendado
      - conta_feriados
      - conta_feriados_sem_domingo

Submódulo inscricao:
--------------------

    - Validações de inscrições e registros nas instâncias federais e estaduais, formatação desses números:
    - limpa_formatacao
    - valida_cnpj e formata_cnpj
    - valida_cpf e formata_cpf
    - valida_ie, formata_ie
    - valida_titulo_eleitor, formata_titulo_eleitor
    - valida_pis, formata_pis
    - constantes para a validação da certidão civil: TIPO_CERTIDAO_CIVIL_NASCIMENTO, TIPO_CERTIDAO_CIVIL_CASAMENTO, TIPO_CERTIDAO_CIVIL_CASAMENTO_RELIGIOSO
    - valida_certidao_civil, formata_certidao_civil
    - separa_certidao_civil: trata a leitura do número da certidão civil no contexto dos contratos do RH

Submódulo produto:
------------------

    - valida_ean: validação dos códigos de barras dos produtos

Submódulo valor:
----------------

    - NumeroPorExtenso: classe para conversão de números por extenso para o Brasil
    - Funções:
      - numero_por_extenso
      - numero_por_extenso_ordinal
      - numero_por_extenso_unidade
      - formata_valor: formatação de valores em português (usada por usuários finais na FP)
    - decimal.py: cópia do código original do Python 2.7, dos tipos Decimal e suas funções,
        tratado para funcionar de forma transparente com tipos float, de forma a gerar os resultados
        esperados pelos usuários finais nos cálculos da FP e do fiscal

Submódulo telefone:
-------------------

    - Validação e formatação de números de telefone no Brasil:
      - valida_fone_fixo
      - valida_fone_celular
      - valida_fone_internacional
      - valida_fone (testa todos os tipos)
      - formata_fone
      - formata_varios_fones (listas de números, tratando o caso do mesmo DDD)

Submódulo ncm:
--------------

    - Classes: NCM, NBS, Servicos
    - Dicionários e constantes:
      - NCM_CODIGO_EX
      - NBS_CODIGO
      - SERVICOS_CODIGO

Submódulo python_pt_BR:

    - Função python_pt_BR
