# import requests as req
import json
import os
import funcs
import datetime
import bcrypt
import utm
import auth

# url = "https://datos.comunidad.madrid/catalogo/dataset/35609dd5-9430-4d2e-8198-3eeb277e5282/resource/c38446ec-ace1-4d22-942f-5cc4979d19ed/download/desfibriladores_externos_fuera_ambito_sanitario.json"
CWD = os.path.dirname(__file__)

# res = req.get(url).json()

# with open(f"{CWD}/deas.json", "w", encoding="utf-8") as file:
#     json.dump(res, file, ensure_ascii=False, indent=4)

data = funcs.get_data(f"{CWD}/deas.json")

# 1. Cuántos DEAS hay en total
print("El total de DEAS en el dataset son: ", len(data["data"]))
print("--------------------")
# 2.Considerando solo los DEAS de los códigos postales dentro de la M-30, cuántos hay?
zip_codes_m30 = [str(zip_code) for zip_code in (28029, 28036, 28046, 28039, 28016, 28020, 28002, 28003, 28015, 28010, 28006, 28028, 28008, 28004, 28001, 280013, 28014, 28009, 28007, 28012, 28005, 28045)]
print("El num de DEAS dentro de la M30 son:", funcs.qty_M30(data["data"], zip_codes_m30))
print("--------------------")
# 3.Cuántos se encuentran en entidades públicas y cuántos en privadas?
print(f"Privadas: {funcs.get_private(data['data'])}\nPublicas: {len(data['data']) - funcs.get_private(data['data'])}")
print("--------------------")

rol_user = ["admin", "agent"]
salir = False
# contraseñas usadas "1234"

while salir != True:
    funcs.menu_inicial()
    user = input("Opcion: ")

    if user.upper() == 'E': # Exit
        salir = True

    elif user == '1':   # Menu users
        auth.auth()

    elif user == '2':   # Menu DEA
        while user.upper() != 'V':
            funcs.menu_dea()
            user = input("Opcion: ")
            if user == '1': # DEA por codigo
                print("--------------------")
                print("Buscar DEA por codigo en construccion")
                
            elif user == '2':   # DEA por posicion
                user_lat = float(input("Lat: "))
                user_lon = float(input("Lon: "))
                user_utm = utm.from_latlon(user_lat, user_lon)
                nearest = funcs.get_nearest(data["data"], user_utm[0], user_utm[1])[1]
                dea_lat, dea_lon = utm.to_latlon(int(nearest["direccion_coordenada_x"]),int(nearest["direccion_coordenada_y"]),30, "T")
                print(dea_lat, dea_lon)
                print(f"https://www.google.com/maps/search/?api=1&query={dea_lat}%2C{dea_lon}")
                print(f"https://www.google.com/maps/dir/?api=1&origin={user_lat}%2C{user_lon}&destination={dea_lat}%2C{dea_lon}&travelmode=walking")
                
            elif user == '3': # Modificar DEA
                if auth.validation():
                    print("--------------------")
                    print("MENU MODIFICAR DEA")
                    print("En construccion...")


