import glpi_api
import pandas as pd
import html
from bs4 import BeautifulSoup
import re
import datetime,time, threading

def checar_chamado():
    # Faz a conexão com a API puxando os Tickets com Status 1 = Novo
    chamados = []

    try:
        with glpi_api.connect(url='http://dominio/glpi/apirest.php/',
                              apptoken='seutoken',
                              auth=('seuuser', 'suasenha')) as glpi:
            glpi = glpi.get_all_items('Ticket', searchText={'status': '1'})
    except glpi_api.GLPIError as err:
        print(str(err))

    df = pd.DataFrame(glpi)
    for i in range(len(df)):

        # puxa as informações do Content em formato HTML
        solicitante = df['content'][i]
        id_chamado = df['id'][i]
        # faz a alteração da variavel Solicitante em html para texto
        decoded_string = html.unescape(solicitante)
        soup = BeautifulSoup(decoded_string, "html.parser")
        text = soup.get_text()

        # Usando expressões regulares para extrair as informações
        solicitante = re.search(
            r"Solicitante:\s*-(.*?)Nome do operador:\s*-(.*?)Carteira:\s*-(.*?)Descrição do problema:\s*-(.*)", text,
            re.DOTALL)

        if solicitante:
            nome_solicitante = solicitante.group(1).strip()
            nome_operador = solicitante.group(2).strip()
            carteira = solicitante.group(3).strip()
            descricao_problema = solicitante.group(4).strip()

            chamado = f"""

Chamado aberto ID - {id_chamado}

            - Solicitante: {nome_solicitante}

            - Nome do Operador: {nome_operador}

            - Carteira: {carteira}

            - Descrição do Problema: {descricao_problema}
            """

            chamados.append(chamado)

    return "\n".join(chamados)


def exibir_chamado():
    chamados = []

    try:
        with glpi_api.connect(url='http://dominio/glpi/apirest.php/',
                              apptoken='seutoken',
                              auth=('seuuser', 'suasenha')) as glpi:
            glpi = glpi.get_all_items('Ticket', searchText={'status': '1'})
    except glpi_api.GLPIError as err:
        print(str(err))

    df = pd.DataFrame(glpi)
    for i in range(len(df)):

        solicitante = df['name'][i]
        id_chamado = df['id'][i]

        chamado =f"""
    /Fechar_{id_chamado} - {solicitante}
    """
        chamados.append(chamado)

    return "\n".join(chamados)

def encerrar_chamado(id):
    try:
        with glpi_api.connect(url='http://dominio/glpi/apirest.php/',
                               apptoken='lqgXI98XoygfItiviU4NAdQqNMguPuOasH8ls2G4',
                                  auth=('user', 'senha')) as glpi:
            glpi = glpi.update('Ticket',
                               {'id': id, 'status': '5', 'content': 'SOLUÇÃO APROVADA VIA SERVIÇO MOBILE', '_close': '1',
                                'add_close': '1'})
    except glpi_api.GLPIError as err:
            print(str(err))

    try:
        with glpi_api.connect(url='http://dominio/glpi/apirest.php/',
                               apptoken='lqgXI98XoygfItiviU4NAdQqNMguPuOasH8ls2G4',
                                  auth=('user', 'senha')) as glpi:
            glpi2 = glpi.add('ticketvalidation',
                           {'id':2,'tickets_id':id, 'comment_submission':'VALIDAÇÃO MOBILE', 'status':5})
    except glpi_api.GLPIError as err:
            print(str(err))
