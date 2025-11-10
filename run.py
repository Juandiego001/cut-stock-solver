from v2.run import run as v2
from ampl.generate_data import run as generate_ampl_data
from ampl.run_case import run as run_ampl_case
from utils.create_cases import run as create_cases
from utils.validate_cases import run as validate_cases
from utils.get_ocupation import run as get_ocupation
from config import instruction_text_main


def run():

    instruction = input(instruction_text_main)
    if not instruction in ['1', '2', '3', '4', '5', '6']:
        print('Instrucción no encontrada ❌!')
        return

    if instruction == '1':
        v2()
    if instruction == '2':
        run_ampl_case()
    if instruction == '3':
        generate_ampl_data()
    if instruction == '4':
        create_cases()
    if instruction == '5':
        validate_cases()
    if instruction == '6':
        get_ocupation()


if __name__ == '__main__':
    run()
