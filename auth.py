import datetime
import os
import bcrypt
import auth_de

def auth():

    CWD = os.path.dirname(__file__)

    rol_user = ["admin", "agent"]
    contra_admin = "1234"
    back = False
    server_token = None
    user_token = None

    while back == False:
        auth_de.menu_usuarios()
        user = input("Opcion: ")

        if user.upper() == "V": # Exit
            back = True

        elif user == "1":   #Create user
            print("-----------------------")
            print("MENU CREAR USUARIO")
            user_name = input("User name: ")
            users = auth_de.read_json("users.json")
            users_names = [user["name"] for user in users["data"]]
            try:
                users_names.index(user_name)
                print("El usuario ya existe")
            except ValueError:
                user_pwd = input("Password: ")
                rol_control = False
                while rol_control == False:
                    print("-----------------------")
                    auth_de.rol_options(rol_user)
                    option = int(input("Opcion: ")) -1
                    if option == 1: # solo consultas // agente
                        user_rol = rol_user[option]
                        rol_control = True
                    elif option == 0: # admin
                        contra_user_admin = input("Introduzca contraseña de administrador: ")
                        if contra_user_admin == contra_admin:
                            print("Contraseña OK.")
                            user_rol = rol_user[option]
                            rol_control = True
                        else:
                            print("Contraseña erronea.")
                users = auth_de.read_json("users.json")
                new_user = {"name": user_name, "pwd": bcrypt.hashpw(user_pwd.encode(), bcrypt.gensalt()).decode(), "rol": user_rol, "user_since": datetime.date.today().isoformat()}
                users["data"].append(new_user)
                auth_de.create_user(users, "users.json")
                print("Usuario creado")

        elif user == "2":   # Log in
            print("-----------------------")
            print("MENU LOG IN")
            user_name = input("Name: ")
            user_pwd = input("Password: ")
            users = auth_de.read_json("users.json")
            encontrado = False
            for user in users["data"]:
                if user["name"] == user_name:
                    encontrado = True
                    if bcrypt.checkpw(user_pwd.encode(), user["pwd"].encode()):
                        print("Log in...")
                        user_token = {"name": user["name"], "expired_date": datetime.datetime.today(), "token": bcrypt.hashpw((user_pwd + user_name).encode(), bcrypt.gensalt())}
                        auth_de.create_user_token(user_token, "cookies.json") # cookies
                        user["token"]= user_token["token"] # saving into users.json
                        auth_de.create_user(users, "users.json") # saving into users.json
                        server_token = user_token["token"]
                    else:
                        print("Password incorrecto")
            if encontrado == False:
                print("Usuario no encontrado")

        elif user == "3":   # cambio password
            if server_token != None:
                print("-----------------------")
                print("MENU CAMBIO PASSWORD")
                if (user_token["expired_date"] + datetime.timedelta(minutes=2)) > datetime.datetime.today():
                    if user_token["token"] != None:
                        user_new_pwd_1 = input("Nuevo password: ")
                        user_new_pwd_2 = input("Repetir password: ")
                        if user_new_pwd_1 == user_new_pwd_2:
                            for user in users["data"]:
                                if user["name"] == user_name:
                                    user["pwd"] = bcrypt.hashpw(user_new_pwd_1.encode(), bcrypt.gensalt()).decode()
                                    auth_de.create_user(users, "users.json")
                                    print("Password modificado...")
                        else:
                            print("El password no coincide!!!")

        elif user == "4":   # eliminar user
            print("-----------------------")
            print("MENU ELIMINAR USUARIOS") # hacer solamente para el rol admin
            print("En construccion...")

def validation():
    user_token = auth_de.read_json("cookies.json")["user_session"]
    print(user_token)
    server_token = auth_de.get_user_by_name("users.json" ,user_token["name"])["token"]
    print(server_token)
    if user_token:
        if (datetime.datetime.fromisoformat(user_token["expired_date"]) + datetime.timedelta(seconds=60)) > datetime.datetime.today():
            print("Date")
            if user_token["token"] == server_token:
                print("Es el mismo token")
                return user_token