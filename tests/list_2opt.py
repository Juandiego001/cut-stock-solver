def generar_permutaciones_2opt(arreglo_original):
    """
    Genera todas las permutaciones posibles de 2-opt (inversión de segmento)
    a partir de un arreglo.

    Args:
        arreglo_original (list): La lista inicial de números.

    Returns:
        list: Una lista de todos los arreglos resultantes de aplicar la operación 2-opt.
    """

    n = len(arreglo_original)
    permutaciones = []

    for i in range(n - 1):
        for k in range(i + 1, n):
            segmento_inicio = arreglo_original[:i]
            segmento_a_invertir = arreglo_original[i:k+1]
            segmento_invertido = segmento_a_invertir[::-1]
            segmento_final = arreglo_original[k+1:]
            nuevo_arreglo = segmento_inicio + segmento_invertido + segmento_final
            if nuevo_arreglo != arreglo_original:
                permutaciones.append(nuevo_arreglo)

    return permutaciones


mi_arreglo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
permutaciones_2opt = generar_permutaciones_2opt(mi_arreglo)
print(f"Arreglo original: {mi_arreglo}")
print(f"Número total de permutaciones 2-opt: {len(permutaciones_2opt)}")
print("\n--- Primeras 10 permutaciones 2-opt generadas ---")
for i, arreglo in enumerate(permutaciones_2opt):
    print(f"  {i+1}: {arreglo}")
