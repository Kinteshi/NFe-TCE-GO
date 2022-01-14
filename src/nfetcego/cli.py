import argparse
import sys

parser = argparse.ArgumentParser(
    prog='NFe TCE-GO', description='development version')

parser.add_argument(
    'task',
    action='store',
    choices=['extract'],
    type=str,
    help='''
        Tarefa: obrigatório. Seleciona a tarefa a ser executada.
        \'extract\' Extrai dados de NFe.
        ''',
)

parser.add_argument(
    '--limit', '-l',
    action='store',
    type=int,
    nargs=1,
    help='''
        Limita o número de NFe extraídas: opcional. Só é funcional quando a tarefa selecionada é \'extract\'.
        ''',
)


def main():
    args = parser.parse_args()
    options = {}
    if args.task == 'extract':
        if args.limit:
            options['limit'] = args.limit[0]
        from nfetcego.workflows.extraction import extraction_flow
        extraction_flow(options)
        sys.exit(0)
