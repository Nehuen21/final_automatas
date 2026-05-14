Entorno virtual (solo para el pandas)

python3 -m venv entornoAut

source entornoAut/bin/activate

pip install pandas openpyxl

El script por ahora solo funciona con un txt lo hice como prueba para ver si iba bien. Hay que probar ahora con el archivo .csv



# Para añadir

- Tendriamos que añadir excepciones para cuando le pongamos algo que no sea una fecha no explote 

- Implementar para que muestre los de un AP en especifico 

- Verificar el mecanismo de líneas faltantes, ya que no se si está bien skipear lineas < 15

- Que exista una opción para mostrar cuantos usuarios se conectaron a cada access point en el periodo de tiempo

1- Que periodo de fechas quiere verificar el usuario
2- Mostrar una lista de todos los access point 
3- Que el usuario elija que  AccessPoint quiere comprobar

DOCUMENTACIÓN ÚTIL:
 resultados_ap: { mac_ap:set(usuarios) }

 fecha de inicio del test: 2020-11-05
 fecha de fin del test: 2021-01-01
 AP de test: 150

fecha más antigua:2019‑01‑01
 fecha más actual: 2023‑03‑17