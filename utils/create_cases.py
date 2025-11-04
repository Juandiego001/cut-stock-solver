import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel


cases_dir = '../cases'

format_indication = '''
Digite el nombre del caso con el siguiente formato: ancho_largo_ocupacion.

Ejemplo:
- 55_55_84.
- 63_78_91.
- 61_28_95.
                
(Deje en blanco para terminar de agregar casos): '''


class Triads(BaseModel):
    num_1: int
    num_2: int
    num_3: int


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


def cargar_configuracion():
    """
    Carga las variables de entorno desde un archivo .env
    y verifica que las variables requeridas estén presentes.
    """

    load_dotenv()

    API_KEY = os.environ.get('API_KEY')
    if not API_KEY:
        print(f"\n--- ERROR FATAL ---")
        print(f"La variable de entorno 'API_KEY' no ha sido establecida.")
        print("El programa no puede continuar sin esta configuración.")
        sys.exit(1)

    return {"API_KEY": API_KEY}


def call_llm(client: genai.Client, target: int, width: str, height: str):

    if width == height:
        contents = f'''Generate the necessary triads that result in {target}. The numbers in the triads must not be greater than {width}.

Ensure that the first number of each triad is the smallest, and avoid the triads repeating their last two numbers.'''
    else:
        contents = f'''Generate the necessary triads that result in {target}. The numbers in the triads must not be greater than {width} or {height}.

Ensure that the first number of each triad is the smallest, and avoid the triads repeating their last two numbers.'''

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type='application/json',
            response_schema=list[Triads],
        ),
        contents=contents,
    )

    return response.parsed


def create_case(case_file: str):

    print(f"Iniciando con: {case_file}")
    width, height, ocupation = case_file.split('_')
    target_value = round(int(width) * int(height) * (int(ocupation)/100))
    the_triads: list[Triads] = call_llm(client, target_value, width, height)

    nombre_archivo = f'{width}_{height}_{ocupation}.txt'
    try:
        with open(f'{cases_dir}/{nombre_archivo}', 'w') as f:
            f.writelines(f'{width},{height}')
            for triad in the_triads:
                f.writelines(
                    f'\n{triad.num_1},{triad.num_2},{triad.num_3}')
        print(f"[ÉXITO] Archivo creado: {nombre_archivo}")
    except IOError as e:
        print(f"[ERROR] No se pudo crear {nombre_archivo}: {e}")


if __name__ == "__main__":

    execution_mode = input('''
¿Cómo desea ejecutar la generación de casos?

1- Todos los casos.
2- Determinados casos.
3- Un caso único.

Ingrese un número: ''')

    config = cargar_configuracion()
    client = genai.Client(api_key=config['API_KEY'])

    if execution_mode == '1':
        for case_file in os.listdir(cases_dir):
            create_case(case_file)
    elif execution_mode == '2':
        selected_cases = []
        while True:
            case_file = input(format_indication)

            if case_file == '':
                break
            selected_cases.append(case_file)

        for case_file in selected_cases:
            create_case(case_file)
    else:
        case_file = input(format_indication)
        create_case(case_file)
