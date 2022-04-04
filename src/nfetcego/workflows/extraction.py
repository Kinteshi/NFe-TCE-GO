import warnings

from nfetcego.dremio import get_data

warnings.filterwarnings('ignore')


def extraction_flow(options: dict):
    print('Preparando e executando consulta...')
    data = get_data(options)
    data = data.reset_index(drop=True)
    print('Salvando base de dados...')
    data.to_csv('nfedata.csv', index=False)
    print('Finalizado.')
