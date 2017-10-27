# -*- coding: utf-8 -*-
#
# PyBrasil - Functions useful for most Brazil's ERPs
#
# Copyright (C) 2016-
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
# PyBrasil - Funções de validação necessárias a ERPs no Brasil
#
# Copyright (C) 2016-
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

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)


from .cnpj_cpf import (valida_cnpj, valida_cpf, formata_cnpj, formata_cpf, limpa_formatacao)
from .inscricao_estadual import (valida_ie, formata_ie)
from .inscricao_estadual import valida_ie as valida_inscricao_estadual
from .inscricao_estadual import formata_ie as formata_inscricao_estadual
from .titulo_eleitor import (valida_titulo_eleitor, formata_titulo_eleitor)
from .pis import (valida_pis, formata_pis)
from .matricula_certidao_civil import (valida_certidao_civil, formata_certidao_civil, separa_certidao_civil)
from .matricula_certidao_civil import (TIPO_CERTIDAO_CIVIL_NASCIMENTO, TIPO_CERTIDAO_CIVIL_CASAMENTO, TIPO_CERTIDAO_CIVIL_CASAMENTO_RELIGIOSO)
from .cei import (valida_cei, formata_cei)
from .codigo_sindical import (valida_codigo_sindical, formata_codigo_sindical)
