import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ampl_data_dir = os.path.join(PROJECT_ROOT, 'ampl_data')
cases_dir = os.path.join(PROJECT_ROOT, 'cases')
v2_reports_dir = os.path.join(PROJECT_ROOT, 'v2/reports')
ampl_run_cases_reports_dir = os.path.join(PROJECT_ROOT, 'ampl/reports')

# Comunes
enter_name_case = 'Digite el nombre del caso que desea ejecutar: '
enter_name_case_multiple = 'Digite el nombre del caso que desea ejecutar (deje en blanco para terminar de seleccionar casos): '


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


instruction_text_utils_create_case_ai_instruction = '''
¿Qué sistema de AI desea utilizar para la generación de los casos?

1- Ollama.
2- Gemini.
3- OpenAI.

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


system_instruction_ollama = '''
You are a mathematics expert generating multiple triads $(a, b, c)$ that fulfill a set of rules.

Your task is to generate a set of triads whose product $(a x b x c)$, when summed, is closest to a target value.

Below are examples:

### Example 1 (Target: 2500)
$10 x 10 x 10 = 1000$
$5 x 10 x 20 = 1000$
$5 x 10 x 10 = 500$
Total Sum: $1000 + 1000 + 500 = 2500$

### Example 2 (Target: 2880)
$6 x 10 x 12 = 720$
$8 x 9 x 10 = 720$
$6 x 8 x 15 = 720$
$4 x 10 x 18 = 720$
Total Sum: $720 + 720 + 720 + 720 = 2880$

### Example 3 (Target: 3240)
$5 x 10 x 20 = 1000$
$5 x 8 x 25 = 1000$
$4 x 5 x 50 = 1000$
$3 x 8 x 10 = 240$
Total Sum: $1000 + 1000 + 1000 + 240 = 3240$

Note that the product of EACH individual triad does NOT have to be the target value; rather, the SUM of all products must be the target value.'''


instruction_text_ampl_run_case = '''
¿Cómo desea ejecutar el caso con AMPL?

1- Todos los casos.
2- Determinados casos.
3- Un caso único.

Ingrese un número: '''

ampl_run_file = 'run.run'
