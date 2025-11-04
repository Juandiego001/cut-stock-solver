def obtener_inserciones_posibles(arreglo_original):
    """
    Genera todos los arreglos resultantes de tomar cada elemento 
    del arreglo original y reinsertarlo en todas las posiciones posibles.
    """

    resultados_totales = {}

    n = len(arreglo_original)

    for i in range(n):

        elemento_a_mover = arreglo_original[i]
        arreglo_sin_elemento = arreglo_original[:i] + arreglo_original[i+1:]
        inserciones_para_elemento = []
        for j in range(n):
            nuevo_arreglo = arreglo_sin_elemento[:]
            nuevo_arreglo.insert(j, elemento_a_mover)
            inserciones_para_elemento.append(nuevo_arreglo)

        resultados_totales[i] = inserciones_para_elemento

    return resultados_totales


mi_arreglo = [7, 12, 3, 4, 5]
resultados_completos = obtener_inserciones_posibles(mi_arreglo)

for indice, arreglos in resultados_completos.items():
    print(
        f"\n--- Elemento movido: {mi_arreglo[indice]} (Índice original: {indice}) ---")
    for arreglo in arreglos:
        print(f"  {arreglo}")
