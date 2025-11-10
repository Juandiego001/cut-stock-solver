'''
Notas.

Este archivo permite la generación de los parámetros para testear el modelo de AMPL.

Aclaración.

a[o,k,q,j] p, parámetro binario o coeficiente binario que se define:

- o: orientación (1: vertical, 0: horizontal).
- q: posición.
- k: plato a cortar.
- j: plato a obtener.
- p: cantidad del plato j a obtener luego del corte.
'''
import os
from datetime import datetime
from config import ampl_data_dir, cases_dir, instruction_text_ampl_generate, enter_name_case_format_multiple, enter_name_case
from multiprocessing import Process


def buscar_pieza(x, y, piezas):
    '''Busca si existe la pieza en la lista sin importar el orden'''

    return (x, y) in piezas or (y, x) in piezas


def indice_pieza(x, y, piezas):
    '''Retorna el índice de la pieza asumiendo que ya existe en la lista piezas'''

    for i, (a, b) in enumerate(piezas):
        if (a == x and b == y) or (a == y and b == x):
            return i


def generate_ampl_data(case_file: str, *args, **kwargs):
    '''Generate ampl data main function'''

    f_test = open(f'{cases_dir}/{case_file}.txt', 'r')
    lines = f_test.readlines()
    ancho_original_str, largo_original_str = lines[0].split(',')
    ancho_original = int(ancho_original_str)  # Ancho de la pieza original
    largo_original = int(largo_original_str)  # Largo de la pieza original
    # Se agrega la pieza original
    piezas = [(ancho_original, largo_original)]

    # Lista de piezas buscadas
    piezas_buscadas = []
    for i in range(1, len(lines)):
        dem_str, ancho_str, largo_str = lines[i].split(',')
        piezas_buscadas.append((int(ancho_str), int(largo_str), int(dem_str)))

    # Archivo data.dat a generar
    f = open(f'{ampl_data_dir}/{case_file}.dat', 'w+', encoding='utf-8')

    # Cortes y generación de piezas - Parámetro a
    contador = 0
    param_a_text = '# Parámetro a\n'
    while (contador != len(piezas)):
        p = piezas[contador]

        cortes_verticales = p[0]  # Cortes verticales = Ancho - 1
        cortes_horizontales = p[1]  # Cortes horizontales = Largo - 1

        if cortes_verticales > 1:
            for i in range(1, cortes_verticales):
                ancho1 = i
                ancho2 = p[0] - i
                largo = p[1]  # Al cortar verticalmente el largo es el mismo

                # Si al cortar se obtuvo el mismo ancho, es porque se obtuvo la misma pieza dos veces
                if ancho1 == ancho2:
                    if not buscar_pieza(ancho1, largo, piezas):
                        piezas.append((ancho1, largo))

                    indice = indice_pieza(ancho1, largo, piezas)
                    param_a_text += f'param a[1,{contador},{i},{indice}] 2;\n'

                # Si al cortar se obtuvieron diferentes anchos, es porque se obtuvieron piezas diferentes
                else:
                    if not buscar_pieza(ancho1, largo, piezas):
                        piezas.append((ancho1, largo))
                    indice = indice_pieza(ancho1, largo, piezas)
                    param_a_text += f'param a[1,{contador},{i},{indice}] 1;\n'

                    if not buscar_pieza(ancho2, largo, piezas):
                        piezas.append((ancho2, largo))
                    indice = indice_pieza(ancho2, largo, piezas)
                    param_a_text += f'param a[1,{contador},{i},{indice}] 1;\n'

        if cortes_horizontales > 1:
            for i in range(1, cortes_horizontales):
                largo1 = i
                largo2 = p[1] - i
                ancho = p[0]  # Al cortar horizontalmente el ancho es el mismo

                # Si al cortar se obtuvo el mismo largo, es porque se obtuvo la misma pieza dos veces
                if largo1 == largo2:
                    if not buscar_pieza(largo1, ancho, piezas):
                        piezas.append((largo1, ancho))

                    indice = indice_pieza(largo1, ancho, piezas)
                    param_a_text += f'param a[0,{contador},{i},{indice}] 2;\n'

                # Si al cortar se obtuvieron diferentes largos, es porque se obtuvieron piezas diferentes
                else:
                    if not buscar_pieza(largo1, ancho, piezas):
                        piezas.append((largo1, ancho))
                    indice = indice_pieza(largo1, ancho, piezas)
                    param_a_text += f'param a[0,{contador},{i},{indice}] 1;\n'

                    if not buscar_pieza(largo2, ancho, piezas):
                        piezas.append((largo2, ancho))
                    indice = indice_pieza(largo2, ancho, piezas)
                    param_a_text += f'param a[0,{contador},{i},{indice}] 1;\n'

        contador += 1

    # Se escribe el comentario de la Indexación de las piezas
    f.writelines('# Indexación de las piezas: (ancho, largo)\n')
    for i, pieza in enumerate(piezas):
        f.writelines(f'# Pieza #{i} con dimensiones {pieza}\n')

    # Se escribe el parámetro de los platos totales
    f.writelines('\n# Parámetro platos\n')
    f.writelines(f'param Platos {contador - 1};\n')

    # Demanda
    demandas = [(indice_pieza(pieza[0], pieza[1], piezas), pieza[2])
                for pieza in piezas_buscadas]

    # Se escribe la demanda
    f.writelines('\n# Demanda')
    f.writelines(
        f'\nset JJ {' '.join([str(demanda[0]) for demanda in demandas])};\n')

    for demanda in demandas:
        f.writelines(f'param Dem[{demanda[0]}] {demanda[1]};\n')

    # Se escribe el parámetro a
    f.writelines(f'\n{param_a_text}')

    # Cantidad de posibles cortes - parámetro Q
    f.writelines('\n# Parámetro Q\n')
    for index, pieza in enumerate(piezas):
        # Cortes verticales = Ancho - 1
        cortes_verticales = [str(i) for i in range(1, pieza[0])]
        # Cortes horizontales = Largo - 1
        cortes_horizontales = [str(i) for i in range(1, pieza[1])]

        if len(cortes_verticales) > 0:
            f.writelines(f'set Q[{index},1] {' '.join(cortes_verticales)};\n')
        else:
            f.writelines(f'set Q[{index},1] ;\n')

        if len(cortes_horizontales) > 0:
            f.writelines(
                f'set Q[{index},0] {' '.join(cortes_horizontales)};\n')
        else:
            f.writelines(f'set Q[{index},0] ;\n')

    # Áreas de cada plato
    f.writelines('\n# Parámetro Area (Áreas)\n')
    for index, pieza in enumerate(piezas):
        area = pieza[0] * pieza[1]
        f.writelines(f'param Area[{index}] {area};\n')


