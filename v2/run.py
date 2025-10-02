import os
import copy
from datetime import datetime
from classes import Item, Solution
from multiprocessing import Process
from main import generate_solution, vecindario_2opt, vecindario_insertions, vecindario_swap
from gen_reports.gen_reports_excel import create_sheets_iterations, create_sheets_summary, write_iterations_summary, write_solution_debug, write_solution_info, write_solution_iteration_info, write_test_case


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
    f = open(f'./cases/small/{case}.txt', 'r')
    lineas_archivo = f.readlines()
    ancho_grande = int(lineas_archivo[0])
    largo_grande = int(lineas_archivo[1])

    for line in lineas_archivo[2:]:
        id, demanda, ancho, largo = line.split(',')
        demanda.replace('\n', '')  # Se remueve el último salto de línea

        for i in range(int(demanda)):
            item = Item(int(id), int(demanda), int(ancho), int(largo))
            items.append(item)

    f.close()
    return ancho_grande, largo_grande, items


def generate_reports(report_folder, data):
    '''Generar reportes de excel'''

    test_case = data['test_case']
    sol_ini: Solution = data['sol_ini']
    vecinos_summary = data['vecinos_summary']
    mejor_solucion: Solution = data['mejor_solucion']
    iterations = data['iterations']

    case = test_case['case']
    items = test_case['items']

    wb_summary = create_sheets_summary()
    write_test_case(wb_summary['Caso'], {
        'ancho_grande': test_case['ancho_grande'],
        'largo_grande': test_case['largo_grande'],
        'items': items
    })

    '''Escribir la solución inicial'''
    write_solution_info(wb_summary['SolInicial_Info'], sol_ini)
    write_solution_debug(wb_summary['SolInicial_Debug'], sol_ini.matrixes)

    '''Escribir el resumen de las iteraciones'''
    for iter, fit_swap, fit_insertions, fit_2opt, best in vecinos_summary:
        write_iterations_summary(wb_summary['Iteraciones'],
                                 iter,
                                 fit_swap,
                                 fit_insertions,
                                 fit_2opt,
                                 best)

    '''Escribir la solución'''
    write_solution_info(wb_summary['Solucion_Info'], mejor_solucion)
    write_solution_debug(wb_summary['Solucion_Debug'], mejor_solucion.matrixes)

    wb_summary.save(f'{report_folder}/{case}_summary.xlsx')
    wb_summary.close()

    '''Escribir el detalle de las iteraciones'''
    os.mkdir(f'{report_folder}/swap')
    os.mkdir(f'{report_folder}/insertions')
    os.mkdir(f'{report_folder}/2opt')

    all_vecinos_swap = iterations['all_vecinos_swap']
    all_vecinos_insertions = iterations['all_vecinos_insertions']
    all_vecinos_2opt = iterations['all_vecinos_2opt']

    for i, iter in enumerate(range(iterations['count'])):

        wb_swap_iteration = create_sheets_iterations(iter)
        write_solution_iteration_info(
            wb_swap_iteration['Info'], all_vecinos_swap[i][0])
        wb_swap_iteration.save(f'{report_folder}/swap/{iter}.xlsx')
        wb_swap_iteration.close()

        wb_insertions_iteration = create_sheets_iterations(iter)
        write_solution_iteration_info(
            wb_insertions_iteration['Info'], all_vecinos_insertions[i][0])
        wb_insertions_iteration.save(f'{report_folder}/insertions/{iter}.xlsx')
        wb_insertions_iteration.close()

        wb_2opt_iteration = create_sheets_iterations(iter)
        write_solution_iteration_info(
            wb_2opt_iteration['Info'], all_vecinos_2opt[i][0])
        wb_2opt_iteration.save(f'{report_folder}/2opt/{iter}.xlsx')
        wb_2opt_iteration.close()

        os.mkdir(f'{report_folder}/swap/{iter}')
        for index, j in enumerate(all_vecinos_swap[i][0]):
            wb_swap_iteration = create_sheets_iterations(iter)
            write_solution_info(wb_swap_iteration['Info'], j)
            write_solution_debug(wb_swap_iteration['Debug'], j.matrixes)
            wb_swap_iteration.save(f'{report_folder}/swap/{iter}/{index}.xlsx')
            wb_swap_iteration.close()

        os.mkdir(f'{report_folder}/insertions/{iter}')
        for index, j in enumerate(all_vecinos_insertions[i][0]):
            wb_insertions_iteration = create_sheets_iterations(iter)
            write_solution_info(wb_insertions_iteration['Info'], j)
            write_solution_debug(wb_insertions_iteration['Debug'], j.matrixes)
            wb_insertions_iteration.save(f'{report_folder}/insertions/{iter}/{index}.xlsx')
            wb_insertions_iteration.close()

        os.mkdir(f'{report_folder}/2opt/{iter}')
        for index, j in enumerate(all_vecinos_2opt[i][0]):
            wb_2opt_iteration = create_sheets_iterations(iter)
            write_solution_info(wb_2opt_iteration['Info'], j)
            write_solution_debug(wb_2opt_iteration['Debug'], j.matrixes)
            wb_2opt_iteration.save(f'{report_folder}/2opt/{iter}/{index}.xlsx')
            wb_2opt_iteration.close()

        iter += 1


