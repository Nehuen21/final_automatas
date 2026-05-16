Entorno virtual (solo para el pandas)

python3 -m venv entornoAut

source entornoAut/bin/activate

pip install pandas openpyxl

El script por ahora solo funciona con un txt lo hice como prueba para ver si iba bien. Hay que probar ahora con el archivo .csv



# Para añadir

-- Falta corregir el contador de repetidos, crear un diccionario para que el contador cuente específicamente cada usuario repetido
y no un contador general con TODOS los usuarios repetidos. --> Hacer un contador que sea un diccionario:
         {Usuario: contador} --> contador_usuario[Usuario] += 1
-- Falta Cambiar el regex de la fecha, e invertir ese regex para que el usuario coloque DD-MM-YYYY
-- NO OLVIDAR LAS FECHAS HARDCODEADAS

CREO que no falta nada más

DOCUMENTACIÓN ÚTIL:
 resultados_ap: { mac_ap:set(usuarios) }

 fecha de inicio del test: 2020-11-05
 fecha de fin del test: 2021-01-01
 AP de test: 150

fecha más antigua:2019‑01‑01
 fecha más actual: 2023‑03‑17