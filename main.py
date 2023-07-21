import telebot
from vars import Comandos, helpdesk, ajuda, ponto_0, ponto_1, ponto_2, batida
from handlers import checar_chamado,exibir_chamado,encerrar_chamado
from time import sleep

KEY = "6326692952:AAHAOzOq7Y3931MQUx4XjB7Vj_ZVUFNRvLo"
bot = telebot.TeleBot(KEY)

def receive_message(message):  # INTERPRETADOR DE TEXTO
    ler_mensagem = message.text
    ler_mensagem = ler_mensagem.upper()

    filtrar_mensagem = ler_mensagem.split('_')[0]

    if ler_mensagem in Comandos:
        Primeiro_Contato(message)

    elif ler_mensagem in ajuda:
        Mensagem_Help(message)

    elif ler_mensagem in helpdesk:
        Chamados_Mensagem(message, checar_chamado())

    elif ler_mensagem in ponto_0:
        Ponto(message)

    elif ler_mensagem in ponto_1:
        Contador(message, tempo=3600)

    elif ler_mensagem in ponto_2:
        Contador(message, tempo=1200)

    elif ler_mensagem in batida:
        Cronometro_Ponto(message,True)

    elif ler_mensagem == "FECHAR":
        Fechar_Lista_Chamado(message)

    elif filtrar_mensagem == "/FECHAR":
        Tenta(message)

    else:
        Erro_Mensagem(message)
    return True


@bot.message_handler(func=receive_message)  # recebendo a função receive_message
def Start(message):
    pass


# =======================================================================================================================
def Primeiro_Contato(message):  # ENVIA UMA MENSAGEM PADRÃO DE BOAS VINDAS
    texto = f"""
🤖 Olá, eu sou o TIverr Bot 🤖

Estou aqui para auxiliar a equipe de TI sempre que necessário.
O que gostaria de ver?

/Chamados - Exibe a lista de Chamados abertos no GLPI

/Ponto - Exibe a lista de opções para notificação de ponto

/Comandos - Exibe a lista de comandos do Bot

Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(message, texto)

# =======================================================================================================================
def Erro_Mensagem(message):  # RETORNA UMA MENSAGEM PADRÃO QUANDO NENHUM COMANDO É RECONHECIDO
    texto = """
Me desculpe, não entendi. . .
Poderia repetir?
Se precisar ver meus comandos é só digitar "comandos", ou "ajuda" para exibir lista de comandos.
"""
    bot.reply_to(message, texto)

# =======================================================================================================================
def Mensagem_Help(message):  # EXIBE A LISTA DE COMANDOS DO BOT
    texto = """
Segue a lista de Comandos do Bot: 
/Chamados - Exibe a lista de Chamados abertos no GLPI
/Ponto - Exibe a lista de opções para notificação de ponto
/Fechar_id - Fecha chamado por ID
"""
    bot.reply_to(message, texto)


# =======================================================================================================================
def Ponto(message):  # Menu de Opções de pausa
    texto = """
⏱️- NOTIFICADOR DE PONTO - ⏱️

Escolha o tipo de pausa que vai fazer:

/PAUSA_60 - Pausa de 1 hora, almoço

/PAUSA_20 - Pausa de 20 minutos
"""
    bot.reply_to(message, texto)

# =======================================================================================================================
def Cronometro_Ponto(message, validador):
    for i in range(60):

        if validador == True:
            bot.reply_to(message, f"""📃 - BATIDA REGISTRADA - 📃""")
            break;

        else:
            sleep(60)
            if i % 5 == 0 and i!=0:
                bot.reply_to(message, f"""⚠️ - BATIDA NÃO REGISTRADA - ⚠️

                Não foi registrado batida de ponto há {i} minutos. 

                Em caso de batida feita use o comando Batida ou Ponto Registrado.   
                """)

# =======================================================================================================================
def Contador(message, tempo=int):  # conta o tempo de pausa
    bot.reply_to(message, f"""⏱️ - CONTADOR INICIADO - ⏱️
TEMPO: {tempo / 60} Minutos""")
    sleep(tempo - 300)  # 3300 - 55 Min
    bot.reply_to(message, """⚠️ - ALERTA DE TEMPO - ⚠️
5 Minutos restantes de sua pausa!""")
    sleep(300)  # 300 - 5 Min
    bot.reply_to(message, """⛔ - ALERTA DE TEMPO - ⛔
SUA PAUSA ACABOU, BATA O PONTO""")

    Cronometro_Ponto(message, False)

# =======================================================================================================================
def Chamados_Mensagem(message, texto):
    texto = f"""📃 - LISTA DE NOVOS CHAMADOS - 📃
    {texto}"""

    bot.reply_to(message, texto)

# =======================================================================================================================
def Fechar_Lista_Chamado(mensagem):
    list_chamado = exibir_chamado()
    texto = f"""
        Escolha uma opção para continuar (Clique no item):

        {list_chamado}

    Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

def Tenta(mensagem):

    ler_id = mensagem.text
    id = ler_id.split('_')[1]

    encerrar_chamado(id)

    bot.reply_to(mensagem, f'Chamado de ID - {id} encerrado via serviço Mobile')

# =======================================================================================================================
bot.infinity_polling()

