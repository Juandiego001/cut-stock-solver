import os
from config import cases_dir, instruction_text_utils_validate_cases, enter_name_case, enter_name_case_multiple, validate_instruction,\
    instruction_text_utils_validate_cases_group, get_group_name, possible_groups, get_cases_by_group


def buscar_pieza(x, y, piezas):
    '''Busca si existe la pieza en la lista sin importar el orden'''

    return (x, y) in piezas or (y, x) in piezas


def validate_cases(case_file: str):

    print(f'\nCaso {case_file}.')
    f_test = open(f'{cases_dir}/{case_file}.txt', 'r')
    lines = f_test.readlines()

    ancho_base, largo_base = lines[0].split(',')
    ancho_base, largo_base = int(ancho_base), int(largo_base)

    piezas = []
    for i in range(1, len(lines)):
        _, ancho, largo = lines[i].split(',')
        ancho = int(ancho)
        largo = int(largo)

        if buscar_pieza(ancho, largo, piezas):
            print(
                f'¡Atención! La pieza {i} con dimensiones {int(ancho)} x {int(largo)} ya existía ❌')
            return

        if (ancho > ancho_base) and (ancho > largo_base):
            print(
                f'¡Atención! La pieza {i} tiene la dimensión del ancho "{ancho}" mayor que las dimensiones base ❌')
            return
        if (largo > ancho_base) and (largo > largo_base):
            print(
                f'¡Atención! La pieza {i} tiene la dimensión del largo "{largo}" mayor que las dimensiones base ❌')
            return

        piezas.append((ancho, largo))

    print('Todo correcto ✅')


def instruction_1():
    '''Todos los casos'''

    for case_file in os.listdir(cases_dir):
        case = case_file.split('.')[0]
        validate_cases(case)


def instruction_2():
    '''Determinados casos'''

    selected_cases = []
    while True:
        case = input(enter_name_case_multiple)
        if case == '':
            break
        selected_cases.append(case)

    for case in selected_cases:
        validate_cases(case)


def instruction_3():
    '''Grupo de casos'''

    cases = get_cases_by_group()
    for case in cases:
        validate_cases(case)


def instruction_4():
    '''Un caso único'''

    case = input(enter_name_case)
    validate_cases(case)


def run():

    instruction = input(instruction_text_utils_validate_cases)
    validate_instruction(4, instruction)

    if instruction == '1':
        instruction_1()
    if instruction == '2':
        instruction_2()
    if instruction == '3':
        instruction_3()
    if instruction == '4':
        instruction_4()
