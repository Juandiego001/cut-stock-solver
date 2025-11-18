import os
import sys
from google import genai
from ollama import Client
from openai import OpenAI
from dotenv import load_dotenv
from .with_gemini import create_case as create_case_gemini
from .with_ollama import create_case as create_case_ollama
from .with_openai import create_case as create_case_openai
from config import cases_dir, instruction_text_utils_create_case, enter_name_case_multiple, instruction_text_utils_create_case_ai_instruction, \
    instruction_text_utils_create_case_ask_save, instruction_text_utils_create_case_group_save, possible_groups, groups_indexes_text, \
    validate_instruction, get_group_name, save_case_in_group, enter_name_case_create_manual, save_file_case


def invalid_env(missin_env: str):
    '''Muestra un error relacionado con la variable de entorno faltante y finaliza el script'''

    print(f"\n--- ERROR FATAL ---")
    print(f"La variable de entorno '{missin_env}' no ha sido establecida.")
    print("El programa no puede continuar sin esta configuración.")
    sys.exit(1)


def get_client(ai_library_instruction: str):
    '''Validar variables de entorno y obtener el cliente correspondiente'''

    load_dotenv()

    if ai_library_instruction == '1':
        OLLAMA_HOST = os.environ.get('OLLAMA_HOST')
        if not OLLAMA_HOST:
            invalid_env('OLLAMA_HOST')

        return Client(host=OLLAMA_HOST)

    if ai_library_instruction == '2':
        GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        if not GEMINI_API_KEY:
            invalid_env('GEMINI_API_KEY')

        return genai.Client(api_key=GEMINI_API_KEY)

    if ai_library_instruction == '3':
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        if not OPENAI_API_KEY:
            invalid_env('OPENAI_API_KEY')

        return OpenAI(api_key=OPENAI_API_KEY)


def instruction_1(save_func: function, client: genai.Client | Client | OpenAI, create_case: function):
    '''Todos los casos'''

    for case_file in os.listdir(cases_dir):
        case = case_file.split('.')[0]
        create_case(client, case)
        save_func(case)


def instruction_2(save_func: function, client: genai.Client | Client | OpenAI, create_case: function):
    '''Determinados casos'''

    selected_cases = []
    while True:
        case = input(enter_name_case_multiple)
        if case == '':
            break
        selected_cases.append(case)

    for case in selected_cases:
        create_case(client, case)
        save_func(case)


def instruction_3(save_func: function, client: genai.Client | Client | OpenAI, create_case: function):
    '''Un caso único'''

    case = input(enter_name_case_multiple)
    create_case(client, case)
    save_func(case)


def get_manual_items(case: str, target: str):
    '''Obtener manualmente las demandas'''

    if target:
        print(
            f"Ingresa las demandas para el caso {case} - Objetivo: {target}. Deja vacío para dejar de agregar demandas: ")
    else:
        print(
            f"Ingresa las demandas para el caso {case}. Deja vacío para dejar de agregar demandas: ")
    triads = []
    while True:
        try:
            line = input()
            if line == '':
                break
        except EOFError:
            break
        triads.append(line.split(','))
    return triads


def instruction_4(save_func: function):
    '''Crear casos manualmente'''

    selected_cases: list[str] = []
    while True:
        case = input(enter_name_case_create_manual)
        if case == '':
            break
        selected_cases.append(case)

    for case in selected_cases:
        data = case.split('_')
        width, height, ocupation = (data[0], data[1], data[2] if len(data) > 2 else None)
        if ocupation:
            target = int(int(width) * int(height) * (int(ocupation)/100))
            the_triads = get_manual_items(case, str(target))
        else:
            the_triads = get_manual_items(case, '')

        save_file_case(width, height, ocupation, the_triads)
        save_func(case)


def ask_save_group(case: str):
    '''Preguntar al usuario en qué grupo se guarda el caso'''

    group = input(f'''
¿En qué grupo deseas guardar el caso {case}?

{groups_indexes_text}

Ingresa un número: ''')

    validate_instruction(len(possible_groups), group)
    save_case_in_group(case, get_group_name(int(group)))


def get_user_instructions():
    '''Obtener indicaciones sobre cómo ejecutar el script'''

    instruction = input(instruction_text_utils_create_case)
    validate_instruction(4, instruction)

    save_cases_instruction = input(instruction_text_utils_create_case_ask_save)
    validate_instruction(3, save_cases_instruction)

    def save_func(x): return None
    if save_cases_instruction == '1':
        group = input(instruction_text_utils_create_case_group_save)
        validate_instruction(4, group)
        def save_func(x): return save_case_in_group(
            x, get_group_name(int(group)))

    if save_cases_instruction == '2':
        def save_func(x): return ask_save_group(x)

    if instruction == '4':
        return instruction, save_func, None

    ai_library_instruction = input(
        instruction_text_utils_create_case_ai_instruction)
    validate_instruction(3, ai_library_instruction)

    return instruction, save_func, ai_library_instruction


def run():

    instruction, save_func, ai_library_instruction = get_user_instructions()
    client: genai.Client | Client | OpenAI = get_client(ai_library_instruction)

    if ai_library_instruction == '1':
        create_case = create_case_ollama
    elif ai_library_instruction == '2':
        create_case = create_case_gemini
    elif ai_library_instruction == '3':
        create_case = create_case_openai

    if instruction == '1':
        instruction_1(save_func, client, create_case)
    if instruction == '2':
        instruction_2(save_func, client, create_case)
    if instruction == '3':
        instruction_3(save_func, client, create_case)
    if instruction == '4':
        instruction_4(save_func)
