import os
import copy
from datetime import datetime
from multiprocessing import Process
from gen_reports.gen_reports_web import write_base_index, write_base_styles_files, write_final_index, write_gen_html_tags, write_gen_konva, write_konva_for_sub_subspaces, write_konva_for_sub_cuts, write_konva_for_sub_matrix, write_iterations_objects
from main import sol_inicial, decode11, vecindario_t, vecindario_h
from gen_reports.gen_reports_excel import create_sheets_summary, create_sheets_iterations, write_test_case, write_solution, write_iterations, write_iterations_summary
from classes import Item


# Definición de variables globales
cases_dir = 'cases'
c: int = 4


def lectura(case: str):
    '''
    Lectura del archivo de pruebas.

    Consideraciones:
    La primer línea del archivo corresponde al ancho.
    La segunda línea del archivo corresponde al largo.
    Las demás líneas corresponden a los ítems con el siguiente formato:
    Id  Demanda Ancho Largo
    '''

    v = []
    f = open(f'./cases/{case}.txt', 'r')
    lineas_archivo = f.readlines()
    ancho_grande = int(lineas_archivo[0])
    largo_grande = int(lineas_archivo[1])

    for line in lineas_archivo[2:]:
        id, demanda, ancho, largo = line.split('\t')
        demanda.replace('\n', '')  # Se remueve el último salto de línea
        item = Item(int(id), int(demanda), int(ancho), int(largo))
        v.append(item)

    f.close()
    items = copy.deepcopy(v)
    return ancho_grande, largo_grande, items


def generate_reports_web(report_folder: str, data: dict):
    '''Generar reportes web'''

    '''Se crean las carpetas donde se guardará el reporte web'''
    os.makedirs(f'{report_folder}/web/js/iterations')
    os.makedirs(f'{report_folder}/web/styles')

    '''Se escriben los archivos de CSS'''
    write_base_styles_files(f'{report_folder}/web/styles')

    '''Se escribe el archivo index.html'''
    write_base_index(f'{report_folder}/web/index.html')

    test_case = data['test_case']
    sol_ini = data['sol_ini']
    vecinos_summary = data['vecinos_summary']
    mejor_solucion = data['mejor_solucion']
    iterations = data['iterations']

    case = test_case['case']
    items = test_case['items']

    # Creación del javascript del caso de prueba
    f = open(f'{report_folder}/web/js/data_caso_prueba.js', 'w', encoding='utf-8')
    data = {
        'anchoGrande': test_case['ancho_grande'],
        'largoGrande': test_case['largo_grande'],
    }

    demandas = []
    for i, item in enumerate(items):
        demanda = {
            'id': i + 1,
            'demanda': item.dem,
            'ancho': item.ancho,
            'largo': item.largo
        }
        demandas.append(demanda)
    data['demandas'] = demandas

    f.write(f'let data_caso_prueba = {str(demandas)};')
    f.close()

    '''Escribir la solución inicial'''
    f = open(f'{report_folder}/web/js/data_sol_inicial.js', 'w', encoding='utf-8')
    f.write(f'let data_sol_inicial = {str(sol_ini.to_dict())};')
    f.close()

    '''Escribir el resumen de las iteraciones'''
    f = open(f'{report_folder}/web/js/data_iterations_summary.js', 'w', encoding='utf-8')
    for iter, fit_t, fit_h, best in vecinos_summary:
        data = {
            'id': iter, 't': fit_t, 'h': fit_h, 'best': best
        }
        # write_iterations_summary_web(iter, fit_t, fit_h, best)
        if fit_t < fit_h and fit_t < best:
            data['moveTo'] = 'h'
        elif fit_h < fit_t and fit_h < best:
            data['moveTo'] = 't'
        f.writelines(f'let data_iteration_{iter} = {str(data)};')
    f.close()

    '''Escribir la solución'''
    f = open(f'{report_folder}/web/js/data_solucion.js', 'w', encoding='utf-8')
    f.write(f'let data_solucion = {str(mejor_solucion.to_dict())};')
    f.close()

    '''Escribir el detalle de las iteraciones'''
    all_vecinos_t = iterations['all_vecinos_t']
    all_vecinos_h = iterations['all_vecinos_h']
    for i, iter in enumerate(range(iterations['count'])):
        v_t, _ = all_vecinos_t[i]
        v_h, _ = all_vecinos_h[i]

        f = open(f'{report_folder}/web/js/iterations/{iter + 1}_t.js', 'w', encoding='utf-8')
        for j, vecino in enumerate(v_t):
            f.writelines(f'let data_iteration_vecino_t_{iter + 1}_{j + 1} = {str(vecino.to_dict())};\n')
        f.close()

        f = open(f'{report_folder}/web/js/iterations/{iter + 1}_h.js', 'w', encoding='utf-8')
        for j, vecino in enumerate(v_h):
            f.writelines(f'let data_iteration_vecino_h_{iter + 1}_{j + 1} = {str(vecino.to_dict())};\n')
        f.close()
    
    '''Escribir los Javascript generadores del contenido de la página'''
    write_gen_html_tags(iterations['count'], c, report_folder)
    write_iterations_objects(iterations['count'], c, report_folder)
    write_konva_for_sub_cuts(report_folder)
    write_konva_for_sub_subspaces(report_folder)
    write_konva_for_sub_matrix(report_folder)
    write_gen_konva(report_folder)

    '''Escribir la parte final del archivo index.html'''
    write_final_index(iterations['count'], f'{report_folder}/web/index.html')


