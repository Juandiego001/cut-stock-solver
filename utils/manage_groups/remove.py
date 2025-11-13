import os
import shutil
from .sort import sort
from config import cases_dir, instruction_text_manage_groups_add_case, save_case_in_group, cases_group_dir


def remove_no_prompt(group: str, cases: set):
    '''Eliminar casos de un grupo (enviando los casos por parámetros)'''

    group_file = f'{group}.txt'
    temp_filename = 'temp.txt'
    try:
        with open(f'{cases_group_dir}/{group_file}', 'r') as fin, open(temp_filename, 'w') as fout:
            for line in fin:
                if line.strip() not in cases:
                    fout.write(line)

        shutil.move(temp_filename, f'{cases_group_dir}/{group_file}')
        print(f"El archivo '{group}' ha sido actualizado.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{group_file}'.")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def remove(group: str):
    '''Eliminar casos de un grupo'''

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

    remove_no_prompt(group, set(cases))
    sort(f'{group}.txt')
