import os
import copy
import random
from datetime import datetime
from classes import Item, Solution
from multiprocessing import Process
from main import generate_solution, vecindario_2opt, vecindario_insertions, vecindario_swap
from ..config import instruction_text_v2_run, instruction_text_v2_instruction_5, instruction_text_v2_instruction_3_4
from gen_reports.gen_reports_excel import create_sheets_iterations, create_sheets_summary, write_iterations_summary, write_solution_debug, write_solution_info, write_solution_iteration_info, write_test_case


cases_dir = '../cases'


def lectura(case: str):
    '''
    Lectura de cada archivo de caso.

    Formato.

    ancho,largo
    demanda,ancho,largo
    demanda1,ancho1,largo1
    ...
    demandaN, anchoN, largoN
    '''

    items = []
    f = open(f'../cases/{case}.txt', 'r')
    lineas_archivo = f.readlines()

    ancho_base, largo_base = lineas_archivo[0].split(',')

    for line in lineas_archivo[1:]:
        demanda, ancho, largo = line.split(',')
        for i in range(int(demanda)):
            item = Item(i+1, int(demanda), int(ancho), int(largo))
            items.append(item)

    f.close()
    # random.shuffle(items) # Random
    # items = sorted(items, key=lambda item: item.ancho * item.largo, reverse=True) # De mayor a menor
    items = sorted(items, key=lambda item: item.ancho * item.largo, reverse=False) # De menor a mayor
    return int(ancho_base), int(largo_base), items


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
    # write_solution_debug(wb_summary['SolInicial_Debug'], sol_ini.matrixes)

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
    # write_solution_debug(wb_summary['Solucion_Debug'], mejor_solucion.matrixes)

    wb_summary.save(f'{report_folder}/{case}_summary.xlsx')
    wb_summary.close()

    with open('output.txt', 'a') as archivo:
        archivo.write(f'\n{case}:\tDesperdicio:\t{mejor_solucion.desperdicio}\tFitness:\t{mejor_solucion.fitness}')

    '''Escribir el detalle de las iteraciones'''
    # os.mkdir(f'{report_folder}/swap')
    # os.mkdir(f'{report_folder}/insertions')
    # os.mkdir(f'{report_folder}/2opt')

    # all_vecinos_swap = iterations['all_vecinos_swap']
    # all_vecinos_insertions = iterations['all_vecinos_insertions']
    # all_vecinos_2opt = iterations['all_vecinos_2opt']

    # for i, iter in enumerate(range(iterations['count'])):

    #   wb_swap_iteration = create_sheets_iterations(iter)
    #   write_solution_iteration_info(
    #       wb_swap_iteration['Info'], all_vecinos_swap[i][0])
    #   wb_swap_iteration.save(f'{report_folder}/swap/{iter}.xlsx')
    #   wb_swap_iteration.close()

    #   wb_insertions_iteration = create_sheets_iterations(iter)
    #   write_solution_iteration_info(
    #       wb_insertions_iteration['Info'], all_vecinos_insertions[i][0])
    #   wb_insertions_iteration.save(f'{report_folder}/insertions/{iter}.xlsx')
    #   wb_insertions_iteration.close()

    #   wb_2opt_iteration = create_sheets_iterations(iter)
    #   write_solution_iteration_info(
    #       wb_2opt_iteration['Info'], all_vecinos_2opt[i][0])
    #   wb_2opt_iteration.save(f'{report_folder}/2opt/{iter}.xlsx')
    #   wb_2opt_iteration.close()

    #   os.mkdir(f'{report_folder}/swap/{iter}')
    #   for index, j in enumerate(all_vecinos_swap[i][0]):
    #       wb_swap_iteration = create_sheets_iterations(iter)
    #       write_solution_info(wb_swap_iteration['Info'], j)
    #       write_solution_debug(wb_swap_iteration['Debug'], j.matrixes)
    #       wb_swap_iteration.save(f'{report_folder}/swap/{iter}/{index}.xlsx')
    #       wb_swap_iteration.close()

    #   os.mkdir(f'{report_folder}/insertions/{iter}')
    #   for index, j in enumerate(all_vecinos_insertions[i][0]):
    #       wb_insertions_iteration = create_sheets_iterations(iter)
    #       write_solution_info(wb_insertions_iteration['Info'], j)
    #       write_solution_debug(wb_insertions_iteration['Debug'], j.matrixes)
    #       wb_insertions_iteration.save(f'{report_folder}/insertions/{iter}/{index}.xlsx')
    #       wb_insertions_iteration.close()

    #   os.mkdir(f'{report_folder}/2opt/{iter}')
    #   for index, j in enumerate(all_vecinos_2opt[i][0]):
    #       wb_2opt_iteration = create_sheets_iterations(iter)
    #       write_solution_info(wb_2opt_iteration['Info'], j)
    #       write_solution_debug(wb_2opt_iteration['Debug'], j.matrixes)
    #       wb_2opt_iteration.save(f'{report_folder}/2opt/{iter}/{index}.xlsx')
    #       wb_2opt_iteration.close()

    #   iter += 1


