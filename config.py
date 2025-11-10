import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ampl_data_dir = os.path.join(PROJECT_ROOT, 'ampl_data')
cases_dir = os.path.join(PROJECT_ROOT, 'cases')
v2_reports_dir = os.path.join(PROJECT_ROOT, 'v2/reports')

# Comunes
enter_name_case = 'Digite el nombre del caso que desea ejecutar: '
enter_name_case_multiple = 'Digite el nombre del caso que desea ejecutar (deje en blanco para terminar de seleccionar casos): '
enter_name_case_format = '''
Digite el nombre del caso que desea ejecutar en el siguiente formato:

--------- ancho_largo_ocupacion ---------

Ejemplo:
- 55_55_84
- 60_60_80
- 50_50_90

Digite el nombre: '''
enter_name_case_format_multiple = '''
Digite el nombre del caso que desea ejecutar en el siguiente formato:

--------- ancho_largo_ocupacion ---------

Ejemplo:
- 55_55_84
- 60_60_80
- 50_50_90

Digite el nombre (deje en blanco para terminar de seleccionar casos): '''


instruction_text_main = '''
Seleccione la opción que desea digitar:
                     
1- Ejecutar un caso con la heurística.
2- Ejecutar un caso con AMPL.
3- Generar .dat para AMPL.
4- Generar un caso.
5- Validar las demandas un caso.
6- Obtener la ocupación de un caso.

Ingrese un número: '''


instruction_text_v2_run = '''
¿Cómo desea ejecutar el algoritmo?

1- Todos los casos (en paralelo).
2- Todos los casos (secuencial).
3- Determinados casos (en paralelo).
4- Determinados casos (en secuencial).
5- Un caso único.

Ingrese un número: '''

instruction_text_v2_report_type = '''
¿Cómo desea generar los reportes?

1- Excel y debug: Todos los casos.
2- Excel y debug: Determinados casos.
3- Excel sin debug: Todos los casos.
4- Excel sin debug: Determinados casos.
5- Reporte mínimo de texto.

Ingrese un número: '''


instruction_text_v2_report_type_single = '''
¿Cómo desea generar el reporte?

1- Excel y debug.
2- Excel sin debug.
3- Reporte mínimo de texto.

Ingrese un número: '''


instruction_text_v2_variant = '''
¿Con cuál variante de permutación inicial desea ejecutar el algoritmo?

1- Random.
2- De mayor a menor.
3- De menor a mayor.
4- Sin modificaciones (por defecto).

Ingrese un número: '''


instruction_text_ampl_generate = '''
¿Cómo desea generar la data de AMPL?

1- Todos los casos (en paralelo).
2- Todos los casos (secuencial).
3- Determinados casos (en paralelo).
4- Determinados casos (en secuencial).
5- Un caso único.

Ingrese un número: '''


instruction_text_utils_create_case = '''
¿Cómo desea ejecutar la generación de casos?

1- Todos los casos (que nada más estén creados en el directorio de cases).
2- Determinados casos.
3- Un caso único.

Ingrese un número: '''


instruction_text_utils_validate_cases = '''
¿Cómo desea ejecutar la validación de casos?

1- Todos los casos.
2- Determinados casos.
3- Un caso único.

Ingrese un número: '''


instruction_text_utils_get_ocupation = '''
¿Cómo desea ejecutar la obtención de ocupación?

1- Todos los casos.
2- Determinados casos.
3- Un caso único.

Ingrese un número: '''


system_instruction = '''You are a mathematics expert in generating multiple triads (minimum 3, maximum needed) that, whose products are summed together, get equal to a determined value.

Below I provide you a series of examples:

Example 1 (Target: 2500)

5x10x10=500
5x20x5=500
5x25x4=500
2x25x10=500

Example 2 (Target: 2880)

6x10x12=720
8x9x10=720
6x8x15=720
4x10x18=720

Example 3 (Target: 3240)

5x10x20=1000
5x8x25=1000
4x5x50=1000
3x8x10=240

'''

instruction_text_ampl_run_case = '''
¿Cómo desea ejecutar el caso con AMPL?

1- Todos los casos.
2- Determinados casos.
3- Un caso único.

Ingrese un número: '''

ampl_run_file = 'run.run'
