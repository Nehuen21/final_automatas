import re
import pandas as pd
from datetime import datetime

regex_fecha = re.compile(r'(\d{4}-\d{2}-\d{2})') # Expresion regular para extraer la fecha en el formato YYYY-MM-DD

regex_mac = re.compile(r'(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}') # Expresion regular para extraer direcciones MAC

print("--- SISTEMA DE SEGUIMIENTO DE APs ---")
while True:
    print("Fechas válidas: 2019-01-01 / 2023-03-07")
    try:
        #fecha_inicio_str = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        #fecha_fin_str = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
        fecha_inicio_str = "2020-11-05"
        fecha_fin_str = "2023-01-01"
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
        fecha_inicio_limite = datetime.strptime("2019-01-01", '%Y-%m-%d')
        fecha_fin_limite = datetime.strptime("2023-03-07", '%Y-%m-%d')

        if fecha_inicio >= fecha_inicio_limite and fecha_fin <= fecha_fin_limite:
            break
        else: continue
    except Exception as e:
        print("Por favor elija una fecha válida")
        




def funcion_procesadora_archivo(archivo, regex_fecha, regex_mac, fecha_inicio, fecha_fin):
    resultados_ap = {}
    contador_de_usuarios_repetidos = 0
    
    for linea in archivo:
        columnas = linea.strip().split(',')
        
        if len(columnas) < 15:
            continue
            
        usuario = columnas[3]
        fecha_str = columnas[6] 
        mac_ap = columnas[14]   
        
        if not regex_fecha.match(fecha_str):
            continue
            
        fecha_log = datetime.strptime(fecha_str, '%Y-%m-%d')
        if not (fecha_inicio <= fecha_log <= fecha_fin):
            continue
            

        if not regex_mac.match(mac_ap):
            continue

        if mac_ap not in resultados_ap:
            resultados_ap[mac_ap] = set()
            

        if usuario in resultados_ap[mac_ap]:

            contador_de_usuarios_repetidos += 1
        else:
            resultados_ap[mac_ap].add(usuario)

    return resultados_ap, contador_de_usuarios_repetidos


# Abrimos el archivo gigante línea por línea
print("--- Procesando Archivo, Por favor espere ---")
# 1. Leemos el archivo y salimos del 'with' rápido
with open('export-2019-to-now-v4.csv', 'r', encoding='utf-8') as archivo:
    next(archivo) # Saltamos la primera línea (encabezados)
    resultados_ap = funcion_procesadora_archivo(
        archivo=archivo, 
        regex_fecha=regex_fecha,
        regex_mac=regex_mac,
        fecha_fin=fecha_fin, 
        fecha_inicio=fecha_inicio
    )

# Ya fuera del archivo, preparamos la lista única de APs.
# Como resultados_ap es un dict, sus keys ya son únicas.
lista_ap = list(resultados_ap.keys())
longitud_lista_ap = len(lista_ap)



while True:
    for idx, ap in enumerate(lista_ap):
        print(f"{idx})- {ap}")
    print(f"\n--- Elija por favor qué AP quiere verificar en el periodo indicado {fecha_inicio_str} / {fecha_fin_str} ---")
    try:
        ap_input = int(input("Ingrese el número del AP a analizar: "))

        if not (0 <= ap_input < longitud_lista_ap):
            print(f"Error: Elija un número válido entre 0 y {longitud_lista_ap - 1}")    
            continue
            
        # Si llegamos aquí, el input es válido
        ap_seleccionado = lista_ap[ap_input]
        
    except ValueError: 
        print(f"Error: Debe ingresar un número. Elija entre 0 y {longitud_lista_ap - 1}")
        continue

    # 1. Mostrar en consola
    print("\n--- RESULTADOS ---")
    datos_excel_AP = []
    
    
    usuarios_del_ap = resultados_ap.get(ap_seleccionado, [])

    for u in usuarios_del_ap:
        datos_excel_AP.append({'Usuarios': u})
        print(u)
            
    print(f"\nLa MAC seleccionada es {ap_seleccionado}.")
    print(f"Lista preparada para Pandas:\n {datos_excel_AP}\n")
    
    # 2. Confirmación del usuario
    input_decision = input("¿El resultado del AP elegido es el deseado? (Y/N): ")
    
    if re.match("^[Yy]$", input_decision):
        break 
    elif re.match("^[Nn]$", input_decision): 
        continue 
    else:
        print("Opción no reconocida. Volviendo al inicio...")

df = pd.DataFrame(datos_excel_AP)
nombre_archivo = f"reporte_{ap_seleccionado}_{fecha_inicio_str}--{fecha_fin_str}.xlsx"
df.to_excel(nombre_archivo, index=False)
print(f"\n¡Datos exportados exitosamente a {nombre_archivo}!")

