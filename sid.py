import aminofix
client = aminofix.Client()
client.login(email="correo@gmail.com", password="contraseña")
print("Disclaimer > copy sid and put it in data in case of using heroku as server.\n\n")
print(f"{client.sid}")