def generate_reports(report_folder, data):
    '''Generar reportes de excel'''

    test_case = data['test_case']
    sol_ini = data['sol_ini']
    vecinos_summary = data['vecinos_summary']
    mejor_solucion = data['mejor_solucion']
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
    write_solution(wb_summary['SolInicial'], sol_ini, 1)

    '''Escribir el resumen de las iteraciones'''
    for iter, fit_t, fit_h, best in vecinos_summary:
        write_iterations_summary(wb_summary['Iteraciones'],
                                 iter,
                                 fit_t,
                                 fit_h,
                                 best)

    '''Escribir la solución'''
    write_solution(wb_summary['Solucion'], mejor_solucion, 1)

    wb_summary.save(f'{report_folder}/{case}_summary.xlsx')
    wb_summary.close()

    '''Escribir el detalle de las iteraciones'''
    os.mkdir(f'{report_folder}/iterations')
    all_vecinos_t = iterations['all_vecinos_t']
    all_vecinos_h = iterations['all_vecinos_h']
    for i, iter in enumerate(range(iterations['count'])):
        iter += 1
        wb_iterations = create_sheets_iterations(iter)

        v_t, _ = all_vecinos_t[i]
        v_h, _ = all_vecinos_h[i]

        write_iterations(
            wb_iterations[f'{iter}_VecinosT'], v_t, iter, c, len(items))
        write_iterations(
            wb_iterations[f'{iter}_VecinosH'], v_h, iter, c, len(items))

        wb_iterations.save(f'{report_folder}/iterations/{case}_{iter}.xlsx')
        wb_iterations.close()


def run_case(report_folder, case, with_reports=True):
    '''Función para ejecutar cada caso'''

    '''Creación de carpeta para cada caso'''
    report_folder = f'{report_folder}/{case}'
    os.mkdir(report_folder)

    ancho_grande, largo_grande, items = lectura(case)

    sol_ini = sol_inicial(ancho_grande, largo_grande, c, items)

    '''Se calcula el z de la solución inicial con decode11'''
    decode11(sol_ini, items)

    mejor_solucion = copy.deepcopy(sol_ini)

    '''Variables para generar al final los reportes de excel'''
    vecinos_summary = []
    all_vecinos_t = []
    all_vecinos_h = []

    iteration = 1
    while True:
        mejor_vecino_t, vecinos_t = vecindario_t(
            mejor_solucion, ancho_grande, largo_grande, c, items)
        mejor_vecino_h, vecinos_h = vecindario_h(
            mejor_solucion, ancho_grande, largo_grande, c, items)

        '''Almacenar para reporte'''
        vecinos_summary.append((iteration,
                                mejor_vecino_t.fitness,
                                mejor_vecino_h.fitness,
                                mejor_solucion.fitness))
        all_vecinos_t.append((vecinos_t, iteration))
        all_vecinos_h.append((vecinos_h, iteration))

        '''Se determina el mejor vecino'''
        if mejor_vecino_h.fitness < mejor_vecino_t.fitness:
            mejor_vecino = mejor_vecino_h
        else:
            mejor_vecino = mejor_vecino_t

        '''Si el mejor vecino es mejor que la mejor solución iterada, entonces actualice la mejor solución iterada,
        de lo contrario termine el ciclo
        '''
        if mejor_vecino.fitness < mejor_solucion.fitness:
            mejor_solucion = mejor_vecino
        else:
            break

        iteration += 1

    print(f'Case {case}, iterations: {iteration}')

    if with_reports:
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
                'all_vecinos_t': all_vecinos_t,
                'all_vecinos_h': all_vecinos_h
            }
        }

        generate_reports(report_folder, data)
        generate_reports_web(report_folder, data)


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
