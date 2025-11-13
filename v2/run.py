import os
import copy
import random
from datetime import datetime
from .classes import Item, Solution
from multiprocessing import Process
from .main import generate_solution, vecindario_2opt, vecindario_insertions, vecindario_swap
from config import cases_dir, v2_reports_dir, instruction_text_v2_run, enter_name_case_multiple, cases_dir, enter_name_case, instruction_text_v2_report_type, \
    instruction_text_v2_report_type_single, instruction_text_v2_variant, validate_instruction, instruction_text_v2_group, possible_groups, get_group_name, cases_group_dir, \
    get_cases_by_group
from .gen_reports.gen_reports_excel import create_sheets_iterations, create_sheets_summary, write_iterations_summary, write_solution_debug, write_solution_info, write_solution_iteration_info, write_test_case


def lectura(case: str, variant: str):
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

    id = 1
    for line in lineas_archivo[1:]:
        demanda, ancho, largo = line.split(',')
        for i in range(int(demanda)):
            item = Item(id, int(demanda), int(ancho), int(largo))
            items.append(item)

        id += 1

    f.close()

    if variant == '1':
        random.shuffle(items)  # Random
    if variant == '2':
        items = sorted(items, key=lambda item: item.ancho *
                       item.largo, reverse=True)  # De mayor a menor
    if variant == '3':
        items = sorted(items, key=lambda item: item.ancho *
                       item.largo, reverse=False)  # De menor a mayor

    return int(ancho_base), int(largo_base), items


