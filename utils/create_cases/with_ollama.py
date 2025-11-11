from typing import List
from pydantic import BaseModel
from config import cases_dir, system_instruction
from ollama import Client, GenerateResponse


class Triads(BaseModel):
    num_1: int
    num_2: int
    num_3: int


class TriadsList(BaseModel):
    triads: List[Triads]


def call_llm(client: Client, target: int, width: str, height: str):

    if width == height:
        prompt = f'''Generate the necessary triads that result in {target}. The numbers in the triads must not be greater than {width}.

Ensure that the first number of each triad is the smallest, and avoid the triads repeating their last two numbers.'''
    else:
        prompt = f'''Generate the necessary triads that result in {target}. The numbers in the triads must not be greater than {width} or {height}.

Ensure that the first number of each triad is the smallest, and avoid the triads repeating their last two numbers.'''

    response: GenerateResponse = client.generate(
        model='llama3.1:70b',
        system=system_instruction,
        prompt=prompt,
        options={
            'num_ctx': 8192,
            'temperature': 0.1
        },
        stream=False,
        format=TriadsList.model_json_schema()
    ).response
    print(response)
    response_model = TriadsList.model_validate_json(response)
    return response_model.triads


def create_case(client: Client, case_file: str):

    print(f"Iniciando con: {case_file}")
    width, height, ocupation = case_file.split('_')
    target_value = round(int(width) * int(height) * (int(ocupation)/100))
    the_triads: list[Triads] = call_llm(client, target_value, width, height)
    print(f"Finalizado")

    # nombre_archivo = f'{width}_{height}_{ocupation}.txt'
    # try:
    #     with open(f'{cases_dir}/{nombre_archivo}', 'w') as f:
    #         f.writelines(f'{width},{height}')
    #         for triad in the_triads:
    #             f.writelines(
    #                 f'\n{triad.num_1},{triad.num_2},{triad.num_3}')
    #     print(f"[ÉXITO] Archivo creado: {nombre_archivo}")
    # except IOError as e:
    #     print(f"[ERROR] No se pudo crear {nombre_archivo}: {e}")
