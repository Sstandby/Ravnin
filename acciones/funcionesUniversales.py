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

import requests, re
from datos import credenciales
from mensajes import mensajesBot
import amino
from os import scandir, getcwd
from os.path import abspath
from io import BytesIO

# Variables
clienteAmino = amino.Client()

correo = credenciales.Usuario.correo
clave = credenciales.Usuario.clave

admins = [
    "c0884d27-5f07-4579-92bf-782563080c16",
    "bb8a21db-3c02-4848-960c-53691b716858",
    "1085f2b5-e314-4a25-9b7a-9fd67fbfd36d",
    "0aef6265-e4a0-42e9-9ff9-3b7e348a75f2",
    "b515fd6b-30a1-410d-9850-da25aa6754ed",
    "f53a515a-f10e-4578-a0e9-367ad118db7b"
]

wikis = {}

#Cliente Ravnin
class ravnin:
    __slots__ = ("subclient", "chatId", "profileId", "author", "content",
                 "messageId", "params", "name", "comId")

    def __init__(self, data, subclient, params):
        self.subclient = subclient
        self.chatId = data.message.chatId
        self.profileId = data.message.author.userId
        self.name = data.message.author.nickname
        self.author = data.message.author
        self.content = data.message.content
        self.messageId = data.message.messageId
        self.params = params
        self.comId = data.comId

    def join_chats(self):
        if re.search("http://aminoapps.com/p/", str(self.params)):
            messageId = self.params.replace("http://aminoapps.com/p/", "")
            ide = self.subclient.get_from_code(messageId).objectId
        else:
            ide = self.subclient.get_from_code(str(self.params)).objectId
        try:
            self.subclient.join_chat(ide)
        except Exception as error:
            mensajesBot.mensajeError(error)

    def join_community(self):
        try:
            id = clienteAmino.search_community(self.params).comId[0]
            clienteAmino.join_community(id)
        except Exception as error:
            mensajesBot.mensajeError(error)

    def play_quiz(self, quizzId=str):
        questions_list = []
        answers_list = []
        quiz_info = self.subclient.get_blog_info(quizzId).json
        questions = quiz_info["blog"]["quizQuestionList"]
        total_questions = quiz_info["blog"]["extensions"][
            "quizTotalQuestionCount"]
        for x, question in enumerate(questions, 1):
            print(
                f"[quiz][{x}/{total_questions}]: Choosing the right answer...")
            question_id = question["quizQuestionId"]
            answers = question["extensions"]["quizQuestionOptList"]
            for answer in answers:
                answer_id = answer["optId"]
                self.subclient.play_quiz(quizId=quizzId,
                                         questionIdsList=[question_id],
                                         answerIdsList=[answer_id])
                latest_score = self.subclient.get_quiz_rankings(
                    quizId=quizzId).profile.latestScore
                if latest_score > 0:
                    print(f"[quiz][{x}/{total_questions}]: Answer found!")
                    questions_list.append(question_id)
                    answers_list.append(answer_id)
        for i in range(2):
            try:
                self.subclient.play_quiz(quizId=quizzId,
                                         questionIdsList=questions_list,
                                         answerIdsList=answers_list,
                                         quizMode=i)
            except amino.exceptions.InvalidRequest:
                pass
        self.subclient.send_message(
            chatId=self.chatId,
            message=
            f"[C]Mi Score de Quizz: <${self.subclient.get_quiz_rankings(quizId=quizzId).profile.highestScore}$> >:3"
        )

    def search_users(self, nombre=str):
        try:
            result = self.subclient.search_users(nombre)
        except Exception as error:
            mensajesBot.mensajeError(error)
        return result


#guardar informacion sacada de las wikis (BASE DE DATOS DENTRO DE AMINO WTF)


class wiki():
    def __init__(self, bienvenida, despedida, help):
        self.leave = None
        self.join = None
        self.lista_negra = None
        self.userBlock = None
        self.mensajeAyuda = None
        self.join_wiki = None
        self.leave_wiki = None
        self.mensajeAyuda_wiki = None
        self.despedida = despedida
        self.bienvenida = bienvenida
        self.ayuda = help
        block = clienteAmino.get_blocked_users(size=100).json
        userBlock = []
        for i in block:
            uidBlock = i["uid"]
            userBlock.append(uidBlock)
        self.lista_negra = userBlock
        self.mensajeAyuda_wiki = wikis.get(self.ayuda,
                                           wiki_content(self.ayuda))
        self.leave_wiki = wikis.get(self.despedida,
                                    wiki_content(self.despedida))
        self.join_wiki = wikis.get(self.bienvenida,
                                   wiki_content(self.bienvenida))
        if self.join is not self.join_wiki:
            self.join = self.join_wiki
        if self.leave is not self.leave_wiki:
            self.leave = self.leave_wiki
        if self.mensajeAyuda is not self.mensajeAyuda_wiki:
            self.mensajeAyuda = self.mensajeAyuda_wiki


def wiki_content(ide):
    subclient = amino.SubClient(comId="8150137", profile=clienteAmino.profile)
    wiki = subclient.get_wiki_info(wikiId=ide).json
    result = wiki["item"]["content"]
    wikis[ide] = result
    return result


def mensajeLogin():
    mensajesBot.mensajeAutor()
    clienteAmino.login(correo, clave)


def pwd(ruta=getcwd()):
    return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file()]


def upload(url):
    link = requests.get(url)
    result = BytesIO(link.content)
    return result
