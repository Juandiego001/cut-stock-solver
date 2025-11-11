import os
import sys
from google import genai
from ollama import Client
from openai import OpenAI
from dotenv import load_dotenv
from .with_gemini import create_case as create_case_gemini
from .with_ollama import create_case as create_case_ollama
from .with_openai import create_case as create_case_openai
from config import cases_dir, instruction_text_utils_create_case, enter_name_case_multiple, instruction_text_utils_create_case_ai_instruction


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


def instruction_1(client: genai.Client | Client | OpenAI, create_case: function):
    '''Todos los casos'''

    for case_file in os.listdir(cases_dir):
        case = case_file.split('.')[0]
        create_case(client, case)


def instruction_2(client: genai.Client | Client | OpenAI, create_case: function):
    '''Determinados casos'''

    selected_cases = []
    while True:
        case_file = input(enter_name_case_multiple)
        if case_file == '':
            break
        selected_cases.append(case_file)

    for case_file in selected_cases:
        create_case(client, case_file)


def instruction_3(client: genai.Client | Client | OpenAI, create_case: function):
    '''Un caso único'''

    case_file = input(enter_name_case_multiple)
    create_case(client, case_file)


def get_user_instructions():
    '''Obtener indicaciones sobre cómo ejecutar el script'''

    instruction = input(instruction_text_utils_create_case)
    if not instruction in ['1', '2', '3']:
        print('Instrucción no encontrada ❌!')
        sys.exit(1)

    ai_library_instruction = input(
        instruction_text_utils_create_case_ai_instruction)
    if not ai_library_instruction in ['1', '2', '3']:
        print('Instrucción no encontrada ❌!')
        sys.exit(1)

    return instruction, ai_library_instruction


def run():

    instruction, ai_library_instruction = get_user_instructions()
    client: genai.Client | Client | OpenAI = get_client(ai_library_instruction)

    if ai_library_instruction == '1':
        create_case = create_case_ollama
    elif ai_library_instruction == '2':
        create_case = create_case_gemini
    elif ai_library_instruction == '3':
        create_case = create_case_openai

    if instruction == '1':
        instruction_1(client, create_case)
    if instruction == '2':
        instruction_2(client, create_case)
    if instruction == '3':
        instruction_3(client, create_case)
