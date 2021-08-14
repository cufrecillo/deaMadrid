import json
import os

CWD = os.path.dirname(__file__)

class DEA:
    def __init__(self, x, y):
        if type(x) != int:
            raise ValueError("Solo se adminten numeros enteros")
        if type(y) != int:
            raise ValueError("Solo se adminten numeros enteros")
        self.x = x
        self.y = y
    def distance(self, user_x, user_y):
        c_1 = (user_x - self.x) ** 2
        c_2 = (user_y - self.y) ** 2
        return ((c_1 + c_2)**0.5)

def get_data(dataset):
    with open(dataset, encoding='utf-8') as file:
        return json.load(file)

def qty_M30(dataset, zc_list):
    return len([dea for dea in dataset if dea["direccion_codigo_postal"] in zc_list])

def get_private(dataset):
    return len([dea for dea in dataset if dea["tipo_titularidad"] == "Privada"])

def menu_inicial():
    print("--------------------")
    print("MENU PRINCIPAL")
    print("1. Usuarios")
    print("2. DEAS")
    print("E. Exit")

def menu_dea():
    print("--------------------")
    print("MENU DEA")
    print("1. Buscar DEA por codigo")
    print("2. Buscar DEA por posicion")
    print("3. Modificar DEA")
    print("V. Volver")

def menu_by_position():
    print("--------------------")
    print("---Busqueda DEA por position---")
    x = int(input("X: "))
    y = int(input("Y: "))
    return (x, y)

def get_nearest(dataset, user_x, user_y):
    result = {}
    dea_x = 'direccion_coordenada_x'
    dea_y = 'direccion_coordenada_y'
    for dea in dataset:
        dea_object = DEA(int(dea[dea_x]), int(dea[dea_y]))
        distance = dea_object.distance(user_x, user_y)
        result[distance] = dea
    return sorted(result.items(), key= lambda  dea: dea[0])[:2]

