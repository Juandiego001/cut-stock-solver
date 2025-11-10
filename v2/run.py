import os
import sys
import copy
import random
from datetime import datetime
from classes import Item, Solution
from multiprocessing import Process
from main import generate_solution, vecindario_2opt, vecindario_insertions, vecindario_swap
from ..config import cases_dir, instruction_text_v2_run, enter_name_case_format_multiple, cases_dir, enter_name_case_format_multiple, enter_name_case_format, instruction_text_v2_with_debug, instruction_text_v2_with_debug_single
from gen_reports.gen_reports_excel import create_sheets_iterations, create_sheets_summary, write_iterations_summary, write_solution_debug, write_solution_info, write_solution_iteration_info, write_test_case


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
    f = open(f'{cases_dir}/{case}.txt', 'r')
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
    items = sorted(items, key=lambda item: item.ancho *
                   item.largo, reverse=False)  # De menor a mayor
    return int(ancho_base), int(largo_base), items


def generate_reports(report_folder,
                     case,
                     ancho_grande,
                     largo_grande,
                     items,
                     sol_ini: Solution,
                     vecinos_summary,
                     mejor_solucion: Solution,
                     iterations,
                     all_vecinos_swap,
                     all_vecinos_insertions,
                     all_vecinos_2opt,
                     debug=False):
    '''Generar reportes de excel'''

    wb_summary = create_sheets_summary()
    write_test_case(wb_summary['Caso'], {
        'ancho_grande': ancho_grande,
        'largo_grande': largo_grande,
        'items': items
    })

    '''Escribir la solución inicial'''
    write_solution_info(wb_summary['SolInicial_Info'], sol_ini)
    if debug:
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
    if debug:
        write_solution_debug(
            wb_summary['Solucion_Debug'], mejor_solucion.matrixes)

    wb_summary.save(f'{report_folder}/{case}_summary.xlsx')
    wb_summary.close()

    # with open('output.txt', 'a') as archivo:
    #     archivo.write(
    #         f'\n{case}:\tDesperdicio:\t{mejor_solucion.desperdicio}\tFitness:\t{mejor_solucion.fitness}')

    '''Escribir el detalle de las iteraciones'''
    if debug:
        os.mkdir(f'{report_folder}/swap')
        os.mkdir(f'{report_folder}/insertions')
        os.mkdir(f'{report_folder}/2opt')

        for i, iter in enumerate(range(iterations)):

            wb_swap_iteration = create_sheets_iterations(iter)
            write_solution_iteration_info(
                wb_swap_iteration['Info'], all_vecinos_swap[i][0])
            wb_swap_iteration.save(f'{report_folder}/swap/{iter}.xlsx')
            wb_swap_iteration.close()

            wb_insertions_iteration = create_sheets_iterations(iter)
            write_solution_iteration_info(
                wb_insertions_iteration['Info'], all_vecinos_insertions[i][0])
            wb_insertions_iteration.save(
                f'{report_folder}/insertions/{iter}.xlsx')
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
                wb_swap_iteration.save(
                    f'{report_folder}/swap/{iter}/{index}.xlsx')
                wb_swap_iteration.close()

            os.mkdir(f'{report_folder}/insertions/{iter}')
            for index, j in enumerate(all_vecinos_insertions[i][0]):
                wb_insertions_iteration = create_sheets_iterations(iter)
                write_solution_info(wb_insertions_iteration['Info'], j)
                write_solution_debug(
                    wb_insertions_iteration['Debug'], j.matrixes)
                wb_insertions_iteration.save(
                    f'{report_folder}/insertions/{iter}/{index}.xlsx')
                wb_insertions_iteration.close()

            os.mkdir(f'{report_folder}/2opt/{iter}')
            for index, j in enumerate(all_vecinos_2opt[i][0]):
                wb_2opt_iteration = create_sheets_iterations(iter)
                write_solution_info(wb_2opt_iteration['Info'], j)
                write_solution_debug(wb_2opt_iteration['Debug'], j.matrixes)
                wb_2opt_iteration.save(
                    f'{report_folder}/2opt/{iter}/{index}.xlsx')
                wb_2opt_iteration.close()

            iter += 1


