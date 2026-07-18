#!/usr/bin/env python3
"""
----------------------------------------------------
Examen Final DevNet
Alumno : Dany Yanez
País   : Chile

GraphHopper API
----------------------------------------------------
"""

import requests
from geopy.geocoders import Nominatim

API_KEY = "30073041-2924-4f98-b492-64cc44dbc2eb"

geolocator = Nominatim(user_agent="iplacex_devnet")


def obtener_coordenadas(ciudad):
    ubicacion = geolocator.geocode(ciudad)

    if ubicacion is None:
        return None

    return f"{ubicacion.latitude},{ubicacion.longitude}"


while True:

    print("\n==============================")
    print("      GRAPHHOPPER ROUTE")
    print("==============================")

    origen = input("\nCiudad de Origen (v para salir): ")

    if origen.lower() == "v":
        print("\nPrograma finalizado.")
        break

    destino = input("Ciudad de Destino: ")

    print("\nMedios disponibles")

    print("1 - Automóvil")
    print("2 - Bicicleta")
    print("3 - Caminando")

    opcion = input("\nSeleccione opción: ")

    perfiles = {
        "1": "car",
        "2": "bike",
        "3": "foot"
    }

    if opcion not in perfiles:
        print("\nOpción inválida.")
        continue

    profile = perfiles[opcion]

    punto_origen = obtener_coordenadas(origen)
    punto_destino = obtener_coordenadas(destino)

    if punto_origen is None:
        print("\nNo se encontró la ciudad de origen.")
        continue

    if punto_destino is None:
        print("\nNo se encontró la ciudad de destino.")
        continue

    url = (
        "https://graphhopper.com/api/1/route?"
        f"point={punto_origen}"
        f"&point={punto_destino}"
        f"&profile={profile}"
        "&locale=es"
        "&instructions=true"
        f"&key={API_KEY}"
    )

    respuesta = requests.get(url)

    if respuesta.status_code != 200:
        print("\nError consultando GraphHopper")
        print(respuesta.text)
        continue

    datos = respuesta.json()

    ruta = datos["paths"][0]

    kilometros = ruta["distance"] / 1000

    millas = kilometros * 0.621371

    segundos = ruta["time"] / 1000

    horas = int(segundos // 3600)

    minutos = int((segundos % 3600) // 60)

    print("\n==============================")
    print("RESULTADO")
    print("==============================")

    print(f"\nOrigen : {origen}")
    print(f"Destino: {destino}")

    print(f"\nDistancia : {kilometros:.2f} km")
    print(f"Distancia : {millas:.2f} millas")

    print(f"Tiempo aproximado: {horas} horas {minutos} minutos")

    print("\nNarrativa del viaje")

    print("--------------------------------")

    for paso in ruta["instructions"]:
        print("•", paso["text"])

    print("--------------------------------")