def generate_excel_report(report_folder,
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


def generate_text_report(report_folder: str, case: str, elapsed_time: float, mejor_solucion: Solution):
    '''Generar reporte de texto simple'''

    if not os.path.exists(f'{report_folder}/summary.txt'):
        with open(f'{report_folder}/summary.txt', 'a+') as archivo:
            archivo.write(
                f'Caso\t\t|\tTiempo\t\t|\tDesperdicio\t|\tFitness\n{"-"*60}\n')

    if mejor_solucion.desperdicio > 999:
        with open(f'{report_folder}/summary.txt', 'a+') as archivo:
            archivo.write(
                f'{case}\t|\t{elapsed_time:.3f}\t\t\t|\t{mejor_solucion.desperdicio}\t\t|\t{mejor_solucion.fitness}\n')
    else:
        with open(f'{report_folder}/summary.txt', 'a+') as archivo:
            archivo.write(
                f'{case}\t|\t{elapsed_time:.3f}\t\t\t|\t{mejor_solucion.desperdicio}\t\t\t|\t{mejor_solucion.fitness}\n')


def vns(report_folder: str, case: str, variant: str, report_type: str = 'TXT'):
    '''Función de búsqueda local

    Report type.
    EXCEL_AND_DEBUG: Con excel y debug.
    EXCEL: Con excel sin debug.
    TXT: Reporte mínimo en texto.
    '''

    start_date = datetime.now()
    with_excel = report_type in ['EXCEL_AND_DEBUG', 'EXCEL']
    with_excel_and_debug = report_type == 'EXCEL_AND_DEBUG'

    ancho_grande, largo_grande, items = lectura(case, variant)
    sol_ini = generate_solution(ancho_grande, largo_grande, items)
    mejor_vecino = mejor_solucion = copy.deepcopy(sol_ini)

    vecinos_summary = []
    if with_excel_and_debug:
        report_folder = f'{report_folder}/{case}'
        os.mkdir(report_folder)

        all_vecinos_swap = []
        all_vecinos_insertions = []
        all_vecinos_2opt = []

    iterations = 1
    while True:
        mejor_vecino_swap, vecinos_swap = vecindario_swap(
            ancho_grande, largo_grande, mejor_solucion.permutation, with_excel_and_debug)
        mejor_vecino_insertions, vecinos_insertions = vecindario_insertions(
            ancho_grande, largo_grande, mejor_solucion.permutation, with_excel_and_debug)
        mejor_vecino_2opt, vecinos_2opt = vecindario_2opt(
            ancho_grande, largo_grande, mejor_solucion.permutation, with_excel_and_debug)

        if with_excel:
            vecinos_summary.append((iterations,
                                    mejor_vecino_swap.fitness,
                                    mejor_vecino_insertions.fitness,
                                    mejor_vecino_2opt.fitness,
                                    mejor_solucion.fitness))

        if with_excel_and_debug:
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
    end_date = datetime.now()
    elapsed_time: float = (end_date - start_date).total_seconds()

    if with_excel:
        generate_excel_report(
            report_folder=report_folder,
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
            debug=with_excel_and_debug)
    else:
        generate_text_report(report_folder, case, elapsed_time, mejor_solucion)


def get_report_type(instruction: str):
    '''Determina el tipo de reporte a generar'''

    if instruction in ['1', '2']:
        return 'EXCEL_AND_DEBUG'

    if instruction in ['3', '4']:
        return 'EXCEL'

    if instruction == '5':
        return 'TXT'

    return 'TXT'


def get_report_type_single(instruction: str):
    '''Determina el tipo de reporte a generar para la instrucción 5'''

    if instruction == '1':
        return 'EXCEL_AND_DEBUG'
    if instruction == '2':
        return 'EXCEL'
    if instruction == '3':
        return 'TXT'

    return 'TXT'


def check_report_type():
    '''Obtiene del usuario el tipo de reporte a generar deseado'''

    instruction = input(instruction_text_v2_report_type)
    validate_instruction(5, instruction)
    return instruction


def parallel_execution(report_folder: str, cases: list[str], variant_instruction: str, report_type_instruction: str):
    '''Ejecución paralela'''

    all_processes: list[Process] = []
    for case in cases:
        report_type = get_report_type(report_type_instruction)
        p = Process(target=vns, args=(report_folder, case,
                    variant_instruction, report_type))
        all_processes.append(p)

    for each_process in all_processes:
        each_process.start()
    for each_process in all_processes:
        each_process.join()


def sequential_execution(report_folder: str, cases: list[str], variant_instruction: str, report_type_instruction: str):
    '''Ejecución secuencial'''

    for case in cases:
        report_type = get_report_type(report_type_instruction)
        vns(report_folder, case, variant_instruction, report_type)

    print(f'Finished execution.')


def get_cases():
    '''Función para ir leyendo los casos ingresados por el usuario'''

    cases = []
    while True:
        case_file = input(enter_name_case_multiple)
        if case_file == '':
            break
        cases.append(case_file)
    return cases


def instruction_1(report_folder: str, variant_instruction: str, report_type_instruction: str):
    '''Todos los casos (en paralelo)'''

    cases = [case_file.split('.')[0] for case_file in os.listdir(cases_dir)]
    parallel_execution(report_folder, cases,
                       variant_instruction, report_type_instruction)


def instruction_2(report_folder: str, variant_instruction: str, report_type_instruction: str):
    '''Todos los casos (secuencial)'''

    cases = [case_file.split('.')[0] for case_file in os.listdir(cases_dir)]
    sequential_execution(report_folder, cases,
                         variant_instruction, report_type_instruction)


def instruction_3(report_folder: str, variant_instruction: str, report_type_instruction: str):
    '''Determinados casos (en paralelo)'''

    cases = get_cases()
    parallel_execution(report_folder, cases,
                       variant_instruction, report_type_instruction)


def instruction_4(report_folder: str, variant_instruction: str, report_type_instruction: str):
    '''Determinados casos (en secuencial)'''

    cases = get_cases()
    sequential_execution(report_folder, cases,
                         variant_instruction, report_type_instruction)


def instruction_5(report_folder: str, variant_instruction: str, report_type_instruction: str):
    '''Grupo de casos (en paralelo)'''

    cases = get_cases_by_group()
    parallel_execution(report_folder, cases,
                       variant_instruction, report_type_instruction)


def instruction_6(report_folder: str, variant_instruction: str, report_type_instruction: str):
    '''Grupo de casos (en secuencial)'''

    cases = get_cases_by_group()
    sequential_execution(report_folder, cases,
                         variant_instruction, report_type_instruction)


def instruction_7(report_folder: str, case_file: str, variant_instruction: str, report_type_instruction: str):
    '''Un caso único'''

    vns(report_folder, case_file, variant_instruction, report_type_instruction)
    print(f'Finished execution.')


def get_user_instructions():
    '''Obtener indicaciones sobre cómo ejecutar el script'''

    instruction = input(instruction_text_v2_run)
    validate_instruction(7, instruction)

    if instruction in ['1', '2', '3', '4', '5', '6']:
        report_type_instruction = check_report_type()
    else:
        report_type_instruction = get_report_type_single(
            input(instruction_text_v2_report_type_single))

    variant_instruction = input(instruction_text_v2_variant)
    validate_instruction(3, variant_instruction)

    case_file = None
    if instruction == '7':
        case_file = input(enter_name_case)

    return instruction, report_type_instruction, variant_instruction, case_file


def run():

    instruction, report_type_instruction, variant_instruction, case_file = get_user_instructions()
    date_now = str(datetime.now().replace(microsecond=0)
                   ).replace(' ', '_').replace(':', '_')
    report_folder = f'{v2_reports_dir}/report_{date_now}'
    os.mkdir(report_folder)

    if instruction == '1':
        instruction_1(report_folder, variant_instruction,
                      report_type_instruction)
    if instruction == '2':
        instruction_2(report_folder, variant_instruction,
                      report_type_instruction)
    if instruction == '3':
        instruction_3(report_folder, variant_instruction,
                      report_type_instruction)
    if instruction == '4':
        instruction_4(report_folder, variant_instruction,
                      report_type_instruction)
    if instruction == '5':
        instruction_5(report_folder, variant_instruction,
                      report_type_instruction)
    if instruction == '6':
        instruction_6(report_folder, variant_instruction,
                      report_type_instruction)
    if instruction == '7':
        instruction_7(report_folder, case_file,
                      variant_instruction, report_type_instruction)
