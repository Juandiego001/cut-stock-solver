from config import cases_group_dir


def sort(group_file: str):
    '''Ordena lexicográficamente los casos de un grupo'''

    try:
        with open(f'{cases_group_dir}/{group_file}', 'r') as f_in:
            lineas = f_in.read().splitlines()

        lineas.sort()
        with open(f'{cases_group_dir}/{group_file}', 'w') as f_out:
            for linea in lineas:
                f_out.write(linea + '\n')

        print(f"El grupo {group_file} ha sido ordenado.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{group_file}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
