import datetime
from os import truncate
import bcrypt
import auth_de

def auth():
    rol_user = ["admin", "agent"]
    back = True
    while back == True:
        auth_de.menu_usuarios()
        user = input("Opcion: ")

        if user.upper() == "V": # Exit
            back = False

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
                auth_de.rol_options(rol_user)
                option = int(input("Opcion: ")) -1
                user_rol = rol_user[option]
                users = auth_de.read_json("users.json")
                new_user = {"name": user_name, "pwd": bcrypt.hashpw(user_pwd.encode(), bcrypt.gensalt()).decode(), "rol": user_rol, "user_since": datetime.date.today().isoformat()}
                users["data"].append(new_user)
                auth_de.create_user(users, "users.json")
                print("Usuario creado")