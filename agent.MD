# Contexto del Agente: Testing de Script "Final Autómatas"

## Rol
Actúa como un Ingeniero de QA especializado en Python, Pandas y Teoría de Autómatas (Expresiones Regulares). Tu objetivo es testear exhaustivamente el script `final_automatas.py`.

## Descripción del Sistema
El script procesa un archivo CSV de logs de tráfico Wi-Fi (que puede pesar más de 100MB). Su función es:
1. Pedir al usuario un rango de fechas en formato `DD-MM-YYYY`.
2. Leer el CSV línea por línea y extraer la fecha, la MAC del Access Point (AP) y el Usuario usando Expresiones Regulares. Las fechas dentro del CSV están en formato `YYYY-MM-DD`. El separador del CSV es la coma `,`.
3. Filtrar los registros que coincidan con las regex y caigan dentro del rango de fechas estipulado.
4. Generar un menú interactivo en consola para que el usuario seleccione un AP específico de los encontrados.
5. Mostrar una visualización previa de los usuarios conectados a ese AP.
6. Pedir confirmación (S/N) y exportar los datos a un archivo Excel usando Pandas.

## Datos de Prueba (Mock Data)
Crea un archivo temporal llamado `export-2019-to-now-v4.csv` con el siguiente contenido para realizar las pruebas (nota: las columnas relevantes están en los índices 3 (Usuario), 6 (Fecha) y 14 (MAC_AP)):

```csv
Tipo__conexión,Inicio_de_Conexión_Dia,Inicio_de_Conexión_Hora,Usuario,Dummy1,Dummy2,Inicio_de_Conexion_Dia_Log,FIN_de_Conexión_Hora,Session_Time,Input_Octects,Output_Octects,Dummy3,Dummy4,Dummy5,MAC_AP,MAC_Cliente,Razon
Wireless-802.11,2019-02-07,19:46:08,invitado-deca,x,y,2019-02-07,11:27:57,25,39517,505219,a,b,c,DC-9F-DB-12-F3-EA:HCDD,DC-BF-E9-1A-B5-D0,User-Request
Wireless-802.11,2019-08-21,12:46:57,alumno_regular,x,y,2019-08-21,19:42:50,4,0,0,a,b,c,04-18-D6-C2-0A-F7:HCDD,A8-51-5B-68-5D-F6,User-Request
Wireless-802.11,2019-02-07,10:14:57,profe_titular,x,y,2019-02-07,10:15:34,36,3084,1344,a,b,c,DC-9F-DB-12-F3-EA:HCDD,E0-98-61-F5-0B-1F,User-Request
ERROR_LINE,le,faltan,columnas