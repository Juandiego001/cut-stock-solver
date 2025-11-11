import json
from typing import List
from pydantic import BaseModel
from config import cases_dir, system_instruction_ollama
from ollama import Client, GenerateResponse


class Triads(BaseModel):
    num_1: int
    num_2: int
    num_3: int


class TriadsList(BaseModel):
    triads: List[Triads]


def call_llm(client: Client, target: int, width: str, height: str):

    if width == height:
        prompt = f'''Generate a set of triads to reach a TOTAL SUM closest to {target}.

STRICTLY follow the following rules:
1. **Target Sum:** The SUM of the products of all triads $(a x b x c + d x e x f + ...)$ must be the closest to **{target}**.
2. **Number Limit:** The numbers in the triads $(a, b, c)$ **MUST NOT** be greater than **{width}**.
3. **Order:** The first number of each triad $(a)$ should be the **smallest** $(a <= b$ and $a <= c)$.
4. **No Repetition:** Avoid the triads repeating their last two numbers (if you have $(2, 5, 10)$, you cannot have $(3, 5, 10)$).

Use the `<scratchpad>` format to show your work and then write the final JSON block.'''
    else:
        prompt = f'''Generate a set of triads to reach a TOTAL SUM closest to {target}.

STRICTLY follow the following rules:
1. **Target Sum:** The SUM of the products of all triads $(a x b x c + d x e x f + ...)$ must be the closest to **{target}**.
2. **Number Limit:** The numbers in the triads $(a, b, c)$ **MUST NOT** be greater than **{width}** or **{height}**.
3. **Order:** The first number of each triad $(a)$ should be the **smallest** $(a <= b$ and $a <= c)$.
4. **No Repetition:** Avoid the triads repeating their last two numbers (if you have $(2, 5, 10)$, you cannot have $(3, 5, 10)$).

Use the `<scratchpad>` format to show your work and then write the final JSON block.'''

    response: str = client.generate(
        model='gemma3:27b',
        system=system_instruction_ollama,
        prompt=prompt,
        options={
            'num_ctx': 8192,
            'temperature': 0.1
        },
        stream=False
    ).response

    try:
        json_part = response.split('```json\n')[1].split('\n```')[0]
        triads_list = json.loads(json_part)
        return triads_list
    except Exception as e:
        print(f"\nNo se pudo extraer el JSON. Error: {e}")
        print("Respuesta completa del modelo:\n", response)

    return response


def create_case(client: Client, case_file: str):

    print(f"Iniciando con: {case_file}")
    width, height, ocupation = case_file.split('_')
    target_value = round(int(width) * int(height) * (int(ocupation)/100))
    the_triads: list[list[int, int, int]] = call_llm(client, target_value, width, height)

    nombre_archivo = f'{width}_{height}_{ocupation}.txt'
    try:
        with open(f'{cases_dir}/{nombre_archivo}', 'w') as f:
            f.writelines(f'{width},{height}')
            for triad in the_triads:
                f.writelines(
                    f'\n{triad[0]},{triad[1]},{triad[2]}')
        print(f"[ÉXITO] Archivo creado: {nombre_archivo}")
    except IOError as e:
        print(f"[ERROR] No se pudo crear {nombre_archivo}: {e}")
