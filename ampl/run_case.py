import os
from amplpy import AMPL
from pathlib import Path
from datetime import datetime
from config import ampl_data_dir, instruction_text_ampl_run_case, enter_name_case_format_multiple, ampl_run_file, enter_name_case_format, ampl_run_cases_reports_dir


def save_report(report_folder: str,
                case: str,
                z: str,
                _ampl_elapsed_time: str,
                _total_solve_elapsed_time: str,
                solve_result_num: str):

    if not os.path.exists(f'{report_folder}/summary.txt'):
        with open(f'{report_folder}/summary.txt', 'a+') as archivo:
            archivo.write(
                f'Caso\t\t|\tDesperdicio\t|\tAMPL Elapsed Time\t|\tTotal Solve Elapsed Time\t|\tStatus\n{"-" * 97}\n')

    with open(f'{report_folder}/summary.txt', 'a+') as archivo:
        archivo.write(
            f'{case}\t|\t{z}\t\t|\t{_ampl_elapsed_time:.6f}\t\t\t|\t{_total_solve_elapsed_time:.6f}\t\t\t\t\t|\t{solve_result_num}\n')


class SilenciosoOutputHandler:
    """Ignora toda la salida de AMPL."""

    def output(self, kind, msg):
        pass


def ejecutar_modelo_ampl(report_folder: str, case: str):
    """
    Ejecuta un script .run de AMPL, inyectando dinámicamente
    el nombre del archivo .dat.

    Args:
        report_folder (str): Generación de reportes.
        data (str): Ruta al archivo .dat que se debe cargar (ej: "50_50_90.dat")
    """

    data = f'{case}.dat'
    if not os.path.exists(f'{ampl_data_dir}/{ampl_run_file}'):
        print(f"Error: No se encuentra el script .run: {ampl_run_file}")
        return
    if not os.path.exists(f'{ampl_data_dir}/{data}'):
        print(f"Error: No se encuentra el archivo de datos: {data}")
        return

    try:
        ampl: AMPL = AMPL()
        ampl.set_output_handler(SilenciosoOutputHandler())
        ampl.set_option('solver_msg', False)
        ampl.cd(ampl_data_dir)
        ampl.eval("param data_file_path symbolic;")
        ampl.param["data_file_path"] = os.path.join(ampl_data_dir, data)
        print(f"--- Ejecutando '{ampl_run_file}' con datos de '{data}' ---")
        ampl.read(f'{ampl_data_dir}/{ampl_run_file}')

        z = ampl.get_objective('z').value()
        _ampl_elapsed_time = ampl.get_parameter("_ampl_elapsed_time").value()
        _total_solve_elapsed_time = ampl.get_parameter(
            "_total_solve_elapsed_time").value()
        solve_result_num = ampl.get_parameter("solve_result_num").value()

        save_report(report_folder,
                    case,
                    z,
                    _ampl_elapsed_time,
                    _total_solve_elapsed_time,
                    solve_result_num)

    except Exception as e:
        print(f"Ha ocurrido un error durante la ejecución de AMPL: {e}")
    finally:
        if 'ampl' in locals():
            ampl.close()

    print("-" * 50)


def instruction_1(report_folder: str):
    '''Todos los casos'''

    all_data_files = [f.name for f in Path(ampl_data_dir).glob('*.dat')]
    for case_file in all_data_files:
        case = case_file.split('.')[0]
        ejecutar_modelo_ampl(report_folder, case)


def instruction_2(report_folder: str):
    '''Determinados casos'''

    selected_cases = []
    while True:
        case_file = input(enter_name_case_format_multiple)
        if case_file == '':
            break
        selected_cases.append(case_file)
    for case_file in selected_cases:
        ejecutar_modelo_ampl(report_folder, case_file)


def instruction_3(report_folder: str):
    '''Un caso único'''

    case_file = input(enter_name_case_format)
    ejecutar_modelo_ampl(report_folder, case_file)


def run():

    instruction = input(instruction_text_ampl_run_case)

    if not instruction in ['1', '2', '3']:
        print('Instrucción no encontrada ❌!')
        return

    date_now = str(datetime.now().replace(microsecond=0)
                   ).replace(' ', '_').replace(':', '_')
    report_folder = f'{ampl_run_cases_reports_dir}/report_{date_now}'
    os.mkdir(report_folder)

    if instruction == '1':
        instruction_1(report_folder)
    if instruction == '2':
        instruction_2(report_folder)
    if instruction == '3':
        instruction_3(report_folder)