def parallel_execution(cases: list[str]):
    '''Ejecución paralela'''

    all_processes: list[Process] = []
    for case in cases:
        p = Process(target=generate_ampl_data, args=(case,))
        all_processes.append(p)

    start_date = datetime.now()
    for each_process in all_processes:
        each_process.start()
    for each_process in all_processes:
        each_process.join()
    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')


def sequential_execution(cases: list[str]):
    '''Ejecución secuencial'''

    for case in cases:
        start_date = datetime.now()
        generate_ampl_data(case)
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


def instruction_1():
    '''Todos los casos (en paralelo)'''

    cases = [case_file.split('.')[0] for case_file in os.listdir(cases_dir)]
    parallel_execution(cases)


def instruction_2():
    '''Todos los casos (secuencial)'''

    cases = [case_file.split('.')[0] for case_file in os.listdir(cases_dir)]
    sequential_execution(cases)


def instruction_3():
    '''Determinados casos (en paralelo)'''

    cases = get_cases()
    parallel_execution(cases)


def instruction_4():
    '''Determinados casos (en secuencial)'''

    cases = get_cases()
    sequential_execution(cases)


def instruction_5():
    '''Un caso único'''

    case_file = input(enter_name_case)
    start_date = datetime.now()
    generate_ampl_data(case_file)
    end_date = datetime.now()
    elapsed_time = (end_date - start_date).seconds
    print(f'Elapsed time: {elapsed_time} seconds')


def run():

    instruction = input(instruction_text_ampl_generate)

    if not instruction in ['1', '2', '3', '4', '5']:
        print('Instrucción no encontrada ❌!')
        return

    if instruction == '1':
        instruction_1()
    if instruction == '2':
        instruction_2()
    if instruction == '3':
        instruction_3()
    if instruction == '4':
        instruction_4()
    if instruction == '5':
        instruction_5()
