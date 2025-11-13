import os
from .remove import remove_no_prompt
from .add import add_no_prompt
from .sort import sort
from config import cases_dir, instruction_text_manage_groups_move_case


def move(group_from: str, group_to: str):
    '''Mover casos de un grupo a otro'''

    cases = []
    while True:
        case = input(instruction_text_manage_groups_move_case)
        if not case:
            break
        if not os.path.exists(f'{cases_dir}/{case}.txt'):
            print(
                f'El caso {case}.txt no existe ❌. Continuando con otro caso...')
            continue
        cases.append(case)

    # Primero se remueven
    remove_no_prompt(group_from, set(cases))
    # Luego se agregan
    add_no_prompt(group_to, cases)
    # Luego se ordenan los dos grupos
    sort(f'{group_from}.txt')
    sort(f'{group_to}.txt')
