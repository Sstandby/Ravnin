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

import ujson as json
import unicodedata
import re, requests, random, urllib.request, urllib.parse
from gtts import gTTS
from urllib.parse import quote
from google_trans_new import google_translator
# Archivos
from acciones.funcionesUniversales import admins, clienteAmino, pwd, upload
from mensajes import mensajesBot


def mostrarAyuda(message, comandoSolicitado):
    comandoRequerido = comandoSolicitado.split(comandoSolicitado[0])

    if comandoSolicitado[0] == "-":
        mensajeRequerido = "mensajeAyuda_"
    elif comandoSolicitado[0] == "~":
        mensajeRequerido = "mensajeAyuda_virguilila_"
    elif comandoSolicitado[0] == ".":
        mensajeRequerido = "mensajeAyuda_punto_"

    comandoAyuda = getattr(mensajesBot, mensajeRequerido + comandoRequerido[1])
    message.update({'message': comandoAyuda()})


def idiomaTrivia(lenguaje):
    with open(f'idiomas/trivia/{lenguaje}-trivia.json', encoding="utf8") as idioma:
        data = json.load(idioma)
        lenguaje = data
        return lenguaje


def trivia(args, lenguaje):
    # Definir categoria para el JSON
    if unicodedata.normalize('NFKD', "Música").encode(
            'ASCII', 'ignore').strip().lower() == unicodedata.normalize(
                'NFKD', args.params).encode('ASCII', 'ignore').strip().lower():
        result = "Música"
    elif unicodedata.normalize('NFKD', "Geografía").encode(
            'ASCII', 'ignore').strip().lower() == unicodedata.normalize(
                'NFKD', args.params).encode('ASCII', 'ignore').strip().lower():
        result = "Geografía"
    elif args.params.lower() == "Arte".lower():
        result = "Arte"
    elif args.params.lower() == "General".lower():
        result = "General"
    elif args.params.lower() == "Ciencia".lower():
        result = "Ciencia"

    idioma = idiomaTrivia(lenguaje)
    question = []
    answer = []
    for i in idioma[f"{result}"]:
        select_preguntas = i["pregunta"]
        select_respuestas = i["respuestas"]
        question.append(select_preguntas)
        answer.append(select_respuestas)
    max = random.randint(0, len(question) - 1)
    uno, dos, tres, cuatro = random.sample([0, 2, 3, 1], 4)
    message = {
        'chatId':
        args.chatId,
        'message':
        "[CB]—可 Quizz {params}❜\n\n\n[C]你好 —  ❥{question}\n\n1 ⇢ {uno} \n2 ⇢ {dos} \n3 ⇢ {tres} \n4 ⇢ {cuatro}\n\n[CB]⸙͎۪۫ Usar -lista"
        .format(params=result,
                question=question[max],
                uno=answer[max][uno],
                dos=answer[max][dos],
                tres=answer[max][tres],
                cuatro=answer[max][cuatro]),
        'replyTo':
        args.messageId
    }
    args.subclient.send_message(**message)


def commentUser(args, lenguaje):
    if re.search("=", args.params):
        tmp = re.split("=", args.params)
        user = args.search_users(tmp[0])
        if not user: return
        message = {'message': tmp[1], 'userId': user.userId[0]}
    else:
        message = {'message': args.params, 'userId': args.profileId}

    message_carga = {
        'chatId':
        args.chatId,
        'message':
        "[C]Comentario enviado. (っ•̀ω•̀)╮ =͟͟͞͞ 💗\n\n\n[C]Gracias por usar el\n[C]servicio de mensaje\n[C]Ravnin. (ง •᷄ω•)ว"
    }

    args.subclient.send_message(**message_carga)
    args.subclient.comment(**message)


def idWiki(args, lenguaje):
    msg_2 = str(args.params)
    messageId = msg_2.replace("http://aminoapps.com/p/", "")
    ide = args.subclient.get_from_code(messageId).objectId
    try:
        args.subclient.send_message(chatId=args.chatId,
                                    message=f"El ide de esta wiki es: {ide}")
    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def destacar(args, lenguaje):

    if re.search("http://aminoapps.com/p/", str(args.params)):
        msg_2 = str(args.params)
        messageId = msg_2.replace("http://aminoapps.com/p/", "")
        ide = args.subclient.get_from_code(messageId).objectId
    else:
        ide = args.subclient.get_from_code(args.params).objectId

    try:

        blog = args.subclient.get_blog_info(ide).json
        titulo = blog["blog"]["title"]
        if args.profileId in admins:
            message_ide = {
                'chatId': args.chatId,
                'message': f"¡Post: {titulo} destacado con exito! >w<"
            }
            args.subclient.send_message(**message_ide)
            args.subclient.feature(time=3, blogId=ide)
        else:
            message_ide = {
                'chatId':
                args.chatId,
                'message':
                f"¿Qué haces usando comando para dueños, {args.name}? ¿Eres tontito/a? -.-'"
            }
            args.subclient.send_message(**message_ide)

    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def playGame(args, lenguaje):
    try:

        messageId = args.params.replace("http://aminoapps.com/p/", "")
        quizzId = str(args.subclient.get_from_code(messageId).objectId)
        args.play_quiz(quizzId)

    except Exception as error:

        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def confession(args, lenguaje):
    search = re.search("=", args.params)
    link_web = re.search("http://aminoapps.com/p/", args.params)
    staff = clienteAmino.get_community_info(args.comId).json
    staff = staff["communityHeadList"]
    staffList = []

    if search:
        if link_web:
            tmp = args.params.replace("http://aminoapps.com/p/", "")
            tmp = re.split("=", args.params)
            user = args.subclient.get_from_code(tmp[0]).objectId
            for i in staff:
                id = i["uid"]
                staffList.append(id)
            if user is not staffList:
                tmp = re.split("=", args.params)
                user = args.subclient.get_from_code(tmp[0]).objectId
                message = {
                    'message': f"[CB]♥ Confesión ♥ (ノ_<。)\n\n{tmp[1]}",
                    'userId': user
                }
            else:
                message = {
                    'message':
                    "¡Intentaron mandarte un mensaje anonimo, cuidado, Staff! >.<",
                    'userId': user
                }
        else:
            message = {
                'message': f"Auto Confesión u.u\n\n{args.params}",
                'userId': args.profileId
            }
    else:
        message = {
            'message': "¿Qué haces usando mal este comando, tonto/a? -,-",
            'userId': args.profileId
        }
    message_carga = {
        'chatId':
        args.chatId,
        'message':
        "[C]Confesión enviada. (っ•̀ω•̀)╮ =͟͟͞͞ 💗\n\n\n[C]Gracias por usar el\n[C]servicio de mensaje\n[C]Ravnin. (ง •᷄ω•)ว"
    }

    args.subclient.send_message(**message_carga)
    args.start_chat(message)


def join(args, lenguaje):
    try:
        args.join_chats()
    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def comunidad(args, lenguaje):
    args.join_community()


def love(args, lenguaje):
    num = requests.get(
        'http://2g.be/twitch/randomnumber.php?=defstart=1&defend=109)%')
    response = json.loads(num.text)
    if int(response) >= 50 and int(response) <= 79:
        message = {
            'chatId':
            args.chatId,
            'message':
            f"Tienen un {response}% {args.name} and {args.params} parecen ser buenos amigos, a lo mejor en un futuro sean mejores amigos. OwO"
        }
    if int(response) >= 80:
        message = {
            'chatId':
            args.chatId,
            'message':
            f"Tienen un {response}% {args.name} and {args.params} parecen ser buenos amigos, a lo mejor son coge amigos... O novios? OwO"
        }
    if int(response) <= 49 and int(response) >= 20:
        message = {
            'chatId':
            args.chatId,
            'message':
            f"Tienen un {response}% {args.name} and {args.params}, probablemente conocidos... Pero lo muy seguro es que se odian, creeme. >.<"
        }
    if int(response) <= 20:
        message = {
            'chatId':
            args.chatId,
            'message':
            f"Tienen un {response}% {args.name} and {args.params} son como la caca y comida, no van.. yny"
        }
    args.subclient.send_message(**message)


def siri(args, lenguaje):
    tts = gTTS(args.params, lang='es')
    file = tts.save('audio.mp3')

    try:

        with open("audio.mp3", "rb") as file:
            message = {
                'chatId': args.chatId,
                'embedContent': 'I am alive.',
                'file': file,
                'fileType': "audio"
            }
            args.subclient.send_message(**message)

    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def everyone(args, lenguaje):
    users = []
    I = 0
    while I < 1:
        people = args.subclient.get_chat_users(args.chatId, size=1090).userId
        for usersin in people:
            users.append(usersin)
            print(users)
        message = {
            'chatId': args.chatId,
            'message': f"<$@{args.params}$>",
            'mentionUserIds': users
        }
        args.subclient.send_message(**message)
        print("send")
        del users
        I += 1


