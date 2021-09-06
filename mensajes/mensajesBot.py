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

import os


def limpiarPantalla():
    if os.name == "posix":
        return os.system("clear")
    else:
        return os.system("cls")


def mensajeAutor():
    limpiarPantalla()
    print("""
          ("`-/")_.-'"``-._
          . . `; -._    )-;-,_`)
          (v_,)'  _  )`-.\  ``-'
          _.- _..-_/ / ((.'
      ((,.-'   ((,/   By- Standby.
      """)


def mensajeBienvenida():
    limpiarPantalla()
    print("""
        ,/|         _.--''^``-...___.._.,;
        /, \'.     _-'          ,--,,,--'''
        { \    `_-''       '    /})
        `;;'            ;   ; ;
    ._.--''     ._,,, _..'  .;.'
    (,_....----'''     (,..--''

        ¡Bienvenido mortal, puedes probar de este maravilloso bot! Pero recuerda, es una prueba, ¿Te gusto? ¡Compralo y estara 24/7!
    """)


def mensajeError(error):
    print(f"\n[Ocurrio un error inesperado]→ {error}\n")


def mensajeAyuda_animales():
    animalesAyuda = open(
        "mensajes/mensajesAyuda/mensajesAyuda_Categorias/aminoAyuda_animales.txt",
        "r")
    aminoAyuda_animales = animalesAyuda.read()

    return aminoAyuda_animales

def mensajeAyuda_acciones():
    accionesAyuda = open(
        "mensajes/mensajesAyuda/mensajesAyuda_Categorias/aminoAyuda_acciones.txt",
        "r")
    aminoAyuda_acciones = accionesAyuda.read()

    return aminoAyuda_acciones

def mensajeAyuda_ayudante():
    animalesAyudante = open(
        "mensajes/mensajesAyuda/mensajesAyuda_Categorias/aminoAyuda_ayudante.txt",
        "r")
    aminoAyuda_ayudante = animalesAyudante.read()

    return aminoAyuda_ayudante

def mensajeAyuda_entretenimiento():
    entretenimientoAyuda = open(
        "mensajes/mensajesAyuda//mensajesAyuda_Categorias/aminoAyuda_entretenimiento.txt",
        "r")
    aminoAyuda_entretenimiento = entretenimientoAyuda.read()

    return aminoAyuda_entretenimiento


def mensajeAyuda_guion():
    guionAyuda = open(
        "mensajes/mensajesAyuda/mensajesAyuda_Categorias/aminoAyuda_guion.txt",
        "r")
    aminoAyuda_guion = guionAyuda.read()

    return aminoAyuda_guion


def mensajeAyuda_ravnin():
    ravninAyuda = open(
        "mensajes/mensajesAyuda/mensajesAyuda_Categorias/aminoAyuda_Ravnin.txt",
        "r")
    aminoAyuda_ravnin = ravninAyuda.read()

    return aminoAyuda_ravnin


def mensajeAyuda_invisible():
    virguililaAyuda = open(
        "mensajes/mensajesAyuda/mensajesAyuda_Categorias/aminoAyuda_virguilila.txt",
        "r")
    aminoAyuda_virguilila = virguililaAyuda.read()

    return aminoAyuda_virguilila


def mensajeAyuda_everyone():
    return """[CB]everyone:
[C]Este comando es para llamar a todos los del chat. Usalo bien y recuerda tener cuidado, te pueden funar. Solo usalo en caso de emergencia y de actividad. ! >w<
[c]
[CB]Uso: -everyone mensaje"""


def mensajeAyuda_id():
    return """[CB]id:
[C]
[C]Esto es para tener el ID de dicho chat.
[C]
[CB]Uso: -id"""


def mensajeAyuda_siri():
    return """[CB]siri:
[C]
[C]Este comando es igual que -speak, pero en vez de texto te lo dice con una voz >:3
[C]
[CB]Uso: -siri mensaje"""


def mensajeAyuda_gay():
    return """[CB]gay:
[C]
[C]Te dira que tan gay eres, muak. uwu
[C]
[CB]Uso: -gay"""


def mensajeAyuda_kick():
    return """[CB]kick:
[C]
[C]Este comando le dara una patada al usuario que quieras sacar. uwu
[C]
[CB]Uso: -kick usuario"""


