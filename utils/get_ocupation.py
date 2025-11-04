import os


cases_dir = '../cases'


def get_ocupacion(the_case: str):
    '''
    Obtener la ocupación a partir de los casos de prueba

    Consideraciones:
    La primer línea del archivo corresponde al ancho.
    La segunda línea del archivo corresponde al largo.
    Las demás líneas corresponden a los ítems con el siguiente formato:
    Id  Demanda Ancho Largo
    '''

    fixed_file = f'{the_case}.txt' if not 'txt' in the_case else the_case

    f = open(f'../cases/{fixed_file}', 'r')
    lineas_archivo = f.readlines()

    ancho_original_str, largo_original_str = lineas_archivo[0].split(',')
    ancho_original = int(ancho_original_str)  # Ancho de la pieza original
    largo_original = int(largo_original_str)  # Largo de la pieza original

    area_total = ancho_original * largo_original
    print(f'Ancho grande: {ancho_original} x Largo grande: {largo_original} = {area_total}')

    total_areas = 0
    lista_permutacion = 0
    for line in lineas_archivo[1:]:
        demanda, ancho, largo = line.split(',')
        demanda = int(demanda)
        ancho = int(ancho)
        largo = int(largo)

        area = demanda*ancho*largo
        total_areas += area
        lista_permutacion += demanda
        print(f'{demanda} x {ancho} x {largo} = {area}')

    print(f'Total suma de áreas: {total_areas}')
    print(f'Total tamaño permutación: {lista_permutacion}')
    print(f'Ocupación: {round((total_areas*100)/area_total, 2)}')
    print('')

    f.close()


if __name__ == '__main__':

    execution_mode = input('''
¿Cómo desea ejecutar la obtención de ocupación?

1- Todos los casos.
2- Determinados casos.
3- Un caso único.

Ingrese un número: ''')


    if execution_mode == '1':
        for case_file in os.listdir(cases_dir):
            get_ocupacion(case_file)
    elif execution_mode == '2':
        selected_cases = []
        while True:
          case_file = input(
            'Digite la ruta o el nombre del caso que desea ejecutar (deje en blanco para terminar de seleccionar casos): ')
          
          if case_file == '': break
          selected_cases.append(case_file)
        
        for case_file in selected_cases:
            get_ocupacion(case_file)
    else:
        case_file = input(
            'Digite la ruta o el nombre del caso que desea ejecutar: ')
        get_ocupacion(case_file)