def traductor(args, lenguaje):
    translator = google_translator()
    translate_text = translator.translate(args.params, lang_tgt='es')
    try:
        message = {'chatId': args.chatId, 'message': f"<${translate_text}$>"}
        args.subclient.send_message(**message)
    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def anfi(args, lenguaje):
    try:
        args.subclient.accept_host(args.chatId)
        message = {
            'chatId': args.chatId,
            'message': "<$¡Gracias por hacerme anfi! >w<$>"
        }
        args.subclient.send_message(**message)
    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def coa(args, lenguaje):
    try:
        args.subclient.accept_organizer(args.chatId)
        message = {
            'chatId': args.chatId,
            'message': "<$¡De coanfitrion a anfi, yeii! uwu$>"
        }
        args.subclient.send_message(**message)
    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def comunidadLike(args, lenguaje):
    try:
        if args.profileId in admins:
            clienteAmino.add_linked_community(args.comId)
            message = {
                'chatId':
                args.chatId,
                'message':
                "<$¡Ya puse esta comunidad como de mis favoritas en mi perfil global, muak! uwu$>"
            }
            args.subclient.send_message(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)
    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def purge(args, lenguaje):
    msg = args.subclient.get_chat_messages(args.chatId, size=args.params)
    if args.profileId in admins:
        for messageId in zip(msg.messageId):
            messageId = list(messageId)
            for x in range(0, len(messageId)):
                args.subclient.delete_message(args.chatId, messageId[x], False)
        message = {
            'chatId': args.chatId,
            'message': "<$Mensajes borrado con exito. >:3$>"
        }
        args.subclient.send_message(**message)
    else:
        message = {
            'chatId': args.chatId,
            'message': "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
        }
        args.subclient.send_messag(**message)


def kick(args, lenguaje):
    user = args.search_users(args.params)
    if args.profileId in admins:
        args.subclient.kick(chatId=args.chatId,
                            userId=user.userId[0],
                            allowRejoin=False)
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$¡Usuario rebelde expulsado del chat con exito! La proxima vez que vuelvas te metere mas patadas. Jum. uwu$>"
        }
        args.subclient.send_message(**message)
    else:
        message = {
            'chatId': args.chatId,
            'message': "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
        }
        args.subclient.send_messag(**message)


def info(args, lenguaje):
    if args.params == None: args.params = ""
    user_info = re.search("@", args.params)
    if user_info:
        params = args.params.replace("@", "")
        usuario_arrobado = args.search_users(params)
        global_user = clienteAmino.get_user_info(
            f"{usuario_arrobado.userId[0]}").aminoId
        message = {
            'chatId': args.chatId,
            'message':
            f"""[IC]‎˖ ࣪‏@stalkeando a esta t̆̈ernurita‬‭ {usuario_arrobado.nickname[0]}˓ ！˖ ࣪

♡̷̷ : : id = {usuario_arrobado.userId[0]}

♡̷̷ : : blogs = {usuario_arrobado.json[0]["blogsCount"]}

♡̷̷ : : online = {bool(int(usuario_arrobado.json[0]["onlineStatus"])%2)}

♡̷̷ : : nivel = {usuario_arrobado.level[0]}

♡̷̷ : : Reputación = {usuario_arrobado.reputation[0]}

♡̷̷ : : Perfil Global = https://aminoapps.com/u/{global_user}
	    
[BC]𝙗𝙞𝙤𝘨𝘳𝘢𝘧𝘪𝘢 ( ꈍᴗꈍ)

♡̷̷ : : bio = {usuario_arrobado.json[0]["content"]}""",
            'embedTitle': f"{usuario_arrobado.nickname[0]}",
            'replyTo': args.messageId,
            'embedImage': upload(usuario_arrobado.icon[0])
        }
        args.subclient.send_message(**message)
    else:
        user = args.search_users(args.name)
        globalId = clienteAmino.get_user_info(f"{args.profileId}").aminoId
        message = {
            'chatId': args.chatId,
            'message': f"""
[IC]‎˖ ࣪‏@stalkeando a esta t̆̈ernurita‬‭ {args.name}˓ ！˖ ࣪
♡̷̷ : : id = {args.profileId}
♡̷̷ : : blogs = {user.json[0]["blogsCount"]}
♡̷̷ : : online = {bool(int(user.json[0]["onlineStatus"])%2)}
♡̷̷ : : nivel = {args.author.level}
♡̷̷ : : Reputación = {args.author.reputation}
♡̷̷ : : Perfil Global = https://aminoapps.com/u/{globalId}
	    
[BC]𝙗𝙞𝙤𝘨𝘳𝘢𝘧𝘪𝘢 ( ꈍᴗꈍ)

♡̷̷ : : bio = {user.json[0]["content"]}""",
            'embedTitle': f"{args.name}",
            'replyTo': args.messageId,
            'embedImage': upload(args.author.icon)
        }
        args.subclient.send_message(**message)


def creditos(args, lenguaje):
    creditos = """[CB]𝓡𝓪𝓿𝓷𝓲𝓷
[C]	    
[C]La verdad no sé por donde empezar... Este proyecto ni siquiera comenzó con el nombre Ravnin ni ideas locas por comenzar, mi primer bot comenzó a decir frases (Y ahora ni tiene eso Ravnin, que loco), luego a comentar en muros, y después termino en un proyecto que le di mucho cariño, en donde pude ponerle cada sentimiento de mí a Ravnin, frases, su forma de ser, estoy feliz de haber conocido a cada dueño y sobre todo estoy totalmente agradecido con; Leah, Macias, Elliot, Manzanita, kain, -Google, Teacito, Vanced, Lobito, Mafia, Darwin, Blue. Y a todos ustedes que usan este bot.
[C]
[C]¡Muchas gracias!
[C]Att. Standby"""
    message = {
        'chatId': args.chatId,
        'message': f"{creditos}",
        'replyTo': args.messageId
    }
    args.subclient.send_message(**message)


def id(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message': f"- comunidad = {args.comId} \n- chat = {args.chatId}"
    }
    args.subclient.send_message(**message)