def mensajeAyuda_strike():
    return """[CB]Strike:
[C]
[C]Este comando solo funciona si soy lider rewer
[C]
[CB]Uso: -strike mensaje"""


def mensajeAyuda_coin():
    return """[CB]coin:
[C]
[C]Lo mas emocionante, lo mas perverso, lo mas adrelaniña, es apostar!!! Recuerda pagar si pierdes.>:3
[C]
[CB]Uso: -coin"""


def mensajeAyuda_leave():
    return """[CB]leave:
[C]
[C]¡Este comando quitara a tu bot del chat!
[C]
[CB]Uso: -leave"""


def mensajeAyuda_like_comunidad():
    return """[CB]like_comunidad:
[C]
[C]¡Pondre esta comunidad en mi perfil global! :3
[C]
[CB]Uso: -like_comunidad"""


def mensajeAyuda_anfi():
    return """[CB]anfi:
[C]
[C]¡Sere tu anfi del chat! >:3
[C]
[CB]Uso: -anfi"""


def mensajeAyuda_coa():
    return """[CB]coa:
[C]
[C]¡Sere tu anfi del chat! Es decir si soy coa y usas este comando me volvere anfitrion. >:3
[C]
[CB]Uso: -coa"""


def mensajeAyuda_chat():
    return """[CB]chat:
[C]
[C]¡Este comando quitara es para hablar conmigo! -w-
[C]
[CB]Uso: -chat mensaje
[C]
[C]Si quieres saber el info de chat-en usa: -help -chat_en :3"""


def mensajeAyuda_chat_siri():
    return """[CB]chat-en:
[C]
[C]¡Escucha esta voz setsual mia al responderte a lo que me digas! -w-
[C]
[CB]Uso: -chat-siri mensaje"""


def mensajeAyuda_chat_en():
    return """[CB]chat-en:
[C]
[C]¡Este comando quitara es para hablar conmigo en inglés! -w-
[C]
[CB]Uso: -chat-en mensaje
[C]
[C]Si quieres saber el info de chat-siri usa: -help -chat_siri :3"""


def mensajeAyuda_tr():
    return """[CB]traductor:
[C]
[C]¿Qué eres bruto con los idiomas? ¡Ño te preocupes, sho te ayudo! 😋
[C]
[CB]Uso: -tr mensaje"""


def mensajeAyuda_purge():
    return """[CB]Purge:
[C]
[C]Elimino los mensajes que quieras, solamente si me haces lider o curador ;3
[C]
[CB]Uso: -purge 3"""


def mensajeAyuda_fondo_bot():
    return """[CB]Fondo:
[C]
[C]Esto pondra un fondo en la cuenta del bot.
[C]
[CB]Uso: -fondo_bot link de la imagne.jpg"""


def mensajeAyuda_icon_bot():
    return """[CB]icon perfil:
[C]
[C]Esto pondra un icon en la cuenta del bot.
[C]
[CB]Uso: -icon_bot link de la imagne.jpg"""


def mensajeAyuda_burbuja():
    return """[CB]icon perfil:
[C]
[C]Esto pondra una burbuja a tu bot.
[C]
[CB]Uso: -burbuja Nombre de la burbuja
[C]
[C]Para sabre el nombre de la burbuja poner:
[C]
[CB]Uso: -burbujas"""


def mensajeAyuda_confession():
    return """[CB]confession:
[C]
[C]Ve a mi priv, y pon una confesion para un usuario que ames mucho >w< o odies mucho, y se lo hare llegar tu mensaje [Todo anonimamente] -n-.
[C]
[CB]Uso: -confession linkdelusuario = mensaje
[C]
[CB]Uso: -confession mensaje"""


def mensajeAyuda_audio():
    return """[CB]audio:
  
[C]¿Quieres escuchar mi voz? owo
[C]
[CB] -audio """


def mensajeAyuda_comunidad():
    return """[CB]audio:
  
[C]Este comando hara que vaya a una comunidad mediante un link ywy
[C]
[CB]Uso -comunidad link de la comunidad"""


def mensajeAyuda_pokedex():
    return """[CB]pokedex:
  
[C]¡Te dare toda la info de tu pokemon favorito! OwO
[C]
[CB]Uso: -pokedex nombre del pokemon"""


