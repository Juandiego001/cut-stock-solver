import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ampl_data_dir = os.path.join(PROJECT_ROOT, 'ampl_data')
cases_dir = os.path.join(PROJECT_ROOT, 'cases')
v2_reports_dir = os.path.join(PROJECT_ROOT, 'v2/reports')
ampl_run_cases_reports_dir = os.path.join(PROJECT_ROOT, 'ampl/reports')
cases_group_dir = os.path.join(PROJECT_ROOT, 'cases_group')

# Possible groups
possible_groups = ['small', 'medium', 'large', 'real']
groups_indexes_text = '\n'.join(
    [f'{i+1}- {group.capitalize()}.' for i, group in enumerate(possible_groups)])

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
7- Gestionar grupos de casos.

Ingrese un número: '''


instruction_text_v2_run = '''
¿Cómo desea ejecutar el algoritmo?

1- Todos los casos (en paralelo).
2- Todos los casos (secuencial).
3- Determinados casos (en paralelo).
4- Determinados casos (en secuencial).
5- Grupo de casos (en paralelo).
6- Grupo de casos (en secuencial).
7- Un caso único.

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


instruction_text_v2_group = f'''
¿Con cuál grupo deseas ejecutar el algoritmo?

{groups_indexes_text}

Ingresa un número: '''


instruction_text_ampl_generate = '''
¿Cómo desea generar la data de AMPL?

1- Todos los casos (en paralelo).
2- Todos los casos (secuencial).
3- Determinados casos (en paralelo).
4- Determinados casos (en secuencial).
5- Grupo de casos (en paralelo).
6- Grupo dec casos (en secuencial).
7- Un caso único.

Ingrese un número: '''


instruction_text_utils_create_case = '''
¿Cómo desea ejecutar la generación de casos?

1- Todos los casos (que nada más estén creados en el directorio de cases).
2- Determinados casos.
3- Un caso único.
4- Manualmente.

Ingrese un número: '''


instruction_text_utils_create_case_ask_save = '''
¿Desea guardar los casos en alguno de los grupos?

1- Sí, todos en el mismo grupo.
2- Sí, cada caso en un grupo distinto.
3- No.

Ingrese un número: '''


instruction_text_utils_create_case_group_save = f'''
¿En qué grupo deseas guardar los casos generados?

{groups_indexes_text}

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
3- Grupo de casos.
4- Un caso único.

Ingrese un número: '''


instruction_text_utils_validate_cases_group = f'''
¿Sobre qué grupo deseas realizar la validación de casos?

{groups_indexes_text}

Ingresa un número: '''


instruction_text_utils_get_ocupation = '''
¿Cómo desea ejecutar la obtención de ocupación?

1- Todos los casos.
2- Determinados casos.
3- Grupo de casos.
4- Un caso único.

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
3- Grupo de casos.
4- Un caso único.

Ingrese un número: '''

ampl_run_file = 'run.run'


instruction_text_manage_groups = '''
¿Qué deseas realizar?

1- Listar casos de un grupo.
2- Ingresar casos en un grupo.
3- Organizar casos de un grupo.
4- Mover casos de un grupo a otro.
5- Eliminar casos de un grupo.
6- Validar casos repetidos.

Ingresa un número: '''


instruction_text_manage_groups_add_case = 'Digite el nombre del caso que deseas agrupar (deja en blanco para terminar de agregar casos): '


instruction_text_manage_groups_sort = f'''
¿Qué grupo deseas organizar?

{groups_indexes_text}

Ingresa un número: '''


instruction_text_manage_groups_add = f'''
¿En qué grupo deseas ingresar casos?

{groups_indexes_text}

Ingresa un número: '''

instruction_text_manage_groups_remove = f'''
¿En qué grupo deseas eliminar casos?

{groups_indexes_text}

Ingresa un número: '''


instruction_text_manage_groups_move_from = f'''
¿Desde qué grupo deseas mover los casos?

{groups_indexes_text}

Ingresa un número: '''


instruction_text_manage_groups_move_to = f'''
¿Hacia qué grupo deseas mover los casos?

{groups_indexes_text}

Ingresa un número: '''


instruction_text_manage_groups_move_case = 'Digite el nombre del caso que mover (deja en blanco para terminar de agregar casos): '


