import os
from .sort import sort
from config import cases_dir, instruction_text_manage_groups_add_case, save_case_in_group


def add_no_prompt(group: str, cases: list):
    '''Ingresa casos en un grupo (enviando los casos por parámetros)'''

    for case in cases:
        save_case_in_group(case, group)


def add(group: str):
    '''Ingresa casos en un grupo'''

    cases = []
    while True:
        case = input(instruction_text_manage_groups_add_case)
        if not case:
            break
        if not os.path.exists(f'{cases_dir}/{case}.txt'):
            print(
                f'El caso {case}.txt no existe ❌. Continuando con otro caso...')
            continue
        cases.append(case)

    add_no_prompt(group, cases)
    sort(f'{group}.txt')
    print('Finalizando adición de casos en grupo.')
