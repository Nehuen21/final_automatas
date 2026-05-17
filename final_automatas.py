import re
import pandas as pd
from datetime import datetime


regex_fecha = re.compile(r'(\d{4}-\d{2}-\d{2})') # Expresion regular para extraer la fecha en el formato YYYY-MM-DD

regex_mac = re.compile(r'(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}(?::[A-Za-z0-9]+)?')
print("--- SISTEMA DE SEGUIMIENTO DE APs ---")
fecha_inicio_str = input("Ingrese la fecha de inicio (DD-MM-YYYY): ")
fecha_fin_str = input("Ingrese la fecha de fin (DD-MM-YYYY): ")



# Convertimos los strings a objetos datetime. 
# Usamos '%d-%m-%Y' porque le pedimos al usuario Día-Mes-Año como pidio la profe
fecha_inicio = datetime.strptime(fecha_inicio_str, '%d-%m-%Y')
fecha_fin = datetime.strptime(fecha_fin_str, '%d-%m-%Y')

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
        fecha_str = columnas[6] # Ajustá este índice según donde caiga la fecha en tu archivo
        mac_ap = columnas[13]   # Ajustá este índice según donde caiga la MAC en tu archivo
        
        # Verificamos que la fecha cumpla con el patrón usando la regex
        if regex_fecha.match(fecha_str):
            fecha_log = datetime.strptime(fecha_str, '%Y-%m-%d')
            
            # Si la fecha está dentro del rango que pidió el usuario...
            if fecha_inicio <= fecha_log <= fecha_fin:
                
                # Verificamos que la MAC cumpla con el patrón usando la regex
                if regex_mac.match(mac_ap):
                    
                    # Lo agregamos a nuestro diccionario
                    if mac_ap not in resultados_ap:
                        resultados_ap[mac_ap] = set()
                    resultados_ap[mac_ap].add(usuario)



# Si no encontró nada en esas fechas, cortamos el programa amablemente
if len(resultados_ap) == 0:
    print("\nNo se encontraron Access Points registrados en ese rango de fechas.")
    exit()

# --- 3. MENÚ DE SELECCIÓN DE AP ---
lista_ap = list(resultados_ap.keys())
longitud_lista_ap = len(lista_ap)

print(f"\n--- APs ENCONTRADOS ENTRE {fecha_inicio_str} Y {fecha_fin_str} ---")
for i, ap in enumerate(lista_ap):
    print(f"{i}) - {ap}")

while True:
    print("\n--- Elija qué AP quiere verificar ---")
    try:
        ap_input = int(input("Ingrese el número del AP a analizar: "))
        if 0 <= ap_input < longitud_lista_ap:
            ap_seleccionado = lista_ap[ap_input]
            break
        else: 
            print(f"Error: Elija un número entre 0 y {longitud_lista_ap - 1}")    
    except ValueError:
        print("Error: Por favor ingrese un número válido.")

# --- 4. VISUALIZACIÓN PREVIA (Lo que pidió la profe) ---
usuarios_seleccionados = resultados_ap[ap_seleccionado]

print("\n" + "="*40)
print("          VISUALIZACIÓN PREVIA")
print("="*40)
print(f"AP Seleccionado : {ap_seleccionado}")
print(f"Total Usuarios  : {len(usuarios_seleccionados)}")
print("-" * 40)
print("Lista de usuarios conectados:")

datos_excel_AP = []
for u in usuarios_seleccionados:
    print(f" - {u}")
    datos_excel_AP.append({'Usuario': u})

print("="*40)

# --- 5. CONFIRMACIÓN Y EXPORTACIÓN ---
while True:
    confirmacion = input("\n¿La información es correcta? ¿Desea exportar a Excel? (S/N): ").strip().upper()
    
    if confirmacion == 'S':
        df = pd.DataFrame(datos_excel_AP)
        ap_limpio = ap_seleccionado.replace(':', '-') 
        nombre_archivo = f"reporte_{ap_limpio}_{fecha_inicio_str}--{fecha_fin_str}.xlsx"
        
        df.to_excel(nombre_archivo, index=False)
        print(f"\n¡Datos exportados exitosamente a {nombre_archivo}! El programa ha finalizado.")
        break
        
    elif confirmacion == 'N':
        print("\nExportación cancelada. El programa ha finalizado.")
        break
        
    else:
        print("Opción no válida. Por favor, ingrese 'S' para exportar o 'N' para cancelar.")





















"""
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
    print(f"--- Elija porfavor que AP quiere verificar en el periodo indicado {fecha_inicio_str} / {fecha_fin_str}")
    try:
        ap_input = int(input("Ingrese el número del AP a analizar: "))

        if 0 < ap_input < longitud_lista_ap:
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
for ap, usuarios in resultados_ap.items():
    #print(f"AP (MAC): {ap} -> Usuarios conectados: {len(usuarios)}")      # Este print Solo muestra la cantidad de usuarios por AP lo podemos meter talvez 
    # print(f"Lista de usuarios: {', '.join(usuarios)}")
    if ap == ap_seleccionado:
        print(usuarios)
        for u in usuarios:
            datos_excel_AP.append({'Usuarios': u})
            print(u)


df = pd.DataFrame(datos_excel_AP)
nombre_archivo = f"reporte_{ap_seleccionado}_{fecha_inicio_str}--{fecha_fin_str}.xlsx"
df.to_excel(nombre_archivo, index=False)
print(f"\n¡Datos exportados exitosamente a {nombre_archivo}!")

# 2. Preparar los datos para Excel usando Pandas"""
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
