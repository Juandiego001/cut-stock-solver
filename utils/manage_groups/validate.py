from config import cases_group_dir


def validate(group_file: str):
    '''Validar casos repetidos de un grupo'''

    cases = set()
    print("Validando casos repetidos...")
    try:
        with open(f'{cases_group_dir}/{group_file}', 'r') as archivo:
            for case in archivo:
                case = case.strip()
                if case in cases:
                    print(f"Caso repetido: {case}")
                else:
                    cases.add(case)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{group_file}'")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    print("Finalizando validación de casos repetidos.")
