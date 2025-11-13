from config import cases_group_dir


def list_groups(group_file: str):
    '''Listar casos de un grupo'''

    previous_key = None
    print("Contenido del archivo agrupado:")
    print("---")
    try:
        with open(f'{cases_group_dir}/{group_file}', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = line.split('_')
                    current_key = f"{parts[0]}_{parts[1]}"
                except IndexError:
                    print(f"- {line}")
                    continue

                if previous_key is not None and current_key != previous_key:
                    print()

                print(f"- {line}")
                previous_key = current_key

        print("---")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{group_file}'.")
