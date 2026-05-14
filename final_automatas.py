import re
import pandas as pd
from datetime import datetime

regex_fecha = re.compile(r'(\d{4}-\d{2}-\d{2})') # Expresion regular para extraer la fecha en el formato YYYY-MM-DD

regex_mac = re.compile(r'(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}') # Expresion regular para extraer direcciones MAC

print("--- SISTEMA DE SEGUIMIENTO DE APs ---")
while True:
    try:
        fecha_inicio_str = str(input("Ingrese la fecha de inicio (YYYY-MM-DD): "))
        fecha_fin_str = str(input("Ingrese la fecha de fin (YYYY-MM-DD): "))

        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
        
        if fecha_inicio >= datetime.strptime("2019‑01‑01", '%Y-%m-%d') and fecha_fin <= datetime.strptime("2019‑01‑01", '%Y-%m-%d'):
            break
        else: continue
    except Exception as e:
        print("Por favor elija una fecha válida")
        
# Convertimos los strings a objetos 'datetime' para poder comparar rangos (<, >)


# Diccionario para guardar los resultados: { 'MAC_AP_1': {'usuario1', 'usuario2'}, ... }
resultados_ap = {}

# Abrimos el archivo gigante línea por línea
print("--- Procesando Archivo, Por favor espere ---")
with open('export-2019-to-now-v4.csv', 'r', encoding='utf-8') as archivo:
    next(archivo) # Saltamos la primera línea si tiene los encabezados
    
    for linea in archivo:
        # Extraemos las columnas separando por tabulaciones o espacios
        columnas = linea.strip().split(',')
        
        # Validación de seguridad: si la línea está rota o incompleta, la saltamos
        if len(columnas) < 15:
            continue
            
        usuario = columnas[3]
        fecha_str = columnas[6] 
        mac_ap = columnas[14]   
        
        # Verificamos que la fecha cumpla con el patrón usando la regex
        if regex_fecha.match(fecha_str):
            fecha_log = datetime.strptime(fecha_str, '%Y-%m-%d')
            
            # Si la fecha está dentro del rango que pidió el usuario
            if fecha_inicio <= fecha_log <= fecha_fin:
                
                # Verificamos que la MAC cumpla con el patrón usando la regex
                if regex_mac.match(mac_ap):
                    
                    # Lo agregamos al diccionario
                    if mac_ap not in resultados_ap:
                        resultados_ap[mac_ap] = set()
                    resultados_ap[mac_ap].add(usuario)

# Que el usuario elija que AP quiere verificar en el periódo de tiempo Indicado previamente
lista_ap = []
lista_ap_index = 0
for ap in resultados_ap:
    if ap not in lista_ap:
        lista_ap.append(ap)
        print(f"{lista_ap_index})- {ap}")
        lista_ap_index += 1
    else: continue
longitud_lista_ap = len(lista_ap)
while True:
    print(f"--- Elija porfavor que AP quiere verificar en el periodo indicado {fecha_inicio_str} / {fecha_fin_str} ---")
    try:
        ap_input = int(input("Ingrese el número del AP a analizar: "))

        if 0 <= ap_input < longitud_lista_ap:
            ap_seleccionado = lista_ap[ap_input]
            break
        else: 
            print(f"Elija un número entre 0 y {longitud_lista_ap - 1}")    
            continue
    except Exception as e:
        print(f"Elija un número entre 0 y {longitud_lista_ap - 1}")


# 1. Mostrar en consola
print("\n--- RESULTADOS ---")
print(resultados_ap)

#Preparamos los datos para pandas
datos_excel_AP = []
ap_regex = re.compile(repr(ap_seleccionado))
for ap, usuarios in resultados_ap.items():
    #print(f"AP (MAC): {ap} -> Usuarios conectados: {len(usuarios)}")      # Este print Solo muestra la cantidad de usuarios por AP lo podemos meter talvez 
    # print(f"Lista de usuarios: {', '.join(usuarios)}")
    if ap_regex.match(ap):
        print(usuarios)
        for u in usuarios:
            datos_excel_AP.append({'Usuarios': u})
            print(u)


df = pd.DataFrame(datos_excel_AP)
nombre_archivo = f"reporte_{ap_seleccionado}_{fecha_inicio_str}--{fecha_fin_str}.xlsx"
df.to_excel(nombre_archivo, index=False)
print(f"\n¡Datos exportados exitosamente a {nombre_archivo}!")

# 2. Preparar los datos para Excel usando Pandas
"""
datos_excel = []
for ap, usuarios in resultados_ap.items():
    for u in usuarios:
        datos_excel.append({'MAC_AP': ap, 'Usuario': u})

cantidad_regsitros = len(datos_excel)
print(f"\nCantidad total de registros para exportar: {cantidad_regsitros}")

df = pd.DataFrame(datos_excel)

# 3. Exportar
nombre_archivo = f"Reporte_APs_{fecha_inicio_str}_al_{fecha_fin_str}.xlsx"
df.to_excel(nombre_archivo, index=False)
print(f"\n¡Datos exportados exitosamente a {nombre_archivo}!")

"""
