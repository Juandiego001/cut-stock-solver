import os
from gen_reports.gen_reports_excel import save_solution
from main import sol_inicial
from classes import Item
from datetime import datetime
from multiprocessing import Process


cases_dir = 'cases'


def lectura(case: str):
    '''
    Lectura del archivo de pruebas.

    Consideraciones:
    La primer línea del archivo corresponde al ancho.
    La segunda línea del archivo corresponde al largo.
    Las demás líneas corresponden a los ítems con el siguiente formato:
    Id  Demanda Ancho Largo
    '''

    items = []
    f = open(f'./cases/{case}.txt', 'r')
    lineas_archivo = f.readlines()
    ancho_grande = int(lineas_archivo[0])
    largo_grande = int(lineas_archivo[1])

    for line in lineas_archivo[2:]:
        id, demanda, ancho, largo = line.split(',')
        demanda.replace('\n', '')  # Se remueve el último salto de línea

        for i in range(int(demanda)):
          item = Item(int(id), int(ancho), int(largo))
          items.append(item)

    f.close()
    return ancho_grande, largo_grande, items

def run_case(report_folder, case, with_reports=True):
    '''Función para ejecutar cada caso'''

    '''Creación de carpeta para cada caso'''
    report_folder = f'{report_folder}/{case}'
    os.mkdir(report_folder)

    ancho_grande, largo_grande, items = lectura(case)

    sol_ini = sol_inicial(ancho_grande, largo_grande, items)

    save_solution(sol_ini)



if __name__ == '__main__':

    '''Tiempo inicial'''
    start_date = datetime.now()

    '''Creación de carpeta de reporte'''
    date_now = str(datetime.now().replace(microsecond=0)
                   ).replace(' ', '_').replace(':', '_')
    report_folder = f'./reports/report_{date_now}'
    os.mkdir(report_folder)

    single_or_multiple_cases = input('¿Ejecutar todos los casos? (Y/N): ')
    if single_or_multiple_cases == 'Y':
        all_processes = []
        for case_file in os.listdir(cases_dir):
            case = case_file.split('.')[0]
            p = Process(target=run_case, args=(report_folder, case))
            all_processes.append(p)

        for each_process in all_processes:
            each_process.start()

        for each_process in all_processes:
            each_process.join()
    else:
        case_file = input(
            'Digite el nombre del caso que desea ejecutar (o dejar en blanco para test1): ')
        case_file = 'test1' if not case_file else case_file
        run_case(report_folder, case_file)

    '''Tiempo final'''
    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')