def mensajeAyuda_pat():
    return """[CB]pat:
  
[C]Te daran un pat en la cabezita uwu
[C]
[CB]Uso: -pat"""


def mensajeAyuda_info():
    return """[CB]info:
  
[C]Tiene dos usos, uno para saber tu info y el otro es para saber la del otro usuario. uwu
[C]
[CB]Uso: -info
[C]
[C]El otro uso que le pueden dar es poniendo:
[C]
[CB]Uso: -info @Usuario"""


def mensajeAyuda_facePalm():
    return """[CB]facePalm:
  
[C]AY DIUS MIU
[C]
[CB]Uso: -facePalm"""


def mensajeAyuda_quizz():
    return """[CB]quizz:
[C]
[C]Resolvere cualquier quizz que me pidas.. -w-
[C]
[CB]Uso: -quizz http/aminoapps.com/linkdelquizz"""


def mensajeAyuda_wink():
    return """[CB]wink:
  
[C]Guiño guiño codo codo ;3
[C]
[CB]Uso: -wink"""


def mensajeAyuda_img():
    return """[CB]audio:
  
[C]¿Quieres ver mi pack...de media/img? owo
[C]
[CB]Uso: -img"""


def mensajeAyuda_kiss():
    return """[CB]kiss:
  
[C]Es un comando para besar apasionadamente aun usuario 7u7
[C]
[CB]Uso: -kiss user"""


def mensajeAyuda_kill():
    return """[CB]kill:
  
[C]¡Este comando le da K'O a su oponente enseguida! D':
[C]
[CB]Uso: -kill user"""


def mensajeAyuda_hug():
    return """[CB]hug:
  
[C]Este comando le dara un gran abrazo >w<
[C]
[CB]Uso: -hug user"""


def mensajeAyuda_comment():
    return """[CB]comment:
  
[C]Este comando te comenta tu muro y de un usuario que prefieras, todo anonimante, pero recuerda, ¡Un gran poder es una gran responsabilidad!.
[C]
[CB]Primer uso, comentar en tu muro: comment MENSAJE
[C]
[CB]Segundo uso, comentar en el muro de otra persona: comment @Usuario = mensajeAutor

Donde es mensaje ponen lo que quieran, y en usuario deben poner el nick del usuario qué esta en el chat. (Recuerden poner el = sino no va a funcionar. Tenkiuuu >w<"""


def mensajeAyuda_virguilila_kiss():
    return """[CB]kiss:
[C] 
[C]Beso fantasma <3
[C]
[CB]Uso: ~kiss user"""


def mensajeAyuda_virguilila_meter():
    return """[CB]meter:
  
E-esto... Es para meter cosas.."""


def mensajeAyuda_virguilila_hug():
    return """[CB]hug:
[C]
[C]Abachooooooooooo >:3
[C]
[BC]Uso: ~hug"""


def mensajeAyuda_virguilila_ban():
    return """[CB]ban:
  
[C]ban fantasma >:l
[C]
[CB]Uso: ~ban user"""


def mensajeAyuda_strikes():
    return """[CB]strike:
  
[C]Este comando...da strikes (?) 
[C]
[CB]Uso: -strike"""


def mensajeAyuda_join():
    return """[CB]join:
  
[C]Este comando es para unirme a tu chat nwn
[C]
[CB]Uso: -join linkdelchat """


def mensajeAyuda_virguilila_lick():
    return """[CB]lick:
  
[C]Este comando es para empezar a lamerte >u<
[C]
[CB]Uso: ~lick manzana """


def mensajeAyuda_virguilila_speak():
    return """[CB]lick:
  
[C]Primo de speak, o sea dira todo lo que tú quieras de forma invisible. >u<
[C]
[CB]Uso: ~speak mensaje"""


def mensajeAyuda_virguilila_hit():
    return """[CB]puñetazo:
  
[C]¡Te dara una golpiza! >:
[C]
[CB]Uso: ~puñetazo user """


def mensajeAyuda_sacarid():
    return """[CB]sacarid:
  
[C]¿Quieres sacar un id? owo
[C]
[CB]Uso: -sacarid http://amino.com/EXAMPLE. """