def vns(report_folder: str, case: str, debug: bool = False):
    '''Función de búsqueda local'''

    report_folder = f'{report_folder}/{case}'
    os.mkdir(report_folder)
    ancho_grande, largo_grande, items = lectura(case)
    sol_ini = generate_solution(ancho_grande, largo_grande, items)
    mejor_vecino = mejor_solucion = copy.deepcopy(sol_ini)

    vecinos_summary = []
    if debug:
        all_vecinos_swap = []
        all_vecinos_insertions = []
        all_vecinos_2opt = []

    iterations = 1
    while True:
        mejor_vecino_swap, vecinos_swap = vecindario_swap(
            ancho_grande, largo_grande, mejor_solucion.permutation, debug)
        mejor_vecino_insertions, vecinos_insertions = vecindario_insertions(
            ancho_grande, largo_grande, mejor_solucion.permutation, debug)
        mejor_vecino_2opt, vecinos_2opt = vecindario_2opt(
            ancho_grande, largo_grande, mejor_solucion.permutation, debug)

        vecinos_summary.append((iterations,
                                mejor_vecino_swap.fitness,
                                mejor_vecino_insertions.fitness,
                                mejor_vecino_2opt.fitness,
                                mejor_solucion.fitness))
        if debug:
            all_vecinos_swap.append((vecinos_swap, iterations))
            all_vecinos_insertions.append((vecinos_insertions, iterations))
            all_vecinos_2opt.append((vecinos_2opt, iterations))

        # Si todos tienen el mismo fitness, se toma el mejor vecino de swap
        mejor_vecino = mejor_vecino_swap
        if mejor_vecino_swap.fitness < mejor_vecino_insertions.fitness and mejor_vecino_swap.fitness < mejor_vecino_2opt.fitness:
            mejor_vecino = mejor_vecino_swap
        if mejor_vecino_insertions.fitness < mejor_vecino_swap.fitness and mejor_vecino_insertions.fitness < mejor_vecino_2opt.fitness:
            mejor_vecino = mejor_vecino_insertions
        if mejor_vecino_2opt.fitness < mejor_vecino_swap.fitness and mejor_vecino_2opt.fitness < mejor_vecino_insertions.fitness:
            mejor_vecino = mejor_vecino_2opt

        if not (mejor_vecino.fitness < mejor_solucion.fitness):
            break

        mejor_solucion = mejor_vecino
        iterations += 1

    print(f'Case {case}, iterations: {iterations}')
    generate_reports(report_folder=report_folder,
                     case=case,
                     ancho_grande=ancho_grande,
                     largo_grande=largo_grande,
                     items=items,
                     sol_ini=sol_ini,
                     vecinos_summary=vecinos_summary,
                     mejor_solucion=mejor_solucion,
                     iterations=iterations,
                     all_vecinos_swap=all_vecinos_swap,
                     all_vecinos_insertions=all_vecinos_insertions,
                     all_vecinos_2opt=all_vecinos_2opt,
                     debug=debug)


def case_debug(instruction: str, case: str):
    '''Procesa los casos para debug'''

    if instruction == '1':
        return True
    if instruction == '2':
        return input(f'¿Ejecutar caso {case} con debug? (y/N): ').upper() == 'Y'
    return False


def check_debug():
    '''Verifica la ejecución con debug'''

    instruction = input(instruction_text_v2_with_debug)
    if not instruction in ['1', '2', '3']:
        print('Instrucción no encontrada ❌!')
        sys.exit(1)

    return instruction


def parallel_execution(report_folder: str, cases: list[str], debug_instruction: str):
    '''Ejecución paralela'''

    all_processes: list[Process] = []
    for case in cases:
        with_debug = case_debug(debug_instruction, case)
        p = Process(target=vns, args=(report_folder, case, with_debug))
        all_processes.append(p)

    start_date = datetime.now()
    for each_process in all_processes:
        each_process.start()
    for each_process in all_processes:
        each_process.join()
    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')


def sequential_execution(report_folder: str, cases: list[str], debug_instruction: str):
    '''Ejecución secuencial'''

    for case in cases:
        with_debug = case_debug(debug_instruction, case)
        start_date = datetime.now()
        vns(report_folder, case, with_debug)
        end_date = datetime.now()
        elapsed_time = (end_date - start_date).seconds
        print(f'Elapsed time: {elapsed_time} seconds for case {case}')


def get_cases():
    '''Función para ir leyendo los casos ingresados por el usuario'''

    cases = []
    while True:
        case_file = input(enter_name_case_format_multiple)
        if case_file == '':
            break
        cases.append(case_file)
    return cases


def instruction_1(report_folder: str):
    '''Todos los casos (en paralelo)'''

    instruction = check_debug()
    cases = [case_file.split('.')[0] for case_file in os.listdir(cases_dir)]
    parallel_execution(report_folder, cases, instruction)


def instruction_2(report_folder: str):
    '''Todos los casos (secuencial)'''

    instruction = check_debug()
    cases = [case_file.split('.')[0] for case_file in os.listdir(cases_dir)]
    sequential_execution(report_folder, cases, instruction)


def instruction_3(report_folder: str):
    '''Determinados casos (en paralelo)'''

    instruction = check_debug()
    cases = get_cases()
    parallel_execution(report_folder, cases, instruction)


def instruction_4(report_folder: str):
    '''Determinados casos (en secuencial)'''

    instruction = check_debug()
    cases = get_cases()
    sequential_execution(report_folder, cases, instruction)


def instruction_5(report_folder: str):
    '''Un caso único'''

    case_file = input(enter_name_case_format)
    with_debug = input(instruction_text_v2_with_debug_single).upper() == 'Y'
    start_date = datetime.now()
    vns(report_folder, case_file, with_debug)
    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')


def run():

    instruction = input(instruction_text_v2_run)
    if not instruction in ['1', '2', '3', '4', '5']:
        print('Instrucción no encontrada ❌!')
        return

    date_now = str(datetime.now().replace(microsecond=0)
                   ).replace(' ', '_').replace(':', '_')
    report_folder = f'./reports/report_{date_now}'
    os.mkdir(report_folder)

    if instruction == '1':
        instruction_1(report_folder)
    if instruction == '2':
        instruction_2(report_folder)
    if instruction == '3':
        instruction_3(report_folder)
    if instruction == '4':
        instruction_4(report_folder)
    if instruction == '5':
        instruction_5(report_folder)
