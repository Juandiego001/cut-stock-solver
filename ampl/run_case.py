import os
from amplpy import AMPL
from pathlib import Path
from config import ampl_data_dir, instruction_text_ampl_run_case, enter_name_case_format_multiple, ampl_run_file, enter_name_case_format


def ejecutar_modelo_ampl(data: str):
    """
    Ejecuta un script .run de AMPL, inyectando dinámicamente
    el nombre del archivo .dat.

    Args:
        ampl_run_file (str): Ruta al script .run modificado (ej: "script_dinamico.run")
        data (str): Ruta al archivo .dat que se debe cargar (ej: "50_50_90.dat")
    """

    data = f'{data}.dat'
    # Validar que los archivos existen
    if not os.path.exists(f'{ampl_data_dir}/{ampl_run_file}'):
        print(f"Error: No se encuentra el script .run: {ampl_run_file}")
        return
    if not os.path.exists(f'{ampl_data_dir}/{data}'):
        print(f"Error: No se encuentra el archivo de datos: {data}")
        return

    try:
        ampl: AMPL = AMPL()
        ampl.cd(ampl_data_dir)
        ampl.eval("param data_file_path symbolic;")
        ampl.param["data_file_path"] = os.path.join(ampl_data_dir, data)
        print(
            f"--- Ejecutando '{ampl_run_file}' con datos de '{data}' ---")
        ampl.read(f'{ampl_data_dir}/{ampl_run_file}')

        print("\n--- Resultados (extraídos en Python) ---")

        # Obtener el valor de la función objetivo
        z = ampl.get_objective('z').value()
        print(f"Valor de la función objetivo (z): {z}")

        # Obtener los parámetros de tiempo que calculaste
        t_carga = ampl.get_parameter("t_carga").value()
        t_solve = ampl.get_parameter("t_solve").value()

        print(f"Tiempo de Carga (t_carga): {t_carga:.4f}s")
        print(f"Tiempo de Solución (t_solve): {t_solve:.4f}s")

    except Exception as e:
        print(f"Ha ocurrido un error durante la ejecución de AMPL: {e}")
    finally:
        if 'ampl' in locals():
            ampl.close()

    print("-" * 50)


def instruction_1():
    '''Todos los casos'''

    all_data_files = [f.name for f in Path(ampl_data_dir).glob('*.dat')]
    for case_file in all_data_files:
        case = case_file.split('.')[0]
        ejecutar_modelo_ampl(case)


def instruction_2():
    '''Determinados casos'''

    selected_cases = []
    while True:
        case_file = input(enter_name_case_format_multiple)
        if case_file == '':
            break
        selected_cases.append(case_file)
    for case_file in selected_cases:
        ejecutar_modelo_ampl(case_file)


def instruction_3():
    '''Un caso único'''

    case_file = input(enter_name_case_format)
    ejecutar_modelo_ampl(case_file)


def run():

    instruction = input(instruction_text_ampl_run_case)

    if not instruction in ['1', '2', '3']:
        print('Instrucción no encontrada ❌!')
        return

    if instruction == '1':
        instruction_1()
    if instruction == '2':
        instruction_2()
    if instruction == '3':
        instruction_3()