instruction_text_manage_groups_list = f'''
¿De qué grupo deseas listar los casos?

{groups_indexes_text}

Ingresa un número: '''


instruction_text_manage_groups_validate = f'''
¿De qué grupo deseas validar casos repetidos?

{groups_indexes_text}

Ingresa un número: '''


def validate_instruction(options: int, instruction: str):
    '''Valida las instrucciones ingresadas por el usuario'''

    # Si no se ingresa ninguna instrucción, se asume finalización del programa
    if not instruction:
        sys.exit(0)

    if not instruction in [f'{i}' for i in range(1, options + 1)]:
        print('Instrucción no encontrada ❌!')
        sys.exit(1)


def get_group_name(group: int) -> str:
    '''Obtiene el nombre del archivo con base en el índice seleccionado por el usuario'''

    return possible_groups[group - 1]


def save_case_in_group(case: str, group: str):
    '''Guardar el caso en un grupo'''

    found = False
    group_file = f'{group}.txt'
    try:
        with open(f'{cases_group_dir}/{group_file}', 'r', encoding='utf-8') as f:
            for linea in f:
                if linea.strip() == case:
                    found = True
                    break

    except FileNotFoundError:
        print(f"Nota: El archivo '{group_file}' no existía. Se creará.")
        pass
    except IOError as e:
        print(f"Error al leer el archivo '{group_file}': {e}")
        return

    if not found:
        try:
            with open(f'{cases_group_dir}/{group_file}', 'a', encoding='utf-8') as f:
                f.write(f"{case}\n")
            print(f"Caso '{case}' agregado a '{group}'.")
        except IOError as e:
            print(f"Error al escribir en el archivo '{group}': {e}")
    else:
        print(
            f"El caso '{case}' ya existe en '{group}'. No se agregó.")


def get_cases_by_group():
    '''Función para obtener casos por grupo'''

    group = input(instruction_text_v2_group)
    validate_instruction(len(possible_groups), group)
    group_name = get_group_name(int(group))

    cases = []
    try:
        with open(f'{cases_group_dir}/{group_name}.txt', 'r') as archivo:
            for case in archivo:
                case = case.strip()
                if case:
                    cases.append(case)

    except FileNotFoundError:
        print(f"Error: El archivo '{group_name}.txt' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    return cases


def save_file_case(width: str, height: str, ocupation: str, the_triads: list[list[str, str, str]]):
    '''Guardar caso'''

    if ocupation:
        nombre_archivo = f'{width}_{height}_{ocupation}.txt'
    else:
        nombre_archivo = f'{width}_{height}.txt'
    try:
        with open(f'{cases_dir}/{nombre_archivo}', 'w') as f:
            f.writelines(f'{width},{height}')
            for triad in the_triads:
                f.writelines(
                    f'\n{triad[0]},{triad[1]},{triad[2]}')
        print(f"[ÉXITO] Archivo creado: {nombre_archivo}")
    except IOError as e:
        print(f"[ERROR] No se pudo crear {nombre_archivo}: {e}")


# Manual prompt
# En caso de que se utilice manualmente un portal como ChatGPT o Gemini, este prompt debería ayudar a generar las triadas.
# Cambiar el valor que se busca en YOUR_RESULT
# Define el ancho máximo en YOUR BASE WIDTH y el alto máximo en YOUR BASE HEIGHT
'''
You are a mathematics expert at generating number triads.

A number triad consists of 3 numbers that are multiplied together.

Generate a minimum of 3 number triads such that when summed together, they result in **`YOUR RESULT`**.

Ensure that the first number of the triad is **always the smallest**.

There must be **no repeated triads**.

The numbers in the triads must be less than **`YOUR BASE WIDTH`** and **`YOUR BASE HEIGHT`**.

### Examples (to sum to 2000):

1,10,50
2,5,50
4,5,25
5,10,10

### Examples (to sum to 2880):

6,10,12
8,9,10
6,8,15
4,10,18

Your output must be the triads separated by a comma:

```json
num1,num2,num3
num1,num2,num3
num1,num2,num3
```

Do not return anything else whatsoever, only the triads.
'''

enter_name_case_create_manual = 'Digite el nombre del caso que desea crear manualmente (deje en blanco para terminar de seleccionar casos): '