def vns(report_folder, case, with_reports=True):
    '''Función de búsqueda local'''

    report_folder = f'{report_folder}/{case}'
    os.mkdir(report_folder)
    ancho_grande, largo_grande, items = lectura(case)
    sol_ini = generate_solution(ancho_grande, largo_grande, items)
    mejor_vecino = mejor_solucion = copy.deepcopy(sol_ini)

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

        vecinos_summary.append((iteration,
                                mejor_vecino_swap.fitness,
                                mejor_vecino_insertions.fitness,
                                mejor_vecino_2opt.fitness,
                                mejor_solucion.fitness))

        # all_vecinos_swap.append((vecinos_swap, iteration))
        # all_vecinos_insertions.append((vecinos_insertions, iteration))
        # all_vecinos_2opt.append((vecinos_2opt, iteration))

        mejor_vecino = mejor_vecino_swap # Si todos tienen el mismo fitness, se toma el mejor vecino de swap
        if mejor_vecino_swap.fitness < mejor_vecino_insertions.fitness and mejor_vecino_swap.fitness < mejor_vecino_2opt.fitness:
            mejor_vecino = mejor_vecino_swap
        if mejor_vecino_insertions.fitness < mejor_vecino_swap.fitness and mejor_vecino_insertions.fitness < mejor_vecino_2opt.fitness:
            mejor_vecino = mejor_vecino_insertions
        if mejor_vecino_2opt.fitness < mejor_vecino_swap.fitness and mejor_vecino_2opt.fitness < mejor_vecino_insertions.fitness:
            mejor_vecino = mejor_vecino_2opt

        if not(mejor_vecino.fitness < mejor_solucion.fitness):
            break

        mejor_solucion = mejor_vecino
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


def instruction_1(report_folder: str):
    '''Todos los casos (en paralelo)'''

    start_date = datetime.now()
    all_processes: list[Process] = []
    for case_file in os.listdir(cases_dir):
        case = case_file.split('.')[0]
        p = Process(target=vns, args=(report_folder, case))
        all_processes.append(p)

    for each_process in all_processes:
        each_process.start()

    for each_process in all_processes:
        each_process.join()

    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')


def instruction_2(report_folder: str):
    '''Todos los casos (secuencial)'''

    for case_file in os.listdir(cases_dir):
        case = case_file.split('.')[0]
        start_date = datetime.now()
        vns(report_folder, case)
        end_date = datetime.now()
        elapsed_time = (end_date - start_date).seconds
        print(f'Elapsed time: {elapsed_time} seconds for case {case_file}')


def instruction_3(report_folder: str):
    '''Determinados casos (en paralelo)'''

    start_date = datetime.now()
    all_processes: list[Process] = []
    selected_cases = []
    while True:
        case_file = input(instruction_text_v2_instruction_3_4)

        if case_file == '':
            break
        selected_cases.append(case_file)

    for case_file in selected_cases:
        p = Process(target=vns, args=(report_folder, case_file))
        all_processes.append(p)

    for each_process in all_processes:
        each_process.start()

    for each_process in all_processes:
        each_process.join()

    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')


def instruction_4(report_folder: str):
    '''Determinados casos (en secuencial)'''

    selected_cases = []
    while True:
        case_file = input(instruction_text_v2_instruction_3_4)

        if case_file == '':
            break
        selected_cases.append(case_file)

    for case_file in selected_cases:
        start_date = datetime.now()
        vns(report_folder, case_file)
        end_date = datetime.now()
        elapsed_time = (end_date - start_date).seconds
        print(f'Elapsed time: {elapsed_time} seconds for case {case_file}')


def instruction_5(report_folder: str):
    '''Un caso único'''

    case_file = input(instruction_text_v2_instruction_5)
    start_date = datetime.now()
    vns(report_folder, case_file)
    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')


def run():
    
    instruction = input(instruction_text_v2_run)
    if not instruction in ['1', '2', '3', '4', '5']:
        print('Instrucción no encontrada ❌!')
        return
    
    date_now = str(datetime.now().replace(microsecond=0)).replace(' ', '_').replace(':', '_')
    report_folder = f'./reports/report_{date_now}'
    os.mkdir(report_folder)

    if instruction == '1': instruction_1(report_folder)
    if instruction == '2': instruction_2(report_folder)
    if instruction == '3': instruction_3(report_folder)
    if instruction == '4': instruction_4(report_folder)
    if instruction == '5': instruction_5(report_folder)
    