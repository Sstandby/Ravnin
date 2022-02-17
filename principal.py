"""
MIT License

Copyright (c) 2021 Standby 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
try:
 import amino
 amino = amino
except:
 import amino
import time
from threading import Timer
from threading import Thread
from acciones.funcionesUniversales import admins, clienteAmino, wiki, upload, ravnin, mensajeLogin
from acciones import funcionesAcciones
from acciones import funcionesMensajes
from mensajes import mensajesBot


content = None
activo = True
ayuda = open("datos/wikis/ayuda.txt", "r").read()
bienvenida = open("datos/wikis/bienvenida.txt", "r").read()
despedida = open("datos/wikis/despedida.txt", "r").read()


def parametros(l):
    return ' '.join(l)

# Funcion de coins al donar


@clienteAmino.event('on_chat_tip')
def on_chat_tiip(data):
    try:
        subClient = amino.SubClient(comId=data.comId,
                                    profile=clienteAmino.profile)
    except Exception:
        return

    raw_data = data.json
    coins = raw_data['chatMessage']['extensions']['tippingCoins']
    mensaje = {
        'message': "[C]¡Muchas gracias! nwn",
        'embedTitle': data.message.author.nickname,
        'chatId': data.message.chatId,
        'embedImage': upload(data.message.author.icon),
        'embedLink': "ndc://user-profile/data.message.author.userId",
        'embedContent': f"Coins donadas: {coins} ♡"
    }
    subClient.send_message(**mensaje)


# Funcion de bienvenida a los usuarios
@clienteAmino.event('on_group_member_join')
def on_group_member_join(data):
    sub = amino.SubClient(comId=data.comId, profile=clienteAmino.profile)
    if data.message.author.userId not in content.lista_negra:
        mensaje = {
            'message': f"{content.join}",
            'embedTitle': data.message.author.nickname,
            'chatId': data.message.chatId,
            'embedImage': upload(data.message.author.icon)
        }
        sub.send_message(**mensaje)


# Funcion de despedida a los usuarios
@clienteAmino.event('on_group_member_leave')
def on_group_member_leave(data):
    sub = amino.SubClient(comId=data.comId, profile=clienteAmino.profile)
    if data.message.author.userId not in content.lista_negra:
        mensaje = {
            'message': f"{content.leave}",
            'chatId': data.message.chatId
        }
        sub.send_message(**mensaje)


# Funcion para las acciones del bot
@clienteAmino.event("on_text_message")
def on_command_text(data):
    def commandos():
        subclient = amino.SubClient(comId=data.comId,
                                    profile=clienteAmino.profile)
        message = {'chatId': data.message.chatId}
        mensaje = data.message.content
        command = mensaje.split(' ')
        tmp = command[1:]
        command = command[0]
        comandoParametro = parametros(tmp)
        lenguaje = clienteAmino.get_community_info(
            comId=data.comId).primaryLanguage

        if activo is True:
            if command in funcionesAcciones.acciones:
                try:

                    if data.message.author.userId not in content.lista_negra:
                        params = parametros(tmp)
                        if params == "":
                            params = None
                        args = ravnin(data, subclient, params)
                        funcionesAcciones.acciones[command](args, lenguaje)
                    else:
                        message.update({
                            'message':
                            "¡Usaste mal mis comandos y tienes el descaro de volver a usarlos! -n-"
                        })
                        subclient.send_message(**message)

                except Exception as Error:
                    print(Error)
                    message.update({
                        'message':
                        "¡Cargando comandos, funciones, listas y clases en Ravnin... ¡1s! ... Intenta ejecutar nuevamente este comando."
                    })
                    subclient.send_message(**message)

            elif command == "-help":

                comandoParametro = parametros(tmp)
                if (comandoParametro in funcionesAcciones.acciones) or (
                        comandoParametro
                        in funcionesMensajes.responder_acciones) or (
                            comandoParametro
                            in funcionesAcciones.categoriasComandos):
                    funcionesAcciones.mostrarAyuda(message, comandoParametro)
                    subclient.send_message(**message)
                else:
                    try:
                        message.update({'message': content.mensajeAyuda})
                        subclient.send_message(**message)
                    except Exception:
                        message.update({
                            'message': "¡Cargando comandos, funciones, listas y clases en Ravnin... ¡1s! ... Intenta ejecutar nuevamente este comando."})
                        subclient.send_message(**message)

    comandos = Timer(0, commandos)
    comandos.start()


@clienteAmino.event("on_text_message")
def on_reply_message(data):
    def reply_message():

        subclient = amino.SubClient(comId=data.comId,
                                    profile=clienteAmino.profile)
        mensaje = data.message.content
        command = mensaje.split(' ')
        tmp = command[1:]
        command = command[0]
        reply = data.json
        lenguaje = clienteAmino.get_community_info(
            comId=data.comId).primaryLanguage

        extension = reply["chatMessage"]["extensions"]
        replyToMessage = extension.get('replyMessageId', None)
        replyMessage = extension.get('replyMessage', None)

        if replyToMessage is not None or replyMessage is not None:
            params = parametros(tmp)
            args = ravnin(data, subclient, params)
            idioma = funcionesAcciones.idiomaTrivia(lenguaje=lenguaje)

            if data.message.author.userId in admins:
                if command in funcionesMensajes.responder_acciones:
                    media = replyMessage["mediaValue"]
                    funcionesMensajes.responder_acciones[command](
                        args=args, media=media, replyToMessage=replyToMessage, admins=admins)
            if re.search("—可 Quizz", str(replyMessage)):
                funcionesMensajes.trivia(args, replyMessage, idioma,
                                         mensaje)

    delete = Timer(0, reply_message)
    delete.start()


@clienteAmino.event("on_text_message")
def contenido(data):

    print(data.message.author.nickname, ":", data.message.content)

    def contenido():
        global content
        if content == None:
            content = wiki(despedida=despedida,
                           bienvenida=bienvenida,
                           help=ayuda)

    if data.message.content.lower().startswith("-cache"):
        content = wiki(despedida=despedida, bienvenida=bienvenida, help=ayuda)

    contenido_wiki = Thread(target=contenido)
    contenido_wiki.start()


@clienteAmino.event("on_text_message")
def on_admin_message(data):
    def admin_message():
        global activo
        subclient = amino.SubClient(comId=data.comId,
                                    profile=clienteAmino.profile)
        mensaje = data.message.content
        chatId = data.message.chatId
        command = mensaje.split(' ')
        command = command[0]

        if data.message.author.userId in admins:
            if command == "-off":

                activo = False
                message_on = {'chatId': chatId, 'message': "¡Bot apagado!"}
                subclient.send_message(**message_on)

            elif activo is False:

                if command == "-on":

                    activo = True
                    message_on = {'chatId': chatId, 'message': "Bot activado"}
                    subclient.send_message(**message_on)

                if command in funcionesAcciones.acciones:

                    message_none = {
                        'chatId':
                        chatId,
                        'message':
                        "Bot en actualización, ¡Ningún comando funcionará!"
                    }
                    subclient.send_message(**message_none)

    admin_on = Timer(0, admin_message)
    admin_on.start()


def join_community():

    community = clienteAmino.get_wall_comments(
        userId=clienteAmino.userId, sorting="newest", start=0, size=100).json
    for i in range(len(community)):
        try:

            community_Link = community[i]["content"]
            """Invitar = re.search("http://aminoapps.com/invite/", community_Link)
            if invitar:
               invitation = client.get_from_code(community_Link).inviteId
               print("invitar; ", invitation)
               Id = client.get_from_code(community_Link).path
               community_Id = Id[1:Id.index("/")]
               client.join_community(comId=community_Id,invitationId=invitation)
            """
            Id = clienteAmino.get_from_code(community_Link).path
            community_Id = Id[1:Id.index("/")]
            clienteAmino.join_community(comId=community_Id)

        except Exception:

            # print(Error)
            Id = None


def loop():
    while True:
        join_community()
        time.sleep(10.0)


# Principal
if __name__ == "__main__":
    try:
        mensajeLogin()
        run = Thread(target=loop)
        run.start()
    except KeyboardInterrupt:
        mensajesBot.limpiarPantalla()
