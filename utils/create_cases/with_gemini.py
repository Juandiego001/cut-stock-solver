from google import genai
from google.genai import types
from pydantic import BaseModel
from config import cases_dir, system_instruction, save_file_case


class Triads(BaseModel):
    num_1: int
    num_2: int
    num_3: int


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
    save_file_case(width, height, ocupation, [
                   [triad.num_1, triad.num_2, triad.num_3] for triad in the_triads])
