import json
import os

CWD = os.path.dirname(__file__)

def menu_usuarios():
    print("--------------------")
    print("MENU USUARIOS")
    print("1. Crear Usuario")
    print("2. Log in")
    print("3. Cambiar Password")
    print("V. Volver")

def rol_options(rol_list):
    print("ROL USUARIO")
    for i, rol in enumerate(rol_list):
        print(f"{i+1}. {rol}")

def read_json(json_file):
    with open(f"{CWD}/{json_file}", encoding="utf8") as file:
        return json.load(file)

def create_user(users_names, json_file):
    with open(f"{CWD}/{json_file}", "w", encoding="utf8") as file:
        json.dump(users_names, file, ensure_ascii=False, indent=4)