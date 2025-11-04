import os


cases_dir = '../cases'


def buscar_pieza(x, y, piezas):
    '''Busca si existe la pieza en la lista sin importar el orden'''

    return (x, y) in piezas or (y, x) in piezas


def indice_pieza(x, y, piezas):
    '''Retorna el índice de la pieza asumiendo que ya existe en la lista piezas'''

    for i, (a, b) in enumerate(piezas):
        if (a == x and b == y) or (a == y and b == x):
            return i


def validate_cases(case_file: str):

    print(f'\nCaso {case_file}.')
    f_test = open(f'{cases_dir}/{case_file}.txt', 'r')
    lines = f_test.readlines()

    piezas = []
    for i in range(1, len(lines)):
        _, ancho, largo = lines[i].split(',')

        if buscar_pieza(ancho, largo, piezas):
            print(f'¡Atención!')
            print(f'La pieza {i} con dimensiones {int(ancho)} x {int(largo)} ya existía ❌.')
            return

        piezas.append((ancho, largo))
    
    print('Todo correcto ✅')


if __name__ == '__main__':

    execution_mode = input('''
¿Cómo desea ejecutar la validación de casos?

1- Todos los casos.
2- Determinados casos.
3- Un caso único.

Ingrese un número: ''')

    if execution_mode == '1':
        for case_file in os.listdir(cases_dir):
            validate_cases(case_file)
    elif execution_mode == '2':
        selected_cases = []
        while True:
            case_file = input(
                'Digite la ruta o el nombre del caso que desea ejecutar (deje en blanco para terminar de seleccionar casos): ')

            if case_file == '':
                break
            selected_cases.append(case_file)

        for case_file in selected_cases:
            validate_cases(case_file)
    else:
        case_file = input(
            'Digite la ruta o el nombre del caso que desea ejecutar: ')
        validate_cases(case_file)