def vns(report_folder, case, with_reports=True):
    '''Función de búsqueda local'''

    '''Creación de carpeta para cada caso'''
    report_folder = f'{report_folder}/{case}'
    os.mkdir(report_folder)

    ancho_grande, largo_grande, items = lectura(case)

    sol_ini = generate_solution(ancho_grande, largo_grande, items)

    mejor_vecino = mejor_solucion = copy.deepcopy(sol_ini)

    '''Variables para generar al final los reportes de excel'''
    vecinos_summary = []
    all_vecinos_swap = []
    all_vecinos_insertions = []
    all_vecinos_2opt = []

    iteration = 1
    while True:
        mejor_vecino_swap, vecinos_swap = vecindario_swap(
            ancho_grande, largo_grande, mejor_solucion.permutation)
        mejor_vecino_insertions, vecinos_insertions = vecindario_insertions(
            ancho_grande, largo_grande, mejor_solucion.permutation)
        mejor_vecino_2opt, vecinos_2opt = vecindario_2opt(
            ancho_grande, largo_grande, mejor_solucion.permutation)

        '''Almacenar para reporte'''
        vecinos_summary.append((iteration,
                                mejor_vecino_swap.fitness,
                                mejor_vecino_insertions.fitness,
                                mejor_vecino_2opt.fitness,
                                mejor_solucion.fitness))

        all_vecinos_swap.append((vecinos_swap, iteration))
        all_vecinos_insertions.append((vecinos_insertions, iteration))
        all_vecinos_2opt.append((vecinos_2opt, iteration))

        '''Se determina el mejor vecino'''
        if mejor_vecino_swap.fitness < mejor_vecino_insertions.fitness and mejor_vecino_swap.fitness < mejor_vecino_2opt.fitness:
            mejor_vecino = mejor_vecino_swap
        elif mejor_vecino_insertions.fitness < mejor_vecino_swap.fitness and mejor_vecino_insertions.fitness < mejor_vecino_2opt.fitness:
            mejor_vecino = mejor_vecino_insertions
        elif mejor_vecino_2opt.fitness < mejor_vecino_swap.fitness and mejor_vecino_2opt.fitness < mejor_vecino_insertions.fitness:
            mejor_vecino = mejor_vecino_2opt
        else:
            # Si todos son iguales, se toma el mejor vecino de swap
            mejor_vecino = mejor_vecino_swap

        '''
        Si el mejor vecino es mejor que la mejor solución iterada, entonces actualice la mejor solución iterada,
        de lo contrario termine el ciclo
        '''
        if mejor_vecino.fitness < mejor_solucion.fitness:
            mejor_solucion = mejor_vecino
        else:
            break

        iteration += 1

    print(f'Case {case}, iterations: {iteration}')

    data = {
        'test_case': {
            'case': case,
            'ancho_grande': ancho_grande,
            'largo_grande': ancho_grande,
            'items': items,
        },
        'sol_ini': sol_ini,
        'vecinos_summary': vecinos_summary,
        'mejor_solucion': mejor_solucion,
        'iterations': {
            'count': iteration,
            'all_vecinos_swap': all_vecinos_swap,
            'all_vecinos_insertions': all_vecinos_insertions,
            'all_vecinos_2opt': all_vecinos_2opt
        }
    }

    generate_reports(report_folder, data)


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
            p = Process(target=vns, args=(report_folder, case))
            all_processes.append(p)

        for each_process in all_processes:
            each_process.start()

        for each_process in all_processes:
            each_process.join()
    else:
        case_file = input(
            'Digite el nombre del caso que desea ejecutar (o dejar en blanco para test1): ')
        case_file = 'test1' if not case_file else case_file
        vns(report_folder, case_file)

    '''Tiempo final'''
    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')
