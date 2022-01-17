import sys

import jaydebeapi
from pandas import DataFrame
from pkg_resources import resource_filename

from nfetcego.cfgparse import (get_dremio_connection, get_dremio_password,
                               get_dremio_user)
from nfetcego.io import read_sql

path_dremio_driver = resource_filename(
    'nfetcego.resources', 'dremio-jdbc-driver.jar')

base_query = '''
        SELECT 
        nfe.nfe_chave_acesso as chave_acesso
        ,nfe.nfe_data_emissao_trunc as data_emissao
        ,nfe.nfe_valor_total as valor_total
        ,nfe.nfe_quantidade_produtos as quantidade_itens
        ,nfe.emitente_cnpj as emitente_cnpj_cpf
        ,nfe.emitente_razao_social as emitente_razao_social
        ,nfe.destinatario_cnpj as destinatario_cnpj
        ,nfe.destinatario_razao_social as destinatario_razao_social
        ,nfe.produto_item_numero
        ,nfe.produto_codigo
        ,nfe.produto_descricao
        ,nfe.produto_tipo_medida
        ,nfe.produto_quantidade
        ,nfe.produto_valor_total
        FROM IE.NFE.NFeComprasGov nfe
        '''


def get_connection():
    conn = jaydebeapi.connect(
        'com.dremio.jdbc.Driver',
        f'jdbc:dremio:direct={get_dremio_connection()}',
        [
            get_dremio_user(),
            get_dremio_password()
        ],
        path_dremio_driver
    )

    return conn


def execute_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    data = DataFrame(
        cursor.fetchall(),
        columns=[i[0] for i in cursor.description]
    )
    if data.empty:
        print('Nenhum registro encontrado.')
        print('Fim da execução.')
        sys.exit(1)
    conn.close()
    return data


def get_data(options):

    if 'from_sql' in options:
        query = read_sql(options['from_sql'])
    else:
        query = construct_query(options)
    data = execute_query(query)
    return data


def construct_query(options):
    query = base_query
    conditions = []

    if 'where' in options:
        # Placeholder for where clauses
        query = query + ' WHERE ' + ' and '.join(conditions)

    conditions = []
    if 'limit' in options:
        limit = options['limit']
        query = query + f' LIMIT {limit}'

    return query