def kill(args, lenguaje):
    kill = [
        f"Le agarra la cabeza {args.params}... Y zaz, lo mata a besitos en el poto",
        f"¡Empieza agarrarlo de los pies a {args.params} y lo manda por los aires!",
        f"Agarra un pan y ¡Oh no! no, no.. Suelta ese pan.. Mato a {args.params} >.<"
        f"Le mando un beso toxico a {args.params}... K.O x.x",
        f"Le recuerda a la ex y lo mata de tristeza a {args.params} u.u",
        f"Empieza a comerse de poco a poco a {args.params}, pero a besos.. @-@"
    ]
    user = args.search_users(args.params)
    if not user: return

    url = f'https://some-random-api.ml/canvas/wasted/?avatar={user.icon[0]}?key=AxFY2cclzlYWbeOrZXnsHpraT'
    file = upload(url)
    try:
        message = {
            'chatId': args.chatId,
            'embedContent': random.choice(kill),
            'embedTitle': f"{args.name}",
            'mentionUserIds': [args.profileId, user.userId[0]],
            'file': file,
            'fileType': "image"
        }
        args.subclient.send_message(**message)

    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def gay(args, lenguaje):
    url = f'https://some-random-api.ml/canvas/gay/?avatar={args.author.icon}?key=AxFY2cclzlYWbeOrZXnsHpraT'
    file = upload(url)
    num = requests.get(
        'http://2g.be/twitch/randomnumber.php?=defstart=1&defend=109)%')
    gay = json.loads(num.text)
    message = {
        'chatId': args.chatId,
        'embedContent': f"Eres un {gay} gay. Grr 6w6",
        'embedTitle': f"{args.name}",
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def coin(args, lenguaje):
    coin = pwd("media/img/monedas")
    random_img = str(random.choice(coin))
    with open((random_img), "rb") as file:
        message = {
            'chatId': args.chatId,
            'embedContent': 'OMG; Que suertudo eres!!! >w<',
            'embedTitle': "⠀",
            'file': file,
            'fileType': "image"
        }
        args.subclient.send_message(**message)


def dance(args, lenguaje):
    ruta = pwd("media/img/dance")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    dance = ["\t\t\t🗣🎤\n\n\t\t\t💃🕺💃🕺💃🕺", "💃🕺"]
    message = {
        'chatId': args.chatId,
        'message': random.choice(dance),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def nalgada(args, lenguaje):
    ruta = pwd("media/img/nalgada")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    nalgada = [
        f"{args.name} le agarra fuertemente la colita a {args.params} uwu",
        f"{args.name} agarra su mano y la lleva al otro mundo para llevarla a este... Y darle una tremenda nalgada a {args.params} >:3",
        f"Que haces mi amooor {args.params}? *Le agarra una nalgita* ve papasito'",
        f"{args.name} le da una nalgada a {args.params} y se va corriendo o.o",
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(nalgada),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def dormir(args, lenguaje):
    ruta = pwd("media/img/dormir")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    dormir = [
        f"Hagamos la mimision, {args.name} -w-",
        f"Zzzz.... ¡¡Qué haces despertandome, {args.name}!! Agh -n-",
        f"Te espero en la camita, {args.name} pa' comerte a besos -w-"
        f"**Mi-mimiendo con mi amado/a {args.name}** uwu",
        f"¡Una nalgada y a mimir {args.name}! :3"
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(dormir),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def hug(args, lenguaje):

    user = args.search_users(args.params)
    if not user: return

    message = {
        'chatId': args.chatId,
        'message':
        f"<$@{args.name}$> abraza con mucho amor a <${args.params}$>... >w<",
        'mentionUserIds': [args.profileId, user.userId[0]],
        'replyTo': args.messageId
    }
    args.subclient.send_message(**message)


def audio(args, lenguaje):

    audio = pwd("media/audio")

    with open(str(random.choice(audio)), "rb") as file:
        message = {
            'chatId': args.chatId,
            'message': 'I am alive.',
            'file': file,
            'fileType': "audio"
        }
        args.subclient.send_message(**message)


def img(args, lenguaje):
    img = pwd("media/img/otros")

    with open(str(random.choice(img)), "rb") as file:
        message = {
            'chatId': args.chatId,
            'message': 'I am alive.',
            'file': file,
            'fileType': "image"
        }
        args.subclient.send_message(**message)


def kiss(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'message':
            f"<$@{args.name}$> besó apasionadamente a <${args.params}$>...",
            'replyTo': args.messageId
        }
        args.subclient.send_message(**message)

    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def speak(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'message': f"{args.params}",
            'replyTo': args.messageId
        }
        args.subclient.send_message(**message)

    except Exception as error:
        args.subclient.send_message(
            chatId=args.chatId,
            message=
            f"<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        )
        mensajesBot.mensajeError(error)


def listaTrivia(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message':
        "[CB]• - ̗̀ ❛Esta es la lista de categorias sobre el juego trivia.‘﹏!˚ • '\n\n\n*ૢ                         ── lυv мe\n╰► ﹫Geografía\n╰► ﹫Ciencia\n╰► ﹫General\n╰► ﹫Arte\n\n[C]➤ Uso: -trivia Geografía",
        'replyTo': args.messageId
    }
    args.subclient.send_message(**message)


def speak_invicible(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message': f"{args.params}",
        'messageType': 109
    }
    args.subclient.send_message(**message)


def strike(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message': f"{args.params}",
        'messageType': 1
    }

    args.subclient.send_message(**message)


def casarse(args, lenguaje):
    casarse = [
        f"\t\tIglesia Ravnin.\n\n Hermanas y hermanos, estamos aquí reunidos para presenciar la boda de {args.name} y {args.params}. Si alguien se opone... Pues chinga su madre, no nos importa >:)",
        f"\t\tIglesia Ravnin.\n\n Hoy celebramos el santo matrimonio de {args.name} y {args.params}.\n\nAquel que se oponga a esta boda, caye ahora o vayase a ver netflix.",
        f"\t\tIglesia Ravnin.\n\n Con el poder de la matrix, yo declaró, casados a {args.name} y {args.params}. Puede besar al novio/a",
        f"\t\tIglesia Ravnin.\n\n Desde hoy, el amor entre {args.name} y {args.params}, queda bendecido por los de arriba."
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(casarse),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def patada(args, lenguaje):
    ruta = pwd("media/img/patada")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    patada = [
        f"Le mete una patada y lo manda por los aires a {args.params} >:3",
        f"Brr... Brrrrrr. Soy franshesco virgolini y yo, te mete una patade de tu de tu vida, {args.params}",
        f"Le mete una patada en las partes bajas... A {args.params} >.<",
        f"Le empieza a dar patadas como otaku a {args.params} -n-'",
        f"Le dio una pantada que lo deja sin hijos a {args.params} yny"
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(patada),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def desaparece(args, lenguaje):
    ruta = pwd("media/img/desaparecer")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    patada = [
        f"{args.name} desaparece como gil",
        f"{args.name} desaparece como nekito",
        f"{args.name} desaparece como furro",
        f"{args.name} desaparece como {args.name}, jaja k sad",
        f"{args.name} desaparece como fuckboy",
        f"{args.name} desaparece como fuckgirl",
        f"{args.name} se va por unos cigarros",
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(patada),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def cry(args, lenguaje):
    ruta = pwd("media/img/cry")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    cry = [
        f"{args.name} empieza a llorar... >n<",
        f"{args.name} sus lagrimas caen de poco a poco por tanta tristeza u.u",
        f"{args.name} llora como furro, eso... Ya es triste",
        f"{args.name} Empieza a sentirse mal, se va a una esquinita, y empieza a llorar solito/a...",
        f"{args.name} todos sus miedos, sus debilidades, sus fracasos... Se los ahorro, pero ya no puede mas, y empieza a llorar.. u.u",
        f"{args.name} le caen lagrimas de felicidad >w<",
        f"{args.name} se pone rojito, y se pone tan feliz que llorar de.. ?¡Felicidad! OwO",
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(cry),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def aparece(args, lenguaje):
    patada = [
        f"{args.name} aparece como gil",
        f"{args.name} aparece como nekito",
        f"{args.name} aparece como furro",
        f"{args.name} aparece como {args.name}, jaja k sad",
        f"{args.name} aparece como fuckboy",
        f"{args.name} aparece como fuckgirl",
        f"{args.name} aparece con 3 hijos, y una vida de gil",
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(patada),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def mishi(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'stickerId': random.choice(sticker_mishi)
        }
        args.subclient.send_message(**message)
    except Exception:
        message = {
            'chatId': args.chatId,
            'message': "No tengo Amino+ tontito/a uwu"
        }
        args.subclient.send_message(**message)


def snake(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'stickerId': random.choice(sticker_snake)
        }
        args.subclient.send_message(**message)
    except Exception:
        message = {
            'chatId': args.chatId,
            'message': "No tengo Amino+ tontito/a uwu"
        }
        args.subclient.send_message(**message)


def pandaBaby(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'stickerId': random.choice(sticker_pandas)
        }
        args.subclient.send_message(**message)
    except Exception:
        message = {
            'chatId': args.chatId,
            'message': "No tengo Amino+ tontito/a uwu"
        }
        args.subclient.send_message(**message)


def ratas(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'stickerId': random.choice(sticker_ratas)
        }
        args.subclient.send_message(**message)
    except Exception:
        message = {
            'chatId': args.chatId,
            'message': "No tengo Amino+ tontito/a uwu"
        }
        args.subclient.send_message(**message)


def randoms(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'stickerId': random.choice(sticker_meme)
        }
        args.subclient.send_message(**message)
    except Exception:
        message = {
            'chatId': args.chatId,
            'message': "No tengo Amino+ tontito/a uwu"
        }
        args.subclient.send_message(**message)


def anime(args, lenguaje):
    try:
        message = {
            'chatId': args.chatId,
            'stickerId': random.choice(sticker_anime)
        }
        args.subclient.send_message(**message)
    except Exception:
        message = {
            'chatId': args.chatId,
            'message': "No tengo Amino+ tontito/a uwu"
        }
        args.subclient.send_message(**message)


def ship(args, lenguaje):
    ship = [
        f"Oye {args.name}, si tú, deberias tener hijos con {args.params} -w-",
        "¡Qué haces perdiendo el tiempo, ya comanse!",
        f"Olvida a {args.params} mi casa esta desocupada, bb.",
        "Grr. Bebé, olvidala a ella, y ven conmigo, te hago ciberbebesbots.",
        f"{args.name} y {args.params}. Ya cansense. Si joden, comanse, no, ni comanse, vayan hagan un hijo.",
        f"Ñam ñam, ojala ustedes tú {args.name} y {args.params} fueran mis padres uwu",
        f"{args.name} y {args.params} son demasiado  goals para este mundo -w-"
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(ship),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def sonrojar(args, lenguaje):
    sonrojar = [
        f"{args.name} Se empezo a sonrojar levemente.. >//<",
        f"La carita de {args.name} se pone como un tomatito ///",
        f"{args.name} empieza a estrecerse y a ponerse rojito/a >u<",
        f"Se tapa la carita de lo sonrojado/a que esta, {args.name} o///o"
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(sonrojar),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def clorox(args, lenguaje):
    ruta = pwd("media/img/clorox")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)


def esquivar(args, lenguaje):
    ruta = pwd("media/img/esquivar")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)


def saludo(args, lenguaje):
    ruta = pwd("media/img/saludo")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    saludo = [
        "Hakuna matata 〜(^∇^〜）", "Holis -w-", "namasté ＼（＠￣∇￣＠）／",
        "salamu alaykum (︶ω︶)", "Hello!!! (｡^‿^｡)", "konichiwa (●⌒∇⌒●)",
        "-Beso en las dos mejillas- muak, muak (*≧▽≦)",
        "-Se besan en la boca como en la madre rusia- (*´°̥̥̥̥̥̥̥̥﹏°̥̥̥̥̥̥̥̥ )人(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥｀)",
        "-Chocan narizes- el aliento de la vida!! (((o(*ﾟ▽ﾟ*)o)))",
        "mano po!!", "-Se abrazan- (/□＼*)・゜ "
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(saludo),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def posar(args, lenguaje):
    ruta = pwd("media/img/posar")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)


def correr(args, lenguaje):
    ruta = pwd("media/img/correr")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)
    correr = [
        "Empieza a correr como gil", "Se fue",
        "Se corr.. Digo, se fue corriendo a por un cafesito>:3",
        "-c va lentamente-",
        "Empieza a correr super rapido... Nadie, lo detiene, sigue corriendo,empieza a correr.. Ya enserio, sal de tu casa y ve a correr de verdad. -w-",
        "Soy franshesco Virgo-lini y soy el autok ma rapidko del planita tirr4"
    ]
    message = {
        'chatId': args.chatId,
        'message': random.choice(correr),
        'messageType': 109
    }
    args.subclient.send_message(**message)


def hack(args, lenguaje):
    message = {'chatId': args.chatId, 'message': "...", 'messageType': 50}
    args.subclient.send_message(**message)


def youtube(args, lenguaje):
    def mecanismoPrincipal(msg):
        msg = msg['message']
        query_string = urllib.parse.urlencode({"search_query": str(msg)})
        html_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'watch\?v=(\S{11}',
                                    html_content.read().decode())
        result = 'https://youtu.be/' + search_results[0]
        message = {
            'message':
            "[CB][Video]: " + result + "\n\n\n[C]Aqui ta tu video >w<",
            'chatId':
            args.chatId,
            'embedLink':
            result,
            'embedContent':
            'Ravnin Contenido',
            'embedTitle':
            'Luego saco el titulo',
            'embedImage':
            upload(f'https://img.youtube.com/vi/{search_results[0]}/1.jpg')
        }

        try:
            args.sub_client.send_message(**message)
        except Exception as error:
            mensajesBot.mensajeError(error)

    msg = {'message': args.params}
    mecanismoPrincipal(msg)


def pokedex(args, lenguaje):

    link = "https://some-random-api.ml/pokedex?pokemon=" + args.params
    response = requests.get(link)
    json_data = json.loads(response.text)
    name = json_data["name"]
    ide = json_data["id"]
    especies = ', '.join(json_data["species"])
    habilidades = ', '.join(json_data["abilities"])
    tipo = ', '.join(json_data["type"])
    height = json_data["height"]
    weight = json_data["weight"]
    base_experience = json_data["base_experience"]
    gender = ', '.join(json_data["gender"])
    egg_groups = ', '.join(json_data["egg_groups"])
    stats = json_data["stats"]
    family = json_data["family"]
    evolutionLine = ', '.join(family["evolutionLine"])
    sprites = json_data["sprites"]
    description = json_data["description"]
    generation = json_data["generation"]

    message = {
        'chatId': args.chatId,
        'message': f"""[CB]猫 Welcome tø the ᐢ..ᐢ
[U]                                  ᝰPokedex ⏎
    𖥻  name: {name}
    —  id: {ide}
    𖥻  type: {tipo}
    —  species: {especies}
    𖥻  abilities: {habilidades}
    —  height: {height}
    𖥻  weight: {weight}
    —  base_experience: {base_experience}
    𖥻  gender: {gender}
    —  egg_groups: {egg_groups}

[CB]⿻ 𝘀𝘁𝗮𝘁𝘀 ഒ 

    —  hp: {stats["hp"]}
    𖥻  attack: {stats["attack"]}
    —  defense: {stats["defense"]}
    𖥻  sp_atk: {stats["sp_atk"]}
    —  sp_def: {stats["sp_def"]}
    𖥻  speed: {stats["speed"]}
    —  total: {stats["total"]}

[CB]⿻ 𝗳𝗮𝗺𝗶𝗹𝘆 ഒ

    —  evolutionStage: {family["evolutionStage"]}
    𖥻  evolutionLine: {evolutionLine}

[CB]⿻ 𝘀𝗽𝗿𝗶𝘁𝗲 ഒ

    𖥻  normal: {sprites["normal"]}
    —  animated: {sprites["animated"]}

    𖥻  description: {description}
    —  generation: {generation}""",
        'embedTitle': f"{name}",
        'replyTo': args.messageId,
        'embedImage': upload(sprites["normal"])
    }
    args.subclient.send_message(**message)


def youtubeComment(args, lenguaje):
    url = f"https://some-random-api.ml/canvas/youtube-comment?avatar={args.author.icon}&comment={args.params}&username={args.name}?key=AxFY2cclzlYWbeOrZXnsHpraT"
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "gif"
    }
    args.subclient.send_message(**message)


def loli(args, lenguaje):
    url = f"https://some-random-api.ml/canvas/lolice/?avatar={args.author.icon}?key=AxFY2cclzlYWbeOrZXnsHpraT"
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def wink(args, lenguaje):
    response = requests.get('https://some-random-api.ml/animu/wink')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "gif"
    }
    args.subclient.send_message(**message)


def hug_hug(args, lenguaje):
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "gif"
    }
    args.subclient.send_message(**message)


def background(args, lenguaje):
    file = upload(args.subclient.get_chat_thread(args.chatId).backgroundImage)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def pat(args, lenguaje):
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "gif"
    }
    args.subclient.send_message(**message)


def facePalm(args, lenguaje):
    response = requests.get('https://some-random-api.ml/animu/face-palm')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "gif"
    }
    args.subclient.send_message(**message)

# Animales
def panda(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/panda')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def redPanda(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/redPanda')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def fox(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/fox')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def dog(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/dog')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def cat(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/cat')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def racoon(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/racoon')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def birb(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/birb')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def koala(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/koala')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


def kangaroo(args, lenguaje):
    response = requests.get('https://some-random-api.ml/img/kangaroo')
    json_data = json.loads(response.text)
    url = json_data['link']
    file = upload(url)
    message = {
        'chatId': args.chatId,
        'message':...,
        'file': file,
        'fileType': "image"
    }
    args.subclient.send_message(**message)


# Funcion que permite al bot comportarse como un ChatBot en ingles y en español
def chat(args, lenguaje):
    translator = google_translator()
    translate_en = translator.translate(args.params, lang_tgt='en')
    args.params = ''.join(map(str, translate_en))
    args.params = args.params.strip("'")
    link = f"https://api.deltaa.me/chatbot?message={quote(args.params)}&gender=Female"
    response = requests.get(link)
    json_data = json.loads(response.text)
    chatbot = translator.translate(json_data["message"], lang_tgt='es')
    message = {
        'chatId': args.chatId,
        'message': f"{chatbot}",
        'replyTo': args.messageId
    }
    args.subclient.send_message(**message)


def chatSiri(args, lenguaje):
    translator = google_translator()
    translate_en = translator.translate(args.params, lang_tgt='en')
    args.params = ''.join(map(str, translate_en))
    args.params = args.params.strip("'")
    link = f"https://api.deltaa.me/chatbot?message={quote(args.params)}&gender=Female"
    response = requests.get(link)
    json_data = json.loads(response.text)
    chatbot = translator.translate(json_data["message"], lang_tgt='es')
    tts = gTTS(f"{chatbot}", lang='es')
    file = tts.save('audio.mp3')
    with open("audio.mp3", "rb") as file:
        message = {
            'chatId': args.chatId,
            'embedContent': 'I am alive.',
            'file': file,
            'fileType': "audio"
        }
        args.subclient.send_message(**message)


def chat_en(args, lenguaje):
    link = f"https://api.deltaa.me/chatbot?message={quote(args.params)}&gender=Female"
    response = requests.get(link)
    json_data = json.loads(response.text)
    chatbot = json_data["message"]
    message = {
        'chatId': args.chatId,
        'message': f"{chatbot}",
        'replyTo': args.messageId
    }
    args.subclient.send_message(**message)


# Comandos con virguilila
def virguilila_kiss(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message':
        f"<$@{args.name}$> besó apasionadamente a  <${args.params}$>...",
        'messageType': 109
    }
    args.subclient.send_message(**message)


def virguilila_ban(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message': f"{args.name} baneó del chat a {args.params}...",
        'messageType': 109
    }
    args.subclient.send_message(**message)


def virguilila_meter(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message':
        f"el Dios todo poderoso {args.name} va a desactivarme metiendome un {args.params}...",
        'messageType': 109
    }
    args.subclient.send_message(**message)


def virguilila_lick(args, lenguaje):
    message = {
        'chatId': args.chatId,
        'message': f"{args.name} le lame a {args.params}... >.<",
        'messageType': 109
    }
    args.subclient.send_message(**message)


def virguilila_hit(args, lenguaje):
    ruta = pwd("media/img/hit")
    file = str(random.choice(ruta))

    with open((file), "rb") as file:
        message_imagen = {
            'chatId': args.chatId,
            'message':...,
            'file': file,
            'fileType': "gif"
        }
        args.subclient.send_message(**message_imagen)

    message = {
        'chatId': args.chatId,
        'message':
        f"{args.name} empieza a darle puñetazos  {args.params}... >:D",
        'messageType': 109
    }
    args.subclient.send_message(**message)


# Comandos solo para administradores
def virguilila_strike(args, lenguaje):

    message = {
        'chatId': args.chatId,
        'message': f"{args.params}...",
        'messageType': 50
    }
    args.subclient.send_message(**message)


def leave(args, lenguaje):
    if args.profileId in admins:
        message = {'chatId': args.chatId}
        message_leave = {
            'chatId':
            args.chatId,
            'message':
            "[C]¡Gracias por tenerme en este chat, pero ya me tengo que ir a descansar! >w<"
        }
        args.subclient.send_message(**message_leave)
        args.subclient.leave_chat(**message)
    else:
        message = {
            'chatId': args.chatId,
            'message': "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
        }
        args.subclient.send_messag(**message)


def edit_nick(args, lenguaje):
    if args.profileId in admins:
        message = {'args.namename': f"{args.params}"}
        args.subclient.edit_profile(args.comId, message)
    else:
        message = {
            'chatId': args.chatId,
            'message': "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
        }
        args.subclient.send_messag(**message)


def ban(args, lenguaje):
    try:
        if args.profileId in admins:
            search = re.search("=", args.params)
            link_web = re.search("http://aminoapps.com/p/", args.params)
            if search:
                if link_web:
                    tmp = args.params.replace("http://aminoapps.com/p/", "")
                    tmp = re.split("=", args.params)
                    user = args.subclient.get_from_code(tmp[0]).objectId
                    staff = clienteAmino.get_community_info(args.comId).json
                    staff = staff["communityHeadList"]
                    staffList = []
                    for i in staff:
                        id = i["uid"]
                        staffList.append(id)

                    if user is not staffList:
                        ban = {'userId': user, 'reason': str(tmp[1])}
                        args.subclient.ban(**ban)
                        message = {
                            'chatId': args.chatId,
                            'message': "<$¡Usuario con ban con exito! owo'$>"
                        }
                        args.subclient.send_messag(**message)
            else:
                message = {
                    'chatId': args.chatId,
                    'message': "Esas usando el comando mal tontito/a -.-'"
                }
                args.subclient.send_message(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def warn(args, lenguaje):
    try:
        if args.profileId in admins:
            search = re.search("=", args.params)
            link_web = re.search("http://aminoapps.com/p/", args.params)
            if search:
                if link_web:
                    tmp = args.params.replace("http://aminoapps.com/p/", "")
                    tmp = re.split("=", args.params)
                    user = args.subclient.get_from_code(tmp[0]).objectId
                    staff = clienteAmino.get_community_info(args.comId).json
                    staff = staff["communityHeadList"]
                    staffList = []
                    for i in staff:
                        id = i["uid"]
                        staffList.append(id)

                    if user is not staffList:
                        warn = {'userId': user, 'reason': str(tmp[1])}
                        args.subclient.warn(**warn)
                        message = {
                            'chatId':
                            args.chatId,
                            'message':
                            "<$¡Usuario con advertencia con exito! owo'$>"
                        }
                        args.subclient.send_messag(**message)
            else:
                message = {
                    'chatId': args.chatId,
                    'message': "Esas usando el comando mal tontito/a -.-'"
                }
                args.subclient.send_messag(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def strike_user(args, lenguaje):
    try:
        if args.profileId in admins:
            search = re.search("=", args.params)
            link_web = re.search("http://aminoapps.com/p/", args.params)
            if search:
                if link_web:
                    tmp = args.params.replace("http://aminoapps.com/p/", "")
                    tmp = re.split("=", args.params)
                    user = args.subclient.get_from_code(tmp[0]).objectId
                    staff = clienteAmino.get_community_info(args.comId).json
                    staff = staff["communityHeadList"]
                    staffList = []
                    for i in staff:
                        id = i["uid"]
                        staffList.append(id)

                    if user is not staffList:
                        strike = {
                            'userId': user,
                            'reason': str(tmp[1]),
                            'time': 3
                        }
                        args.subclient.strike(**strike)
                        message = {
                            'chatId': args.chatId,
                            'message': "<$¡Usuario con falta con exito! owo'$>"
                        }
                        args.subclient.send_messag(**message)
            else:
                message = {
                    'chatId': args.chatId,
                    'message': "Esas usando el comando mal tontito/a -.-'"
                }
                args.subclient.send_message(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:

        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def bloquear(args, lenguaje):
    try:
        if args.profileId in admins:
            link_web = re.search("http://aminoapps.com/p/", args.params)
            if link_web:
                tmp = args.params.replace("http://aminoapps.com/p/", "")
                user = args.subclient.get_from_code(tmp).objectId
                message = {
                    'chatId': args.chatId,
                    'message': "<$¡Usuario bloqueado con exito! owo'$>"
                }
                args.subclient.send_message(**message)
                args.subclient.block(userId=user)
            else:
                message = {
                    'chatId': args.chatId,
                    'message': "<$¡Usaste el comando mal tontito! -w-$>"
                }
                args.subclient.send_message(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_message(**message)

    except Exception as error:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)
        print("error: ", error)


def desbloquear(args, lenguaje):
    try:
        if args.profileId in admins:
            link_web = re.search("http://aminoapps.com/p/", args.params)
            if link_web:
                tmp = args.params.replace("http://aminoapps.com/p/", "")
                user = args.subclient.get_from_code(tmp).objectId
                message = {
                    'chatId': args.chatId,
                    'message': "<$¡Usuario desbloqueado con exito! >:3$>"
                }
                args.subclient.send_message(**message)
                args.subclient.unblock(userId=user)
            else:
                message = {
                    'chatId': args.chatId,
                    'message': "<$¡Usaste el comando mal tontito! -w-$>"
                }
                args.subclient.send_message(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def edit_chat_view(args, lenguaje):
    try:
        if args.profileId in admins:

            if args.params is not None:
                message_verdadero = {
                    'chatId': args.chatId,
                    'message': "<$¡Ahora nadie puede leer el chat! uwu$>"
                }
                args.subclient.send_message(**message_verdadero)
            if args.params is None:
                message_falso = {
                    'chatId': args.chatId,
                    'message': "<$¡Ahora cualquiera puede leer el chat! uwu$>"
                }
                args.subclient.send_message(**message_falso)

            chat = {'chatId': args.chatId, 'viewOnly': args.params}
            args.subclient.edit_chat(**chat)
        else:

            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:

        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def edit_chat_content(args, lenguaje):
    try:
        if args.profileId in admins:
            chat = {'chatId': args.chatId, 'content': args.params}
            args.subclient.edit_chat(**chat)
            message = {
                'chatId': args.chatId,
                'message': "<$¡Contenido del chat cambiado! uwu$>"
            }
            args.subclient.send_message(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def edit_chat_clave(args, lenguaje):
    try:
        if args.profileId in admins:

            chat = {'chatId': args.chatId, 'keywords': args.params}
            args.subclient.edit_chat(**chat)
            message = {
                'chatId': args.chatId,
                'message': "<$¡Clave cambiado de chat cambiado! uwu$>"
            }
            args.subclient.send_message(**message)

        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def edit_chat_anuncio(args, lenguaje):
    try:
        if args.profileId in admins:

            chat = {'chatId': args.chatId, 'announcement': args.params}
            chat_pin = {'chatId': args.chatId, 'pinAnnouncement': True}
            args.subclient.edit_chat(**chat_pin)
            args.subclient.edit_chat(**chat)
            message = {
                'chatId': args.chatId,
                'message': "<$¡Anuncio cambiado de chat cambiado! uwu$>"
            }
            args.subclient.send_message(**message)

        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def edit_chat_pinAnnouncement(args, lenguaje):
    try:
        if args.profileId in admins:

            if args.params is not None:
                message_verdadero = {
                    'chatId': args.chatId,
                    'message': "<$¡Anuncio fijado del chat! uwu$>"
                }
                args.subclient.send_message(**message_verdadero)
            if args.params is None:
                message_falso = {
                    'chatId': args.chatId,
                    'message': "<$¡Anuncio desfijado del chat! uwu$>"
                }
                args.subclient.send_message(**message_falso)
            chat = {'chatId': args.chatId, 'pinAnnouncement': args.params}
            args.subclient.edit_chat(**chat)
        else:

            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def edit_chat_canInvite(args, lenguaje):
    try:
        if args.profileId in admins:

            if args.params is not None:
                message_verdadero = {
                    'chatId': args.chatId,
                    'message': "<$¡Ahora pueden invitar en el chat! uwu$>"
                }
                args.subclient.send_message(**message_verdadero)
            if args.params is None:
                message_falso = {
                    'chatId': args.chatId,
                    'message': "<$¡Ahora nadie puede invitar en el chat! uwu$>"
                }
                args.subclient.send_message(**message_falso)
            chat = {'chatId': args.chatId, 'canInvite': args.params}
            args.subclient.edit_chat(**chat)

        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:

        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def edit_chat_title(args, lenguaje):
    try:
        if args.profileId in admins:
            chat = {'chatId': args.chatId, 'title': args.params}
            args.subclient.edit_chat(**chat)
            message = {
                'chatId': args.chatId,
                'message': "<$¡Titulo cambiado de chat cambiado! uwu$>"
            }
            args.subclient.send_message(**message)
        else:
            message = {
                'chatId': args.chatId,
                'message':
                "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
            }
            args.subclient.send_messag(**message)

    except Exception:
        message = {
            'chatId':
            args.chatId,
            'message':
            "<$[C]¡Error, pon bien el comando tontito/a! -w-\n\n[C]Recuerda poner -help -comando para saber como usarlo uwu$>"
        }
        args.subclient.send_message(**message)


def burbuja(args, lenguaje):
    result = burbuja[args.params]
    if args.profileId in admins:
        message_buble = {'defaultBubbleId': str(result)}
        args.subclient.edit_profile(args.comId, message_buble)
        message = {
            'chatId': args.chatId,
            'message': "¡Tu burbuja de chat fue cambiada con exito! :3"
        }
        args.subclient.send_message(**message)
    else:
        message = {
            'chatId': args.chatId,
            'message': "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
        }
        args.subclient.send_messag(**message)


def edit_bio(args, lenguaje):
    if args.profileId in admins:
        message = {'content': f"{args.params}"}
        args.subclient.edit_profile(args.comId, message)
    else:
        message = {
            'chatId': args.chatId,
            'message': "Ño eres mi dueño, ¿Qué haces usando este comando? -.-'"
        }
        args.subclient.send_messag(**message)


# Arrays
categoriasComandos = [
    "-animales", "-entretenimiento", "-guion", "-invisible", "-ravnin",
    "-ayudante", "-acciones"
]

acciones = {
    #"-comment": commentUser,
    "-info": info,
    "-burbuja": burbuja,
    "-join": join,
    "-desaparece": desaparece,
    "-wiki": idWiki,
    "-loli": loli,
    "-gay": gay,
    "-id": id,
    "-biografia": edit_bio,
    "-name": edit_nick,
    "-confession": confession,
    "-kill": kill,
    "-hug": hug,
    "-saludo": saludo,
    "-esquivar": esquivar,
    "-pokedex": pokedex,
    "-audio": audio,
    "-like_comunidad": comunidadLike,
    "-img": img,
    "-casarse": casarse,
    "-panda": panda,
    "-redPanda": redPanda,
    "-racoon": racoon,
    "-kangaroo": kangaroo,
    "-koala": koala,
    "-wink": wink,
    "-nalgada": nalgada,
    "-facePalm": facePalm,
    "-pat": pat,
    "-patada": patada,
    "-ship": ship,
    "-coa": coa,
    "-anfi": anfi,
    "-sonrojar": sonrojar,
    "-correr": correr,
    "-love": love,
    "-kick": kick,
    "-birb": birb,
    "-cat": cat,
    "-chat_siri": chatSiri,
    "-fox": fox,
    "-mishi": mishi,
    "-snake": snake,
    "-pandaBaby": pandaBaby,
    "-random": randoms,
    "-anime": anime,
    "-rata": ratas,
    "-dormir": dormir,
    "-tr": traductor,
    "-chat": chat,
    "-siri": siri,
    "-leave": leave,
    "-kiss": kiss,
    "-cry": cry,
    "-dance": dance,
    "-coin": coin,
    "-aparece": aparece,
    "-comunidad": comunidad,
    "-quizz": playGame,
    "-speak": speak,
    "-strike": strike,
    "-purge": purge,
    "-lista": listaTrivia,
    "-hack": hack,
    "-chat_en": chat_en,
    "-background": background,
    "-creditos": creditos,
    "-youtubeComment": youtubeComment,
    "-everyone": everyone,
    "-youtube": youtube,
    "-dog": dog,
    "~panda": panda,
    "~hug": hug_hug,
    "-clorox": clorox,
    "-trivia": trivia,
    "-posar": posar,
    "~speak": speak_invicible,
    "~kiss": virguilila_kiss,
    "~ban": virguilila_ban,
    "~meter": virguilila_meter,
    "~lick": virguilila_lick,
    "~hit": virguilila_hit,
    "~strike": virguilila_strike,
    ".titulo": edit_chat_title,
    ".contenido": edit_chat_content,
    ".view": edit_chat_view,
    ".invitar": edit_chat_canInvite,
    ".anuncio": edit_chat_anuncio,
    ".fijar": edit_chat_pinAnnouncement,
    ".clave": edit_chat_clave,
    ".ban": ban,
    ".strike": strike_user,
    ".bloquear": bloquear,
    ".desbloquear": desbloquear,
    ".warn": warn,
    ".destacar": destacar,
}

burbuja = {
    'Thunder Cloud': '48a9620b-8dd6-43f8-ab01-eaeb3e5dd0fd',
    'Vial': 'a2ac6450-fcb5-463c-aa27-80edbce63c4c',
    'Cream Cookie': '87ad68cf-e50e-4191-afb4-30949219bcbc',
    'Churro': '8d56bfd0-5244-4678-88d2-a7179e414b4d',
    'Book': '1ccffff1-3bf3-4d3e-ae67-dd84443c493a',
    'Taco': 'c9f021c7-db2f-4ea1-9645-fc2f5c4d262f',
    'Galaxy': '3cec711f-a27e-4813-9514-7efa571eb163',
    'Monster': '0d9e6dda-8586-4943-8957-45b7e38597a0',
    'Robocat': '4aefe846-47c2-4f14-b278-a0c9072e5063',
    'Glitch': '654488a6-4e7e-4b0b-9c5f-5d1640538a1f',
    'Leaf': '832f3e2f-d6da-49e6-9a5e-d74bbd89ca78',
    'Salami': '7c42f72c-1c1a-4713-b6f2-e587c7d135e8',
    'Party': '1f80006b-5feb-4925-8f8a-212509331c4e',
    'Memphis': '2eccf68b-f8fd-4e42-b304-d3d9113efe34',
    'Paint Streak': 'f7daf8df-3b99-46be-9ffa-b3fc12f529ac',
    'Browser': 'c6af0bca-636e-44db-bc72-d22b91970cd5',
    'Camel': '39598cde-701a-46b9-812c-d46634b48ad0',
    'Burger': 'b4a0d2e9-05e9-404a-b074-738d1fb85071',
    'Grass': '0193277b-0415-4c66-a7be-906629df2861',
    'Chili': 'd07de212-f159-4609-8de0-8b1bafc1dde3',
    'Neon': '817c94af-9311-4856-b0a2-f02c031a09f5',
    'Cheese': 'e4b8ccc5-6575-4031-b680-58ca49f7c4ee',
    'Smart Phone': '0cd6efc7-f94d-4139-b414-d0f1990612d8',
    'Milk Jug': 'b5480f93-1880-4e34-a4a5-202f91094c31',
    'Duck': '2c6d5e56-7d28-4e03-87d1-bc8929d888c5',
    'Cauldron': 'ba63246f-90db-4166-b639-979fa24c7164',
    'Pencil': '8482f00f-f3f8-47f5-95a0-21f28da61234',
    'Skateboard': '46bcd1cc-8cd9-4b4b-badb-d70d0a30608a',
    'Snail': '8d2d2abc-91ea-4828-a277-38acae371de8',
    'Bunny': '8c65dbb3-3aac-484f-81e6-b6b779d9e79b',
    'Tortoise': '82b11c0d-726b-4d06-91e2-fa8b93f3726a',
    'Crown': '06e0fa38-ddab-4f08-aa7b-b7f6e8c11bf5',
    'Spare Change': 'fecfd35d-4a06-4c58-a588-31bf03af563b',
    'Planet': '71e750ef-992c-4e36-864b-fd6e379049eb',
    'Puddle': '636d3a9c-8dfc-4f91-82fc-6219349fae55',
    'Cardboard': 'ff1c7826-279b-47e3-a387-6bd52b3ee7e4',
    'Chocolate Bar': 'c6633c06-8585-4cc8-b402-983c5affb64d',
    'Love Letter': 'c9d68fcf-93d9-465f-b5d1-9611ca79213b',
    'Comics': 'd3b014d1-2fc9-460a-bf7e-94a00db6a549',
    'Coffee': 'a8bab9af-cad0-4103-9f89-e0dfe6303667',
    'Reindeer': 'b1b42225-f76a-49aa-8055-0171a9f91284',
    'Gift': '61eb6146-0263-4ffd-ba0f-942e567b0953',
    'Stocking': '5f07df1d-61c5-4ce4-83d3-1e6ae0cb26cd',
    'Snowman': '5b6f3f26-498f-4776-94a7-dcae221820d6',
    'Maki': '0fd88590-9af7-4484-b4f6-a4160bf5e02e',
    'Egg': '1deebeec-302a-45d6-b135-990d986b6b49',
    'Black Cat': '0c3917a9-f804-4c40-a703-0c14535bb4c1',
    'Pumpkin': '384ac1b6-85c0-49a1-8135-b6368a5e73be',
    'Ghost': 'b78ad22b-4da6-49d7-a38e-1ddaaf9bf608',
    'Vampire Fangs': 'bfcbd1fe-be4d-404a-a669-393c590d9531',
    'TV': 'c26fc182-07cd-4818-837c-dfac3308514b',
    'Picture Frame': 'f83337a0-4383-4935-bb09-633dc29f89d3',
    'Toast': 'd5e067f0-8e51-4bc4-9e86-ab6a5124543f',
    'Pixel': 'fd95b369-1935-4bc5-b014-e92c45b8e222',
    'Meat': '5eaba40c-b081-4649-a5b3-b9e9eac05618',
    'Pop Art 3': '339ccdd5-a321-457b-a756-74cc5888a052',
    'Hipster Plaid': 'f6d62ae1-8c34-4812-b185-d033199022e2',
    'Comeback Bubble': 'cb614c73-9823-4ae6-922c-797ca477a37d',
    'Rain Boot': '690ac950-9543-4f89-8af6-c5ff4dd63d93',
    'Pig': '40fdfa29-1422-41ae-af7d-19c7098527dd',
    'Lumberjack Plaid': 'b96f1f52-a9f7-48a1-8724-5d9290ff969d',
    'Pop Art 2': 'd5fb317c-2cd3-4bcb-8b41-5e47764a1c35',
    'Cloud': '62af12a8-c394-42de-a28c-e04478508849',
    'A Boat': 'a3b8e34f-5a0a-4f2f-99de-d2772d23bf86',
    "It's Orange": '8b88133e-7abd-45da-b9c4-9055870b7145',
    'Penguin': '28377fb3-aee2-43bc-abcf-95bec8db19d0',
    'Soda Can': '05b7cb37-31ba-4b97-b767-be9b7c37f63b',
    'Tooth': '93713c10-3b20-414c-8fbf-d8061a3c603c',
    'Watermelon': 'aeca597c-2cc8-45ff-b6c2-df0d022a5f52',
    'Knife': '74a02e4f-c6c6-4e51-a29c-c6cd8bff4fa6',
    'Feather': 'cc2b76ca-16f8-4c8d-93fd-7dc24d132c06',
    'Pop Art': '51f51b15-9802-47ca-99c7-01dfb7475699',
    'TP': 'ce7c7fdf-d625-456f-b6e8-c856f2a44213',
    'Pride': 'dae946ad-08ca-45dc-b7e2-8c2929ba4e32',
    'Ruby': '4661c167-cc3b-4321-897a-8ffc67587a3d',
    'Frog': 'fc869158-6d2f-4124-a48b-a61cefc3d663',
    'Log': '1cfa6a74-fa5d-46ab-bfcf-13fa3dc4fa58',
    'Slime': 'db898cd5-c925-44e4-a764-63bb39212fa3',
    'Retro PC': '5df838da-1816-40a3-87c6-c85ed5bd8920',
    'Butter': '85045ed8-b05b-40de-907e-ec886889d086',
    'Cactus': 'bfe1a6fe-1b40-4535-a90e-5863f9cca231',
    'Original Plaid': '4ec27e32-163e-4ac2-a0ec-73d20f1f32d3',
    'Prism': 'd88643d8-c932-4bf7-86f6-a2c102f4955c',
    'Anime': '036d33b8-e995-4211-b435-414c60ee8fc1',
    'Whale': '51ed2ea0-957b-4fb3-bed5-01fff68dde9b',
    'Hot Dog': '9b4412a8-30e8-4a26-9622-92934ef1c931',
    'Pink Cloud': '4c2d0076-8812-4023-be6a-68146bdae66d',
    'Tea Time': '6001cf5a-9bdc-46ad-9116-1c80615b3e5d',
    'K-Pop': 'a5a427cb-2ee8-4ec4-90e3-ccf5bd0b665b',
    'Scroll': '8170e7bf-4289-4609-89bd-9fad7a6de4bd',
    'Balanced Breakfast': 'de9852ea-179c-4cee-9745-ba2ca61ebd09',
    'Spring': 'b468602e-a43e-41e3-92ec-cfcc3c5028fd',
    'Scream': 'c0534cb2-b40b-4a47-a4c0-1fcf84658015',
    'Suave': '0ecb533d-952f-4a24-ab82-d96462cd3efe',
    'Odd Friend': '250ca460-0f4e-420f-bcac-ec7e9d7eb3a6'
}


sticker_anime = [
    'aea3d4b5-fd7c-4121-9317-97f3967939f2',
    '56e29514-b7a2-4f7b-b8f5-638cd6150500',
    'd5d28718-6e21-450e-9e6a-66f9c3ff751c',
    'fbc8bcf6-5d96-4077-bf9c-8e716dfba6d2',
    '2053be46-8675-4d60-8fdc-5dcc67a56eba',
    '9c4f0f35-64df-4cf3-b455-65a71d862f9d',
    '16f9080d-db47-4ce6-94d3-f4bfef89fe38',
    '9d419f35-a372-4b8e-8064-1907e73565b7',
    '29287049-f00e-4cbd-bdd7-fec9918f0408',
    '118eeb8c-4455-4fb9-bc0d-3914626a65d4',
    '345ffa25-0d6f-4155-bf49-724622f251b0',
    'bb3de1e3-1896-47eb-9d7b-fbd33be142d7',
    '9435a684-ad31-4ca1-b46b-312c1b01f687',
    'dc79f470-d8f6-49c6-9bf1-349ba3581450',
    'da8e50de-376c-4a71-975d-b4843beb8b9f',
    '63556682-88c5-47f2-96c0-4092eabf20f4',
    '7345b766-42bc-4538-bf02-fb3840c944b7',
    '73001b6b-388b-4135-ac54-13f9387b5905',
    'a6bf3721-c715-4fea-9859-54ed885018c6'
]

sticker_snake = [
    '6dfe0418-6802-4130-ae2c-8657f9fab7f4',
    '827ae652-2ff1-4b07-92f1-a10e8a641cc8',
    '884e1a95-7c6c-46bc-b7bf-c101abfed060',
    '961b2cb2-37a2-4f59-acf5-61c5add5a6f1',
    '39426ab7-c1bb-48f4-ad7a-d7073f43ddf1',
    '82ff8542-9cbb-48b8-a20e-d8ad65088ce6',
    'ed91af21-bc2b-46bf-a4db-c5960ba2c9fc',
    '6481aacb-decb-4dc6-896b-80dc41a7bf94',
    '181a1520-dd95-4560-bafd-d510bcf399ad',
    'fcda6228-8394-4767-b876-3bf694490246',
    '40f3487d-759c-4bf3-b9f4-721bb4a6063d',
    '8b3f22dc-7c7b-4378-bc97-e2800cfa6746',
    '5beccb1e-6a63-426c-8ee0-d24717d55a00',
    '9bbb17b4-36c5-4400-9844-48e84c773449',
    '8db2a943-cfa6-4cc6-b31f-fdcfa91e299c',
    '962981df-0913-4bf0-9ede-fda36d765ac5',
    '3d0c4d2e-3830-4645-8963-63c0f51f6b7d',
    'cbc00b4f-5373-47f6-beeb-b8a167a05944',
    'a515aa62-a87b-4675-86f5-bcbccbd29725',
    'b1b06fee-4de2-445c-bb38-4083c7b8fc98',
    'fe62b033-a826-47da-bc8f-388f885866c6',
    'b498e0c9-6fcf-464c-8edb-eb2cb422d581',
    'e730a688-ed00-444c-b6e6-9e0e9679f105'
]

sticker_meme = [
    '6612dd76-4316-4fb8-99c8-96525be99f78',
    'e86578c6-5e72-4a99-ad71-300c07fdcccd',
    'ed224cb6-b725-4f44-aee7-ea895ad86fb2',
    '9ead30f4-8592-40a4-b305-31ff238fbe19',
    'd9b34728-63e0-489b-a957-ff315f169d55',
    '4d0f102d-16de-403c-b831-819e7ef39119',
    'ba0dfe59-94e5-4b24-a76e-97826352fb52',
    '2d8d6c63-2868-4a84-a14a-2ea22add64c5',
    '1dde0fbd-0366-4c29-b9b4-85ab763a35bb',
    '2a584a12-2c79-4b8e-9e9f-81a8d0bf5e5e',
    'b126fd02-97d4-43f3-a313-67454c7c95c3',
    '5dbac28c-d5a2-4f98-9d53-f73f0bc009f3',
    'beaf4ba5-ecd6-4fef-a924-96675695e9b5',
    '06ffa137-01e8-4d1f-af8a-4a0b035e10a2',
    'e34895fa-073b-4077-9d38-c322be9923e4',
    'e19a9ff7-3cc8-491e-83b5-f0adff11ae30',
    '56a9f7f1-a03b-4e7b-98b5-95264790a45c',
    'c29859d7-1a2e-4eb9-ba10-9fe062672f02',
    '1358950a-5a78-48b6-bde1-9cc7161c8156',
    'acf598bf-1f8b-4895-9b71-76cc32da02c7',
    '79788599-bf36-497d-b502-572021b2a18b'
]

sticker_pandas = [
    'b62af73c-9db4-4eaf-a6f3-8f657535bc41',
    '1adbd4e4-1f96-4344-9957-b171ce90d4d6',
    '9e1811c5-4e9a-41e0-9a50-673e8c32aa13',
    '9e68d899-53f2-482e-90b0-afb9a1af3a11',
    '863f7c91-7b90-4e20-8e6e-4be5f25ee1cd',
    '180fa9b8-d6d0-4574-9604-3b849ad096d5',
    '0b465450-0124-4fda-aa4c-638e6de9551d',
    'f1708772-d865-49cc-a9f4-7d507a2500f4',
    '7af62a61-c04b-4de7-bca8-233d145bc435',
    'f7433d0c-de65-41cb-a8e0-4b950b4522b8',
    'f538ad4c-8348-4964-95b1-2d945d40d31b',
    '4f5e5b4c-70d4-427e-b1c6-3c37327cb7c8',
    '3f5b50b6-56df-4f76-b0d3-75c85a16224e',
    '40e005cb-6c93-4840-81de-08a91cc72f82',
    'f87770f8-e2de-4094-8623-57e7d7cb0286',
    '6f2a2d4a-2965-48f0-9024-37fd85a13577',
    'cd59f20d-ddd0-4f07-94a8-fa598c4a7d8d',
    'fd50f9c8-d9af-4a90-b99c-f34c93640237'
]

sticker_ratas = [
    'd89907e1-6047-4608-a5e6-2af2be49fc55',
    'd7853ae9-88fa-40cc-886d-ff9603772f6f',
    'b5ac88c5-ee37-4bc8-bdfc-947da76ee8a5',
    '8d8e5358-4fcb-40a6-94d9-2f1e1efd08c1',
    '7dd46f2c-f03e-4e88-b2ab-b6f5a21bc5ce',
    'f03d7970-c5e2-4463-8c6a-d43db9d90482',
    'c39e908a-52c3-41ba-9156-914e789ed482',
    '8f2f3b34-e210-4743-93bc-eb8b02b56f92',
    'd2db9fc5-87ce-46f8-a482-8443e07bef87',
    'b6ca42b8-f22e-481b-a16f-2c25c2ec7efa',
    '2f807d47-4e78-40c6-9641-a2faa8d44b1e',
    'bfb46c2b-8433-4266-b7dd-bfcfef65a560',
    'cd792bf9-a2f8-4139-8fb7-e65e66b7efb4',
    '1de47cbd-2ac5-446f-a85d-85f5aea3f0f6',
    '8daf524f-7d4b-418b-a9ce-d1a22394d040',
    'cd532e9d-3504-459a-8033-936dbf16ae7f',
    'e09dbd90-78a1-41f8-87b6-db0e03d4e569',
    'e549fe06-c955-435e-accc-5bd4bc881e36',
    '467bbb50-bef3-4590-8c64-8d033c8c4ebe',
    '889ddd5e-5bb3-40f2-a4d3-4763078c34ee',
    '57a94e1f-9332-4d35-9b6a-1cdd911d13c4',
    '60bc1b6d-5e9f-4b17-b0fb-a1308b9beb27',
    'c07dd553-3174-4d77-8851-fc1912bc2b69',
    '6cda2a1a-5db3-4f05-a153-0f71341a3f88',
    '73afb29d-7486-4cf4-a3f1-bc0ff27eac05',
    '058ae8d5-9107-46a6-b3b4-2d9722d82245',
    '48061515-bd3b-4988-8025-c234d9b88610',
    'c697b72a-1c20-493e-93bd-263932ed4fa5',
    '54cd3ee5-c6bd-4926-bdce-78105e9e256a',
    '3abdcaff-c980-46ef-b0ad-c6ea27b15318',
    '4cbb7752-ad20-4d25-a8b4-c63a8d079636',
    '0d0393d0-c2f4-4215-8490-a0e146272d89',
    'b8c9b41d-8fc3-4631-84b8-d49029331539',
    '6eb92db8-9d0d-41ef-bb61-e9d7727ad4ec',
    '2bd8bb34-45ae-491b-b06c-1da30c855020',
    '69e7f12d-98d9-4324-b1bd-c46f875a9826',
    'fc0ac70e-f838-4f04-8c80-2a3e00054a6d',
    'd90b5aa7-5c9b-40c3-b9d2-9ae7bfad542d',
    'c1c2d47c-e8f3-4570-ac92-4d0419ad6829',
    'f0160959-4330-461b-991b-abae9b252ee7',
    '2bd051b1-d41b-47b4-8e4e-e619886843c7',
    '45a0dc87-6141-4090-93f3-690f70c85272'
]

sticker_mishi = [
    'bb58cab2-3b26-47dd-a904-275ca37a61e6',
    'c31c5ab1-ab49-4523-9385-e8079400427d',
    '298a2359-6184-454d-9ac1-5f95cd3ded12',
    '015fcd98-2a9c-460c-885d-91ca7d8a3b29',
    'c7323ae5-c875-4123-b3cb-eff01a22cf0f',
    '01b8754d-54c9-48a3-90a6-3a2267004cd9',
    'e19f5ebe-685e-4203-b49f-27372f781c3d',
    'ddf596a2-98a7-4498-bde2-ec1df317ba21',
    '9027509d-b065-4111-8512-cdb31118e75f',
    '5cf7eea9-50a2-4078-837c-e37d8dc1f2f7',
    '979a2acd-5e9b-4e1b-8db6-1482f6854517',
    '294b1563-511d-4a19-8c41-a2385dd5cb9d',
    '9dfe65fe-6be3-40d7-b97c-bc64b3fdf892',
    'b90f3c52-1b94-4088-a44f-c0707971e99a',
    '7bff9fad-0b17-4dfe-81cb-09cb9b48f058',
    '163dac06-75f3-403d-acdf-db5a9af00d44',
    '42a1a040-f39d-445b-baea-c4ec08487410',
    'a865a788-77c4-452d-a636-8908215ec41d',
    'ac70a4c8-192b-468f-b25e-f1374101f491'
]