def mensajeAyuda_punto_fondo():
    return """[CB]Fondo
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es mandar una imagen en el chat (Recuerda, este comando es para ponerle fondo al chat, pero solo si soy coa o anfi)
[C]
[C]En este punto ya tenemos claros muchas cosas, ahora que enviaste el fondo responde ese mismo mensaje y pon .fondo, esto le pondra el fondo que enviaste en el chat. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .fondo"""

def mensajeAyuda_punto_contenido():
    return """[CB]contenido
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .contenido Hola como estas y esto pondra en la biografia del chat Hola como estas, puedes mandar cualquier texto que quieras. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .contenido mensaje"""

def mensajeAyuda_punto_view():
    return """[CB]view
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .view cualquier cosa y esto pondra el chat en modo visualizacion, y si pones .view quitara el modo visualizacion del chat. Recuerden, si ponen solo view se desactiva, y si ponen una palabra lo activan. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Activar: .view palabra
[CB]Desactivar: .view"""

def mensajeAyuda_punto_anuncio():
    return """[CB]anuncio
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .anuncio Hola como estas y esto pondra un anuncio del chat con Hola como estas, puedes mandar cualquier texto que quieras. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .anuncio mensaje"""

def mensajeAyuda_punto_fijar():
    return """[CB]fijar
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .fijar palabra (Puede ser cualquier cosa) y esto quitara el mensaje de anuncio, y si pones .fijar fijaras un anuncio.. Pero espera, ¿Cual anuncio? ¡Usa el comando .anuncio! (๑•̀ㅂ •́)و✧ 
[C]
[CB]Activar: .fijar palabra
[CB]Desactivar: .fijar"""

def mensajeAyuda_punto_invitar():
    return """[CB]invitar
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .invitar palabra (Puede ser cualquier palabra) y esto hara que cualquiera pueda invitar a su amigo al chat, pero si pones .invitar solo los coa y anfi podran invitar. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Activar: .invitar palabra
[CB]Desactivar: .invitar"""

def mensajeAyuda_punto_clave():
    return """[CB].clave
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .clave Hola, y esto pondra palabras claves en el chat. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .clave palabra"""

def mensajeAyuda_punto_portada():
    return """[CB]portada
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es mandar una imagen en el chat (Recuerda, este comando es para ponerle portada al chat, pero solo si soy coa o anfi)
[C]
[C]En este punto ya tenemos claros muchas cosas, ahora que enviaste el portada responde ese mismo mensaje y pon .portada, esto pondra la imagen que envias como foto de portada del chat. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .portada"""

def mensajeAyuda_punto_ban():
    return """[CB].ban
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .ban link del perfil del usuario = Razon del Baneo, y esto lo baneara de la comunidad. Usalo solo si es necesario y no esta algun lider. ¡Recuerda poner el = con el motivo del baneo, se chico/a e informa! (Este comando no tiene efecto contra el staff) (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .ban https://aminoapps/linkdelusuario.com = razon del baneo"""

def mensajeAyuda_punto_strike():
    return """[CB].strike
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .strike link del perfil del usuario = Razon del Baneo, y esto lo baneara de la comunidad. Usalo solo si es necesario y no esta algun lider. ¡Recuerda poner el = con el motivo del baneo, se chico/a e informa! (Este comando no tiene efecto contra el staff) (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .strike https://aminoapps/linkdelusuario.com = razon del baneo"""


def mensajeAyuda_punto_bloquear():
    return """[CB].bloquear
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .bloquear link del usuario, y esto bloqueara al usuario para que no use los comandos. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .bloquear https://aminoapps/linkdelusuario.com"""


def mensajeAyuda_punto_titulo():
    return """[CB].titulo
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .titulo Holaa como estas, y esto cambiara el titulo del chat a Holaa como estas, puede ser cualquier mensaje o titulo que quieras. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .titulo  mensaje"""

def mensajeAyuda_punto_warn():
    return """[CB].warn
[C]
[C]¡Hoy te enseñare a usar este comando! Lo primero que tienes que hacer es poner .warn link del usuario = razon de la advertencia, recuerda es importante poner el link y el =, si no te dara error. (๑•̀ㅂ •́)و✧ 
[C]
[CB]Uso: .warn link del usuario = razon de la advertencia"""
