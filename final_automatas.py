import re
import pandas as pd
from datetime import datetime

# --- 1. EXPRESIONES REGULARES ---
# Regex para formato YYYY-MM-DD en el archivo
regex_fecha = re.compile(r'(\d{4}-\d{2}-\d{2})') 
# Regex para direcciones MAC contemplando sufijo opcional
regex_mac = re.compile(r'(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}') 

print("--- SISTEMA DE SEGUIMIENTO DE APs ---")

# --- 2. INPUT DEL USUARIO CON LÍMITES (Logica  Franco) ---
while True:
    print("\nFechas válidas en el registro: 01-01-2019 al 07-03-2023")
    try:
        fecha_inicio_str = input("Ingrese la fecha de inicio (DD-MM-YYYY): ")
        fecha_fin_str = input("Ingrese la fecha de fin (DD-MM-YYYY): ")
        
        # Parseamos el input del usuario
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%d-%m-%Y')
        fecha_fin = datetime.strptime(fecha_fin_str, '%d-%m-%Y')

        # Límites de la base de datos real
        fecha_inicio_limite = datetime.strptime("2019-01-01", '%Y-%m-%d')
        fecha_fin_limite = datetime.strptime("2023-03-07", '%Y-%m-%d')

        if fecha_inicio >= fecha_inicio_limite and fecha_fin <= fecha_fin_limite:
            break
        else: 
            print("Error: Las fechas ingresadas están fuera del límite de los registros.")
            continue
    except ValueError:
        print("Error: Por favor elija una fecha válida con el formato DD-MM-YYYY.")


# --- 3. FUNCIÓN PROCESADORA CON CONTADOR ---
def funcion_procesadora_archivo(archivo, regex_fecha, regex_mac, fecha_inicio, fecha_fin):
    resultados_ap = {}
    
    for linea in archivo:
        columnas = linea.strip().split(',')
        
        if len(columnas) < 14:
            continue
            
        usuario = columnas[3]
        fecha_str = columnas[6] 
        mac_ap = columnas[13] # Índice 13  (columna que estaba mal)
        
        if not regex_fecha.match(fecha_str): #para verificar que la fecha tenga el formato correcto antes de intentar parsearla
            continue
            
        fecha_log = datetime.strptime(fecha_str, '%Y-%m-%d') # Parseamos la fecha del log para compararla con el rango ingresado por el usuario
        if not (fecha_inicio <= fecha_log <= fecha_fin):
            continue
            
        if not regex_mac.match(mac_ap):
            continue

        # Lógica del contador: Creamos un diccionario interno por cada MAC
        if mac_ap not in resultados_ap:
            resultados_ap[mac_ap] = {} 
            
        if usuario in resultados_ap[mac_ap]:
            resultados_ap[mac_ap][usuario] += 1 # Sumamos 1 conexión más
        else:
            resultados_ap[mac_ap][usuario] = 1  # Primera conexión (inicializamos)

    return resultados_ap


# --- 4. APERTURA DE ARCHIVO ---
print("\n--- Procesando Archivo, Por favor espere ---")
with open('export-2019-to-now-v4.csv', 'r', encoding='utf-8') as archivo:
    next(archivo) # Saltamos la primera línea (encabezados)
    
    # Desempaquetamos correctamente para evitar el error de Tupla
    resultados_ap = funcion_procesadora_archivo(
        archivo=archivo, 
        regex_fecha=regex_fecha,
        regex_mac=regex_mac,
        fecha_fin=fecha_fin, 
        fecha_inicio=fecha_inicio
    )

# Control de archivo vacío (Logica  Nehuen)
if len(resultados_ap) == 0:
    print("\nNo se encontraron Access Points registrados en ese rango de fechas.")
    exit()

# --- 5. MENÚ DE SELECCIÓN (Logica Nehuen) ---
lista_ap = list(resultados_ap.keys())
longitud_lista_ap = len(lista_ap)

print(f"\n--- APs ENCONTRADOS ENTRE {fecha_inicio_str} Y {fecha_fin_str} ---")
for idx, ap in enumerate(lista_ap):
    print(f"{idx}) - {ap}")

while True:
    print("\n--- Elija qué AP quiere verificar ---")
    try:
        ap_input = int(input("Ingrese el número del AP a analizar: "))

        if 0 <= ap_input < longitud_lista_ap:
            ap_seleccionado = lista_ap[ap_input]
            break
        else: 
            print(f"Error: Elija un número válido entre 0 y {longitud_lista_ap - 1}")    
            continue
    except ValueError:
        print(f"Error: Debe ingresar un número. Elija entre 0 y {longitud_lista_ap - 1}")
        continue


# --- 6. VISUALIZACIÓN PREVIA (Logica Nehuen Adaptada) ---
usuarios_seleccionados = resultados_ap[ap_seleccionado]

print("\n" + "="*50)
print("          VISUALIZACIÓN PREVIA")
print("="*50)
print(f"AP Seleccionado : {ap_seleccionado}")
print(f"Total Usuarios únicos: {len(usuarios_seleccionados)}")
print("-" * 50)
print("Lista de usuarios y sus conexiones totales:")

datos_excel_AP = []
# Iteramos el diccionario para mostrar al usuario y sus conexiones
for u, conexiones in usuarios_seleccionados.items():
    print(f" - Usuario: {u} | Cant. de Conexiones: {conexiones}")
    datos_excel_AP.append({'Usuario': u, 'Cant_Conexiones': conexiones})

print("="*50)

# --- 7. CONFIRMACIÓN Y EXPORTACIÓN (Lógica Franco con bug para windows arreglado) ---
while True:
    input_decision = input("\n¿El resultado del AP elegido es el deseado? ¿Desea exportar a Excel? (Y/N): ")
    
    if re.match("^[YySs]$", input_decision): # Acepta Y, y, S, s
        df = pd.DataFrame(datos_excel_AP)
        
        # Limpieza de la MAC para evitar error en Windows al crear el Excel
        ap_limpio = ap_seleccionado.replace(':', '-') 
        nombre_archivo = f"reporte_{ap_limpio}_{fecha_inicio_str}--{fecha_fin_str}.xlsx"
        
        df.to_excel(nombre_archivo, index=True)
        print(f"\n¡Datos exportados exitosamente a {nombre_archivo}! El programa ha finalizado.")
        break 
        
    elif re.match("^[Nn]$", input_decision): 
        print("\nExportación cancelada. Puede volver a ejecutar el programa si desea buscar otro AP.")
        break 
        
    else:
        print("Opción no reconocida. Ingrese Y para exportar o N para cancelar.")