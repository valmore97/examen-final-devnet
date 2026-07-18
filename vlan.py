#!/usr/bin/env python3

"""
Examen Final DevNet
Validador de VLAN
Autor: Dany Yanez
"""

try:
    vlan = int(input("Ingrese el número de VLAN: "))

    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} pertenece al rango NORMAL (1-1005).")

    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} pertenece al rango EXTENDIDO (1006-4094).")

    else:
        print(f"La VLAN {vlan} no es válida.")

except ValueError:
    print("Error: Debe ingresar un número entero.")
