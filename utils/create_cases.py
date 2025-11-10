import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel
from ..config import cases_dir, instruction_text_utils_create_case, enter_name_case_format_multiple, system_instruction


class Triads(BaseModel):
    num_1: int
    num_2: int
    num_3: int


def cargar_configuracion():
    '''Validar y cargar variables de entorno'''

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
        contents=contents
    )

    return response.parsed


def create_case(client: genai.Client, case_file: str):

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


def instruction_1(client: genai.Client):
    '''Todos los casos'''

    for case_file in os.listdir(cases_dir):
        case = case_file.split('.')[0]
        create_case(client, case)


def instruction_2(client: genai.Client):
    '''Determinados casos'''

    selected_cases = []
    while True:
        case_file = input(enter_name_case_format_multiple)
        if case_file == '':
            break
        selected_cases.append(case_file)

    for case_file in selected_cases:
        create_case(client, case_file)


def instruction_3(client: genai.Client):
    '''Un caso único'''

    case_file = input(enter_name_case_format_multiple)
    create_case(client, case_file)


def run():

    instruction = input(instruction_text_utils_create_case)
    if not instruction in ['1', '2', '3']:
        print('Instrucción no encontrada ❌!')
        return

    config = cargar_configuracion()
    client: genai.Client = genai.Client(api_key=config['API_KEY'])

    if instruction == '1':
        instruction_1(client)
    if instruction == '2':
        instruction_2(client)
    if instruction == '3':
        instruction_3(client)
