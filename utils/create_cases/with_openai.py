from config import cases_dir, system_instruction
from pydantic import BaseModel
from openai import OpenAI


class Triads(BaseModel):
    num_1: int
    num_2: int
    num_3: int

class TriadsList(BaseModel):
    triads: list[Triads]


def call_llm(client: OpenAI, target: int, width: str, height: str):

    if width == height:
        contents = f'''Generate the necessary triads that result in {target}. The numbers in the triads must not be greater than {width}.

Ensure that the first number of each triad is the smallest, and avoid the triads repeating their last two numbers.'''
    else:
        contents = f'''Generate the necessary triads that result in {target}. The numbers in the triads must not be greater than {width} or {height}.

Ensure that the first number of each triad is the smallest, and avoid the triads repeating their last two numbers.'''

    response = client.responses.parse(
        model="gpt-4o-mini-2024-07-18",
        input=[
            {
                "role": "system",
                "content": system_instruction,
            },
            {"role": "user", "content": contents},
        ],
        text_format=TriadsList
    )

    return response.output_parsed


def create_case(client: OpenAI, case_file: str):

    print(f"Iniciando con: {case_file}")
    width, height, ocupation = case_file.split('_')
    target_value = round(int(width) * int(height) * (int(ocupation)/100))
    the_triads: list[Triads] = call_llm(client, target_value, width, height)
    print(the_triads)

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
