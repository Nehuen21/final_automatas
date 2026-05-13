import re
import pandas as pd
from datetime import datetime

regex_fecha = re.compile(r'(\d{4}-\d{2}-\d{2})') # Expresion regular para extraer la fecha en el formato YYYY-MM-DD

regex_mac = re.compile(r'(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}') # Expresion regular para extraer direcciones MAC

print("--- SISTEMA DE SEGUIMIENTO DE APs ---")
fecha_inicio_str = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
fecha_fin_str = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

# Convertimos los strings a objetos 'datetime' para poder comparar rangos (<, >)
fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')


# Diccionario para guardar los resultados: { 'MAC_AP_1': {'usuario1', 'usuario2'}, ... }
resultados_ap = {}

# Abrimos el archivo gigante línea por línea
with open('log_wifi.txt', 'r', encoding='utf-8') as archivo:
    next(archivo) # Saltamos la primera línea si tiene los encabezados
    
    for linea in archivo:
        # Extraemos las columnas separando por tabulaciones o espacios
        columnas = re.split(r'\s+', linea.strip())
        
        # Validación de seguridad: si la línea está rota o incompleta, la saltamos
        if len(columnas) < 15:
            continue
            
        usuario = columnas[3]
        fecha_str = columnas[6] # Ajustá este índice según donde caiga la fecha en tu archivo
        mac_ap = columnas[14]   # Ajustá este índice según donde caiga la MAC en tu archivo
        
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

# 1. Mostrar en consola
print("\n--- RESULTADOS ---")
for ap, usuarios in resultados_ap.items():
    #print(f"AP (MAC): {ap} -> Usuarios conectados: {len(usuarios)}")
    # print(f"Lista de usuarios: {', '.join(usuarios)}")
    pass
# 2. Preparar los datos para Excel usando Pandas
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