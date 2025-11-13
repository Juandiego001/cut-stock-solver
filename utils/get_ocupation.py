import os
from config import cases_dir, instruction_text_utils_get_ocupation, enter_name_case, enter_name_case_multiple, validate_instruction, get_cases_by_group


def get_ocupacion(the_case: str):

    f = open(f'{cases_dir}/{the_case}.txt', 'r')
    lineas_archivo = f.readlines()

    ancho_original_str, largo_original_str = lineas_archivo[0].split(',')
    ancho_original = int(ancho_original_str)  # Ancho de la pieza original
    largo_original = int(largo_original_str)  # Largo de la pieza original

    area_total = ancho_original * largo_original
    print(
        f'Ancho grande: {ancho_original} x Largo grande: {largo_original} = {area_total}')

    total_areas = 0
    lista_permutacion = 0
    for line in lineas_archivo[1:]:
        demanda, ancho, largo = line.split(',')
        demanda = int(demanda)
        ancho = int(ancho)
        largo = int(largo)

        area = demanda*ancho*largo
        total_areas += area
        lista_permutacion += demanda
        print(f'{demanda} x {ancho} x {largo} = {area}')

    print(f'Total suma de áreas: {total_areas}')
    print(f'Total tamaño permutación: {lista_permutacion}')
    print(f'Ocupación: {round((total_areas*100)/area_total, 2)}')
    print('')

    f.close()


def instruction_1():
    '''Todos los casos'''

    for case_file in os.listdir(cases_dir):
        case = case_file.split('.')[0]
        get_ocupacion(case)


def instruction_2():
    '''Determinados casos'''

    selected_cases = []
    while True:
        case = input(enter_name_case_multiple)
        if case == '':
            break
        selected_cases.append(case)

    for case in selected_cases:
        get_ocupacion(case)


def instruction_3():
    '''Grupo de casos'''

    cases = get_cases_by_group()
    for case in cases:
        get_ocupacion(case)


def instruction_4():
    '''Un caso único'''

    case_file = input(enter_name_case)
    get_ocupacion(case_file)


def run():

    instruction = input(instruction_text_utils_get_ocupation)
    validate_instruction(4, instruction)

    if instruction == '1':
        instruction_1()
    if instruction == '2':
        instruction_2()
    if instruction == '3':
        instruction_3()
    if instruction == '4':
        instruction_4()
